#!/usr/bin/env python3
"""Draw "The World Today" - a one-page world news broadsheet.

The page covers Friday 20 November 2026: a masthead, three headline cards,
a schematic world map with twelve numbered pins, twenty-eight one-line
briefs, and a footer date check. Everything is drawn with Pillow and the
system DejaVu fonts. No network, no photos, no fetched images.

Usage:
    python3 draw.py

Writes entry.png (1024x1024, under 1 MiB) next to this file. The drawing is
fully deterministic: running it twice produces byte-identical output.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "entry.png")

PAGE_W, PAGE_H = 1024, 1024
MARGIN = 30
CONTENT_W = PAGE_W - 2 * MARGIN

# --- palette ---------------------------------------------------------------
PAPER = (255, 255, 255)
INK = (22, 28, 36)
BODY = (48, 56, 66)
NAVY = (13, 43, 77)
CRIMSON = (176, 32, 32)
GOLD = (222, 178, 60)
TEAL = (14, 110, 120)
GREEN = (34, 112, 66)
MUTED = (96, 106, 118)
RULE = (205, 212, 220)
CARD_EDGE = (198, 206, 214)
SEA = (216, 233, 245)
LAND = (198, 216, 180)
LAND_EDGE = (150, 175, 135)
GRID = (190, 210, 225)
TAGLINE = (170, 190, 210)

DATE_LINE = "Friday 20 November 2026"
FOOTER_LINE = "All stories first reported Friday 20 November 2026"

# --- fonts -----------------------------------------------------------------
def load_font(bold, size):
    """Load a DejaVu font from the usual system paths, else PIL's default."""
    stem = "DejaVuSans-Bold" if bold else "DejaVuSans"
    for folder in ("/usr/share/fonts/truetype/dejavu", "/usr/share/fonts/dejavu"):
        path = os.path.join(folder, stem + ".ttf")
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def wrap_text(draw, text, font, max_width):
    """Greedy word wrap; returns the list of lines that fit max_width."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


# --- masthead --------------------------------------------------------------
def draw_masthead(draw):
    draw.rectangle([0, 0, PAGE_W, 110], fill=NAVY)
    draw.rectangle([0, 110, PAGE_W, 114], fill=CRIMSON)
    title_font = load_font(True, 56)
    date_font = load_font(True, 23)
    draw.text((MARGIN, 26), "THE WORLD TODAY", font=title_font, fill=PAPER)
    date_w = draw.textlength(DATE_LINE, font=date_font)
    draw.text((PAGE_W - MARGIN - date_w, 38), DATE_LINE, font=date_font, fill=GOLD)
    tag_font = load_font(False, 12)
    draw.text(
        (MARGIN, 88),
        "WORLD NEWS  -  ONE PAGE  -  EVERY STORY CHECKED",
        font=tag_font,
        fill=TAGLINE,
    )


def section_label(draw, y, text):
    """A small-caps style section heading with a rule underneath."""
    font = load_font(True, 14)
    draw.text((MARGIN, y), text, font=font, fill=NAVY)
    draw.line([MARGIN, y + 20, PAGE_W - MARGIN, y + 20], fill=RULE, width=1)


# --- headline cards --------------------------------------------------------
HEADLINES = [
    {
        "kicker": "CYCLONE AKVAN",
        "color": TEAL,
        "icon": "cyclone",
        "headline": "Cyclone Akvan slams into Odisha coast",
        "summary": (
            "Landfall near Gopalpur at dawn, winds 70-80 km/h, gusts to 90. "
            "About 300,000 evacuated; 28+ trains cancelled."
        ),
        "dateline": "GOPALPUR, ODISHA",
    },
    {
        "kicker": "KYIV UNDER ATTACK",
        "color": CRIMSON,
        "icon": "burst",
        "headline": "Ballistic missiles strike Kyiv bridges",
        "summary": (
            "Ballistic missiles struck Kyiv on Friday, and several bridges "
            "across the capital were hit in the attack."
        ),
        "dateline": "KYIV, UKRAINE",
    },
    {
        "kicker": "COP31  -  FINAL DAY",
        "color": GREEN,
        "icon": "globe",
        "headline": "COP31 deadlocked on final day",
        "summary": (
            "Climate talks in Antalya reached their final day still "
            "deadlocked, with fossil fuels dropped from the draft text."
        ),
        "dateline": "ANTALYA, TURKIYE",
    },
]


def draw_cyclone(draw, cx, cy, r, color):
    """A storm spiral built from three broken concentric arcs."""
    for i, rad in enumerate((r, int(r * 0.72), int(r * 0.45))):
        start = 20 + i * 140
        draw.arc(
            [cx - rad, cy - rad, cx + rad, cy + rad],
            start,
            start + 300,
            fill=color,
            width=4,
        )
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=color)


def draw_burst(draw, cx, cy, r, color):
    """A sixteen-point starburst for an explosion / impact story."""
    points = []
    for k in range(16):
        ang = math.pi * k / 8
        rad = r if k % 2 == 0 else r * 0.45
        points.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(points, fill=color)
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=PAPER)


def draw_globe(draw, cx, cy, r, color):
    """A wireframe globe for the climate summit story."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=4)
    draw.ellipse(
        [cx - int(r * 0.45), cy - r, cx + int(r * 0.45), cy + r],
        outline=color,
        width=2,
    )
    draw.line([cx - r, cy, cx + r, cy], fill=color, width=2)
    draw.arc(
        [cx - r, cy - int(r * 0.55), cx + r, cy + int(r * 0.55)],
        0,
        360,
        fill=color,
        width=2,
    )


