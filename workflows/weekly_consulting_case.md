# Weekly Consulting Case: Newsletter + Companion Deck

## Objective

Once a week, produce two artifacts and send them together in a single Gmail
send to `tiffanychow214@gmail.com`:

1. A **newsletter** studying one real AI/data consulting engagement in
   depth: the client, the problem, the consultancy's approach, the
   technology, and a critical evaluation of the evidence behind it — ending
   in a new, related client problem the reader must solve before reading the
   model approach.
2. A **companion deck** — your recurring AI/data systems-engineering
   learning artifact. It doesn't recap the case; it teaches the underlying
   technical system: how it works, how it would be designed, evaluated,
   deployed, operated, secured, scaled, maintained, and improved. See
   `workflows/consulting_framework.md`'s Engineering Dimensions for the
   fixed candidate list this draws from each week.

This project trains a different skill from the sibling AI Agents Weekly
project. That project asks "how is this AI product architected?" — this one
asks **"what technology solution did the consultancy choose to solve the
client's business problem, and why, and would I have chosen the same
thing?"** The goal is not to memorize consulting frameworks — it's to get
better at independently answering: given a messy business problem, what
should the organization actually do, why, and how would it be implemented.

**The real case is always the center of gravity.** The week's core
curriculum topic is a lens on the case — it shapes which questions get
emphasized, what the challenge foregrounds, what the reflection focuses on
— but it never bends, weakens, or reinterprets the case to fit. Case
selection happens entirely on the case's own merits (see Picking the case
below) before the curriculum topic or any analytical lens is even
considered.

The newsletter is the **primary** weekly learning artifact — it must stand
alone and be readable without ever opening the deck. The deck is a
**companion** deep-study artifact — it must not simply repeat the
newsletter's content. See `workflows/consulting_framework.md` for the
reasoning-loop, core curriculum, Analytical Lenses, and evidence-model
reference this workflow applies every week.

## Required input

1. **Today's date.**
2. **Tracker history** — run `python tools/manage_sheet.py tracker-read` to
   get every past row: `week_number, date, consultancy, client_or_case,
   industry, curriculum_topic, pass, key_takeaway, evidence_quality,
   lenses_used`. Compute this week's `week_number` as `len(rows) + 1` (or
   `1` if the tracker is empty). Use the `lenses_used` history for Lens
   Selection and the vignette judgment call below.
3. **Glossary** — run `python tools/manage_sheet.py glossary-read` to get
   every term already defined: `term, definition, first_seen_week,
   first_seen_topic`. Used in the Terminology step below.

## Picking the case

Research a real, named AI/data consulting engagement. Candidate sources
(not exhaustive, not ordered, not a constraint): McKinsey, BCG, Bain,
Accenture, Deloitte, PwC, EY, KPMG, Capgemini, Slalom, IBM Consulting,
Thoughtworks, AWS Professional Services, Microsoft, Google Cloud, the
Databricks/Snowflake ecosystems, or any other credible AI/data/technology
consultancy. Prioritize organizations that combine strategy → data →
engineering → AI → implementation, not strategy-only firms.

Score every candidate against the **case selection criteria** in
`workflows/consulting_framework.md` (strong problem, clear intervention,
technology relevance, business relevance, architecture value,
critical-thinking value, transferability, with a domain tie-breaker for
travel/e-commerce/marketplace/retail only when candidates are otherwise
equal) before committing. Check this week's candidate against every past
`client_or_case` in the tracker read above — if it's a duplicate, pick a
different case. A 2024 case with excellent public documentation is more
valuable than a 2026 case with almost no substance.

**Never weaken this selection to match the week's curriculum topic or to
manufacture relevance for a particular analytical lens.** The case is
chosen first, entirely on its own merits; topic and lenses are determined
afterward, from the case as selected.

If nothing suitable turns up after a genuine search, broaden the source
pool (Section "No suitable case" below) rather than defaulting to a weak
case.

## Picking the curriculum topic

Follow `workflows/consulting_framework.md`'s fixed 25-topic core curriculum
and pass-progression logic exactly. This week's topic and pass are computed
from the tracker read above, per that file's rules — this workflow does not
duplicate that logic here. Remember: the topic shapes emphasis on the
already-selected case; it never causes the case to be reselected or
reframed to fit.

## Lens Selection

