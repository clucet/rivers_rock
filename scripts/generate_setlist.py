#!/usr/bin/env python3
"""Generate Rivers Rock setlist PDF (A4 Portrait, Scène & Vintage)."""

import os, sys, math, random
sys.path.insert(0, os.path.dirname(__file__))
from logoutils import reportlab_crest, BEBAS_PATH, MONTSERRAT_PATH, create_bleed_canvas, save_with_crop_marks
from palette import ACTIVE as CFG
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import Color
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

OUTPUT = os.path.join(os.path.dirname(__file__), "..", "pdf", "setlist-rivers-rock.pdf")

BLEU_SEINE = CFG.rl("bleu_seine")
TEAL_PROFOND = CFG.rl("teal_profond")
ACCENT = CFG.rl("accent")
TERRACOTTA = CFG.rl("terracotta")
OR_VIEILLI = CFG.rl("or_vieilli")
BLANC = CFG.rl("blanc")

pdfmetrics.registerFont(TTFont("BebasNeue", BEBAS_PATH))
pdfmetrics.registerFont(TTFont("Montserrat", MONTSERRAT_PATH))

W, H = A4[0], A4[1]

SETLIST = [
    ("NIAGARA", "J'ai vu"),
    ("AC/DC", "You shook me all night long"),
    ("DOLLY", "Je n'veux pas rester sage"),
    ("THE PIXIES", "Where is my mind"),
    ("PJ HARVEY", "Good fortune"),
    ("BELLA CIAO", ""),
    ("SMASHING PUMPKINS", "Today"),
    ("RADIOHEAD", "Creep"),
    ("DESIRELESS", "Voyage, voyage"),
    ("QUEEN", "We will rock you"),
    ("ROLLING STONES", "Jumping jack flash"),
    ("WHITE STRIPES", "Seven nation army"),
]

GREEN_INDICES = {0, 3, 6}

W, H = A4[0], A4[1]

BADGE_R = 12
MARGIN_H = 16
GAP = 8
ARTIST_BASELINE = 5
TITLE_BASELINE = -17
BADGE_Y_OFFSET = 15
SHADOW_OFFSET = 4
SHADOW_ALPHA = 0.20

CARD_W = 250
CARD_H = 74
CARD_R = 6
COL_GAP = (W - 2 * CARD_W) / 3
COL_CENTERS = [COL_GAP + CARD_W / 2, COL_GAP * 2 + CARD_W + CARD_W / 2]
ROW_PITCH = 86
ROWS_TOP = 610


def draw_gradient(cv):
    steps = 120
    dh = H / steps
    for i in range(steps):
        t = i / (steps - 1)
        r = BLEU_SEINE.red + (TEAL_PROFOND.red - BLEU_SEINE.red) * t
        g = BLEU_SEINE.green + (TEAL_PROFOND.green - BLEU_SEINE.green) * t
        b = BLEU_SEINE.blue + (TEAL_PROFOND.blue - BLEU_SEINE.blue) * t
        cv.setFillColor(Color(r, g, b))
        cv.rect(0, i * dh, W, dh + 1, stroke=0, fill=1)


def draw_grain(cv):
    random.seed(42)
    for _ in range(3000):
        x = random.uniform(0, W)
        y = random.uniform(0, H)
        a = random.uniform(0.02, 0.06)
        cv.setFillColor(Color(1, 1, 1, alpha=a))
        cv.circle(x, y, random.uniform(0.3, 1.0), stroke=0, fill=1)


def draw_waves(cv):
    cv.setFillColor(Color(1, 1, 1, alpha=0.06))
    for row in range(3):
        y_base = 20 + row * 30
        amp = 8 + row * 6
        period = 28 + row * 12
        segments = 300
        step_x = W / segments
        p = cv.beginPath()
        p.moveTo(0, y_base)
        for i in range(segments + 1):
            px = i * step_x
            py = y_base + amp * math.sin(i * 2 * math.pi / period)
            p.lineTo(px, py)
        p.lineTo(W, 0)
        p.lineTo(0, 0)
        p.close()
        cv.drawPath(p, fill=1, stroke=0)
    cv.setStrokeColor(OR_VIEILLI)
    cv.setLineWidth(1.5)
    y_line = H - 45
    segments = 200
    step_x = W / segments
    p = cv.beginPath()
    p.moveTo(0, y_line)
    for i in range(segments + 1):
        px = i * step_x
        py = y_line + 8 * math.sin(i * 2 * math.pi / 32)
        p.lineTo(px, py)
    cv.drawPath(p, stroke=1, fill=0)


def draw_logo(cv):
    crest_scale = 2.2
    reportlab_crest(cv, W / 2, H - 115, crest_scale)


