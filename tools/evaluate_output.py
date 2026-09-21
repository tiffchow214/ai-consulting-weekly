"""Pre-send QA gate for the weekly newsletter + deck.

Usage:
    python tools/evaluate_output.py \\
        --newsletter .tmp/newsletter.html \\
        --deck-json .tmp/weekly_deck_content.json \\
        --deck-pptx <path printed by build_deck.py> \\
        [--skip-llm-judge]

Runs after `build_deck.py` succeeds and before `send_email.py` runs. Combines
three deterministic, no-API-call checks (newsletter section structure, deck
JSON schema + slide-count bounds via `build_deck.validate()`, and pptx zip
validity — this replaces the standalone `zipfile.testzip()` snippet that used
to live inline in workflows/weekly_consulting_case.md's Edge Cases) with one
LLM-judge call that re-reads the finished newsletter + deck against the
Evidence & Source Discipline rubric in workflows/consulting_framework.md and
flags unlabeled claims, suspiciously precise unlabeled statistics, and a
thin/duplicate-case signal.

The judge call uses the Anthropic API directly (model claude-haiku-4-5-20251001,
NOT the `claude` CLI — a single structured call, not another agent loop).
Makes exactly one API call per run — an expected cost of a normal run, same
category as the kie.ai diagram call. `--skip-llm-judge` runs the deterministic
checks only (used by the test suite and for cheap dry runs).

Prints the result as JSON to stdout: {"pass": bool, "issues": [...],
"llm_judge": {...} | None}. Exits non-zero on FAIL, matching build_deck.py/
send_email.py's fail-loudly convention — a failed judge API call is itself a
FAIL with an issue string, never a silent skip.
"""

import argparse
import json
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_deck import validate as validate_deck, DeckContentError  # noqa: E402

REQUIRED_SECTION_MARKERS = [
    "The Consulting Case",
    "Behind the Engagement",
    "Technology Choice",
    "Consultant's Eye",
    "Your Turn",
    "Model Approach",
    "Consulting Takeaway",
    "Further Reading",
]
MIN_DECK_SLIDES = 10
MAX_DECK_SLIDES = 14
JUDGE_MODEL = "claude-haiku-4-5-20251001"

EVIDENCE_LABELS = [
    "VERIFIED FACT",
    "CLIENT-REPORTED RESULT",
    "CONSULTANCY-REPORTED CLAIM",
    "INFERENCE",
    "UNKNOWN",
]


def check_newsletter_structure(html_text: str) -> list[str]:
    """Confirms REQUIRED_SECTION_MARKERS all appear, in order. Numbered lens
    subsections (04+) are optional per Lens Selection and not checked here —
    only presence/order of the fixed markers."""
    issues = []
    last_pos = -1
    last_marker = None
    for marker in REQUIRED_SECTION_MARKERS:
        pos = html_text.find(marker)
        if pos == -1:
            issues.append(f"Missing required section: {marker!r}.")
            continue
        if pos < last_pos:
            issues.append(
                f"Section {marker!r} appears before {last_marker!r}; expected order "
                f"{REQUIRED_SECTION_MARKERS}."
            )
        last_pos = pos
        last_marker = marker
    return issues


def check_deck_structure(deck_data: dict) -> list[str]:
    """Reuses build_deck.validate() for schema checks, then additionally
    enforces the workflow's tighter 10-14 slide-count rule (build_deck.py's
    own MIN/MAX_SLIDES are looser global bounds)."""
    issues = []
    try:
        validate_deck(deck_data)
    except DeckContentError as e:
        issues.append(f"Deck schema invalid: {e}")
        return issues

    slide_count = len(deck_data.get("slides", []))
    if not (MIN_DECK_SLIDES <= slide_count <= MAX_DECK_SLIDES):
        issues.append(
            f"Deck has {slide_count} slides; expected between "
            f"{MIN_DECK_SLIDES} and {MAX_DECK_SLIDES}."
        )
    return issues


def check_pptx_zip(pptx_path: Path) -> list[str]:
    if not pptx_path.exists():
        return [f"Deck file not found: {pptx_path}."]
    try:
        bad_file = zipfile.ZipFile(pptx_path).testzip()
    except zipfile.BadZipFile as e:
        return [f"Deck file is not a valid zip: {e}"]
    if bad_file is not None:
        return [f"Deck zip is corrupt at member: {bad_file}."]
    return []