ICONS = {"cyclone": draw_cyclone, "burst": draw_burst, "globe": draw_globe}


def draw_headline_card(draw, x, y, w, h, item):
    draw.rectangle([x, y, x + w, y + h], fill=PAPER, outline=CARD_EDGE, width=1)
    draw.rectangle([x, y, x + w, y + 30], fill=item["color"])
    kick_font = load_font(True, 13)
    draw.text((x + 14, y + 8), item["kicker"], font=kick_font, fill=PAPER)

    cx = x + w // 2
    ICONS[item["icon"]](draw, cx, y + 74, 36, item["color"])

    inner = w - 28
    hl_font = load_font(True, 19)
    hl_lines = wrap_text(draw, item["headline"], hl_font, inner)[:2]
    hy = y + 126
    for line in hl_lines:
        draw.text((x + 14, hy), line, font=hl_font, fill=INK)
        hy += 24

    draw.line([x + 14, hy + 6, x + w - 14, hy + 6], fill=RULE, width=1)

    sum_font = load_font(False, 12)
    sum_lines = wrap_text(draw, item["summary"], sum_font, inner)[:3]
    sy = hy + 16
    for line in sum_lines:
        draw.text((x + 14, sy), line, font=sum_font, fill=BODY)
        sy += 17

    date_font = load_font(True, 10)
    draw.text((x + 14, y + h - 24), item["dateline"], font=date_font, fill=MUTED)


# --- world map -------------------------------------------------------------
# (name, latitude, longitude); numbered west to east.
PLACES = [
    ("Cincinnati", 39.10, -84.51),
    ("Washington", 38.90, -77.04),
    ("London", 51.50, -0.13),
    ("Genoa", 44.41, 8.93),
    ("Kyiv", 50.45, 30.52),
    ("Gaza", 31.50, 34.47),
    ("Tbilisi", 41.72, 44.79),
    ("Riyadh", 24.71, 46.68),
    ("Mogadishu", 2.05, 45.32),
    ("Gopalpur", 19.26, 84.92),
    ("Tokyo", 35.68, 139.69),
    ("New Caledonia", -21.50, 165.50),
]

