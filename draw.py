#!/usr/bin/env python3
"""Draw the 19 November 2026 front page: six stories, one image.

Python 3, Pillow only, no network, no photos, no copied art.
Deterministic: fixed palette, fixed geometry, fixed fonts.
Writes entry.png (1024x1024 RGB) next to this file.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

PAPER = (247, 242, 231)
INK = (26, 26, 26)
RED = (164, 18, 31)
NAVY = (31, 58, 95)
GOLD = (184, 134, 11)
TEAL = (14, 110, 110)
SLATE = (90, 90, 90)
PANEL = (255, 255, 255)
FOOTER = (26, 26, 26)
SKY = (214, 232, 240)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


# ---------------- pictograms (flat, drawn from scratch) ----------------

def pic_trilateral(d, x, y, w, h):
    # Three leader busts side by side, centred in the band.
    cols = [RED, NAVY, (42, 82, 150)]
    for i, c in enumerate(cols):
        bx = x + 30 + i * 62
        d.ellipse([bx, y + 12, bx + 44, y + 56], fill=c)
        d.pieslice([bx - 4, y + 50, bx + 48, y + 92], 180, 360, fill=c)


def pic_ipo(d, x, y, w, h):
    # Rising bars, a big arrow, and a dollar coin.
    base = y + h - 18
    bars = [(x + 30, 26), (x + 70, 44), (x + 110, 62), (x + 150, 80)]
    for bx, bh in bars:
        d.rectangle([bx, base - bh, bx + 28, base], fill=TEAL)
    d.line([(x + 30, base - 30), (x + 95, base - 58),
            (x + 135, base - 44), (x + 175, base - 92)],
           fill=RED, width=6)
    d.polygon([(x + 175, base - 92), (x + 158, base - 92),
               (x + 175, base - 74)], fill=RED)
    d.ellipse([x + w - 78, y + 6, x + w - 14, y + 70], fill=GOLD,
              outline=(140, 100, 0), width=3)
    d.text((x + w - 62, y + 18), "$", font=font(BOLD, 34), fill=(255, 255, 255))


def pic_bridge(d, x, y, w, h):
    # Arch bridge over water with a broken span in the middle.
    base = y + h - 26
    d.rectangle([x, base, x + w, base + 8], fill=(120, 160, 190))
    for i in range(5):
        wx = x + 18 + i * 34
        d.arc([wx, base - 6, wx + 26, base + 8], 180, 360, fill=(255, 255, 255), width=3)
    d.rectangle([x + 16, y + 44, x + 30, base], fill=NAVY)
    d.rectangle([x + w - 30, y + 44, x + w - 16, base], fill=NAVY)
    d.arc([x + 16, y + 8, x + w - 16, y + 92], 180, 360, fill=NAVY, width=7)
    # broken gap: erase a chunk of the arch and deck centre
    gap_cx = x + w // 2
    d.polygon([(gap_cx - 22, y + 8), (gap_cx + 22, y + 8),
               (gap_cx + 12, y + 44), (gap_cx - 12, y + 44)], fill=SKY)
    d.rectangle([gap_cx - 24, y + 40, gap_cx + 24, y + 48], fill=SKY)
    d.polygon([(gap_cx - 26, y + 48), (gap_cx - 6, y + 48),
               (gap_cx - 16, y + 66)], fill=NAVY)
    d.polygon([(gap_cx + 6, y + 48), (gap_cx + 26, y + 48),
               (gap_cx + 16, y + 66)], fill=NAVY)
    # smoke puffs above the gap
    for sx, sy, r in [(gap_cx - 12, y + 2, 7), (gap_cx + 8, y - 2, 9),
                      (gap_cx, y + 10, 6)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(150, 150, 150))


def pic_gaza(d, x, y, w, h):
    # Cracked building beside a ballot box with a check mark.
    base = y + h - 14
    d.rectangle([x + 24, y + 30, x + 86, base], fill=NAVY)
    d.rectangle([x + 34, y + 44, x + 46, y + 56], fill=SKY)
    d.rectangle([x + 62, y + 44, x + 74, y + 56], fill=SKY)
    d.rectangle([x + 34, y + 68, x + 46, y + 80], fill=SKY)
    d.rectangle([x + 62, y + 68, x + 74, y + 80], fill=SKY)
    d.line([(x + 55, y + 30), (x + 48, y + 52), (x + 62, y + 70),
            (x + 52, base)], fill=RED, width=4)
    d.rectangle([x + 118, y + 56, x + 178, base], fill=GOLD)
    d.rectangle([x + 128, y + 44, x + 168, y + 56], fill=(140, 100, 0))
    d.line([(x + 132, y + 78), (x + 144, y + 90), (x + 166, y + 64)],
           fill=(255, 255, 255), width=5)


def pic_cyclone(d, x, y, w, h):
    # Spiral storm over a coastline, with rain.
    cx, cy = x + w // 2 - 14, y + h // 2 - 6
    for r, a0 in [(52, 0), (40, 60), (28, 120), (16, 180)]:
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a0 + 250,
              fill=TEAL, width=6)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED)
    d.line([(x + w - 52, y + 4), (x + w - 52, y + h - 10)], fill=GOLD, width=5)
    d.line([(x + w - 52, y + h - 10), (x + w, y + h - 10)], fill=GOLD, width=5)
    for rx in (x + 8, x + 30, x + 52):
        d.line([(rx, y + h - 22), (rx - 4, y + h - 10)], fill=NAVY, width=3)


def pic_jeffries(d, x, y, w, h):
    # Capitol dome over a podium, with a gavel.
    cx = x + w // 2
    d.polygon([(cx - 66, y + 52), (cx + 66, y + 52), (cx + 66, y + 60),
               (cx - 66, y + 60)], fill=NAVY)
    d.rectangle([cx - 56, y + 60, cx + 56, y + 78], fill=NAVY)
    d.pieslice([cx - 30, y + 8, cx + 30, y + 56], 180, 360, fill=NAVY)
    d.rectangle([cx - 3, y + 2, cx + 3, y + 14], fill=NAVY)
    d.rectangle([cx - 78, y + 78, cx + 78, y + 88], fill=GOLD)
    d.rectangle([cx - 88, y + 88, cx + 88, y + 96], fill=(140, 100, 0))
    d.line([(cx + 96, y + 30), (cx + 128, y + 62)], fill=(120, 80, 20), width=5)
    d.rectangle([cx + 118, y + 58, cx + 138, y + 70], fill=(120, 80, 20))


PANELS = [
    ("SHENZHEN  •  TRILATERAL — PLANNED", RED,
     "Xi, Trump & Putin to meet for the first time",
     "First-ever Xi-Trump-Putin talks; nuclear arms on agenda",
     pic_trilateral),
    ("WALL STREET  •  IPO", TEAL,
     "Anthropic debuts in the biggest IPO ever",
     "Record $81.3bn IPO; trading starts today as ANT",
     pic_ipo),
    ("CRIMEA  •  BRIDGE", NAVY,
     "Kerch Bridge hit for a third time this week",
     "Third strike this week; traffic halted, damage checked",
     pic_bridge),
    ("GAZA  •  ISRAEL", RED,
     "First Gaza ground op since the ceasefire",
     "First Gaza ground op since ceasefire; Eisenkot tapped to govern",
     pic_gaza),
    ("INDIA  •  CYCLONE AKVAN — FORECAST", TEAL,
     "Severe cyclone Akvan nears the Andhra coast",
     "Severe storm off Andhra coast; landfall forecast Fri",
     pic_cyclone),
    ("WASHINGTON  •  SPEAKER", NAVY,
     "Democrats nominate Jeffries for Speaker",
     "Democrats pick Jeffries 251-11; first Black Speaker if elected 3 Jan",
     pic_jeffries),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 118], fill=INK)
    d.text((24, 12), "THE WORLD TODAY", font=font(BOLD, 52), fill=(255, 255, 255))
    d.text((24, 76), "THURSDAY 19 NOVEMBER 2026  —  THE DAY IN ONE IMAGE",
           font=font(BOLD, 22), fill=(232, 196, 90))
    d.rectangle([W - 118, 14, W - 24, 104], outline=(232, 196, 90), width=3)
    d.text((W - 106, 26), "19", font=font(BOLD, 40), fill=(255, 255, 255))
    d.text((W - 106, 70), "NOV", font=font(BOLD, 20), fill=(232, 196, 90))

    # ---- grid: 2 cols x 3 rows ----
    gx, gy = 16, 130
    pw, ph, gap = 488, 252, 16
    for i, (kicker, accent, headline, caption, pic) in enumerate(PANELS):
        px = gx + (i % 2) * (pw + gap)
        py = gy + (i // 2) * (ph + gap)
        d.rectangle([px, py, px + pw, py + ph], fill=PANEL,
                    outline=(200, 190, 170), width=2)
        d.rectangle([px, py, px + pw, py + 6], fill=accent)
        d.text((px + 14, py + 14), kicker, font=font(BOLD, 15), fill=accent)
        # pictogram band
        pic_y = py + 38
        d.rectangle([px + 14, pic_y, px + pw - 14, pic_y + 96], fill=SKY)
        pic(d, px + 130, pic_y, pw - 274, 96)
        y = pic_y + 106
        hl = wrap(d, headline, font(BOLD, 24), pw - 28)
        y = text_block(d, px + 14, y, hl, font(BOLD, 24), INK, 28)
        cap = wrap(d, caption, font(REG, 16), pw - 28)
        text_block(d, px + 14, y + 2, cap, font(REG, 16), SLATE, 20)

    # ---- footer ticker ----
    fy = 130 + 3 * ph + 2 * gap + 12
    d.rectangle([0, fy, W, H], fill=FOOTER)
    d.text((24, fy + 12), "ALSO TODAY",
           font=font(BOLD, 18), fill=(232, 196, 90))
    ticker = ("GTA VI out today  •  Voyager 1 confirmed one light-day from "
              "Earth  •  EU proposes €45bn Ukraine loan")
    lines = wrap(d, ticker, font(REG, 19), W - 48)
    text_block(d, 24, fy + 38, lines, font(REG, 19), (255, 255, 255), 25)

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
