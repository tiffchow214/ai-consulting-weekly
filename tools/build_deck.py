"""Render a structured slide-content JSON file into a styled .pptx deck.

Usage:
    python tools/build_deck.py <input.json> <output_dir>

Writes to <output_dir>/{date}_{case-slug}_{client-slug}.pptx — the filename
is computed from the JSON's own date/case/client fields, not passed in, so
it can never drift from the content it describes. Prints the full resulting
path on success.

Input JSON schema (see workflows/weekly_consulting_case.md for the
authoritative description the agent is briefed on):

{
  "client": "string",
  "date": "YYYY-MM-DD",
  "case": "string",
  "slides": [
    {"type": "title", "title": "string", "subtitle": "string"},

    {"type": "content", "title": "string", "bullets": ["string", ...]},
    # Wrap a name in **double asterisks** inside a bullet (e.g. "**Acme
    # Corp** cut lead time by...") to render it bold and accent-colored —
    # this is how named clients/consultancies should be called out.

    {"type": "chart", "title": "string", "chart": {
        "type": "bar", "categories": ["string", ...],
        "series_name": "string", "values": [number, ...]
    }},

    {"type": "diagram", "title": "string", "image": "path/to/rendered.png"}
    # Path to a PNG already rendered by the excalidraw-visuals pipeline (see
    # workflows/weekly_consulting_case.md). This is the only way diagram
    # content reaches the deck — build_deck.py never draws diagram
    # mechanics itself, it just places the image, scaled to fit the slide's
    # content area without distorting its aspect ratio, and centered.

    {"type": "profile", "title": "string", "subtitle": "string",
     "fields": [{"label": "string", "value": "string"}, ...]}
    # A structured approach/architecture deep-dive card, or (repurposed) a
    # Key Terms slide: term as "label", plain-language definition as "value".

    {"type": "snapshot", "title": "string",
     "stats": [{"label": "string", "value": "string", "icon": "string"}, ... exactly 3],
     "subsectors": [{"name": "string", "note": "string"}, ...]}
    # A compressed one-slide client/problem snapshot: exactly 3 icon-badge
    # stat callouts plus one line per sub-topic — not a recap of the
    # newsletter's Behind the Engagement section, just enough context before
    # the deck moves on to the case analysis. "icon" per stat is optional
    # (one of VALID_ICONS; defaults to "chart" if omitted).

    {"type": "table", "title": "string",
     "rows": [{"claim": "string", "evidence": "string", "caveat": "string"}, ...]}
    # An evidence ledger: one row per material claim, "evidence" must be one
    # of VALID_EVIDENCE_LABELS (VERIFIED FACT / CLIENT-REPORTED RESULT /
    # CONSULTANCY-REPORTED CLAIM / INFERENCE / UNKNOWN — see
    # workflows/consulting_framework.md), "caveat" is what's missing or
    # worth questioning about that claim. This is the deck's one place to
    # tabulate evidence quality — don't duplicate it elsewhere in the deck.

    {"type": "comparison", "title": "string",
     "columns": ["string", ...],
     "rows": [["string", ...], ...]}
    # An arbitrary-column comparison table for candidates/options, e.g.
    # columns=["Model","Precision","Recall","Latency","Verdict"] (ML
    # Decision Lens) or columns=["Method","Assumption","Confidence"]
    # (Impact & Causal Inference Lens) — see
    # workflows/consulting_framework.md's Analytical Lenses. Each row must
    # have exactly one cell per column. Distinct from "table" above: this is
    # for comparing options against arbitrary criteria, not for tabulating
    # evidence labels — use "table" for the evidence ledger and this for a
    # lens's model/option comparison.
  ]
}

On any structural problem, this raises and exits non-zero rather than
emitting a partial deck — a malformed run should fail loudly, not ship a
text-only fallback.

PALETTE and the icon-badge treatment below follow design/system.md — the
canonical source of truth. workflows/weekly_consulting_case.md inlines the
same hex values for the newsletter HTML so the email and deck never visually
drift. This palette matches AI Agents Weekly's exactly, with accent emphasis
swapped (dusty blue promoted to primary, rose demoted to secondary) so the
two newsletters/decks read as a visual family while staying distinguishable
at a glance.
"""

import argparse
import json
import re
import sys
from pathlib import Path

from PIL import Image as PILImage
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.util import Emu, Inches, Pt