After the case is researched and the reasoning loop reaches Opportunity/
Options (see `workflows/consulting_framework.md`'s reasoning loop), for
each of the four Analytical Lenses ask explicitly: **does this case's
actual decision/data genuinely call for this lens?**

- **ML Decision Lens** — is the actual decision a prediction problem where
  ML is a real candidate?
- **Impact & Causal Inference Lens** — is the actual decision "did this
  work / what caused this," not "what will happen"?
- **LLM/NLP Analytics Lens** — does the case use an LLM/NLP component as a
  pipeline step (raw text → structured data → analytics), not just a
  chatbot/agent front-end?
- **Marketplace Lens** — does the case involve two-sided supply/demand
  matching?

Zero, one, or multiple lenses may activate. **State explicitly which
activated and why, or state plainly that none did.** A zero-lens week is a
complete, valid outcome — write it that way, not as something missing (see
Newsletter/Deck structure below).

**Vignette judgment call.** Before finalizing which lenses are active,
weigh whether a short illustrative vignette is worth adding for a lens the
real case doesn't naturally touch. Consider together: how stale that lens
looks from the `lenses_used` history (a rough sense, not a countdown), how
important that lens is to the broader learning goal right now, and whether
the real case offers any natural partial angle into it before resorting to
an invented scenario. Staleness alone is not sufficient reason — most weeks
should have zero vignettes. When one does get added, it's a short paragraph
that seeds that week's "Your Turn" challenge; it never becomes a second
full case study, and the real case is still analyzed entirely on its own
merits first.

## Dimension Selection (deck)

Run this after Lens Selection, once the case's architecture is understood
— it drives the companion deck the same way Lens Selection drives the
newsletter's lens subsections. For each of the 13 Engineering Dimensions in
`workflows/consulting_framework.md`, ask: **is this materially relevant to
this case, this week?**

**Architecture** and **Technical Evaluation** are near-always material —
every real system has an architecture and some way to know if it's
working — and default to getting deck slide depth unless the case is
genuinely too thin to support either. The other 11 dimensions are
selective: assessed every week, but typically only **2-4 earn real slide
depth** in any given week. A dimension that doesn't earn a slide either
gets folded into a one-line mention inside Architectural Reasoning or
another material dimension's slide, or is silently not material this week
— the same "zero, one, or multiple, stated explicitly" discipline as Lens
Selection, not a checklist to cover exhaustively. **State explicitly which
dimensions got depth and why** on the deck's Engineering Challenge slide's
lead-in (see Deck content structure below) — never all 13, and never
padding a thin week to look comprehensive. If a lens is active, let it feed
technology-specific detail into the relevant dimension (e.g. an active ML
Decision Lens feeds Technical Evaluation's ML metric-selection detail, an
LLM/NLP Analytics Lens feeds Security's prompt-injection consideration
where material) rather than the dimension and the lens duplicating each
other.

## Research instructions

Use WebSearch/WebFetch to research the case directly — there is no separate
research tool; case selection, evidence classification, lens selection, and
critical analysis are reasoning tasks this agent performs directly.

Never invent a client name, consultancy claim, statistic, ROI figure,
architecture detail, model performance figure, causal effect, or extraction
accuracy. If evidence is thin, say less. Every material claim gets one of
the five evidence labels from `workflows/consulting_framework.md` applied
inline, using whichever lens-specific checklist applies (ROI, model
performance, causal/impact, extraction accuracy, or marketplace trade-off —
see that file's Evidence & Source Discipline section) — the same discipline
applies no matter which lens, or no lens, is active.

## Terminology

Before drafting, decide this week's 2-4 core vocabulary terms relevant to
this week's curriculum topic *and* any activated lens (e.g. for "Root-cause
analysis": five whys, fishbone/Ishikawa; for an active ML Decision Lens:
class imbalance, threshold, drift; for "Process mapping": SIPOC, BPMN — see
`workflows/consulting_framework.md`'s AI Value Discovery Framework for the
full set of named techniques these topics draw from). For each term, check
the Glossary read above (case-insensitive match on `term`):

- **Not yet defined** → give it a full plain-language definition in the
  deck's Key Terms slide, and queue it for `glossary-append` after a
  successful send.
- **Already defined** → don't redefine it. Add a brief inline pointer where
  it would otherwise appear unexplained, e.g. "five whys (see Week 3)" —
  citing `first_seen_week`. Only include it on the Key Terms slide if it's
  central enough to be worth a one-line reminder.

## Newsletter content structure

Core sections 01-03 and the final block run every week. The lens slot and
Consultant's Eye that follow it are **one subsection per activated lens**
(zero, one, or several), then a single Consultant's Eye — never a fixed
"ML Decision Lens" / "Production Lens" pairing regardless of which lens
actually fired.

**01 — The Consulting Case.** Narrative (not a bulleted fact list):
consultancy, client, industry, problem, context, current state,
intervention, outcome.

**02 — Behind the Engagement.** Short subsections: the real problem the
client needed solved · the current process/workflow · the consultancy's
approach · the technology · the outcome. Reconstruct the problem/process
subsections through `workflows/consulting_framework.md`'s AI Value Discovery
Framework — Business Process Mapping and User-Centred Discovery are Essential
tier, considered on every case regardless of curriculum topic — naming the
actual technique the evidence supports (e.g. "the public case study
describes a SIPOC-style handoff between X and Y") rather than a generic
process description; say so plainly when the source material doesn't
establish enough to name one.

**03 — Technology Choice.** Brief, business-level: what tool or platform the
consultancy chose and why (build vs. buy, vendor, category), in a few
sentences — not an architecture or data-flow breakdown. That depth belongs
to the companion deck's Engineering Dimensions (see
`workflows/consulting_framework.md`); point the reader there rather than
duplicating it here.

**[04, 05, ... — one per activated lens, if any].** Each activated lens
gets its own subsection at newsletter depth (prose, not deck-length detail),
following that lens's own reasoning steps from
`workflows/consulting_framework.md`:
- *ML Decision Lens* → business problem → ML formulation → data →
  baseline → candidate models → why this approach and why not the
  alternatives.
- *Impact & Causal Inference Lens* → the business question → whether
  randomisation was possible (and if so, why A/B testing is the natural
  first method) → the method actually used or that should be → key
  assumption(s) and limitation(s).
- *LLM/NLP Analytics Lens* → the extraction/transformation problem → why
  an LLM was/wasn't the right tool vs. rules/NLP/ML → how correctness would
  be evaluated.
- *Marketplace Lens* → supply/demand/matching → the key trade-off at stake.

If zero lenses activated, these numbered slots are simply omitted — the
newsletter renumbers straight from 03 to Consultant's Eye below, with no
gap and no filler.

**[Next] — Consultant's Eye.** Critical analysis: assumptions, missing
information, trade-offs, questionable claims, alternative approaches —
including a critique of any lens subsection(s) above. Include a compact
evidence ledger here (2-4 rows: claim | evidence label | what's missing) —
this is the only place evidence labels get tabulated in the newsletter.
**Always end this section with one explicit line stating which lens(es), if
any, activated this week and why** — e.g. "This case turned on ranking
quality under a fixed intervention budget — the ML Decision Lens applies"
or "This is a workflow/change-management story; no technical lens was the
right fit here, and that's the point: not every problem needs one." The
absence of a lens is a taught outcome, never a silent gap.

**[Next] — 🛑 Your Turn.** A related but NEW client problem — enough detail
to reason about problem, process, data, systems, constraints, objectives,
and stakeholders. Sourced in priority order per
`workflows/consulting_framework.md`'s Weekly challenge sourcing: (1) a real-
case extension, preferred whenever the case supports it; (2) a related-but-
new scenario when the real case doesn't stretch far enough; (3) a short
vignette, only when it adds genuine learning value (see Lens Selection
above) — never the default. End with an explicit line: **"STOP HERE —
solve this before reading on."**

**[Next] — Model Approach.** Run the new problem through the reasoning loop
in `workflows/consulting_framework.md`, including any activated lens's own
pipeline. Explicitly note where multiple approaches are defensible and why
— never present the model answer as the only possible one. Where useful,
call out what a strong answer would have covered that's easy to miss (a gap
diagnosis in prose, not a score).

**[Next] — Consulting Takeaway.** One sentence, one principle.

**[Next] — Further Reading.** 2-4 high-quality links, no more.

## Newsletter output format

A single self-contained HTML file written to `.tmp/newsletter.html` — inline
styles only, no external CSS/JS, table/div layout (no flexbox/grid), dark
masthead, a row of 3 stat tiles, at least one `<div>`-bar bar chart, the
sections above in order (with lens subsections included or omitted per Lens
Selection), and a footer line if tracker reading failed this run.

**Palette — use these exact hex values** (must match `tools/build_deck.py`'s
`PALETTE` dict and `design/system.md`):

| Role | Hex |
|---|---|
| Page background | `#FBF1E4` |
| Masthead / dark background | `#3D2F35` |
| Primary accent (dusty blue) | `#7FA8C9` |
| Secondary accent (rose) | `#D98C86` |
| Tertiary accent (gold) | `#E8B84B` |
| Quaternary accent (sage) | `#93B584` |
| Quinary accent (mauve) | `#B592C4` |
| Body text | `#453740` |
| Muted text | `#8A7A82` |
| Light background / tile fill | `#F5E6D3` |

No drop shadows, no custom fonts (stay on Arial/Helvetica), no background
blob shapes, no real icon images — an icon-style accent, if used, is a
plain CSS circle `div` with a bold unicode glyph/letter inside, never an
image file.

## Deck content structure — 10-14 slides

The deck is your recurring engineering-judgment artifact, not a slide-length
restatement of the newsletter — see `workflows/consulting_framework.md`'s
Engineering Dimensions and the Dimension Selection step above. Every deck
slide must teach something the newsletter doesn't already cover: the
newsletter owns the case, the evidence, and the business recommendation;
the deck owns how the underlying system works, how it would be designed,
evaluated, deployed, operated, secured, scaled, maintained, and improved.
Slide types come from `tools/build_deck.py` — see that file's docstring for
the exact JSON schema.

**Always present, minimal footprint:**
1. **Title** — case/topic name as the title. Subtitle: client, industry,
   consultancy, curriculum topic + pass, date, and any activated lens(es).
2. **Snapshot** — `snapshot` type: exactly 3 stats + sub-topic notes.
   Orientation only — the newsletter owns the full case narrative.
3. **Underlying Technical Concept** — `profile` type. Teaches a
   *transferable* concept, not a case recap: what it is, how it works, what
   data it needs, how it differs from adjacent approaches, when to use it,
   when not to.
3a. **Key Terms** — `profile` type, optional. Only when this week's
   Terminology step (above) queued newly-defined terms — one row per term,
   plain-language definition. Omit entirely on a week with nothing new to
   define.

**Architecture (near-always material — see Dimension Selection above):**
4. **Architecture & Data Flow** — `diagram` type, Verified / Inferred /
   Reference labels applied explicitly. Fold the client's before-state
   process into the same image as a before→after pair where that reads
   clearly; only render it as a separate diagram slide when the case
   genuinely needs both shown independently.
5. **Architectural Reasoning** — `content` (+ `comparison` if a real
   alternatives table exists) covering: why this architecture, why not the
   alternatives, what trade-off the choice introduces, what happens at 10x
   scale, what happens when a dependency fails, how it's operated and
   maintained. Merge into slide 4 as its body when there isn't enough
   distinct material to justify a second slide.

**Per activated lens (repeat this pair for each lens that activated; omit
entirely for a zero-lens week):**
6. **[Lens] Decision** — `content` type (+ `chart` if a concrete metric
   comparison exists), following that lens's own reasoning steps.
7. **[Lens] Comparison** — `comparison` type: candidates/options ×
   criteria, e.g. Model | Precision | Recall | Latency | Verdict for the ML
   Decision Lens, or Method | Assumption | Confidence for the Impact &
   Causal Lens. Skip this slide for a lens where no concrete comparison
   table applies (e.g. Marketplace Lens usually doesn't need one).

**Technical Evaluation (near-always material — see Dimension Selection
above):**
8. **Evaluation** — technology-specific per
   `workflows/consulting_framework.md`'s Engineering Dimension 13 (ML
   metrics, LLM/NLP task accuracy + hallucination/groundedness, RAG
   retrieval vs. generation quality, agentic task-completion/tool-use/
   trajectory, or process/data-system conformance — whichever the case
   actually uses), always distinguishing technical performance from
   business impact. Fold into slide 4/5 when there's too little distinct
   evaluation material to earn its own slide.

**Material Engineering Dimensions (0-N slides — typically 2-4, from
Dimension Selection above):** one slide per dimension judged material this
week, from the remaining 11 in `workflows/consulting_framework.md`'s
Engineering Dimensions (Data Quality/Readiness, Performance & Latency,
Reliability, Observability, Security, Scalability, Maintainability,
Cost & Value, Failure Modes, Human Oversight). `content` type unless a
concrete comparison applies. State on this block's lead-in which
dimensions got depth and why — never cover all 11, and never pad a thin
week to look comprehensive.

**Always present, closing:**
9. **Engineering Challenge** — `content` type, reusing the `**bold**`
   accent convention for emphasis. Varies by week to match what's material:
   design an architecture, choose an ML/LLM approach, design an evaluation
   framework, diagnose a production failure, reduce cost, improve
   reliability, address a security risk, or redesign the system. Distinct
   from the newsletter's business "🛑 Your Turn" — this trains engineering
   judgment, not business recommendation.
10. **Engineering Approach** — the model answer to slide 9, `content` +
    `profile` combo, drawing on whichever dimensions/lens pipeline this
    week's challenge exercises. Merge with slide 9 into one `profile` slide
    when the case is thin; keep as two when there's enough material for
    both — never pad.
11. **Engineering Takeaway** — `content` type, one systems-design
    principle, distinct from the newsletter's consulting takeaway.
12. **Further Reading (Technical)** — `content` type: sources on the
    underlying concept/technique, distinct from the newsletter's
    case/evidence sources.

A zero-lens, 2-material-dimension week naturally lands around 10-11 slides
(skip the lens pair entirely); a one-lens, 3-dimension week runs closer to
13-14. Stay within the hard cap of 14 regardless of how many lenses or
dimensions are material — merge or drop the thinnest material rather than
padding a week to cover everything shallowly. Depth over coverage: choosing
which 2-4 dimensions earn a slide is the point, not a shortcoming.

### Diagram generation

All diagrams (process-map, architecture, and any lens-specific diagram) are
pre-rendered PNGs via the vendored Excalidraw-style image pipeline — never
drawn by `build_deck.py` itself. Run from the project root:

```bash
node tools/excalidraw-visuals/generate-visual.js "<FULL_PROMPT>" \
  ".tmp/diagram_<case-slug>_<slide-slug>.png" "16:9" \
  --input "tools/excalidraw-visuals/brand-assets/excalidraw-style-reference.png"
```

Build `<FULL_PROMPT>` as the **light-mode style prefix** from
`tools/excalidraw-visuals/style-guide.md`, verbatim and unmodified, followed
by a diagram-specific description (title, layout, elements with exact
colors/fills/borders per the palette in that file, connections, labels — max
1-3 words per box, title max 5 words, total under ~30 words). Pick a layout
matching the actual mechanics: left-to-right flow for a process map,
layered/hub-and-spoke for an architecture diagram. This calls the kie.ai
image API (`KIE_AI_API_KEY`) and costs money per generation — treat this as
an expected cost of a normal run. Eyeball the generated PNG before embedding
it — regenerate with simplified wording if a label is garbled.

Reference the output path in the slide JSON:
`{"type": "diagram", "title": "...", "image": ".tmp/diagram_....png"}`.

## Tool calls

Run these in order, from the project root:

```bash
python tools/build_deck.py .tmp/weekly_deck_content.json .tmp
```

`build_deck.py` computes its own output filename from the JSON's
`date`/`case`/`client` fields — `{date}_{case-slug}_{client-slug}.pptx` —
and prints the full path on success. Read that exact path from the command
output and use it verbatim in the QA gate call and the `--attach` argument
below.

Before sending, run the QA gate — a single deterministic-plus-LLM-judge
pass over the finished newsletter and deck (see Edge Cases below for the
FAIL path). This also covers the iCloud-sync-race pptx zip-validity check
that used to be a standalone command here:

```bash
python tools/evaluate_output.py \
  --newsletter .tmp/newsletter.html \
  --deck-json .tmp/weekly_deck_content.json \
  --deck-pptx <path printed by build_deck.py>
```

Prints `{"pass": bool, "issues": [...], "llm_judge": {...}}` as JSON and
exits non-zero on FAIL. **Only proceed to `send_email.py` if this exits 0.**

```bash
python tools/send_email.py \
  --html .tmp/newsletter.html \
  --subject "AI Consulting Weekly: <Consultancy> × <Client> — <Curriculum Topic> — <YYYY-MM-DD>" \
  --to tiffanychow214@gmail.com \
  --attach <path printed by build_deck.py>
```

## History update

Only after `send_email.py` exits 0:

```bash
python tools/manage_sheet.py tracker-append \
  --week <week_number computed above> \
  --date YYYY-MM-DD \
  --consultancy "Consultancy Name" \
  --client "Client or case identifier" \
  --industry "Industry" \
  --topic "Curriculum Topic" \
  --pass N \
  --takeaway "This week's one-line consulting takeaway" \
  --evidence-quality "Strong|Mixed|Weak" \
  --lenses "ML Decision,Marketplace" \
  --concepts "five whys,class imbalance" \
  --production-concepts "monitoring,drift,rollback" \
  --difficulty "Understand|Apply|Design-Defend" \
  --challenge-type "real-case extension|related scenario|vignette" \
  --qa-gate-result "Pass|Fail" \
  --qa-issues-count <N>
```

`--qa-gate-result` and `--qa-issues-count` come straight from
`evaluate_output.py`'s own JSON output for this run (`pass` → `Pass`/`Fail`,
`len(issues)`) — the mechanically-computed counterpart to the self-reported
`--evidence-quality` flag above. Since `tracker-append` only runs after
`send_email.py` exits 0, and the QA gate already gated the send,
`qa_gate_result` will be `Pass` on essentially every logged row by
construction; the useful signal for `tracker-summary` (see
`tools/manage_sheet.py`) is `qa_issues_count` trending over time (near-misses
that still passed) and any historical blank values from before this feature
existed.

