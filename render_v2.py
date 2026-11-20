#!/usr/bin/env python3
"""Render v2 of the 19 November 2026 front page — 'Night Desk' system.

Philosophy: the world desk after dark. Deep ink-navy paper, one gold accent,
every visual hand-coded vector geometry — no stock, no AI imagery, no faces,
no glow, no decorative filler. Every mark encodes a real story: the halftone
globe (one world, one day), scales (ICJ verdict), three nodes (trilateral),
gamepad (GTA VI), rising chart (IPO). Same 17 verified 19-Nov stories as v1;
only the visual system changes.

Deterministic: no network, no clock, no randomness.
Run: python3 render_v2.py  ->  writes entry.png next to this file.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
CW = W - 2 * MARGIN  # 952

NAVY = (14, 27, 46)
PANEL = (22, 39, 63)
CREAM = (242, 234, 216)
MUTED = (154, 168, 188)
GOLD = (227, 179, 65)
DOT = (124, 147, 176)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


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


def text_block(draw, x, y, text, fnt, max_w, fill=CREAM, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.18)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=GOLD):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def halftone_globe(draw, cx, cy, r):
    """A sphere built from dots — dense at the centre, sparse at the rim."""
    step = 9
    for gy in range(cy - r, cy + r + 1, step):
        for gx in range(cx - r, cx + r + 1, step):
            d = math.hypot(gx - cx, gy - cy) / r
            if d >= 1:
                continue
            rad = 1.0 + 3.0 * (1 - d * d)
            draw.ellipse([gx - rad, gy - rad, gx + rad, gy + rad], fill=DOT)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=2)


def icon_scales(draw, cx, cy, col=GOLD, w=3):
    draw.line([(cx, cy - 20), (cx, cy + 20)], fill=col, width=w)
    draw.line([(cx - 22, cy - 14), (cx + 22, cy - 14)], fill=col, width=w)
    for sx in (-22, 22):
        draw.line([(cx + sx, cy - 14), (cx + sx, cy + 2)], fill=col, width=2)
        draw.polygon([(cx + sx - 9, cy + 2), (cx + sx + 9, cy + 2),
                      (cx + sx, cy + 12)], fill=col)
    draw.line([(cx - 10, cy + 20), (cx + 10, cy + 20)], fill=col, width=w)


def icon_nodes(draw, cx, cy, col=GOLD, w=3):
    pts = [(cx - 20, cy + 10), (cx + 20, cy + 10), (cx, cy - 14)]
    for a in range(3):
        for b in range(a + 1, 3):
            draw.line([pts[a], pts[b]], fill=col, width=2)
    for (px, py) in pts:
        draw.ellipse([px - 6, py - 6, px + 6, py + 6], outline=col,
                     width=w, fill=NAVY)


def icon_gamepad(draw, cx, cy, col=GOLD, w=3):
    draw.rounded_rectangle([cx - 26, cy - 14, cx + 26, cy + 14], radius=9,
                           outline=col, width=w)
    draw.rectangle([cx - 19, cy - 3, cx - 11, cy + 3], fill=col)
    draw.rectangle([cx - 16, cy - 6, cx - 14, cy + 6], fill=col)
    for (bx, by) in ((cx + 12, cy - 4), (cx + 19, cy + 3)):
        draw.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=col)


def icon_chart(draw, cx, cy, col=GOLD, w=3):
    draw.line([(cx - 24, cy + 16), (cx + 24, cy + 16)], fill=col, width=w)
    draw.line([(cx - 24, cy + 16), (cx - 24, cy - 18)], fill=col, width=w)
    pts = [(cx - 20, cy + 10), (cx - 6, cy + 2), (cx + 6, cy + 4),
           (cx + 20, cy - 12)]
    draw.line(pts, fill=col, width=w, joint="curve")
    draw.polygon([(cx + 20, cy - 12), (cx + 12, cy - 12), (cx + 20, cy - 4)],
                 fill=col)


def lead_panel(draw, x, y, pw, ph, icon, kicker, head, deck):
    draw.rectangle([x, y, x + pw, y + ph], fill=PANEL)
    draw.rectangle([x, y, x + pw, y + ph], outline=GOLD, width=1)
    icon(draw, x + pw // 2, y + 34)
    f_kick = font(SANS_B, 12)
    kt = kicker
    draw.text(((x + x + pw - draw.textlength(kt, font=f_kick)) / 2, y + 66),
              kt, font=f_kick, fill=GOLD)
    y2 = text_block(draw, x + 16, y + 88, head, font(SERIF_B, 23), pw - 32,
                    leading=26)
    text_block(draw, x + 16, y2 + 4, deck, font(SANS, 14), pw - 32,
               fill=MUTED, leading=18)


def main():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # ---- Masthead: title left, halftone globe right ----
    halftone_globe(d, 936, 56, 44)
    f_mast = font(SERIF_B, 50)
    d.text((MARGIN, 26), "THE WORLD IN ONE DAY", font=f_mast, fill=CREAM)
    f_date = font(SERIF_B, 27)
    d.text((MARGIN, 90), "THURSDAY, 19 NOVEMBER 2026", font=f_date,
           fill=GOLD)
    f_sub = font(SANS, 15)
    d.text((MARGIN, 126),
           "One day of world news — every story below happened or was first reported on this day",
           font=f_sub, fill=MUTED)
    rule(d, MARGIN, 154, W - MARGIN, 2)

    # ---- Three illustrated lead panels ----
    pw, ph, gap = 304, 208, 20
    py = 170
    lead_panel(d, MARGIN, py, pw, ph, icon_scales,
               "THE HAGUE — ICJ", "MYANMAR COMMITTED GENOCIDE",
               "World court rules 9–6 — the first state held responsible.")
    lead_panel(d, MARGIN + pw + gap, py, pw, ph, icon_nodes,
               "SHENZHEN — APEC", "TRUMP, XI AND PUTIN MEET",
               "First trilateral: four-point declaration on nuclear risk, UN reform and energy.")
    lead_panel(d, MARGIN + 2 * (pw + gap), py, pw, ph, icon_gamepad,
               "CULTURE — VIDEO GAMES", "GTA VI IS OUT",
               "Launches worldwide on PS5 and Xbox Series X|S, $79.99.")

    # ---- Markets strip ----
    sy = 392
    d.rectangle([MARGIN, sy, W - MARGIN, sy + 66], fill=PANEL)
    d.rectangle([MARGIN, sy, W - MARGIN, sy + 66], outline=GOLD, width=1)
    icon_chart(d, MARGIN + 40, sy + 33)
    d.text((MARGIN + 76, sy + 10), "ANTHROPIC DEBUTS",
           font=font(SERIF_B, 22), fill=CREAM)
    d.text((MARGIN + 76, sy + 38),
           "ANT closes at $97.17 on Nasdaq, up 17% — record $81.3bn IPO.",
           font=font(SANS, 14), fill=MUTED)
    apec = "APEC adopts the Shenzhen Outlook."
    d.text((W - MARGIN - d.textlength(apec, font=font(SANS_B, 14)), sy + 24),
           apec, font=font(SANS_B, 14), fill=GOLD)

    # ---- Grid heading ----
    gy = 476
    d.text((MARGIN, gy), "THE DAY IN BRIEF", font=font(SANS_B, 14), fill=CREAM)
    rule(d, MARGIN, gy + 22, W - MARGIN, 1)

    stories = [
        ("CLIMATE  •  ANTALYA", "COP31 draft drops fossil fuels",
         "Revised text deletes phase-out language."),
        ("GAZA", "Nuseirat raid ends; plan scores 4/26",
         "Aid groups rate the peace plan."),
        ("UKRAINE", "Third strike on Crimea Bridge",
         "Kyiv hit; embassies damaged, one killed."),
        ("MONGOLIA", "President resigns",
         "Parliament accepts it, 96–104."),
        ("GREENLAND", "Denmark backs US deal, 109–0",
         "Pituffik base to expand."),
        ("ENERGY", "IEA: Hormuz is the biggest threat ever",
         "Historic energy risk, says Outlook."),
        ("BANGLADESH", "Lockdown violence grips Dhaka",
         "Awami League protest; arson reported."),
        ("SOUTH KOREA", "Ex-PM Han gets a retrial",
         "15-year martial-law sentence overturned."),
        ("SPORT", "FIFA race: two challenge Infantino",
         "Diallo, Tashima contest 2027 vote."),
        ("AFRICA", "Somalia expels UAE envoy",
         "72 hours to leave, envoy recalled."),
        ("KENYA", "US-led group wins rare-earth tender",
         "Mrima Hill beats Chinese rivals."),
        ("SPACE", "Voyager 1, one light-day out",
         "NASA confirms it; crossed 18 Nov."),
    ]
    col_w = (CW - 2 * 20) // 3
    row_h = 106
    gy += 34
    for i, (tag, head, deck) in enumerate(stories):
        col, row = i % 3, i // 3
        x = MARGIN + col * (col_w + 20)
        y = gy + row * row_h
        d.text((x, y), tag, font=font(SANS_B, 12), fill=GOLD)
        y += 17
        y = text_block(d, x, y, head, font(SERIF_B, 16), col_w, leading=19)
        text_block(d, x, y, deck, font(SANS, 13), col_w, fill=MUTED,
                   leading=16)

    ty = gy + 4 * row_h + 4
    rule(d, MARGIN, ty, W - MARGIN, 1)
    ticker = ("ALSO:  NASA pauses Mars science  •  Jepchirchir banned 3 years for EPO  •  "
              "Ethiopia–Eritrea troops mass near Badme")
    text_block(d, MARGIN, ty + 9, ticker, font(SANS_B, 12), CW, fill=MUTED,
               leading=16)
    f_foot = font(SANS, 12)
    foot = "Sources: ICJ  •  Reuters  •  AP  •  BBC  •  AFP  •  NASA  •  IEA  —  All events 19 November 2026"
    d.text(((W - d.textlength(foot, font=f_foot)) / 2, H - 26),
           foot, font=f_foot, fill=MUTED)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