# Coarse continent outlines as (longitude, latitude) pairs - schematic only.
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-120, 71), (-100, 69), (-85, 68), (-75, 72),
     (-65, 60), (-55, 52), (-60, 46), (-70, 42), (-75, 36), (-80, 26),
     (-85, 30), (-90, 21), (-96, 16), (-92, 15), (-86, 12), (-80, 8),
     (-83, 15), (-90, 21), (-97, 26), (-105, 23), (-112, 29), (-120, 34),
     (-124, 42), (-125, 49), (-133, 55), (-145, 60), (-155, 58), (-165, 60)],
    # South America
    [(-80, 10), (-72, 12), (-62, 10), (-52, 5), (-50, 0), (-44, -3),
     (-35, -8), (-39, -15), (-41, -23), (-48, -28), (-55, -35), (-62, -41),
     (-66, -47), (-69, -52), (-72, -54), (-74, -48), (-73, -38), (-72, -28),
     (-78, -18), (-81, -8), (-80, 0), (-81, 6)],
    # Africa
    [(-6, 35), (-10, 31), (-15, 27), (-17, 21), (-17, 15), (-15, 11),
     (-8, 5), (-4, 5), (6, 4), (9, 4), (9, -1), (12, -6), (13, -12),
     (12, -17), (15, -22), (18, -29), (20, -35), (26, -34), (31, -29),
     (33, -25), (35, -18), (39, -13), (40, -8), (43, -2), (48, 0),
     (51, 11), (48, 12), (44, 13), (41, 15), (39, 20), (38, 24),
     (36, 28), (33, 31), (30, 32), (24, 33), (19, 33), (13, 34),
     (10, 37), (5, 37), (0, 36), (-6, 35)],
    # Eurasia
    [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 51), (4, 53), (8, 57),
     (12, 59), (18, 56), (21, 55), (25, 59), (28, 60), (30, 65), (28, 70),
     (35, 68), (40, 68), (45, 68), (50, 69), (55, 68), (60, 69), (66, 69),
     (70, 72), (75, 73), (80, 73), (90, 75), (100, 76), (110, 74),
     (120, 73), (130, 72), (140, 72), (150, 70), (160, 69), (170, 67),
     (178, 65), (178, 62), (170, 60), (162, 56), (158, 52), (150, 59),
     (142, 59), (140, 54), (135, 44), (130, 42), (127, 39), (122, 38),
     (120, 32), (121, 28), (118, 24), (110, 20), (108, 17), (105, 9),
     (103, 7), (100, 8), (98, 10), (95, 16), (92, 21), (89, 22),
     (86, 20), (80, 13), (77, 8), (74, 12), (72, 20), (68, 23),
     (66, 25), (61, 25), (57, 26), (54, 27), (51, 29), (49, 30),
     (47, 30), (44, 29), (41, 27), (39, 21), (37, 24), (35, 28),
     (34, 31), (36, 36), (33, 36), (30, 36), (27, 37), (23, 36),
     (22, 39), (19, 42), (15, 44), (12, 44), (8, 44), (3, 42),
     (0, 39), (-2, 37), (-6, 36)],
    # Australia
    [(113, -22), (114, -30), (115, -34), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (137, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -22), (146, -19), (142, -11), (141, -14),
     (137, -15), (135, -15), (132, -12), (130, -13), (126, -14), (122, -17),
     (118, -20)],
]


def project(lon, lat, box):
    """Equirectangular projection into the map box (x, y, w, h)."""
    x0, y0, w, h = box
    x = x0 + (lon + 180.0) / 360.0 * w
    y = y0 + (78.0 - lat) / 136.0 * h
    return (x, y)


def draw_map(draw, box):
    x0, y0, w, h = box
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=SEA, outline=CARD_EDGE, width=1)
    for lon in range(-150, 181, 30):
        gx, _ = project(lon, 0, box)
        draw.line([gx, y0, gx, y0 + h], fill=GRID, width=1)
    for lat in range(-60, 79, 30):
        _, gy = project(0, lat, box)
        draw.line([x0, gy, x0 + w, gy], fill=GRID, width=1)
    for poly in CONTINENTS:
        pts = [project(lon, lat, box) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_EDGE)
    # Small island marks for the UK and Japan.
    for lon, lat in ((-2.0, 54.0), (139.0, 38.0)):
        ix, iy = project(lon, lat, box)
        draw.ellipse([ix - 3, iy - 3, ix + 3, iy + 3], fill=LAND, outline=LAND_EDGE)

    pin_font = load_font(True, 10)
    for idx, (_name, lat, lon) in enumerate(PLACES, start=1):
        px, py = project(lon, lat, box)
        r = 8
        draw.ellipse(
            [px - r, py - r, px + r, py + r], fill=CRIMSON, outline=PAPER, width=2
        )
        label = str(idx)
        tw = draw.textlength(label, font=pin_font)
        draw.text((px - tw / 2, py - 5), label, font=pin_font, fill=PAPER)

    leg_font = load_font(False, 11)
    for col in range(4):
        for row in range(3):
            idx = col * 3 + row
            if idx >= len(PLACES):
                continue
            lx = MARGIN + col * 245
            ly = 620 + row * 16
            draw.text((lx, ly), f"{idx + 1}. {PLACES[idx][0]}", font=leg_font, fill=INK)