`--lenses` is comma-separated, using the exact lens names from
`workflows/consulting_framework.md` (`ML Decision`, `Impact & Causal
Inference`, `LLM/NLP Analytics`, `Marketplace`), or omitted/empty for a
zero-lens week. `--concepts` and `--production-concepts` are lightweight,
comma-separated, and optional — free-text tags for concepts practiced
beyond the headline curriculum topic (empty when nothing further to note;
`--production-concepts` empty on a week with no meaningful production
content). `--difficulty` is a short free-text tier describing the case's
difficulty (distinct from the numeric `--pass`), and `--challenge-type`
records which of the Weekly challenge sourcing options
(`workflows/consulting_framework.md`) supplied this week's "Your Turn."
None of these four are scored or graded — they exist purely to make
learning coverage visible over time.

Then, for each newly-defined term queued in the Terminology step:

```bash
python tools/manage_sheet.py glossary-append \
  --term "five whys" \
  --definition "..." \
  --week <same week_number> \
  --topic "Curriculum Topic"
```

## Run status reporting

The unattended CI job cannot tell a genuine send from an aborted run just
from `claude`'s own exit code — an agent that reasons its way to "abort, do
not send" per an Edge Case below and stops cleanly still exits 0. To make
that distinguishable, **the very last action of every run, whatever the
outcome, is writing `.tmp/run_status.json`**:

