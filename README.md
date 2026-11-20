# The World Today — Friday 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/longtime04/makefun-news-1120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/longtime04/makefun-news-1120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A one-page world news broadsheet for Friday 20 November 2026, drawn from
scratch with Pillow and the system DejaVu fonts. No network access, no
photos, no fetched images — every pixel is generated locally.

## What's on the page

- **Masthead** — "THE WORLD TODAY" with the date, Friday 20 November 2026.
- **Top stories** — three headline cards: Cyclone Akvan's landfall near
  Gopalpur, Odisha; ballistic missile strikes on Kyiv's bridges; and the
  COP31 deadlock in Antalya on the summit's final day.
- **World map** — a schematic map with twelve numbered pins marking the
  day's key locations, from Cincinnati to New Caledonia.
- **In brief** — twenty-eight one-line briefs covering the rest of the day's
  verified news, from the GTA VI launch week to the 5.6-magnitude quake
  near New Caledonia.
- **Footer** — a date check line confirming every story was first reported
  on Friday 20 November 2026.

## How to build it

```sh
python3 draw.py
```

This writes `entry.png` (1024×1024, under 1 MiB) next to `draw.py`. Run it
twice and the file is byte-identical — the drawing is fully deterministic.

## How to submit it

`main.py` copies `entry.png` into `$MAKEFUN_OUTPUT_DIR` (default: the
current directory) using only the Python standard library:

```sh
MAKEFUN_OUTPUT_DIR=/path/to/output python3 main.py
```

## Links

- Competition: https://make.fun/bounty/news-image-20261120
- Repository: https://github.com/longtime04/makefun-news-1120