# Palette per design/system.md — single source of truth, mirrored in the
# newsletter's inline CSS hex values so the email and deck never drift.
# Same hexes as AI Agents Weekly, accent emphasis rotated (dusty blue is now
# primary, rose secondary, sage moved to quaternary) to keep the two
# products visually related but distinguishable at a glance.
PALETTE = {
    "background": "FBF1E4",
    "masthead": "3D2F35",
    "accent_primary": "7FA8C9",
    "accent_secondary": "D98C86",
    "accent_tertiary": "E8B84B",
    "accent_quaternary": "93B584",
    "accent_quinary": "B592C4",
    "body_text": "453740",
    "muted_text": "8A7A82",
    "light_bg": "F5E6D3",
}

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ICONS_DIR = PROJECT_ROOT / "assets" / "icons"
DEFAULT_ICON = "gear"
VALID_ICONS = {"gear", "shield", "network", "chart", "checkmark", "warning", "book", "search", "scale", "stop", "bulb"}
VALID_EVIDENCE_LABELS = {
    "VERIFIED FACT",
    "CLIENT-REPORTED RESULT",
    "CONSULTANCY-REPORTED CLAIM",
    "INFERENCE",
    "UNKNOWN",
}
EVIDENCE_COLOR = {
    "VERIFIED FACT": "accent_quaternary",
    "CLIENT-REPORTED RESULT": "accent_tertiary",
    "CONSULTANCY-REPORTED CLAIM": "accent_secondary",
    "INFERENCE": "accent_quinary",
    "UNKNOWN": "muted_text",
}

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
MARGIN = Inches(0.6)
CONTENT_W = SLIDE_W - 2 * MARGIN
CHART_COLOR_CYCLE = ["accent_primary", "accent_secondary", "accent_tertiary", "accent_quaternary", "accent_quinary"]


def rgb(hex_str: str) -> RGBColor:
    return RGBColor.from_string(hex_str)


DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
MIN_SLIDES = 4
MAX_SLIDES = 20
VALID_TYPES = {"title", "content", "chart", "diagram", "profile", "snapshot", "table", "comparison"}


class DeckContentError(ValueError):
    pass