def build_judge_prompt(newsletter_text: str, deck_data: dict) -> str:
    labels = "\n".join(f"- {label}" for label in EVIDENCE_LABELS)
    deck_json = json.dumps(deck_data, indent=2)
    return f"""You are a QA reviewer for a weekly AI/data consulting newsletter and its
companion slide deck. Every material claim in this content must carry one of
these five evidence labels, applied inline or in an evidence-ledger table:

{labels}

Review the newsletter text and deck JSON below. Respond with JSON only, no
prose, matching exactly this shape:

{{
  "unlabeled_claims": ["<claim text>", ...],
  "suspicious_stats": ["<statistic and why it looks unlabeled/invented>", ...],
  "thin_or_duplicate": <true|false>,
  "notes": "<one sentence, or empty string>"
}}

An empty list means none found. Only include a statistic in "suspicious_stats"
if it carries NONE of the five evidence labels anywhere in its immediate
surrounding text (same bar as "unlabeled_claims" — this field exists purely
to catch numbers that slipped through with no label at all, not to
second-guess ones that already have one). A statistic that IS labeled is
never suspicious, no matter how hedged, uncertain, or heavily caveated that
label's accompanying text is (e.g. "UNKNOWN — no control group or period
disclosed" next to a figure is the discipline working correctly, not a
red flag) — do not flag a claim's own honest caveat about itself as evidence
of invention. thin_or_duplicate is true only if the case itself looks too
thin to support a real analysis, or looks like it's rehashing an extremely
generic/templated case with no specific client detail.

=== NEWSLETTER TEXT ===
{newsletter_text}

=== DECK JSON ===
{deck_json}
"""


def run_llm_judge(newsletter_text: str, deck_data: dict, client=None) -> dict:
    """The only networked function. `client` is dependency-injected
    (defaults to anthropic.Anthropic()) so tests can pass a fake."""
    if client is None:
        import anthropic
        client = anthropic.Anthropic()

    prompt = build_judge_prompt(newsletter_text, deck_data)
    try:
        message = client.messages.create(
            model=JUDGE_MODEL,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        raw_text = message.content[0].text
    except Exception as e:
        raise ValueError(f"LLM judge call failed: {e}") from e

    raw_text = raw_text.strip()
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]
        raw_text = raw_text.strip()

    try:
        result = json.loads(raw_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM judge returned unparseable JSON: {e}") from e

    return result


def evaluate(newsletter_html: str, deck_data: dict, pptx_path: Path,
             skip_llm_judge: bool = False, client=None) -> dict:
    issues: list[str] = []
    issues.extend(check_newsletter_structure(newsletter_html))
    issues.extend(check_deck_structure(deck_data))
    issues.extend(check_pptx_zip(pptx_path))

    llm_judge = None
    if not skip_llm_judge:
        try:
            llm_judge = run_llm_judge(newsletter_html, deck_data, client=client)
        except ValueError as e:
            issues.append(str(e))
        else:
            for claim in llm_judge.get("unlabeled_claims", []):
                issues.append(f"Unlabeled claim: {claim}")
            for stat in llm_judge.get("suspicious_stats", []):
                issues.append(f"Suspicious unlabeled statistic: {stat}")
            if llm_judge.get("thin_or_duplicate"):
                issues.append(
                    f"LLM judge flagged the case as thin/duplicate-ish: "
                    f"{llm_judge.get('notes', '')}"
                )

    return {"pass": not issues, "issues": issues, "llm_judge": llm_judge}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--newsletter", required=True, type=Path, help="Path to the newsletter HTML file.")
    parser.add_argument("--deck-json", required=True, type=Path, help="Path to the deck content JSON file.")
    parser.add_argument("--deck-pptx", required=True, type=Path, help="Path to the built .pptx deck.")
    parser.add_argument("--skip-llm-judge", action="store_true", help="Run deterministic checks only, no API call.")
    args = parser.parse_args()

    if not args.newsletter.exists():
        print(f"Error: newsletter file not found: {args.newsletter}", file=sys.stderr)
        sys.exit(1)
    if not args.deck_json.exists():
        print(f"Error: deck JSON file not found: {args.deck_json}", file=sys.stderr)
        sys.exit(1)

    newsletter_html = args.newsletter.read_text(encoding="utf-8")
    try:
        deck_data = json.loads(args.deck_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"Error: deck JSON is malformed: {e}", file=sys.stderr)
        sys.exit(1)

    result = evaluate(newsletter_html, deck_data, args.deck_pptx, skip_llm_judge=args.skip_llm_judge)
    print(json.dumps(result, indent=2))
    if not result["pass"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
