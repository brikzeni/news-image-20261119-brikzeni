#!/usr/bin/env python3
"""Render the 19 November 2026 world-news front page, 1024x1024.

Deterministic: no network, no clock, no randomness. Every story below was
verified against credible reporting (ICJ, Reuters, AP, BBC, AFP, NASA, IEA)
as having happened or first been reported on Thursday 19 November 2026.
Stories that happened on 18 November are deliberately excluded.
Run: python3 render.py  ->  writes entry.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
CW = W - 2 * MARGIN  # 952

PAPER = (250, 246, 236)
INK = (18, 18, 18)
RED = (178, 34, 34)
GREY = (90, 88, 82)
LIGHT = (238, 233, 220)
NAVY = (16, 42, 74)
GREEN = (18, 110, 60)

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


def text_block(draw, x, y, text, fnt, max_w, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.18)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    f_mast = font(SERIF_B, 54)
    title = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(title, font=f_mast)) / 2, 22),
           title, font=f_mast, fill=INK)
    rule(d, MARGIN, 92, W - MARGIN, 3)

    # ---- Date bar ----
    d.rectangle([MARGIN, 100, W - MARGIN, 142], fill=INK)
    f_date = font(SERIF_B, 30)
    date = "THURSDAY, 19 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=f_date)) / 2, 106),
           date, font=f_date, fill=PAPER)
    f_sub = font(SANS, 16)
    sub = "One day of world news — every story below happened or was first reported on this day"
    d.text(((W - d.textlength(sub, font=f_sub)) / 2, 150),
           sub, font=f_sub, fill=GREY)

    # ---- Lead story (left) ----
    y = 180
    f_kick = font(SANS_B, 15)
    d.text((MARGIN, y), "THE HAGUE  •  INTERNATIONAL COURT OF JUSTICE",
           font=f_kick, fill=RED)
    y += 24
    y = text_block(d, MARGIN, y, "MYANMAR COMMITTED GENOCIDE",
                   font(SERIF_B, 46), 560, leading=50)
    y += 4
    y = text_block(d, MARGIN, y,
                   "The world court rules 9–6 against the Rohingya — the first "
                   "time it has held a state responsible for genocide.",
                   font(SERIF, 19), 560, leading=24)
    y += 6
    d.text((MARGIN, y), "2017 Rakhine crackdown — at least 10,000 killed.",
           font=font(SANS, 15), fill=GREY)

    # ---- Second lead (right) ----
    rx = 636
    y2 = 180
    d.text((rx, y2), "SHENZHEN  •  APEC", font=f_kick, fill=RED)
    y2 += 26
    y2 = text_block(d, rx, y2, "TRUMP, XI AND PUTIN MEET",
                    font(SERIF_B, 33), 352, leading=38)
    y2 += 4
    y2 = text_block(d, rx, y2,
                    "First trilateral summit issues a four-point declaration "
                    "on nuclear risk, UN reform and energy — no mention "
                    "of Ukraine.",
                    font(SERIF, 18), 352, leading=23)
    y2 += 6
    d.rectangle([rx, y2, W - MARGIN, y2 + 48], fill=LIGHT)
    text_block(d, rx + 10, y2 + 7,
               "APEC adopts the Shenzhen Outlook by consensus.",
               font(SANS_B, 15), 332, leading=19)

    rule(d, MARGIN, 436, W - MARGIN, 2)

    # ---- Middle band: culture + markets ----
    by = 448
    bh = 108
    # GTA VI (navy)
    d.rectangle([MARGIN, by, MARGIN + 466, by + bh], fill=NAVY)
    d.text((MARGIN + 16, by + 10), "CULTURE  •  VIDEO GAMES",
           font=f_kick, fill=(255, 214, 90))
    text_block(d, MARGIN + 16, by + 34, "GTA VI IS OUT",
               font(SERIF_B, 30), 434, fill=PAPER, leading=34)
    text_block(d, MARGIN + 16, by + 66,
               "Rockstar's game launches worldwide on PS5 and Xbox Series X|S, $79.99.",
               font(SANS, 15), 434, fill=(225, 228, 235), leading=19)
    # Anthropic (light)
    ax = MARGIN + 486
    d.rectangle([ax, by, ax + 466, by + bh], fill=LIGHT)
    d.rectangle([ax, by, ax + 466, by + bh], outline=INK, width=2)
    d.text((ax + 16, by + 10), "MARKETS  •  NEW YORK", font=f_kick, fill=RED)
    text_block(d, ax + 16, by + 34, "ANTHROPIC DEBUTS",
               font(SERIF_B, 28), 434, leading=32)
    text_block(d, ax + 16, by + 68,
               "ANT closes at $97.17 on Nasdaq, up 17% on day one after a record $81.3bn IPO.",
               font(SANS, 15), 434, leading=19)

    # ---- Grid heading ----
    gy = 566
    d.text((MARGIN, gy), "THE DAY IN BRIEF", font=f_kick, fill=INK)
    rule(d, MARGIN, gy + 22, W - MARGIN, 1)
    gy += 32

    stories = [
        ("CLIMATE  •  ANTALYA",
         "COP31 draft drops fossil fuels",
         "Revised text deletes phase-out language."),
        ("GAZA",
         "Nuseirat raid ends; plan scores 4/26",
         "Aid groups rate the peace plan."),
        ("UKRAINE",
         "Third strike on Crimea Bridge",
         "Kyiv hit; embassies damaged, one killed."),
        ("MONGOLIA",
         "President resigns",
         "Parliament accepts it, 96–104."),
        ("GREENLAND",
         "Denmark backs US deal, 109–0",
         "Pituffik base to expand."),
        ("ENERGY",
         "IEA: Hormuz is the biggest threat ever",
         "Historic energy risk, says Outlook."),
        ("BANGLADESH",
         "Lockdown violence grips Dhaka",
         "Awami League protest; arson reported."),
        ("SOUTH KOREA",
         "Ex-PM Han gets a retrial",
         "15-year martial-law sentence overturned."),
        ("SPORT",
         "FIFA race: two challenge Infantino",
         "Diallo, Tashima contest 2027 vote."),
        ("AFRICA",
         "Somalia expels UAE envoy",
         "72 hours to leave, envoy recalled."),
        ("KENYA",
         "US-led group wins rare-earth tender",
         "Mrima Hill beats Chinese rivals."),
        ("SPACE",
         "Voyager 1, one light-day out",
         "NASA confirms it; crossed 18 Nov."),
    ]
    col_w = (CW - 2 * 20) // 3
    row_h = 86
    f_tag = font(SANS_B, 12)
    f_head = font(SERIF_B, 16)
    f_deck = font(SANS, 13)
    for i, (tag, head, deck) in enumerate(stories):
        col, row = i % 3, i // 3
        x = MARGIN + col * (col_w + 20)
        y = gy + row * row_h
        d.text((x, y), tag, font=f_tag, fill=RED)
        y += 17
        y = text_block(d, x, y, head, f_head, col_w, leading=19)
        text_block(d, x, y, deck, f_deck, col_w, fill=GREY, leading=16)

    ty = gy + 4 * row_h + 4
    rule(d, MARGIN, ty, W - MARGIN, 1)
    f_tick = font(SANS_B, 12)
    ticker = ("ALSO:  NASA pauses Mars science  •  Jepchirchir banned 3 years for EPO  •  "
              "Ethiopia–Eritrea troops mass near Badme")
    text_block(d, MARGIN, ty + 9, ticker, f_tick, CW, leading=16)
    f_foot = font(SANS, 12)
    foot = "Sources: ICJ  •  Reuters  •  AP  •  BBC  •  AFP  •  NASA  •  IEA  —  All events 19 November 2026"
    d.text(((W - d.textlength(foot, font=f_foot)) / 2, H - 26),
           foot, font=f_foot, fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
