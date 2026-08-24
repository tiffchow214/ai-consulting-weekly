"""Generate the deck's icon set as flat, single-color PNGs.

Usage:
    python tools/generate_icons.py

Deterministically draws each icon with Pillow (no image-generation model, no
external icon library/font) and writes them to assets/icons/*.png: solid
white glyphs on a transparent background, sized to be centered inside an
accent-colored circle badge per design/system.md. Re-run any time to
regenerate all icons identically — nothing here is hand-tweaked pixel art.

Icons are built as an 'L' (grayscale) mask — 255 = opaque white glyph,
0 = transparent — so a shape can be cut out of an earlier one just by
drawing over it with fill=0 (e.g. the gear's inner hole, the exclamation
mark's gap in the warning triangle). The mask becomes the alpha channel of
a solid-white RGBA image.
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ICONS_DIR = PROJECT_ROOT / "assets" / "icons"
SIZE = 256


def new_mask() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    mask = Image.new("L", (SIZE, SIZE), 0)
    return mask, ImageDraw.Draw(mask)


def finalize(mask: Image.Image) -> Image.Image:
    icon = Image.new("RGBA", (SIZE, SIZE), (255, 255, 255, 0))
    white = Image.new("RGBA", (SIZE, SIZE), (255, 255, 255, 255))
    return Image.composite(white, icon, mask)


def rotated_rect(cx, cy, w, h, angle_deg):
    """Return the 4 corners of a w x h rectangle centered at (cx, cy), rotated."""
    angle = math.radians(angle_deg)
    hw, hh = w / 2, h / 2
    corners = [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]
    pts = []
    for x, y in corners:
        rx = x * math.cos(angle) - y * math.sin(angle)
        ry = x * math.sin(angle) + y * math.cos(angle)
        pts.append((cx + rx, cy + ry))
    return pts


def draw_gear(d: ImageDraw.ImageDraw) -> None:
    c = SIZE / 2
    r_outer, r_inner, r_hub = SIZE * 0.30, SIZE * 0.20, SIZE * 0.09
    d.ellipse([c - r_outer, c - r_outer, c + r_outer, c + r_outer], fill=255)
    d.ellipse([c - r_inner, c - r_inner, c + r_inner, c + r_inner], fill=0)
    d.ellipse([c - r_hub, c - r_hub, c + r_hub, c + r_hub], fill=255)

    n_teeth = 8
    tooth_w, tooth_h = SIZE * 0.10, SIZE * 0.10
    r_tooth = r_outer + tooth_h * 0.35
    for i in range(n_teeth):
        angle = 360 / n_teeth * i
        tx = c + r_tooth * math.cos(math.radians(angle))
        ty = c + r_tooth * math.sin(math.radians(angle))
        d.polygon(rotated_rect(tx, ty, tooth_w, tooth_h, angle), fill=255)


def draw_shield(d: ImageDraw.ImageDraw) -> None:
    w, h = SIZE * 0.62, SIZE * 0.74
    x0, y0 = (SIZE - w) / 2, SIZE * 0.10
    points = [
        (x0, y0), (x0 + w, y0),
        (x0 + w, y0 + h * 0.55),
        (x0 + w / 2, y0 + h),
        (x0, y0 + h * 0.55),
    ]
    d.polygon(points, fill=255)

    # checkmark cutout
    cx, cy = SIZE / 2, SIZE * 0.48
    d.line(
        [(cx - SIZE * 0.13, cy), (cx - SIZE * 0.03, cy + SIZE * 0.10), (cx + SIZE * 0.16, cy - SIZE * 0.13)],
        fill=0, width=int(SIZE * 0.07), joint="curve",
    )


def draw_network(d: ImageDraw.ImageDraw) -> None:
    c = SIZE / 2
    r_node, r_edge_node = SIZE * 0.09, SIZE * 0.065
    line_w = int(SIZE * 0.045)
    outer_r = SIZE * 0.30
    for i, angle in enumerate([90, 210, 330]):
        ox = c + outer_r * math.cos(math.radians(angle))
        oy = c + outer_r * math.sin(math.radians(angle))
        d.line([(c, c), (ox, oy)], fill=255, width=line_w)
        d.ellipse([ox - r_edge_node, oy - r_edge_node, ox + r_edge_node, oy + r_edge_node], fill=255)
    d.ellipse([c - r_node, c - r_node, c + r_node, c + r_node], fill=255)


def draw_chart(d: ImageDraw.ImageDraw) -> None:
    base_y = SIZE * 0.78
    bar_w, gap = SIZE * 0.13, SIZE * 0.07
    heights = [0.28, 0.48, 0.36, 0.60]
    n = len(heights)
    total_w = n * bar_w + (n - 1) * gap
    x = (SIZE - total_w) / 2
    for h_frac in heights:
        bar_h = SIZE * h_frac
        d.rectangle([x, base_y - bar_h, x + bar_w, base_y], fill=255)
        x += bar_w + gap


def draw_checkmark(d: ImageDraw.ImageDraw) -> None:
    c = SIZE / 2
    d.line(
        [(c - SIZE * 0.24, c + SIZE * 0.02), (c - SIZE * 0.06, c + SIZE * 0.20), (c + SIZE * 0.28, c - SIZE * 0.20)],
        fill=255, width=int(SIZE * 0.11), joint="curve",
    )


def draw_warning(d: ImageDraw.ImageDraw) -> None:
    w, h = SIZE * 0.72, SIZE * 0.62
    x0, y0 = (SIZE - w) / 2, SIZE * 0.16
    d.polygon([(SIZE / 2, y0), (x0 + w, y0 + h), (x0, y0 + h)], fill=255)

    bar_w, bar_h = SIZE * 0.055, SIZE * 0.22
    cx = SIZE / 2
    bar_top = y0 + h * 0.30
    d.rectangle([cx - bar_w / 2, bar_top, cx + bar_w / 2, bar_top + bar_h], fill=0)
    dot_r = SIZE * 0.03
    dot_cy = bar_top + bar_h + SIZE * 0.06
    d.ellipse([cx - dot_r, dot_cy - dot_r, cx + dot_r, dot_cy + dot_r], fill=0)


def draw_book(d: ImageDraw.ImageDraw) -> None:
    w, h = SIZE * 0.62, SIZE * 0.56
    x0, y0 = (SIZE - w) / 2, (SIZE - h) / 2
    radius = SIZE * 0.03
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=radius, fill=255)

    line_w = SIZE * 0.44
    line_h = SIZE * 0.035
    lx = x0 + (w - line_w) / 2
    for i, ly_frac in enumerate([0.28, 0.46, 0.64]):
        ly = y0 + h * ly_frac
        this_w = line_w if i < 2 else line_w * 0.6
        d.rectangle([lx, ly, lx + this_w, ly + line_h], fill=0)


def draw_search(d: ImageDraw.ImageDraw) -> None:
    c = SIZE * 0.42
    r_outer, r_inner = SIZE * 0.20, SIZE * 0.13
    d.ellipse([c - r_outer, c - r_outer, c + r_outer, c + r_outer], fill=255)
    d.ellipse([c - r_inner, c - r_inner, c + r_inner, c + r_inner], fill=0)

    handle_len = SIZE * 0.26
    angle = math.radians(45)
    hx0 = c + r_outer * math.cos(angle)
    hy0 = c + r_outer * math.sin(angle)
    hx1 = hx0 + handle_len * math.cos(angle)
    hy1 = hy0 + handle_len * math.sin(angle)
    d.line([(hx0, hy0), (hx1, hy1)], fill=255, width=int(SIZE * 0.09))


def draw_scale(d: ImageDraw.ImageDraw) -> None:
    cx = SIZE / 2
    post_w = SIZE * 0.05
    top_y, base_y = SIZE * 0.16, SIZE * 0.82
    d.rectangle([cx - post_w / 2, top_y, cx + post_w / 2, base_y], fill=255)

    beam_y = top_y
    beam_half = SIZE * 0.28
    d.line([(cx - beam_half, beam_y), (cx + beam_half, beam_y)], fill=255, width=int(SIZE * 0.045))

    base_w = SIZE * 0.36
    d.rectangle([cx - base_w / 2, base_y, cx + base_w / 2, base_y + SIZE * 0.05], fill=255)

    pan_r = SIZE * 0.12
    for side in (-1, 1):
        pan_cx = cx + side * beam_half
        pan_cy = beam_y + SIZE * 0.16
        d.arc(
            [pan_cx - pan_r, pan_cy - pan_r, pan_cx + pan_r, pan_cy + pan_r],
            start=20, end=160, fill=255, width=int(SIZE * 0.045),
        )
        d.line([(pan_cx - pan_r, pan_cy), (cx + side * beam_half, beam_y)], fill=255, width=int(SIZE * 0.03))
        d.line([(pan_cx + pan_r, pan_cy), (cx + side * beam_half, beam_y)], fill=255, width=int(SIZE * 0.03))


def draw_stop(d: ImageDraw.ImageDraw) -> None:
    c = SIZE / 2
    r_outer, r_inner = SIZE * 0.32, SIZE * 0.24
    n_sides = 8
    outer_pts = [
        (c + r_outer * math.cos(math.radians(45 * i - 22.5)), c + r_outer * math.sin(math.radians(45 * i - 22.5)))
        for i in range(n_sides)
    ]
    inner_pts = [
        (c + r_inner * math.cos(math.radians(45 * i - 22.5)), c + r_inner * math.sin(math.radians(45 * i - 22.5)))
        for i in range(n_sides)
    ]
    d.polygon(outer_pts, fill=255)
    d.polygon(inner_pts, fill=0)

    bar_w, bar_h = SIZE * 0.34, SIZE * 0.09
    d.rectangle([c - bar_w / 2, c - bar_h / 2, c + bar_w / 2, c + bar_h / 2], fill=255)


def draw_bulb(d: ImageDraw.ImageDraw) -> None:
    c = SIZE / 2
    bulb_cy = SIZE * 0.40
    r = SIZE * 0.24
    d.ellipse([c - r, bulb_cy - r, c + r, bulb_cy + r], fill=255)

    base_w, base_h = SIZE * 0.20, SIZE * 0.16
    base_top = bulb_cy + r * 0.55
    d.rectangle([c - base_w / 2, base_top, c + base_w / 2, base_top + base_h], fill=255)

    gap_h = SIZE * 0.025
    for i in range(2):
        gy = base_top + base_h * (0.3 + i * 0.35)
        d.rectangle([c - base_w / 2 - SIZE * 0.01, gy, c + base_w / 2 + SIZE * 0.01, gy + gap_h], fill=0)


ICONS = {
    "gear": draw_gear,
    "shield": draw_shield,
    "network": draw_network,
    "chart": draw_chart,
    "checkmark": draw_checkmark,
    "warning": draw_warning,
    "book": draw_book,
    "search": draw_search,
    "scale": draw_scale,
    "stop": draw_stop,
    "bulb": draw_bulb,
}


def main() -> None:
    ICONS_DIR.mkdir(parents=True, exist_ok=True)
    for name, draw_fn in ICONS.items():
        mask, d = new_mask()
        draw_fn(d)
        icon = finalize(mask)
        out_path = ICONS_DIR / f"{name}.png"
        icon.save(out_path)
        print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
