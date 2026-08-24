"""Read/append the weekly tracker + terminology glossary in a Google Sheet.

Usage:
    python tools/manage_sheet.py tracker-read
    python tools/manage_sheet.py tracker-append --week 3 --date YYYY-MM-DD \\
        --consultancy "McKinsey" --client "Acme Corp" --industry "Retail" \\
        --topic "Root-cause analysis" --pass 1 \\
        --takeaway "..." --evidence-quality "Mixed" \\
        --lenses "ML Decision,Marketplace" \\
        --concepts "five whys,class imbalance" \\
        --production-concepts "monitoring,drift" \\
        --difficulty "Apply" --challenge-type "real-case extension"
    python tools/manage_sheet.py glossary-read
    python tools/manage_sheet.py glossary-append --term "double diamond" \\
        --definition "..." --week 1 --topic "Problem framing"

Two tabs, same spreadsheet:
- Tracker: week_number, date, consultancy, client_or_case, industry,
  curriculum_topic, pass, key_takeaway, evidence_quality, lenses_used.
  Client/case has no repeat gate structurally, but the agent should check
  tracker-read for a duplicate client_or_case before committing to a new
  case (see workflows/weekly_consulting_case.md). curriculum_topic follows a
  fixed curriculum sequence (see workflows/consulting_framework.md for the
  ordered list and pass logic) — this tool just stores/returns whatever the
  caller decides; it doesn't know the curriculum itself. week_number/pass
  are likewise agent-computed from tracker-read's row count, not derived
  here. evidence_quality is a quick self-flag (e.g. Strong/Mixed/Weak) for
  how much of the week's case rested on verified fact vs. inference/unknown.
  lenses_used is a comma-separated list of Analytical Lenses activated that
  week (e.g. "ML Decision,Marketplace"), or empty for a zero-lens week — see
  workflows/consulting_framework.md's "Lens depth tracking": the agent
  derives each lens's current pass/depth by counting this column's past
  occurrences via tracker-read, so this tool doesn't compute or interpret
  lens depth itself, just stores/returns the raw history. concepts_practised
  and production_concepts are lightweight, optional, comma-separated
  free-text tags (empty when nothing further to note) for visibility into
  learning coverage over time — not scored, not interpreted by this tool.
  difficulty is a short free-text tier (e.g. Understand/Apply/Design-Defend)
  distinct from the numeric pass column. challenge_type records which of
  the Weekly challenge sourcing options (real-case extension / related
  scenario / vignette — see workflows/consulting_framework.md) supplied
  that week's "Your Turn".
- Glossary: term, definition, first_seen_week, first_seen_topic. Lets the
  newsletter/deck reference a term briefly ("double diamond — see Week 1")
  once it's already been defined, instead of re-explaining or duplicating it.

The target spreadsheet's ID lives in history/google_sheet_id.txt (a small
pointer file committed to the repo; the actual log data lives in the Sheet,
per CLAUDE.md's rule that anything the user needs to see/reference lives in
a cloud service, not a local file).

If that file is missing, a new spreadsheet is created via the Sheets API and
owned by the service account — note that a service-account-created sheet is
NOT automatically visible in a human Google account's Drive. Prefer creating
the sheet yourself and sharing it (Editor) with the service account's
client_email from service_account.json, then dropping its ID into
history/google_sheet_id.txt.

Auth: service_account.json (Google Cloud service account key, gitignored,
never logged). Needs Sheets API enabled and, if the sheet was created by a
human, shared with the service account's client_email as Editor.
"""

import argparse
import json
import re
import sys
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SERVICE_ACCOUNT_PATH = PROJECT_ROOT / "service_account.json"
SHEET_ID_PATH = PROJECT_ROOT / "history" / "google_sheet_id.txt"
SHEET_TITLE = "AI Consulting Weekly — Tracker"
TRACKER_TAB_FALLBACK = "History"  # used only if we ever create the spreadsheet ourselves
GLOSSARY_TAB = "Glossary"
TRACKER_HEADER = [
    "week_number", "date", "consultancy", "client_or_case", "industry",
    "curriculum_topic", "pass", "key_takeaway", "evidence_quality",
    "lenses_used", "concepts_practised", "production_concepts",
    "difficulty", "challenge_type",
]
GLOSSARY_HEADER = ["term", "definition", "first_seen_week", "first_seen_topic"]
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def get_service():
    if not SERVICE_ACCOUNT_PATH.exists():
        raise FileNotFoundError(
            f"{SERVICE_ACCOUNT_PATH} not found. Download a service account key JSON "
            "from Google Cloud Console and save it there."
        )
    creds = service_account.Credentials.from_service_account_file(
        str(SERVICE_ACCOUNT_PATH), scopes=SCOPES
    )
    return build("sheets", "v4", credentials=creds)