def validate(data: dict) -> None:
    if not isinstance(data, dict):
        raise DeckContentError("Top-level JSON must be an object.")

    for key in ("client", "date", "case", "slides"):
        if key not in data:
            raise DeckContentError(f"Missing required top-level key: '{key}'.")

    if not isinstance(data["client"], str) or not data["client"].strip():
        raise DeckContentError("'client' must be a non-empty string.")

    if not isinstance(data["case"], str) or not data["case"].strip():
        raise DeckContentError("'case' must be a non-empty string.")

    if not isinstance(data["date"], str) or not DATE_RE.match(data["date"]):
        raise DeckContentError("'date' must be a string in YYYY-MM-DD format.")

    slides = data["slides"]
    if not isinstance(slides, list) or not slides:
        raise DeckContentError("'slides' must be a non-empty list.")
    if not (MIN_SLIDES <= len(slides) <= MAX_SLIDES):
        raise DeckContentError(
            f"'slides' has {len(slides)} entries; expected between "
            f"{MIN_SLIDES} and {MAX_SLIDES}."
        )

    for i, slide in enumerate(slides):
        prefix = f"slides[{i}]"
        if not isinstance(slide, dict):
            raise DeckContentError(f"{prefix} must be an object.")

        slide_type = slide.get("type")
        if slide_type not in VALID_TYPES:
            raise DeckContentError(
                f"{prefix}.type must be one of {sorted(VALID_TYPES)}, got {slide_type!r}."
            )

        if not isinstance(slide.get("title"), str) or not slide["title"].strip():
            raise DeckContentError(f"{prefix}.title must be a non-empty string.")

        if slide_type == "content":
            bullets = slide.get("bullets")
            if not isinstance(bullets, list) or not bullets:
                raise DeckContentError(f"{prefix}.bullets must be a non-empty list.")
            if not all(isinstance(b, str) and b.strip() for b in bullets):
                raise DeckContentError(f"{prefix}.bullets must all be non-empty strings.")

        elif slide_type == "chart":
            chart = slide.get("chart")
            if not isinstance(chart, dict):
                raise DeckContentError(f"{prefix}.chart must be an object.")
            if chart.get("type") != "bar":
                raise DeckContentError(f"{prefix}.chart.type must be 'bar' (only type supported).")
            categories = chart.get("categories")
            values = chart.get("values")
            if not isinstance(categories, list) or not categories:
                raise DeckContentError(f"{prefix}.chart.categories must be a non-empty list.")
            if not isinstance(values, list) or not values:
                raise DeckContentError(f"{prefix}.chart.values must be a non-empty list.")
            if len(categories) != len(values):
                raise DeckContentError(
                    f"{prefix}.chart.categories and .values must be the same length "
                    f"({len(categories)} vs {len(values)})."
                )
            if not all(isinstance(v, (int, float)) for v in values):
                raise DeckContentError(f"{prefix}.chart.values must all be numbers.")
            if not isinstance(chart.get("series_name"), str) or not chart["series_name"].strip():
                raise DeckContentError(f"{prefix}.chart.series_name must be a non-empty string.")

        elif slide_type == "diagram":
            image = slide.get("image")
            if not isinstance(image, str) or not image.strip():
                raise DeckContentError(
                    f"{prefix}.image must be a non-empty string path to an excalidraw-visuals-generated PNG."
                )
            if not Path(image).is_file():
                raise DeckContentError(f"{prefix}.image does not exist: {image!r}.")

        elif slide_type == "profile":
            fields = slide.get("fields")
            if not isinstance(fields, list) or not fields:
                raise DeckContentError(f"{prefix}.fields must be a non-empty list.")
            for j, field in enumerate(fields):
                if not isinstance(field, dict):
                    raise DeckContentError(f"{prefix}.fields[{j}] must be an object.")
                if not isinstance(field.get("label"), str) or not field["label"].strip():
                    raise DeckContentError(f"{prefix}.fields[{j}].label must be a non-empty string.")
                if not isinstance(field.get("value"), str) or not field["value"].strip():
                    raise DeckContentError(f"{prefix}.fields[{j}].value must be a non-empty string.")

        elif slide_type == "snapshot":
            stats = slide.get("stats")
            if not isinstance(stats, list) or len(stats) != 3:
                raise DeckContentError(f"{prefix}.stats must be a list of exactly 3 items.")
            for j, stat in enumerate(stats):
                if not isinstance(stat, dict):
                    raise DeckContentError(f"{prefix}.stats[{j}] must be an object.")
                if not isinstance(stat.get("label"), str) or not stat["label"].strip():
                    raise DeckContentError(f"{prefix}.stats[{j}].label must be a non-empty string.")
                if not isinstance(stat.get("value"), str) or not stat["value"].strip():
                    raise DeckContentError(f"{prefix}.stats[{j}].value must be a non-empty string.")
                if "icon" in stat and stat["icon"] not in VALID_ICONS:
                    raise DeckContentError(
                        f"{prefix}.stats[{j}].icon must be one of {sorted(VALID_ICONS)}, got {stat['icon']!r}."
                    )

            subsectors = slide.get("subsectors")
            if not isinstance(subsectors, list) or not subsectors:
                raise DeckContentError(f"{prefix}.subsectors must be a non-empty list.")
            for j, sub in enumerate(subsectors):
                if not isinstance(sub, dict):
                    raise DeckContentError(f"{prefix}.subsectors[{j}] must be an object.")
                if not isinstance(sub.get("name"), str) or not sub["name"].strip():
                    raise DeckContentError(f"{prefix}.subsectors[{j}].name must be a non-empty string.")
                if not isinstance(sub.get("note"), str) or not sub["note"].strip():
                    raise DeckContentError(f"{prefix}.subsectors[{j}].note must be a non-empty string.")

        elif slide_type == "table":
            rows = slide.get("rows")
            if not isinstance(rows, list) or not rows:
                raise DeckContentError(f"{prefix}.rows must be a non-empty list.")
            for j, row in enumerate(rows):
                if not isinstance(row, dict):
                    raise DeckContentError(f"{prefix}.rows[{j}] must be an object.")
                for field in ("claim", "evidence", "caveat"):
                    if not isinstance(row.get(field), str) or not row[field].strip():
                        raise DeckContentError(f"{prefix}.rows[{j}].{field} must be a non-empty string.")
                if row["evidence"] not in VALID_EVIDENCE_LABELS:
                    raise DeckContentError(
                        f"{prefix}.rows[{j}].evidence must be one of {sorted(VALID_EVIDENCE_LABELS)}, "
                        f"got {row['evidence']!r}."
                    )

        elif slide_type == "comparison":
            columns = slide.get("columns")
            if not isinstance(columns, list) or len(columns) < 2:
                raise DeckContentError(f"{prefix}.columns must be a list of at least 2 column names.")
            if not all(isinstance(c, str) and c.strip() for c in columns):
                raise DeckContentError(f"{prefix}.columns must all be non-empty strings.")

            rows = slide.get("rows")
            if not isinstance(rows, list) or not rows:
                raise DeckContentError(f"{prefix}.rows must be a non-empty list.")
            for j, row in enumerate(rows):
                if not isinstance(row, list) or len(row) != len(columns):
                    raise DeckContentError(
                        f"{prefix}.rows[{j}] must be a list with exactly {len(columns)} cells "
                        f"(one per column), got {len(row) if isinstance(row, list) else type(row).__name__}."
                    )
                if not all(isinstance(cell, str) and cell.strip() for cell in row):
                    raise DeckContentError(f"{prefix}.rows[{j}] cells must all be non-empty strings.")