- On a successful send: `{"email_sent": true, "week_number": <N>, "date": "YYYY-MM-DD", "case": "<client_or_case>"}`.
- On any abort (QA gate fails twice, no suitable case found, tracker/glossary
  write failure after a successful send is NOT an abort — see below, etc.):
  `{"email_sent": false, "reason": "<one-sentence reason>"}`.

The CI workflow reads this file after the run and fails the job when
`email_sent` is not `true` — this is what turns a silent no-send week into a
visible red X in GitHub Actions instead of a misleading green check.

## Edge cases

- **Weak consultancy case** — find another case or clearly state the
  limitations of the one selected. Never publish a thin case as substantive.
- **Consultancy marketing claims** — attribute them explicitly as
  CONSULTANCY-REPORTED CLAIM, not fact.
- **Missing ROI / architecture / model performance / causal effect /
  extraction accuracy** — do not invent it, for any lens; label UNKNOWN and
  say the public source does not establish it.
- **Conflicting sources** — identify the disagreement explicitly and explain
  which source is more credible and why.
- **Case disappears mid-run** — use information already retrieved for this
  run; don't treat `.tmp/` as permanent history.
- **Duplicate case** — checked against the tracker in the case-selection
  step; if found, pick a different case.
- **No suitable case** — broaden the source pool before ever defaulting to
  a weak case.