def get_or_create_sheet_id(service) -> str:
    if SHEET_ID_PATH.exists():
        sheet_id = SHEET_ID_PATH.read_text().strip()
        if sheet_id:
            return sheet_id

    spreadsheet = service.spreadsheets().create(
        body={
            "properties": {"title": SHEET_TITLE},
            "sheets": [{"properties": {"title": TRACKER_TAB_FALLBACK}}],
        },
        fields="spreadsheetId",
    ).execute()
    sheet_id = spreadsheet["spreadsheetId"]

    SHEET_ID_PATH.parent.mkdir(parents=True, exist_ok=True)
    SHEET_ID_PATH.write_text(sheet_id + "\n")
    print(
        f"Created new spreadsheet {sheet_id} (owned by the service account — "
        "share it with your own Google account to view it), saved to "
        f"{SHEET_ID_PATH}",
        file=sys.stderr,
    )
    return sheet_id


def get_tab_titles(service, sheet_id: str) -> list[str]:
    meta = service.spreadsheets().get(
        spreadsheetId=sheet_id, fields="sheets.properties.title"
    ).execute()
    return [s["properties"]["title"] for s in meta["sheets"]]


def get_tracker_tab(service, sheet_id: str) -> str:
    """The tracker lives in whatever the spreadsheet's first tab is named —
    don't assume 'History'/'Sheet1'; a manually-created sheet defaults differently
    than one this tool creates itself."""
    return get_tab_titles(service, sheet_id)[0]


def ensure_glossary_tab(service, sheet_id: str, existing_tabs: list[str]) -> None:
    if GLOSSARY_TAB in existing_tabs:
        return
    service.spreadsheets().batchUpdate(
        spreadsheetId=sheet_id,
        body={"requests": [{"addSheet": {"properties": {"title": GLOSSARY_TAB}}}]},
    ).execute()


def ensure_header(service, sheet_id: str, tab: str, header: list[str]) -> None:
    """Always (re)write the header row to match the current schema — these tabs
    only ever hold this tool's data, so overwriting the header row is safe and
    keeps a schema change (like this one) from silently leaving a stale header."""
    n = len(header)
    last_col = chr(ord("A") + n - 1)
    service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range=f"'{tab}'!A1:{last_col}1",
        valueInputOption="RAW",
        body={"values": [header]},
    ).execute()


def read_rows(service, sheet_id: str, tab: str, header: list[str]) -> list[dict]:
    n = len(header)
    last_col = chr(ord("A") + n - 1)
    result = service.spreadsheets().values().get(
        spreadsheetId=sheet_id, range=f"'{tab}'!A2:{last_col}"
    ).execute()
    rows = result.get("values", [])
    return [dict(zip(header, row + [""] * (n - len(row)))) for row in rows]