# ---------------------------------------------------------------------------
# Rendering helpers
# ---------------------------------------------------------------------------


def add_bold_runs(paragraph, text: str, base_size: Pt, base_color: RGBColor,
                   bold_color: RGBColor = None) -> None:
    """Split text on **bold** markers and add styled runs to paragraph."""
    bold_color = bold_color or rgb(PALETTE["accent_primary"])
    pos = 0
    for m in BOLD_RE.finditer(text):
        if m.start() > pos:
            run = paragraph.add_run()
            run.text = text[pos:m.start()]
            run.font.size = base_size
            run.font.color.rgb = base_color
        run = paragraph.add_run()
        run.text = m.group(1)
        run.font.size = base_size
        run.font.bold = True
        run.font.color.rgb = bold_color
        pos = m.end()
    if pos < len(text):
        run = paragraph.add_run()
        run.text = text[pos:]
        run.font.size = base_size
        run.font.color.rgb = base_color


def add_chrome(slide, title: str, footer_text: str, page_num: int) -> None:
    """Top accent bar, title, underline rule, and footer branding/page number
    shared by every non-title slide, for a consistent look across the deck."""
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, Inches(0.14))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = rgb(PALETTE["accent_primary"])
    top_bar.line.fill.background()
    top_bar.shadow.inherit = False

    title_box = slide.shapes.add_textbox(MARGIN, Inches(0.35), CONTENT_W, Inches(0.7))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = rgb(PALETTE["masthead"])

    rule = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, MARGIN, Inches(1.0), Inches(1.1), Pt(3))
    rule.fill.solid()
    rule.fill.fore_color.rgb = rgb(PALETTE["accent_tertiary"])
    rule.line.fill.background()
    rule.shadow.inherit = False

    footer = slide.shapes.add_textbox(MARGIN, Inches(7.08), CONTENT_W, Inches(0.35))
    ftf = footer.text_frame
    fp = ftf.paragraphs[0]
    fp.text = footer_text
    fp.font.size = Pt(10)
    fp.font.color.rgb = rgb(PALETTE["muted_text"])

    page_box = slide.shapes.add_textbox(SLIDE_W - Inches(1.1), Inches(7.08), Inches(0.7), Inches(0.35))
    ptf = page_box.text_frame
    pp = ptf.paragraphs[0]
    pp.text = str(page_num)
    pp.font.size = Pt(10)
    pp.font.color.rgb = rgb(PALETTE["muted_text"])
    pp.alignment = PP_ALIGN.RIGHT


def add_title_slide(prs: Presentation, slide_data: dict, client: str, date: str) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank layout
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = rgb(PALETTE["masthead"])

    title_box = slide.shapes.add_textbox(Inches(0.75), Inches(2.3), Inches(11.83), Inches(1.5))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = slide_data["title"]
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = RGBColor.from_string("FFFFFF")

    subtitle = slide_data.get("subtitle") or f"{client} — {date}"
    sub_box = slide.shapes.add_textbox(Inches(0.75), Inches(3.7), Inches(11.83), Inches(1))
    stf = sub_box.text_frame
    stf.word_wrap = True
    sp = stf.paragraphs[0]
    sp.text = subtitle
    sp.font.size = Pt(20)
    sp.font.color.rgb = rgb(PALETTE["accent_primary"])

    # Decorative multi-color stripe at the bottom, echoing the deck's palette.
    stripe_y = Inches(6.9)
    stripe_h = Inches(0.12)
    seg_w = Emu(int(SLIDE_W / len(CHART_COLOR_CYCLE)))
    for i, color_key in enumerate(CHART_COLOR_CYCLE):
        seg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, i * seg_w, stripe_y, seg_w, stripe_h)
        seg.fill.solid()
        seg.fill.fore_color.rgb = rgb(PALETTE[color_key])
        seg.line.fill.background()
        seg.shadow.inherit = False


