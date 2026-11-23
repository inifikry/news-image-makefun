#!/usr/bin/env python3
"""Draw the front page of 23 November 2026 as a 1024x1024 PNG.

Pure Pillow, deterministic, no network, no AI-generated art.
Every fact on the page was verified against wire/news reports
published on Monday 23 November 2026 (see BUILD_REPORT.md).
"""
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
CW = W - 2 * MARGIN  # 952

PAPER = (251, 248, 241)
INK = (17, 17, 17)
RED = (176, 30, 30)
NAVY = (30, 78, 140)
GRAY = (90, 90, 90)
LIGHT = (238, 233, 224)
GOLD = (184, 134, 11)

FDIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap using real text widths."""
    words = text.split()
    lines, cur = [], ""
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


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, y, x0=MARGIN, x1=W - MARGIN, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def kicker(draw, x, y, text, size=19):
    f = SANS_B(size)
    draw.text((x, y), text, font=f, fill=RED)
    return y + size + 8


# ---- small drawn icons (no text, no borrowed art) ----
def globe(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=4)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
                 outline=NAVY, width=3)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=NAVY, width=3)
    draw.line([(cx - int(r * 0.85), cy - int(r * 0.55)),
               (cx + int(r * 0.85), cy - int(r * 0.55))], fill=NAVY, width=2)
    draw.line([(cx - int(r * 0.85), cy + int(r * 0.55)),
               (cx + int(r * 0.85), cy + int(r * 0.55))], fill=NAVY, width=2)


def burst(draw, x, y, w, h):
    import math
    cx, cy, r = x + w // 2, y + h // 2, min(w, h) // 2
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=RED)


def bars(draw, x, y, w, h):
    vals = [1.0, 0.78, 0.55, 0.34]
    bw = w // 5
    for i, v in enumerate(vals):
        bh = int(h * v)
        draw.rectangle([x + i * (bw + 4), y + h - bh,
                        x + i * (bw + 4) + bw, y + h], fill=RED)


def flags(draw, x, y, w, h):
    draw.line([(x + 6, y), (x + 6, y + h)], fill=INK, width=3)
    draw.line([(x + w - 6, y), (x + w - 6, y + h)], fill=INK, width=3)
    draw.rectangle([x + 8, y, x + w // 2 + 4, y + h // 2], fill=NAVY)
    draw.rectangle([x + w // 2 - 2, y + 4, x + w - 8, y + h // 2 + 4],
                   fill=(70, 130, 180))


def ballot(draw, x, y, w, h):
    draw.rectangle([x, y + h // 3, x + w, y + h], outline=INK, width=3)
    draw.rectangle([x + w // 4, y, x + 3 * w // 4, y + h // 2],
                   outline=INK, width=3, fill=(255, 255, 255))
    draw.line([(x + w // 3, y + h // 4), (x + w // 2 - 2, y + h // 3),
               (x + 2 * w // 3, y + h // 8)], fill=(20, 120, 40), width=4)


def story(draw, x, y, w, kick, head, body, icon=None, head_size=27):
    y = kicker(draw, x, y, kick, size=17)
    hf = SERIF_B(head_size)
    lines = wrap(draw, head, hf, w - (90 if icon else 0))
    hy = y
    for line in lines:
        draw.text((x, hy), line, font=hf, fill=INK)
        hy += head_size + 5
    if icon:
        icon(draw, x + w - 78, y + 2, 78, 44)
    y = para(draw, x, hy + 2, body, SANS(19), w, 23)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.text((W // 2, 30), "THE WORLD TODAY", font=SERIF_B(60),
           fill=INK, anchor="ma")
    rule(d, 108, width=3)
    d.text((W // 2, 120), "MONDAY, 23 NOVEMBER 2026", font=SANS_B(30),
           fill=RED, anchor="ma")
    d.text((W // 2, 154), "THE DAY'S NEWS IN ONE PAGE",
           font=SANS(16), fill=GRAY, anchor="ma")
    rule(d, 182, width=2)

    # ---- lead story: COP31 ----
    y = 198
    y = kicker(d, MARGIN, y, "CLIMATE  •  ANTALYA, TURKEY", size=19)
    d.text((MARGIN, y), "COP31 COLLAPSES", font=SERIF_B(44), fill=INK)
    d.text((MARGIN, y + 50), "WITHOUT A DEAL", font=SERIF_B(44), fill=INK)
    globe(d, 888, 300, 72)
    y = para(d, MARGIN, y + 112,
             "The UN climate summit in Antalya ended on Sunday with no "
             "overall deal, after the EU and about 130 other parties "
             "rejected a draft text that omitted fossil fuels. It was the "
             "longest UN climate summit ever held.",
             SANS(20), 640, 26)
    rule(d, 452, width=2)

    # ---- middle grid: two columns, two stories each ----
    col_w = (CW - 24) // 2
    left, right = MARGIN, MARGIN + col_w + 24
    y0 = 464
    y1 = story(d, left, y0, col_w, "WAR  •  KYIV REGION, UKRAINE",
               "Russian strike kills at least 10 near Kyiv",
               "A strike on Dymer, north of Kyiv, killed at least 10 "
               "people. Rescuers pulled a 7-year-old boy alive from the "
               "rubble.", icon=burst)
    y1 = story(d, left, y1 + 10, col_w,
               "DIPLOMACY  •  ALASKA / ABU DHABI",
               "Trump to meet Putin tomorrow",
               "Trump said Russia faces “very severe consequences” if it "
               "rejects a ceasefire. His envoy floated a NATO-style "
               "security guarantee for Kyiv; US-brokered talks in Abu "
               "Dhabi ended with no breakthrough.", icon=flags)
    y2 = story(d, right, y0, col_w, "MARKETS  •  NEW YORK / TOKYO",
               "AI sell-off rattles world markets",
               "The S&P 500 fell 3.7% and Japan's Nikkei dropped 5.1%. "
               "Nvidia hit a 52-week low, down nearly half from its "
               "October peak, despite record $115.8bn quarterly "
               "revenue.", icon=bars)
    y2 = story(d, right, y2 + 10, col_w, "POLITICS  •  WASHINGTON",
               "Democrats take 258 House seats",
               "A North Carolina recount win gives Democrats their "
               "largest House majority in over 30 years — their best "
               "result since 1992.", icon=ballot)
    y = max(y1, y2) + 6
    rule(d, y, width=2)

    # ---- justice strip ----
    y += 10
    d.rectangle([MARGIN, y, W - MARGIN, y + 80], fill=LIGHT,
                outline=INK, width=1)
    d.text((MARGIN + 14, y + 8), "JUSTICE  •  SINALOA, MEXICO",
           font=SANS_B(17), fill=RED)
    d.text((MARGIN + 14, y + 28),
           "FBI most-wanted “El Chapo Isidro” captured",
           font=SERIF_B(26), fill=INK)
    d.text((MARGIN + 14, y + 58),
           "Drug lord Fausto Isidro Meza Flores was arrested in Guasave, "
           "north-western Mexico.",
           font=SANS(15), fill=GRAY)
    y += 80 + 8
    rule(d, y, width=2)

    # ---- also today ----
    y += 8
    d.text((MARGIN, y), "ALSO TODAY", font=SANS_B(17), fill=RED)
    y += 22
    y = para(d, MARGIN, y,
             "Delta outage delays 1,600+ flights  •  Penny ends after "
             "232 years  •  Márquez wins 8th MotoGP title  •  AI-assisted "
             "Riemann proof verified in Lean",
             SANS(18), CW, 23)
    y += 4
    d.text((W // 2, y),
           "Front page compiled from wire reports published "
           "Monday 23 November 2026.",
           font=SANS(13), fill=GRAY, anchor="ma")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