def draw_setlist_subtitle(cv):
    cv.setFillColor(ACCENT)
    cv.setFont("BebasNeue", 28)
    cv.drawCentredString(W / 2, H - 165, "SETLIST")
    cv.setStrokeColor(OR_VIEILLI)
    cv.setLineWidth(1.5)
    wave_len = 160
    wave_x0 = W / 2 - wave_len / 2
    wave_y = H - 178
    segs = 30
    p = cv.beginPath()
    p.moveTo(wave_x0, wave_y)
    for i in range(segs + 1):
        t = i / segs
        px = wave_x0 + t * wave_len
        py = wave_y + 3.5 * math.sin(t * 2 * math.pi * 4)
        p.lineTo(px, py)
    cv.drawPath(p, stroke=1, fill=0)


def find_uniform_artist_size():
    longest_idx = max(range(len(SETLIST)), key=lambda i: len(SETLIST[i][0]))
    artist = SETLIST[longest_idx][0]
    max_w = CARD_W - 2 * MARGIN_H - BADGE_R * 2 - GAP
    lo, hi = 1, 200
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if pdfmetrics.stringWidth(artist, "BebasNeue", mid) <= max_w:
            lo = mid
        else:
            hi = mid - 1
    return lo


def draw_card_bg(cv, card_left, cy, bg):
    steps = 30
    dh = CARD_H / steps
    for i in range(steps):
        t = i / (steps - 1)
        lighten = 0.18 * (1 - t)
        r = min(1, bg.red + lighten)
        g = min(1, bg.green + lighten)
        b = min(1, bg.blue + lighten)
        cv.setFillColor(Color(r, g, b))
        cv.rect(card_left, cy - CARD_H / 2 + i * dh, CARD_W, dh + 0.5, stroke=0, fill=1)


def draw_cards(cv):
    uniform_size = find_uniform_artist_size()

    for idx, (artist, title) in enumerate(SETLIST):
        col = idx // 6
        row = idx % 6
        cx = COL_CENTERS[col]
        cy = ROWS_TOP - row * ROW_PITCH
        card_left = cx - CARD_W / 2
        bg = TEAL_PROFOND if idx in GREEN_INDICES else TERRACOTTA
        card_bottom = cy - CARD_H / 2

        cv.setFillColor(Color(0, 0, 0, alpha=SHADOW_ALPHA))
        cv.roundRect(card_left + SHADOW_OFFSET, card_bottom - SHADOW_OFFSET, CARD_W, CARD_H, CARD_R, stroke=0, fill=1)

        draw_card_bg(cv, card_left, cy, bg)

        cv.setStrokeColor(Color(1, 1, 1, alpha=0.5))
        cv.setLineWidth(0.5)
        cv.roundRect(card_left, card_bottom, CARD_W, CARD_H, CARD_R, stroke=1, fill=0)

        cv.setStrokeColor(OR_VIEILLI)
        cv.setLineWidth(0.8)
        cv.roundRect(card_left - 0.5, card_bottom - 0.5, CARD_W + 1, CARD_H + 1, CARD_R, stroke=1, fill=0)

        artist_width = pdfmetrics.stringWidth(artist, "BebasNeue", uniform_size)
        total_w = BADGE_R * 2 + GAP + artist_width
        start_x = cx - total_w / 2

        badge_cx = start_x + BADGE_R
        num_color = OR_VIEILLI if idx in GREEN_INDICES else ACCENT
        badge_cy = cy + BADGE_Y_OFFSET
        cv.setFillColor(BLANC)
        cv.circle(badge_cx, badge_cy, BADGE_R, stroke=0, fill=1)
        cv.setFillColor(num_color)
        cv.setFont("Montserrat", 12)
        cv.drawCentredString(badge_cx, badge_cy - 4.5, f"{idx+1:02d}")

        cv.setFillColor(BLANC)
        cv.setFont("BebasNeue", uniform_size)
        cv.drawString(start_x + BADGE_R * 2 + GAP, cy + ARTIST_BASELINE + 1, artist)

        if title:
            cv.setFillColor(Color(1, 1, 1, alpha=0.80))
            title_size = 14
            title_width = pdfmetrics.stringWidth(title, "Montserrat", title_size)
            max_title_w = CARD_W - 2 * MARGIN_H
            if title_width > max_title_w:
                title_size = title_size * max_title_w / title_width
            cv.setFont("Montserrat", title_size)
            cv.drawCentredString(cx, cy + TITLE_BASELINE, title)


def create_pdf():
    cv, _, _, bleed = create_bleed_canvas(OUTPUT, W, H)
    draw_gradient(cv)
    draw_grain(cv)
    draw_waves(cv)
    draw_logo(cv)
    draw_setlist_subtitle(cv)
    draw_cards(cv)
    cv.setFillColor(Color(1, 1, 1, alpha=0.18))
    cv.setFont("Montserrat", 7)
    text = "R O U E N"
    tracking = 3
    x = W / 2 - (sum(pdfmetrics.stringWidth(c, "Montserrat", 7) for c in text) + tracking * (len(text) - 1)) / 2
    for c in text:
        w = pdfmetrics.stringWidth(c, "Montserrat", 7)
        cv.drawString(x, 14, c)
        x += w + tracking
    save_with_crop_marks(cv, W, H, bleed)
    print(f"PDF généré : {OUTPUT}")


if __name__ == "__main__":
    create_pdf()