def add_content_slide(prs: Presentation, slide_data: dict, footer_text: str, page_num: int) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_chrome(slide, slide_data["title"], footer_text, page_num)

    body = slide.shapes.add_textbox(MARGIN, Inches(1.35), CONTENT_W, Inches(5.5))
    tf = body.text_frame
    tf.word_wrap = True
    for i, bullet in enumerate(slide_data["bullets"]):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(16)
        marker = p.add_run()
        marker.text = "▸  "
        marker.font.size = Pt(16)
        marker.font.bold = True
        marker.font.color.rgb = rgb(PALETTE["accent_tertiary"])
        add_bold_runs(p, bullet, Pt(16), rgb(PALETTE["body_text"]))


def add_chart_slide(prs: Presentation, slide_data: dict, footer_text: str, page_num: int) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_chrome(slide, slide_data["title"], footer_text, page_num)

    chart_spec = slide_data["chart"]
    chart_data = CategoryChartData()
    chart_data.categories = chart_spec["categories"]
    chart_data.add_series(chart_spec["series_name"], chart_spec["values"])

    x, y, cx, cy = Inches(1.2), Inches(1.5), Inches(10.9), Inches(5.1)
    graphic_frame = slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data
    )
    chart = graphic_frame.chart
    chart.has_legend = False

    plot = chart.plots[0]
    plot.has_data_labels = True
    plot.gap_width = 60
    data_labels = plot.data_labels
    data_labels.font.size = Pt(14)
    data_labels.font.bold = True
    data_labels.font.color.rgb = rgb(PALETTE["body_text"])
    data_labels.position = XL_LABEL_POSITION.OUTSIDE_END

    chart.category_axis.tick_labels.font.size = Pt(13)
    chart.category_axis.format.line.color.rgb = rgb(PALETTE["muted_text"])
    chart.value_axis.visible = False
    chart.value_axis.has_major_gridlines = False

    series = plot.series[0]
    n_points = len(chart_spec["values"])
    for i in range(n_points):
        point = series.points[i]
        point.format.fill.solid()
        color_key = CHART_COLOR_CYCLE[i % len(CHART_COLOR_CYCLE)]
        point.format.fill.fore_color.rgb = rgb(PALETTE[color_key])


def add_icon_badge(slide, center_x, center_y, diameter, icon_name: str, color_key: str) -> None:
    """A solid accent-colored circle with a centered white icon glyph, per
    design/system.md's icon-badge spec."""
    left, top = center_x - diameter / 2, center_y - diameter / 2
    circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, diameter, diameter)
    circle.fill.solid()
    circle.fill.fore_color.rgb = rgb(PALETTE[color_key])
    circle.line.fill.background()
    circle.shadow.inherit = False

    icon_path = ICONS_DIR / f"{icon_name}.png"
    icon_size = Emu(int(diameter * 0.55))
    slide.shapes.add_picture(
        str(icon_path), center_x - icon_size / 2, center_y - icon_size / 2, icon_size, icon_size
    )