def append_row(service, sheet_id: str, tab: str, header: list[str], values: list) -> None:
    n = len(header)
    last_col = chr(ord("A") + n - 1)
    service.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range=f"'{tab}'!A:{last_col}",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body={"values": [values]},
    ).execute()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("tracker-read", help="Print the current tracker log as JSON.")

    tracker_append = subparsers.add_parser("tracker-append", help="Append one row to the tracker.")
    tracker_append.add_argument("--week", dest="week_num", type=int, required=True, help="Absolute week number (tracker-read row count + 1).")
    tracker_append.add_argument("--date", required=True, help="YYYY-MM-DD")
    tracker_append.add_argument("--consultancy", required=True, help="e.g. McKinsey, BCG, Thoughtworks, AWS Professional Services.")
    tracker_append.add_argument("--client", dest="client_or_case", required=True, help="Client name or case identifier.")
    tracker_append.add_argument("--industry", required=True)
    tracker_append.add_argument("--topic", dest="curriculum_topic", required=True, help="This week's curriculum topic.")
    tracker_append.add_argument("--pass", dest="pass_num", type=int, required=True, help="Curriculum pass number (1, 2, ...).")
    tracker_append.add_argument("--takeaway", dest="key_takeaway", required=True, help="This week's one-line consulting takeaway.")
    tracker_append.add_argument("--evidence-quality", dest="evidence_quality", default="", help="Quick self-flag, e.g. Strong / Mixed / Weak.")
    tracker_append.add_argument("--lenses", dest="lenses_used", default="", help="Comma-separated Analytical Lenses activated this week (e.g. 'ML Decision,Marketplace'), or empty for a zero-lens week.")
    tracker_append.add_argument("--concepts", dest="concepts_practised", default="", help="Optional comma-separated concepts practiced beyond the headline curriculum topic.")
    tracker_append.add_argument("--production-concepts", dest="production_concepts", default="", help="Optional comma-separated production-lifecycle concepts practiced this week; empty if none.")
    tracker_append.add_argument("--difficulty", default="", help="Optional free-text difficulty tier, e.g. Understand / Apply / Design-Defend.")
    tracker_append.add_argument("--challenge-type", dest="challenge_type", default="", help="Optional: real-case extension / related scenario / vignette.")

    subparsers.add_parser("glossary-read", help="Print the current glossary as JSON.")

    glossary_append = subparsers.add_parser("glossary-append", help="Append one term to the glossary.")
    glossary_append.add_argument("--term", required=True)
    glossary_append.add_argument("--definition", required=True)
    glossary_append.add_argument("--week", dest="week_num", type=int, required=True, help="Week this term was first defined.")
    glossary_append.add_argument("--topic", dest="curriculum_topic", required=True, help="Curriculum topic this term was first defined under.")

    args = parser.parse_args()

    if args.command == "tracker-append" and not DATE_RE.match(args.date):
        print(f"Error: --date must be YYYY-MM-DD, got {args.date!r}", file=sys.stderr)
        sys.exit(1)

    try:
        service = get_service()
        sheet_id = get_or_create_sheet_id(service)
        tabs = get_tab_titles(service, sheet_id)
        tracker_tab = tabs[0]
        ensure_header(service, sheet_id, tracker_tab, TRACKER_HEADER)
        ensure_glossary_tab(service, sheet_id, tabs)
        ensure_header(service, sheet_id, GLOSSARY_TAB, GLOSSARY_HEADER)

        if args.command == "tracker-read":
            print(json.dumps(read_rows(service, sheet_id, tracker_tab, TRACKER_HEADER), indent=2))

        elif args.command == "tracker-append":
            append_row(service, sheet_id, tracker_tab, TRACKER_HEADER, [
                str(args.week_num), args.date, args.consultancy, args.client_or_case,
                args.industry, args.curriculum_topic, str(args.pass_num),
                args.key_takeaway, args.evidence_quality, args.lenses_used,
                args.concepts_practised, args.production_concepts,
                args.difficulty, args.challenge_type,
            ])
            print(
                f"Appended week {args.week_num}: {args.date} — consultancy={args.consultancy!r} "
                f"client={args.client_or_case!r} industry={args.industry!r} "
                f"topic={args.curriculum_topic!r} pass={args.pass_num} "
                f"lenses={args.lenses_used!r}"
            )

        elif args.command == "glossary-read":
            print(json.dumps(read_rows(service, sheet_id, GLOSSARY_TAB, GLOSSARY_HEADER), indent=2))

        elif args.command == "glossary-append":
            append_row(service, sheet_id, GLOSSARY_TAB, GLOSSARY_HEADER, [
                args.term, args.definition, str(args.week_num), args.curriculum_topic,
            ])
            print(f"Appended glossary term: {args.term!r} (first seen week {args.week_num}, {args.curriculum_topic!r})")

    except HttpError as e:
        print(f"Error: Sheets API request failed: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
