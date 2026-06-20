#!/usr/bin/env python3
"""Generate Rivers Rock A4 concert poster (no setlist)."""

import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from logoutils import reportlab_crest, BEBAS_PATH, MONTSERRAT_PATH
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

OUTPUT = os.path.join(os.path.dirname(__file__), "..", "pdf", "poster-a4.pdf")

BLEU_SEINE = HexColor("#1A3A5C")
VERT_EAU = HexColor("#4A9B8E")
ACCENT = HexColor("#E85D3A")
BLANC = HexColor("#FFFFFF")

pdfmetrics.registerFont(TTFont("BebasNeue", BEBAS_PATH))
pdfmetrics.registerFont(TTFont("Montserrat", MONTSERRAT_PATH))

W, H = A4


def draw_gradient(cv):
    steps = 120
    dh = H / steps
    for i in range(steps):
        t = i / (steps - 1)
        r = BLEU_SEINE.red + (VERT_EAU.red - BLEU_SEINE.red) * t
        g = BLEU_SEINE.green + (VERT_EAU.green - BLEU_SEINE.green) * t
        b = BLEU_SEINE.blue + (VERT_EAU.blue - BLEU_SEINE.blue) * t
        cv.setFillColor(Color(r, g, b))
        cv.rect(0, i * dh, W, dh + 1, stroke=0, fill=1)


def draw_logo(cv):
    reportlab_crest(cv, W / 2, H - 190, 2.2)


def draw_waves(cv):
    cv.setFillColor(Color(1, 1, 1, alpha=0.07))
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
    cv.setStrokeColor(Color(1, 1, 1, alpha=0.1))
    cv.setLineWidth(2)
    segments = 300
    step_x = W / segments
    p = cv.beginPath()
    p.moveTo(0, H - 45)
    for i in range(segments + 1):
        px = i * step_x
        py = H - 45 + 10 * math.sin(i * 2 * math.pi / 36)
        p.lineTo(px, py)
    cv.drawPath(p, stroke=1, fill=0)


def draw_poster_info(cv):
    cv.setFillColor(ACCENT)
    cv.setFont("Montserrat", 12)
    cv.drawCentredString(W / 2, H - 270, "PROCHAIN CONCERT")

    cv.setFillColor(BLANC)
    cv.setFont("BebasNeue", 48)
    cv.drawCentredString(W / 2, H - 340, "[DATE]")

    cv.setFillColor(Color(1, 1, 1, alpha=0.7))
    cv.setFont("Montserrat", 16)
    cv.drawCentredString(W / 2, H - 380, "[LIEU]")

    cv.setStrokeColor(Color(1, 1, 1, alpha=0.2))
    cv.setLineWidth(1.5)
    wave_len = 160
    wave_x0 = W / 2 - wave_len / 2
    wave_y = H - 410
    segs = 30
    p = cv.beginPath()
    p.moveTo(wave_x0, wave_y)
    for i in range(segs + 1):
        t = i / segs
        px = wave_x0 + t * wave_len
        py = wave_y + 3.5 * math.sin(t * 2 * math.pi * 4)
        p.lineTo(px, py)
    cv.drawPath(p, stroke=1, fill=0)

    cv.setFillColor(BLANC)
    cv.setFont("Montserrat", 7)
    text = "R O U E N"
    tracking = 3
    x = W / 2 - (sum(pdfmetrics.stringWidth(c, "Montserrat", 7) for c in text) + tracking * (len(text) - 1)) / 2
    for c in text:
        w = pdfmetrics.stringWidth(c, "Montserrat", 7)
        cv.drawString(x, 14, c)
        x += w + tracking


cv = canvas.Canvas(OUTPUT, pagesize=(W, H))
draw_gradient(cv)
draw_waves(cv)
draw_logo(cv)
draw_poster_info(cv)
cv.save()
print(f"Affiche générée : {OUTPUT}")
