#!/usr/bin/env python3
"""Draw entry.png: a one-page newspaper front page summing up
Friday 20 November 2026 in a single image.

PIL only, system DejaVu fonts, deterministic output: the same
bytes on every run (no timestamps, no randomness).
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
BODY = (40, 40, 40)
NAVY = (11, 31, 58)
GOLD = (212, 175, 55)
RED = (176, 42, 48)
WHITE = (255, 255, 255)
MAP_BG = (18, 50, 79)
LAND = (61, 106, 148)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def serif_b(s):
    return font("DejaVuSerif-Bold.ttf", s)


def sans_b(s):
    return font("DejaVuSans-Bold.ttf", s)


def sans(s):
    return font("DejaVuSans.ttf", s)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def center(d, cx, y, text, fnt, fill):
    d.text((cx - d.textlength(text, font=fnt) / 2, y),
           text, font=fnt, fill=fill)


def draw_masthead(d):
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 118, W, 122], fill=GOLD)
    center(d, W // 2, 12, "THE WORLD TODAY", serif_b(60), WHITE)
    center(d, W // 2, 82, "Friday 20 November 2026",
           sans_b(28), GOLD)


def icon_cyclone(d, cx, top):
    """Spiral for the cyclone: concentric arcs in storm blue."""
    for i, r in enumerate([52, 40, 28, 16]):
        col = (30, 90, 160) if i % 2 == 0 else (120, 170, 220)
        d.ellipse([cx - r, top + 52 - r, cx + r, top + 52 + r],
                  outline=col, width=5)
    d.ellipse([cx - 7, top + 45, cx + 7, top + 59],
              fill=RED, outline=WHITE, width=2)


def icon_kyiv(d, cx, top):
    """A bridge under attack: deck, two towers, burst above."""
    d.rectangle([cx - 62, top + 40, cx + 62, top + 50], fill=NAVY)
    d.rectangle([cx - 48, top + 8, cx - 40, top + 44], fill=NAVY)
    d.rectangle([cx + 40, top + 8, cx + 48, top + 44], fill=NAVY)
    d.line([cx - 44, top + 10, cx, top + 40], fill=NAVY, width=2)
    d.line([cx + 44, top + 10, cx, top + 40], fill=NAVY, width=2)
    # Burst: red star above the deck.
    bx, by = cx, top + 2
    for ang in range(0, 360, 45):
        import math
        x2 = bx + 16 * math.cos(math.radians(ang))
        y2 = by + 16 * math.sin(math.radians(ang))
        d.line([bx, by, x2, y2], fill=RED, width=4)
    d.ellipse([bx - 5, by - 5, bx + 5, by + 5], fill=RED)


def icon_cop(d, cx, top):
    """A globe with a leaf: climate talks."""
    d.ellipse([cx - 30, top, cx + 30, top + 60], fill=(14, 122, 77),
              outline=WHITE, width=3)
    d.ellipse([cx - 30, top, cx + 30, top + 60], outline=(14, 122, 77))
    d.arc([cx - 30, top, cx + 30, top + 60], 200, 340, fill=WHITE, width=2)
    d.arc([cx - 30, top, cx + 30, top + 60], 20, 160, fill=WHITE, width=2)
    d.line([cx, top, cx, top + 60], fill=WHITE, width=2)
    # Gold leaf at the lower right of the globe.
    d.pieslice([cx + 8, top + 30, cx + 40, top + 58], 270, 90,
               fill=GOLD)
    d.pieslice([cx + 8, top + 30, cx + 40, top + 58], 90, 270,
               fill=(184, 148, 40))


def draw_hero(d, x, y, w, h, accent, headline, summary, icon):
    d.rectangle([x, y, x + w, y + h], fill=WHITE,
                outline=NAVY, width=2)
    d.rectangle([x, y, x + w, y + 8], fill=accent)
    icon(d, x + w // 2, y + 20)
    center(d, x + w // 2, y + 92, headline, sans_b(24), INK)
    lines = wrap(d, summary, sans(15), w - 28)
    ly = y + 128
    for ln in lines[:3]:
        center(d, x + w // 2, ly, ln, sans(15), BODY)
        ly += 20


def draw_map(d):
    x0, y0, x1, y1 = 16, 348, 1008, 462
    d.rectangle([x0, y0, x1, y1], fill=MAP_BG, outline=NAVY, width=2)
    d.text((x0 + 12, y0 + 6), "WORLD MAP  —  PINS 1-12 MARK THE LEAD STORIES",
           font=sans_b(14), fill=GOLD)
    # Schematic continents: simple light blobs on the dark sea.
    d.ellipse([60, 392, 250, 438], fill=LAND)    # N. America
    d.ellipse([225, 428, 315, 458], fill=LAND)   # S. America
    d.ellipse([472, 384, 568, 416], fill=LAND)   # Europe
    d.ellipse([496, 414, 606, 458], fill=LAND)   # Africa
    d.ellipse([612, 384, 908, 434], fill=LAND)   # Asia
    d.ellipse([828, 434, 912, 456], fill=LAND)   # Australia
    # 1 Washington DC, 2 London, 3 Paris, 4 Genoa, 5 Kyiv, 6 Antalya,
    # 7 Gaza, 8 Tbilisi, 9 Somalia, 10 Gopalpur, 11 Tokyo, 12 New Caledonia.
    # Pins are spread out so no two numbers overlap.
    pins = [
        (150, 408), (488, 390), (508, 406), (530, 396),
        (556, 386), (580, 402), (596, 416), (608, 392),
        (600, 442), (745, 418), (875, 402), (895, 440),
    ]
    f = sans_b(11)
    for i, (px, py) in enumerate(pins, start=1):
        d.ellipse([px - 10, py - 10, px + 10, py + 10],
                  fill=RED, outline=WHITE, width=2)
        label = str(i)
        d.text((px - d.textlength(label, font=f) / 2, py - 8),
               label, font=f, fill=WHITE)


BRIEFS = [
    ("GAMES", "GTA VI launch week sets records."),
    ("UKRAINE", "UK pledges 1,000+ drones and £260m military aid."),
    ("US", "Trump posthumously pardons baseball legend Pete Rose."),
    ("US", "US sanctions Comancheros and 'Ndrangheta crime groups."),
    ("TECH", "Meta rethinks its 2030 net-zero goal."),
    ("US", "US auctions its first deep-sea mining leases."),
    ("AFRICA", "Somalia expels the UAE ambassador."),
    ("GAZA", "Residents return as Israeli ground operation ends."),
    ("UK-EU", "UK and EU agree a youth mobility scheme."),
    ("EUROPE", "Youth protest cost of living and militarisation."),
    ("TECH", "California probes Nvidia over AI chips for China."),
    ("US", "Hippo Fiona dies at Cincinnati Zoo after eating a hat."),
    ("ASIA", "APEC ministers issue a joint statement."),
    ("MARKETS", "JPMorgan, Visa, Mastercard flag supplier network incident."),
    ("US", "Senators propose AUDIT AI Act on AI investment disclosure."),
    ("PACIFIC", "Magnitude 5.6 quake strikes near New Caledonia."),
    ("YEMEN", "Houthis claim four Saudi targets; two drones shot down."),
    ("LEBANON", "Israel strikes Hezbollah missile sites in the east."),
    ("JAPAN", "Tens of thousands protest Takaichi policies in Tokyo."),
    ("ITALY", "Genoa airport shut after unknown drone sighting."),
    ("GEORGIA", "Gas blast in Ponichala kills six."),
    ("FRANCE", "Fire in 18-storey block kills one, injures 15."),
    ("US", "Pentagon: Iran war has cost US over $48bn."),
    ("GAZA", "Nearly 65,000 approved tents wait to enter Gaza."),
    ("INDIA", "About 300,000 evacuated in Odisha as cyclone nears."),
    ("INDIA", "28+ trains cancelled ahead of Cyclone Akvan."),
    ("UKRAINE", "Several Kyiv bridges hit in missile attack."),
    ("CLIMATE", "COP31 draft drops fossil fuels amid deadlock."),
]


def draw_briefs(d):
    d.text((16, 472), "THE DAY IN BRIEF  —  28 STORIES",
           font=sans_b(17), fill=NAVY)
    d.line([16, 496, 1008, 496], fill=NAVY, width=2)
    col_w = 484
    col_x = [16, 524]
    row_h = 35
    top = 504
    for idx, (tag, text) in enumerate(BRIEFS):
        col = idx // 14
        row = idx % 14
        y = top + row * row_h
        x = col_x[col]
        if row % 2 == 0:
            d.rectangle([x - 4, y - 3, x + col_w, y + row_h - 6],
                        fill=(238, 233, 220))
        num = str(idx + 1) + "."
        nf = sans_b(15)
        d.text((x, y), num, font=nf, fill=RED)
        nx = x + d.textlength(num, font=nf) + 6
        tf = sans_b(13)
        d.text((nx, y + 1), tag, font=tf, fill=NAVY)
        tx = nx + d.textlength(tag, font=tf) + 7
        # Shrink the story text until it fits the column on one line.
        size = 15
        while size > 12:
            f = sans(size)
            if tx + d.textlength(text, font=f) <= x + col_w:
                break
            size -= 1
        d.text((tx, y), text, font=sans(size), fill=INK)


def draw_footer(d):
    center(d, W // 2, 994,
           "All stories first reported Friday 20 November 2026",
           sans_b(15), NAVY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    hy, hh, hw = 132, 204, 322
    draw_hero(d, 16, hy, hw, hh, (30, 90, 160), "CYCLONE AKVAN",
              "Landfall near Gopalpur, Odisha, early today. "
              "Winds 70-80 km/h, gusts 90; about 300,000 "
              "evacuated.", icon_cyclone)
    draw_hero(d, 351, hy, hw, hh, RED, "KYIV UNDER FIRE",
              "Ballistic missiles strike Kyiv today; several "
              "bridges hit as air defences answer the morning "
              "attack.", icon_kyiv)
    draw_hero(d, 686, hy, hw, hh, (14, 122, 77), "COP31 DEADLOCK",
              "Final day in Antalya ends in deadlock; fossil "
              "fuels are deleted from the draft text.",
              icon_cop)
    draw_map(d)
    draw_briefs(d)
    draw_footer(d)
    img.save(OUT, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