def add_diagram_slide(prs: Presentation, slide_data: dict, footer_text: str, page_num: int) -> None:
    """Place a pre-rendered excalidraw-visuals PNG, scaled to fit the slide's
    content area without distorting its aspect ratio, and centered. Diagram
    mechanics are never drawn by this script — see workflows/weekly_deep_dive.md."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_chrome(slide, slide_data["title"], footer_text, page_num)

    image_path = slide_data["image"]
    box_left, box_top = MARGIN, Inches(1.35)
    box_w, box_h = CONTENT_W, Inches(5.55)

    with PILImage.open(image_path) as img:
        img_w, img_h = img.size
    img_ratio = img_w / img_h
    box_ratio = box_w / box_h

    if img_ratio > box_ratio:
        draw_w, draw_h = box_w, Emu(int(box_w / img_ratio))
    else:
        draw_h, draw_w = box_h, Emu(int(box_h * img_ratio))

    left = box_left + (box_w - draw_w) / 2
    top = box_top + (box_h - draw_h) / 2
    slide.shapes.add_picture(image_path, left, top, draw_w, draw_h)


def add_profile_slide(prs: Presentation, slide_data: dict, footer_text: str, page_num: int) -> None:
    """Platform deep-dive: a card with a colored header band and a stack of
    labeled fields (Built on / Framework / Integrates with / Named adopters)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    header = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, Inches(1.5))
    header.fill.solid()
    header.fill.fore_color.rgb = rgb(PALETTE["masthead"])
    header.line.fill.background()
    header.shadow.inherit = False

    title_box = slide.shapes.add_textbox(MARGIN, Inches(0.32), CONTENT_W, Inches(0.65))
    tp = title_box.text_frame.paragraphs[0]
    tp.text = slide_data["title"]
    tp.font.size = Pt(30)
    tp.font.bold = True
    tp.font.color.rgb = RGBColor.from_string("FFFFFF")

    subtitle = slide_data.get("subtitle")
    if subtitle:
        sub_box = slide.shapes.add_textbox(MARGIN, Inches(0.98), CONTENT_W, Inches(0.45))
        sp = sub_box.text_frame.paragraphs[0]
        sp.text = subtitle
        sp.font.size = Pt(14)
        sp.font.color.rgb = rgb(PALETTE["accent_tertiary"])

    fields = slide_data["fields"]
    row_top = Inches(1.85)
    row_h = Inches(1.1)
    label_w = Inches(2.6)
    value_w = CONTENT_W - label_w - Inches(0.3)

    for i, field in enumerate(fields):
        y = row_top + i * row_h
        chip = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, MARGIN, y, label_w, Inches(0.5))
        chip.fill.solid()
        color_key = CHART_COLOR_CYCLE[i % len(CHART_COLOR_CYCLE)]
        chip.fill.fore_color.rgb = rgb(PALETTE[color_key])
        chip.line.fill.background()
        chip.shadow.inherit = False
        ctf = chip.text_frame
        ctf.word_wrap = True
        cp = ctf.paragraphs[0]
        cp.text = field["label"]
        cp.font.size = Pt(13)
        cp.font.bold = True
        cp.font.color.rgb = RGBColor.from_string("FFFFFF")
        cp.alignment = PP_ALIGN.CENTER

        value_box = slide.shapes.add_textbox(MARGIN + label_w + Inches(0.3), y - Inches(0.05), value_w, row_h)
        vtf = value_box.text_frame
        vtf.word_wrap = True
        vp = vtf.paragraphs[0]
        add_bold_runs(vp, field["value"], Pt(14), rgb(PALETTE["body_text"]))

    footer = slide.shapes.add_textbox(MARGIN, Inches(7.08), CONTENT_W, Inches(0.35))
    fp = footer.text_frame.paragraphs[0]
    fp.text = footer_text
    fp.font.size = Pt(10)
    fp.font.color.rgb = rgb(PALETTE["muted_text"])

    page_box = slide.shapes.add_textbox(SLIDE_W - Inches(1.1), Inches(7.08), Inches(0.7), Inches(0.35))
    pp = page_box.text_frame.paragraphs[0]
    pp.text = str(page_num)
    pp.font.size = Pt(10)
    pp.font.color.rgb = rgb(PALETTE["muted_text"])
    pp.alignment = PP_ALIGN.RIGHT


