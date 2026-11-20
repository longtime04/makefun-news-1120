[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/longtime04/makefun-news-1120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/longtime04/makefun-news-1120/reward.svg)](https://make.fun/bounty/news-image-20261120)

# The World Today — 20 November 2026

A one-page newspaper front page that sums up Friday 20 November 2026
in a single image: Cyclone Akvan making landfall in Odisha, ballistic
missiles striking Kyiv, and COP31 ending in deadlock in Antalya lead
the page, followed by a world map with numbered pins and 28 one-line
briefs covering the day's world news.

## What the image shows

- **Masthead** — "THE WORLD TODAY" with the date, Friday 20 November 2026.
- **Three hero stories** — Cyclone Akvan (landfall near Gopalpur, Odisha;
  winds 70–80 km/h, gusts to 90; about 300,000 evacuated; 28+ trains
  cancelled), Kyiv Under Fire (ballistic missiles strike the capital;
  several bridges hit), and COP31 Deadlock (final day in Antalya ends
  in deadlock; fossil fuels deleted from the draft text).
- **World map strip** — a schematic map with numbered pins 1–12 marking
  the lead stories, from Washington DC to New Caledonia.
- **28 numbered briefs** — one line each, from the GTA VI launch week
  to the nearly 65,000 approved tents waiting to enter Gaza.
- **Footer** — every story was first reported on Friday 20 November 2026.

## How it works

`draw.py` draws the whole page with Python PIL only, using system DejaVu
fonts — no photos, no AI imagery, no network access. The output is
deterministic: running it twice produces byte-identical PNGs.

`main.py` (standard library only) copies the pre-drawn `entry.png` into
`$MAKEFUN_OUTPUT_DIR` (default: the current directory).

## How to run it

```bash
python3 draw.py            # regenerates entry.png (1024x1024)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # copies entry.png into out/
```

## License

MIT — see [LICENSE](LICENSE).
