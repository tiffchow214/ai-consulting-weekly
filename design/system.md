# Design System — AI Consulting Weekly (Newsletter + Deck)

Same palette and component system as AI Agents Weekly's `design/system.md`
(the sibling project this one was built from), applied mechanically every
week by `tools/build_deck.py` and the newsletter's inline CSS. Accent
emphasis is rotated relative to the sibling project — dusty blue is primary
here instead of rose — so the two newsletters/decks read as a visual family
while staying distinguishable at a glance in an inbox or on a screen.

## Palette

Single source of truth for `PALETTE` in `tools/build_deck.py`; the
newsletter's inline hex values must match exactly so the email and deck
never visually drift.

| Role | Hex | Used for |
|---|---|---|
| `background` | `#FBF1E4` | Title-slide fill, newsletter page background |
| `masthead` | `#3D2F35` | Dark card/header bands, newsletter masthead |
| `accent_primary` (dusty blue) | `#7FA8C9` | Primary accent — bars, rules, badges |
| `accent_secondary` (rose) | `#D98C86` | Secondary accent |
| `accent_tertiary` (gold) | `#E8B84B` | Tertiary accent |
| `accent_quaternary` (sage) | `#93B584` | 4th categorical accent |
| `accent_quinary` (mauve) | `#B592C4` | 5th categorical accent |
| `body_text` | `#453740` | Body copy on light backgrounds |
| `muted_text` | `#8A7A82` | Captions, footers, secondary text |
| `light_bg` (tile fill) | `#F5E6D3` | Stat tiles, card fills — one step deeper than `background` so cards read as distinct from the page |

Five accents so icon badges, diagram nodes, and the evidence-ledger table
have enough variety to avoid repeating a color within one slide. Evidence
labels (see `workflows/consulting_framework.md`) map to specific accents via
`EVIDENCE_COLOR` in `build_deck.py`, so the same claim type always reads as
the same color across every week's deck.

Rationale for readability: accent badges hold a **white** icon glyph, so
each accent is kept mid-depth (not baby-pastel-light) — light enough to
read as "soft," dark enough that a white glyph stays legible. `body_text`
and `masthead` are warm charcoal/plum tones, not pure black, to stay in the
same warm family as the cream background rather than reading as jarring on
top of it.

## Type scale

Point-size constants in `build_deck.py`:

| Role | Size |
|---|---|
| Title slide headline | 40pt bold |
| Title slide subtitle | 20pt |
| Section slide title | 26pt bold |
| Content body / bullets | 16-18pt |
| Stat tile value | 26pt bold |
| Stat tile label / captions | 11pt |
| Table cell text | 12-14pt |
| Footer / page number | 10pt |

## Spacing

- Slide margin: 0.6in on all sides (`MARGIN` constant).
- Slide canvas: 13.333in × 7.5in (16:9).
- Card/tile gaps: 0.3in between stat tiles and between diagram nodes.

## Icon badges

- A solid-fill circle, one accent color from the 5-color cycle, fixed
  diameter (~0.6in on stat callouts, ~0.9in on diagram nodes).
- A single-color **white** flat-line icon glyph centered inside, sized to
  roughly 55% of the circle's diameter.
- Icon set (generated once, deterministically, via `tools/generate_icons.py`
  using Pillow — no image-generation tool, no external icon library):
  `gear` (mechanism/process), `shield` (safety/governance/risk), `network`
  (systems/integration), `chart` (stats/value), `checkmark`
  (success/resolution), `warning` (risk/misconception), `book` (further
  reading/reference), `search` (research/discovery questioning), `scale`
  (risk & trade-off analysis), `stop` ("Your Turn" challenge), `bulb`
  (consulting takeaway). Extendable later without changing the
  badge-rendering code — new icons are just new PNGs in `assets/icons/`.
- Diagram-slide nodes get an optional `"icon"` key per step (content picks
  the icon explicitly) so it's never guessed from label text; defaults to
  `gear` if omitted.

## Evidence ledger table

The `table` slide type (see `tools/build_deck.py`'s `add_table_slide`) is
this project's one addition beyond the sibling project's slide types: a
3-column claim/evidence/caveat table, header row in `masthead` with white
text, body rows alternating `background`/`light_bg`, and the evidence
column's text colored per `EVIDENCE_COLOR` so a reader can scan a slide's
overall evidence quality at a glance.

## Newsletter constraints (unchanged from the sibling project)

- Inline styles only, no external CSS/JS, table/div layout (no
  flexbox/grid) — email-client safety.
- No drop shadows, no custom/rounded fonts (stay on Arial/Helvetica), no
  background blob shapes.
- No real icon images in the email — any icon-style accent is a plain CSS
  circle `div` with a bold unicode glyph/letter inside, never an image
  file.