# --- briefs ----------------------------------------------------------------
BRIEFS = [
    "GTA VI launch week sets records.",
    "UK pledges 1,000+ drones and 260m pounds of aid to Ukraine.",
    "Trump posthumously pardons baseball legend Pete Rose.",
    "US sanctions Comancheros and 'Ndrangheta crime groups.",
    "Meta rethinks its 2030 net-zero target.",
    "US auctions first deep-sea mining leases.",
    "Somalia expels the UAE ambassador.",
    "Gaza residents return as rare Israeli ground operation ends.",
    "UK and EU agree a youth mobility scheme.",
    "Young Europeans protest living costs and militarisation.",
    "California probes Nvidia's AI chips for China.",
    "Cincinnati Zoo hippo Fiona dies after swallowing a cap.",
    "APEC ministers issue a joint statement.",
    "JPMorgan, Visa and Mastercard disclose a vendor network incident.",
    "US senators unveil the AUDIT AI bill on AI investment disclosure.",
    "Magnitude 5.6 quake strikes near New Caledonia.",
    "Houthis claim strikes on four Saudi targets.",
    "Saudi air defences down two Houthi drones.",
    "Israel hits Hezbollah missile sites in eastern Lebanon.",
    "10,000+ march in Tokyo against Takaichi's policies.",
    "Genoa airport halts flights over mystery drones.",
    "Gas blast in Georgia's Ponichala kills six.",
    "Fire in an 18-storey French block kills one, injures 15.",
    "Pentagon: Iran war has cost the US over $48bn.",
    "Nearly 65,000 approved tents wait to enter Gaza.",
    "Cyclone Akvan: 300,000 evacuated in Odisha.",
    "Cyclone Akvan: 28+ trains cancelled.",
    "COP31 draft drops fossil fuels.",
]


def draw_briefs(draw, y_top, y_bottom):
    """Two columns of one-line briefs; shrink the font until they fit."""
    col_w = (CONTENT_W - 24) // 2
    half = (len(BRIEFS) + 1) // 2
    for size in (12, 11, 10):
        font = load_font(False, size)
        line_h = size + 4
        columns = []
        fits = True
        for col in range(2):
            items = BRIEFS[col * half:(col + 1) * half]
            laid = []
            total = 0
            for text in items:
                lines = wrap_text(draw, text, font, col_w - 14)[:2]
                laid.append(lines)
                total += len(lines) * line_h + 4
            if total > y_bottom - y_top:
                fits = False
            columns.append(laid)
        if fits:
            break
    for col in range(2):
        x = MARGIN + col * (col_w + 24)
        y = y_top
        for lines in columns[col]:
            draw.rectangle([x, y + 4, x + 5, y + 9], fill=CRIMSON)
            ty = y
            for line in lines:
                draw.text((x + 12, ty), line, font=font, fill=INK)
                ty += line_h
            y = ty + 4


# --- footer ----------------------------------------------------------------
def draw_footer(draw):
    draw.rectangle([0, 984, PAGE_W, PAGE_H], fill=NAVY)
    font = load_font(True, 14)
    tw = draw.textlength(FOOTER_LINE, font=font)
    draw.text(((PAGE_W - tw) / 2, 998), FOOTER_LINE, font=font, fill=PAPER)


# --- page ------------------------------------------------------------------
def build():
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    section_label(draw, 124, "TOP STORIES")
    card_w = 310
    for i, item in enumerate(HEADLINES):
        x = MARGIN + i * (card_w + 17)
        draw_headline_card(draw, x, 150, card_w, 286, item)
    section_label(draw, 448, "THE WORLD IN BRIEF - 12 PLACES TO WATCH")
    draw_map(draw, (MARGIN, 474, CONTENT_W, 140))
    section_label(draw, 668, "IN BRIEF")
    draw_briefs(draw, 694, 972)
    draw_footer(draw)
    return img


def main():
    img = build()
    img.save(OUT_PATH, format="PNG")
    size = os.path.getsize(OUT_PATH)
    print(f"wrote {OUT_PATH} ({img.size[0]}x{img.size[1]}, {size} bytes)")


if __name__ == "__main__":
    main()
