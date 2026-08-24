# AI Consulting Weekly

An autonomous pipeline that researches, writes, and emails a weekly two-part
deliverable studying a real AI/data consulting engagement:

1. **A newsletter** covering one real, named consulting case in depth — the
   client, the problem, the consultancy's approach, a brief technology
   choice, and a critical evaluation of the evidence behind it — ending in a
   new, related client problem the reader must solve before reading the
   model approach.
2. **A companion deck** — a recurring AI/data systems-engineering learning
   artifact, not a slide-length recap of the newsletter. Each week it
   assesses 13 candidate engineering dimensions (architecture, data quality,
   performance, reliability, observability, security, scalability,
   maintainability, cost/value, failure modes, human oversight, technical
   evaluation) for materiality and gives real depth only to the 2-4 that
   actually apply, plus a technology-specific evaluation walkthrough and a
   varying engineering challenge (design an architecture, diagnose a
   failure, reduce cost, etc.) distinct from the newsletter's business one.

It runs unattended on a weekly GitHub Actions cron (Sundays) and emails both
to a single recipient.

## Why this exists

This is a personal learning project: a forcing function to develop the
ability to think like an AI/data solutions consultant — problem framing,
discovery questioning, root-cause analysis, AI suitability judgement,
solution architecture, ROI reasoning, risk analysis, and executive
communication — by studying real engagements and then solving a related new
problem myself before ever seeing a model answer.

It is the sibling project to **AI Agents Weekly**, which asks "how is this
AI product architected?" This project asks a different question: **"what
technology solution did the consultancy choose to solve the client's
business problem, and why, and would I have chosen the same thing?"**

It's also another demonstration of the **WAT framework** — separating
*Workflows* (plain-language instructions), *Agents* (the orchestrating LLM),
and *Tools* (deterministic scripts). See [`CLAUDE.md`](CLAUDE.md) for the
full architecture writeup, and
[`workflows/consulting_framework.md`](workflows/consulting_framework.md)
for the reasoning-loop, curriculum, and evidence-model reference this
project applies every week.

## How a week runs

1. Reads history from a Google Sheet: which weeks/cases/curriculum topics
   have already run (`tools/manage_sheet.py`), and which terminology has
   already been defined.
2. Picks this week's **case** (a real consulting engagement, scored against
   explicit selection criteria, checked against the tracker for duplicates)
   and this week's **curriculum topic** from a fixed, 26-topic curriculum
   that never skips or repeats within a pass.
3. Researches the case via web search — never invents a client name,
   statistic, ROI figure, or architecture detail. Every material claim is
   tagged as VERIFIED FACT / CLIENT-REPORTED RESULT /
   CONSULTANCY-REPORTED CLAIM / INFERENCE / UNKNOWN.
4. Writes the newsletter as a single self-contained HTML file, ending in a
   "Your Turn" challenge with an explicit stop instruction.
5. Builds the deck's diagrams as hand-drawn-style PNGs via
   [`tools/excalidraw-visuals/`](tools/excalidraw-visuals/), then renders
   the full slide deck with `tools/build_deck.py` (python-pptx) — the
   newsletter is the one place evidence quality gets tabulated; the deck's
   slides are earned per Engineering Dimension, not templated from it.
6. Emails both to the recipient via `tools/send_email.py`, then appends
   this week's row to the tracker sheet — only after a successful send.

The full step-by-step instructions the agent follows live in
[`workflows/weekly_consulting_case.md`](workflows/weekly_consulting_case.md).

## Project layout

```
workflows/      Markdown SOPs — what to do, in what order, how to handle failures
tools/          Deterministic Python/Node scripts that do the actual work
design/         The palette/component system shared by the newsletter and deck
assets/         Generated icon set used in the deck
.github/        The weekly cron (GitHub Actions)
```

## Running it yourself

Requires:
- Python 3.11+ (`pip install -r requirements.txt`)
- Node 18+ (for the diagram-generation script — stdlib only, no npm install)
- A Google Cloud service account with Sheets API access (`service_account.json`)
  — the same one used by AI Agents Weekly works fine, just share the new
  spreadsheet with it (Editor).
- A Gmail account with an app password
- An Anthropic API key and a kie.ai API key

Environment variables (`.env`, never committed):

```
GMAIL_ADDRESS=
GMAIL_APP_PASSWORD=
ANTHROPIC_API_KEY=
KIE_AI_API_KEY=
```

Then, from the project root:

```bash
claude -p "$(cat workflows/weekly_consulting_case.md)"
```

The GitHub Actions workflow (`.github/workflows/weekly_consulting_case.yml`)
runs the same command on a weekly Sunday schedule using repo secrets instead
of a local `.env`.
