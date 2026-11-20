#!/usr/bin/env python3
"""Composite v4 of the 19 November 2026 image — 'The Balance' (illustrated).

Base art: an original flat editorial illustration generated in-session
(illustrations/media-generation-balance-*.png — golden scales of justice
with a dotted-globe finial, navy + gold + cream, no text). This script
scales it to 824x824, pastes it on a navy canvas, and typesets the
headline, date and labels deterministically with Pillow/DejaVu — so every
word is sharp and factually exact.

Deterministic: same art + same script = same bytes (no network, clock,
randomness). Run: python3 compose_v4.py -> writes entry.png next to it.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (14, 27, 46)
CREAM = (242, 234, 216)
MUTED = (154, 168, 188)
GOLD = (227, 179, 65)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def centered(draw, cx, y, text, fnt, fill=CREAM):
    draw.text((cx, y), text, font=fnt, fill=fill, anchor="ma")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    art_path = os.path.join(here, "illustrations", "balance.png")
    art = Image.open(art_path).convert("RGB").resize((824, 824),
                                                     Image.LANCZOS)
    img = Image.new("RGB", (W, H), NAVY)
    img.paste(art, (100, 200))
    d = ImageDraw.Draw(img)

    # ---- Top band: title, date, concept, supporting line ----
    centered(d, 512, 30, "THE DAY THE WORLD WAS WEIGHED",
             font(SERIF_B, 40))
    centered(d, 512, 84, "THURSDAY, 19 NOVEMBER 2026",
             font(SERIF_B, 28), fill=GOLD)
    centered(d, 512, 124,
             "Justice weighed a nation. Three powers met. The world moved on.",
             font(SANS, 16), fill=MUTED)
    centered(d, 512, 152,
             "GTA VI launches worldwide  •  Anthropic debuts +17%  •  COP31 drops fossil fuels  •  Gaza plan 4/26",
             font(SANS, 15))
    d.line([(200, 180), (824, 180)], fill=GOLD, width=2)

    # ---- Pan labels (pan centres measured: 314 and 710 in the composite) ----
    for cx, kick, h1, h2, deck in (
            (314, "THE HAGUE — ICJ", "MYANMAR GUILTY", "OF GENOCIDE",
             "First state ever held responsible."),
            (710, "SHENZHEN — APEC", "TRUMP · XI · PUTIN", "MEET",
             "First trilateral of the three powers.")):
        centered(d, cx, 888, kick, font(SANS_B, 12), fill=GOLD)
        centered(d, cx, 908, h1, font(SERIF_B, 20))
        centered(d, cx, 932, h2, font(SERIF_B, 20))
        centered(d, cx, 962, deck, font(SANS, 14), fill=MUTED)

    out = os.path.join(here, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
