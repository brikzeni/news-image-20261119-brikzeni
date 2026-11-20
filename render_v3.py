#!/usr/bin/env python3
"""Render v3 of the 19 November 2026 image — 'The Balance'.

A poster, not a page. One monumental scales of justice pivoting on a
halftone globe, a gold 9–6 medallion at the pivot: the day the world was
weighed — in court (ICJ genocide verdict) and in a summit room (the first
Trump–Xi–Putin trilateral). Everything else is two pan labels and two
supporting lines. ~55 words total. No boxes, no grid, no cards, no columns.

All visuals are hand-coded vector geometry (no stock, no AI imagery, no
faces, no glow). Palette: ink navy + one gold accent, cream text.
Deterministic: no network, no clock, no randomness.
Run: python3 render_v3.py  ->  writes entry.png next to this file.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (14, 27, 46)
CREAM = (242, 234, 216)
MUTED = (154, 168, 188)
GOLD = (227, 179, 65)
DOT = (124, 147, 176)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def halftone_globe(draw, cx, cy, r):
    """A sphere built from dots — dense at the centre, sparse at the rim."""
    step = 8
    for gy in range(cy - r, cy + r + 1, step):
        for gx in range(cx - r, cx + r + 1, step):
            d = math.hypot(gx - cx, gy - cy) / r
            if d >= 1:
                continue
            rad = 1.0 + 3.0 * (1 - d * d)
            draw.ellipse([gx - rad, gy - rad, gx + rad, gy + rad], fill=DOT)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=2)


def rotated_rect(draw, cx, cy, angle_deg, length, width, fill):
    a = math.radians(angle_deg)
    dx, dy = math.cos(a), math.sin(a)
    px, py = -dy, dx
    hl, hw = length / 2, width / 2
    pts = [(cx + dx * hl + px * hw, cy + dy * hl + py * hw),
           (cx + dx * hl - px * hw, cy + dy * hl - py * hw),
           (cx - dx * hl - px * hw, cy - dy * hl - py * hw),
           (cx - dx * hl + px * hw, cy - dy * hl + py * hw)]
    draw.polygon(pts, fill=fill)


def icon_gavel(draw, cx, cy, col=NAVY):
    # horizontal gavel: block head, handle down, end knob
    draw.rounded_rectangle([cx - 32, cy - 18, cx + 32, cy - 2], radius=4,
                           fill=col)
    draw.line([(cx, cy - 2), (cx, cy + 26)], fill=col, width=6)
    draw.ellipse([cx - 4, cy + 24, cx + 4, cy + 32], fill=col)


def icon_nodes(draw, cx, cy, col=NAVY):
    pts = [(cx - 24, cy + 8), (cx + 24, cy + 8), (cx, cy - 20)]
    for a in range(3):
        for b in range(a + 1, 3):
            draw.line([pts[a], pts[b]], fill=col, width=3)
    for (px, py) in pts:
        draw.ellipse([px - 9, py - 9, px + 9, py + 9], outline=col,
                     width=3, fill=GOLD)


def pan(draw, cx, rim_y, half_w=90, depth=60):
    """A hanging pan: chains fanning from the beam to a gold half-disc."""
    bbox = [cx - half_w, rim_y - depth, cx + half_w, rim_y + depth]
    for ex in (cx - half_w + 20, cx, cx + half_w - 20):
        draw.line([(cx, 330), (ex, rim_y)], fill=GOLD, width=3)
    draw.chord(bbox, 0, 180, fill=GOLD, outline=NAVY, width=2)


def centered(draw, cx, y, text, fnt, fill=CREAM):
    draw.text((cx, y), text, font=fnt, fill=fill, anchor="ma")


def main():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # ---- Title, date, concept line ----
    centered(d, 512, 40, "THE DAY THE WORLD WAS WEIGHED",
             font(SERIF_B, 42))
    centered(d, 512, 96, "THURSDAY, 19 NOVEMBER 2026",
             font(SERIF_B, 30), fill=GOLD)
    centered(d, 512, 140,
             "Justice weighed a nation. Three powers met. The world moved on.",
             font(SANS, 16), fill=MUTED)

    # ---- Globe finial ----
    halftone_globe(d, 512, 215, 34)

    # ---- Post, beam, medallion ----
    d.rectangle([507, 249, 517, 790], fill=GOLD)
    d.line([(170, 330), (854, 330)], fill=GOLD, width=8)
    for ex in (170, 854):
        d.ellipse([ex - 8, 322, ex + 8, 338], fill=GOLD)
    d.ellipse([512 - 46, 330 - 46, 512 + 46, 330 + 46], fill=GOLD)
    d.text((512, 330), "9–6", font=font(SERIF_B, 32), fill=NAVY,
           anchor="mm")

    # ---- Pans + icons ----
    pan(d, 170, 580)
    pan(d, 854, 580)
    icon_gavel(d, 170, 612)
    icon_nodes(d, 854, 612)

    # ---- Stepped base ----
    d.polygon([(468, 790), (556, 790), (574, 812), (450, 812)], fill=GOLD)
    d.line([(430, 812), (594, 812)], fill=GOLD, width=3)

    # ---- Pan labels ----
    for cx, kick, h1, h2, deck in (
            (170, "THE HAGUE — ICJ", "MYANMAR GUILTY", "OF GENOCIDE",
             "First state ever held responsible."),
            (854, "SHENZHEN — APEC", "TRUMP · XI · PUTIN", "MEET",
             "First trilateral of the three powers.")):
        centered(d, cx, 656, kick, font(SANS_B, 12), fill=GOLD)
        centered(d, cx, 676, h1, font(SERIF_B, 20))
        centered(d, cx, 700, h2, font(SERIF_B, 20))
        centered(d, cx, 730, deck, font(SANS, 14), fill=MUTED)

    # ---- Supporting lines ----
    d.line([(200, 850), (824, 850)], fill=GOLD, width=2)
    centered(d, 512, 870,
             "GTA VI launches worldwide  •  Anthropic debuts on Nasdaq, +17%",
             font(SANS, 16))
    centered(d, 512, 902,
             "COP31 draft drops fossil fuels  •  Gaza peace plan scores 4/26",
             font(SANS, 16))
    centered(d, 512, 984,
             "All events 19 November 2026 — ICJ  •  Reuters  •  AP  •  BBC  •  AFP  •  NASA  •  IEA",
             font(SANS, 12), fill=MUTED)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