def add_snapshot_slide(prs: Presentation, slide_data: dict, footer_text: str, page_num: int) -> None:
    """Compressed client/problem snapshot: 3 stat tiles + one line per
    sub-topic. Deliberately lightweight — the deck's remaining slides carry
    the case analysis; this is just enough context to ground it, not a
    newsletter recap."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_chrome(slide, slide_data["title"], footer_text, page_num)

    stats = slide_data["stats"]
    tile_top = Inches(1.35)
    tile_h = Inches(1.3)
    gap = Inches(0.3)
    tile_w = Emu(int((CONTENT_W - gap * 2) / 3))
    badge_d = Inches(0.7)
    badge_pad = Inches(0.18)

    for i, stat in enumerate(stats):
        left = MARGIN + i * (tile_w + gap)
        tile = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, tile_top, tile_w, tile_h)
        tile.fill.solid()
        tile.fill.fore_color.rgb = rgb(PALETTE["light_bg"])
        tile.line.fill.background()
        tile.shadow.inherit = False

        icon_name = stat.get("icon", "chart")
        color_key = CHART_COLOR_CYCLE[i % len(CHART_COLOR_CYCLE)]
        badge_center_x = left + badge_pad + badge_d / 2
        badge_center_y = tile_top + tile_h / 2
        add_icon_badge(slide, badge_center_x, badge_center_y, badge_d, icon_name, color_key)

        text_left = left + badge_pad + badge_d + badge_pad
        text_width = tile_w - (text_left - left) - badge_pad
        text_box = slide.shapes.add_textbox(text_left, tile_top + Inches(0.2), text_width, tile_h - Inches(0.3))
        tf = text_box.text_frame
        tf.word_wrap = True
        vp = tf.paragraphs[0]
        vp.text = stat["value"]
        vp.font.size = Pt(22)
        vp.font.bold = True
        vp.font.color.rgb = rgb(PALETTE["masthead"])
        lp = tf.add_paragraph()
        lp.text = stat["label"]
        lp.font.size = Pt(10)
        lp.font.color.rgb = rgb(PALETTE["muted_text"])

    sub_top = tile_top + tile_h + Inches(0.4)
    subsectors = slide_data["subsectors"]
    body = slide.shapes.add_textbox(MARGIN, sub_top, CONTENT_W, Inches(3.3))
    tf = body.text_frame
    tf.word_wrap = True
    for i, sub in enumerate(subsectors):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(12)
        name_run = p.add_run()
        name_run.text = f"{sub['name']}  —  "
        name_run.font.size = Pt(15)
        name_run.font.bold = True
        name_run.font.color.rgb = rgb(PALETTE["accent_primary"])
        note_run = p.add_run()
        note_run.text = sub["note"]
        note_run.font.size = Pt(15)
        note_run.font.color.rgb = rgb(PALETTE["body_text"])


def add_table_slide(prs: Presentation, slide_data: dict, footer_text: str, page_num: int) -> None:
    """Evidence ledger: claim / evidence label / caveat, one row per material
    claim. The evidence column is colored per EVIDENCE_COLOR so the reader can
    scan a slide's overall evidence quality at a glance without rereading
    every label."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_chrome(slide, slide_data["title"], footer_text, page_num)

    rows_data = slide_data["rows"]
    col_headers = ["Claim", "Evidence", "Caveat"]
    n_rows = len(rows_data) + 1
    n_cols = 3

    table_left, table_top = MARGIN, Inches(1.35)
    table_w, table_h = CONTENT_W, Inches(5.55)

    graphic_frame = slide.shapes.add_table(n_rows, n_cols, table_left, table_top, table_w, table_h)
    table = graphic_frame.table
    table.columns[0].width = Emu(int(table_w * 0.42))
    table.columns[1].width = Emu(int(table_w * 0.26))
    table.columns[2].width = Emu(int(table_w * 0.32))

    for c, header in enumerate(col_headers):
        cell = table.cell(0, c)
        cell.fill.solid()
        cell.fill.fore_color.rgb = rgb(PALETTE["masthead"])
        cell.margin_top = cell.margin_bottom = Pt(6)
        p = cell.text_frame.paragraphs[0]
        p.text = header
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = RGBColor.from_string("FFFFFF")

    for r, row in enumerate(rows_data, start=1):
        claim_cell = table.cell(r, 0)
        claim_cell.fill.solid()
        claim_cell.fill.fore_color.rgb = rgb(PALETTE["background"] if r % 2 else PALETTE["light_bg"])
        cp = claim_cell.text_frame.paragraphs[0]
        cp.text = row["claim"]
        cp.font.size = Pt(13)
        cp.font.color.rgb = rgb(PALETTE["body_text"])
        claim_cell.text_frame.word_wrap = True

        evidence_cell = table.cell(r, 1)
        evidence_cell.fill.solid()
        evidence_cell.fill.fore_color.rgb = rgb(PALETTE["background"] if r % 2 else PALETTE["light_bg"])
        ep = evidence_cell.text_frame.paragraphs[0]
        ep.text = row["evidence"]
        ep.font.size = Pt(12)
        ep.font.bold = True
        ep.font.color.rgb = rgb(PALETTE[EVIDENCE_COLOR[row["evidence"]]])
        evidence_cell.text_frame.word_wrap = True

        caveat_cell = table.cell(r, 2)
        caveat_cell.fill.solid()
        caveat_cell.fill.fore_color.rgb = rgb(PALETTE["background"] if r % 2 else PALETTE["light_bg"])
        vp = caveat_cell.text_frame.paragraphs[0]
        vp.text = row["caveat"]
        vp.font.size = Pt(12)
        vp.font.color.rgb = rgb(PALETTE["muted_text"])
        caveat_cell.text_frame.word_wrap = True