- **Curriculum topic doesn't naturally fit the case** — this is expected
  and fine. The topic shapes emphasis on the case as selected; it never
  causes the case to be swapped, weakened, or reinterpreted. If the topic
  genuinely can't be connected to the case at all, say so plainly in the
  newsletter rather than forcing an artificial connection.
- **No lens applies this week** — a fully valid, complete outcome. State it
  explicitly in section 04 (see Newsletter content structure) rather than
  leaving an unexplained gap. Do not manufacture a lens or add a vignette
  just to have one — see the Lens Selection vignette judgment call.
- **Multiple lenses activate in the same week** — cover each with its own
  slide pair (deck) and subsection (newsletter); if this pushes the deck
  past the 14-slide cap, merge the thinner lens's slides rather than
  dropping a lens or padding.
- **Too difficult a challenge** — adjust the "Your Turn" problem's
  difficulty while keeping the same underlying learning objective (core
  topic + pass, and any active lens's own pass) — don't silently swap to an
  easier topic or drop the lens.
- **Newsletter/deck overlap** — the two artifacts have different jobs, not
  just different formats: the newsletter owns the case, the evidence, and
  the business recommendation (what happened, why the client did it, what
  evidence supports it, what a consultant should recommend); the deck owns
  the underlying technical system (how it works, how it would be designed,
  evaluated, deployed, operated, secured, scaled, maintained, improved) —
  see `workflows/consulting_framework.md`'s Engineering Dimensions. This is
  structural, not just a style rule: the deck's Dimension Selection step
  (see above) means its slides are earned per-dimension based on what's
  actually material, not templated from the newsletter's sections — a deck
  slide that could be dropped without losing any engineering content the
  newsletter doesn't already have is a slide that shouldn't exist. The
  deck's snapshot slide may reuse headline stats for orientation, but
  nothing beyond that is shared prose.
- **`build_deck.py` fails** (malformed JSON, missing required fields,
  invalid `comparison` slide data) — read the full error, fix the JSON
  content, and retry. Do not fall back to a text-only email.
- **`evaluate_output.py` reports FAIL** — read the `issues` list. If the
  issues are fixable by revising the newsletter/deck content (e.g. an
  unlabeled claim, a suspiciously precise unlabeled statistic), retry the
  drafting step **once**, addressing every flagged issue specifically, then
  rebuild the deck and re-run the QA gate. If it fails a second time, or the
  issue is structural/unfixable within this run (e.g. the judge flags the
  case itself as thin/duplicate-ish), **abort without sending and without
  appending to the tracker** — surface the full issue list so the run
  visibly fails, exactly as an unattended `send_email.py` failure would.
  Never send on a FAIL, and never retry more than once (same "no silent or
  repeated retries" discipline as `send_email.py`).
- **`excalidraw-visuals` generation fails** — retry once with a simplified
  prompt if it looks like a content/spelling issue, otherwise surface the
  failure. Do not substitute a text/bullet slide for a diagram.
- **iCloud sync race condition** — this project's directory sits under
  iCloud-synced `~/Desktop`. A built `.pptx` can grow/become an invalid zip
  between `build_deck.py` finishing and the attach step; `evaluate_output.py`
  checks this as part of the QA gate. If it reports a corrupt zip, rebuild
  and re-run the gate, or copy the freshly-built file to a non-synced
  scratch path immediately before re-checking and attaching.
- **`send_email.py` fails** — read the full error; do not retry beyond the
  tool's own internal single retry. Do **not** mark the week complete in
  the tracker.
- **Tracker/glossary unreadable or write fails** — if reading fails before
  the run starts: still send, defaulting to topic #1 / pass 1, with a
  footer line noting sequence tracking failed this run (lens depth will
  also be unavailable this run — proceed with a conservative Pass 1
  assumption for any lens used). If the write fails **after** a successful
  email send: the email was already delivered — do not treat this as a
  failed run, but surface the failure so the log can be repaired manually.
- **My answer is weak / strong** — this only applies retroactively; the
  Model Approach section should make gaps easy to notice on review, not
  flatter or score numerically.
- **Multiple valid answers to the challenge** — explain in the Model
  Approach section why different recommendations could be defensible.
- **Paid API failure** (WebSearch/WebFetch, model calls, kie.ai diagram
  generation, `evaluate_output.py`'s LLM-judge call) — expected costs of a
  normal run; don't check in before making them. Do check in before
  *repeatedly* retrying a call that keeps failing.
