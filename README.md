# 19 November 2026 — the day in one image

A front-page infographic summing up Thursday 19 November 2026 in six
panels, plus an "Also today" ticker. Entry for the make.fun competition
`news-image-20261119`.

## What the image shows

1. **Shenzhen — trilateral, planned.** First-ever Xi-Trump-Putin talks
   planned for 19 Nov on the APEC sidelines; nuclear arms on the agenda.
   (Reuters / CNA / Chinese Foreign Ministry)
2. **Wall Street — Anthropic IPO.** Priced $83 on 18 Nov, 980m shares,
   ~$81.3bn — the largest IPO ever; trading starts 19 Nov on Nasdaq as
   ANT. (Reuters / BusinessWorld)
3. **Crimea — bridge hit again.** Third attack this week, overnight into
   19 Nov; traffic suspended, damage assessed. (Reuters / BBC)
4. **Gaza + Israel.** First Israeli ground op in central Gaza across the
   Yellow Line since the Oct 2025 ceasefire (IDF: tunnel op near
   Nuseirat; Hamas: ceasefire breach); President Herzog tapped Gadi
   Eisenkot to try to form a government. (AFP / NBC / Reuters)
5. **India — Cyclone Akvan, forecast.** Severe cyclonic storm ~470 km
   ESE of Narsapur, winds 90–100 km/h gusting 110; landfall on the
   Narsapur–Puri coast forecast by noon Fri 20 Nov. (IMD Bulletin 28,
   19 Nov 05:30 IST)
6. **Washington — Speaker.** House Democrats nominated Hakeem Jeffries
   251–11 on 18 Nov; he would be the first Black Speaker if elected by
   the full House on 3 Jan 2027. (CNN / NPR / USA Today)

Footer ticker: GTA VI out today; Voyager 1 confirmed one light-day from
Earth; EU proposes a €45bn Ukraine loan. Planned and forecast items are
labelled as such in the image, and conflicting accounts are attributed.

## How to run

```sh
python3 draw.py
MAKEFUN_OUTPUT_DIR=out node main.ts
```

`draw.py` (Python 3, Pillow only) draws `entry.png` (1024×1024) from
scratch — flat pictograms, no photos, no network. `main.ts` (Node 22,
stdlib only) copies it to `$MAKEFUN_OUTPUT_DIR/entry.png`.

## Notes

- No network access at run time; the program is deterministic — repeated
  runs produce byte-identical output.
- MIT licensed (see LICENSE).