def add_comparison_slide(prs: Presentation, slide_data: dict, footer_text: str, page_num: int) -> None:
    """Arbitrary-column comparison table for candidates/options (model
    selection, causal-method comparison, etc.) — distinct from add_table_slide's
    fixed claim/evidence/caveat evidence ledger. Columns and cell values are
    whatever the lens content calls for; no evidence-color mapping applies
    here since the columns aren't fixed."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_chrome(slide, slide_data["title"], footer_text, page_num)

    columns = slide_data["columns"]
    rows_data = slide_data["rows"]
    n_rows = len(rows_data) + 1
    n_cols = len(columns)

    table_left, table_top = MARGIN, Inches(1.35)
    table_w, table_h = CONTENT_W, Inches(5.55)

    graphic_frame = slide.shapes.add_table(n_rows, n_cols, table_left, table_top, table_w, table_h)
    table = graphic_frame.table
    first_col_w = Emu(int(table_w * 0.28))
    other_col_w = Emu(int((table_w - first_col_w) / (n_cols - 1))) if n_cols > 1 else Emu(0)
    table.columns[0].width = first_col_w
    for c in range(1, n_cols):
        table.columns[c].width = other_col_w

    for c, header in enumerate(columns):
        cell = table.cell(0, c)
        cell.fill.solid()
        cell.fill.fore_color.rgb = rgb(PALETTE["masthead"])
        cell.margin_top = cell.margin_bottom = Pt(6)
        p = cell.text_frame.paragraphs[0]
        p.text = header
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = RGBColor.from_string("FFFFFF")

    for r, row in enumerate(rows_data, start=1):
        for c, cell_value in enumerate(row):
            cell = table.cell(r, c)
            cell.fill.solid()
            cell.fill.fore_color.rgb = rgb(PALETTE["background"] if r % 2 else PALETTE["light_bg"])
            p = cell.text_frame.paragraphs[0]
            p.text = cell_value
            p.font.size = Pt(12)
            p.font.bold = (c == 0)
            p.font.color.rgb = rgb(PALETTE["body_text"])
            cell.text_frame.word_wrap = True


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug


def compute_output_path(data: dict, output_dir: Path) -> Path:
    filename = f"{data['date']}_{slugify(data['case'])}_{slugify(data['client'])}.pptx"
    return output_dir / filename


def build_deck(data: dict, output_path: Path) -> None:
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    client = data["client"]
    date = data["date"]
    footer_text = f"AI Consulting Weekly — {client}"

    page_num = 1
    for slide_data in data["slides"]:
        slide_type = slide_data["type"]
        if slide_type == "title":
            add_title_slide(prs, slide_data, client, date)
        elif slide_type == "content":
            add_content_slide(prs, slide_data, footer_text, page_num)
        elif slide_type == "chart":
            add_chart_slide(prs, slide_data, footer_text, page_num)
        elif slide_type == "diagram":
            add_diagram_slide(prs, slide_data, footer_text, page_num)
        elif slide_type == "profile":
            add_profile_slide(prs, slide_data, footer_text, page_num)
        elif slide_type == "snapshot":
            add_snapshot_slide(prs, slide_data, footer_text, page_num)
        elif slide_type == "table":
            add_table_slide(prs, slide_data, footer_text, page_num)
        elif slide_type == "comparison":
            add_comparison_slide(prs, slide_data, footer_text, page_num)
        page_num += 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(output_path))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input_json", type=Path, help="Path to the slide-content JSON file.")
    parser.add_argument("output_dir", type=Path, help="Directory to write the rendered .pptx file into.")
    args = parser.parse_args()

    if not args.input_json.exists():
        print(f"Error: input file not found: {args.input_json}", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(args.input_json.read_text())
    except json.JSONDecodeError as e:
        print(f"Error: {args.input_json} is not valid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        validate(data)
    except DeckContentError as e:
        print(f"Error: malformed deck content — {e}", file=sys.stderr)
        sys.exit(1)

    output_path = compute_output_path(data, args.output_dir)

    try:
        build_deck(data, output_path)
    except Exception:
        print("Error: failed to render deck.", file=sys.stderr)
        raise

    print(f"Wrote {len(data['slides'])} slides to {output_path}")


if __name__ == "__main__":
    main()
