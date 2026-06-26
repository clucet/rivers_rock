#!/usr/bin/env python3
"""Generate Rivers Rock A4 concert poster — Scène & Vintage."""

import os, sys, math, random
sys.path.insert(0, os.path.dirname(__file__))
from logoutils import reportlab_crest, BEBAS_PATH, MONTSERRAT_PATH, create_bleed_canvas, save_with_crop_marks
from logoutils import draw_gradient_pdf, draw_waves_pdf, draw_grain_pdf
from palette import ACTIVE as CFG
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import Color
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

OUTPUT = os.path.join(os.path.dirname(__file__), "..", "pdf", "poster-a4.pdf")

BLEU_SEINE = CFG.rl("bleu_seine")
TEAL_PROFOND = CFG.rl("teal_profond")
ACCENT = CFG.rl("accent")
OR_VIEILLI = CFG.rl("or_vieilli")
BLANC = CFG.rl("blanc")

pdfmetrics.registerFont(TTFont("BebasNeue", BEBAS_PATH))
pdfmetrics.registerFont(TTFont("Montserrat", MONTSERRAT_PATH))

W, H = int(A4[0]), int(A4[1])

# Bleed canvas uses the original float dimensions
_PW, _PH = A4[0], A4[1]


def draw_halftone(cv):
    cv.setFillColor(Color(1, 1, 1, alpha=0.04))
    for y in range(20, H - 20, 8):
        for x in range(20, W - 20, 8):
            d = min(x, W - x, y, H - y)
            if d < 100:
                r = random.uniform(0.5, 1.5)
                cv.circle(x, y, r, stroke=0, fill=1)


def draw_logo(cv):
    reportlab_crest(cv, W / 2, H - 190, 2.2)


def draw_wave_stroke(cv):
    """Decorative gold wave stroke at bottom of poster."""
    cv.setStrokeColor(OR_VIEILLI)
    cv.setLineWidth(1.5)
    segments = 200
    step_x = W / segments
    p = cv.beginPath()
    p.moveTo(0, H - 45)
    for i in range(segments + 1):
        px = i * step_x
        py = H - 45 + 8 * math.sin(i * 2 * math.pi / 32)
        p.lineTo(px, py)
    cv.drawPath(p, stroke=1, fill=0)


def draw_poster_info(cv):
    cv.setFillColor(OR_VIEILLI)
    cv.setFont("Montserrat", 12)
    cv.drawCentredString(W / 2, H - 270, "LES SOIREES NOCTURNES")

    cv.setFillColor(BLANC)
    cv.setFont("BebasNeue", 56)
    cv.drawCentredString(W / 2, H - 340, "VEN 26 JUIN 2026")

    cv.setFillColor(Color(1, 1, 1, alpha=0.7))
    cv.setFont("Montserrat", 18)
    cv.drawCentredString(W / 2, H - 385, "Montigny · 19h30")

    cv.setStrokeColor(OR_VIEILLI)
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

    cv.setFillColor(Color(1, 1, 1, alpha=0.5))
    cv.setFont("Montserrat", 7)
    text, tr = "R O U E N", 3
    x = W / 2 - (sum(pdfmetrics.stringWidth(c, "Montserrat", 7) for c in text) + tr * (len(text) - 1)) / 2
    for c in text:
        w = pdfmetrics.stringWidth(c, "Montserrat", 7)
        cv.drawString(x, 14, c)
        x += w + tr


def gen_poster():
    global cv
    cv, _, _, bleed = create_bleed_canvas(OUTPUT, _PW, _PH)
    draw_gradient_pdf(cv, W, H, BLEU_SEINE, TEAL_PROFOND)
    draw_grain_pdf(cv, W, H)
    draw_halftone(cv)
    draw_waves_pdf(cv, W, H)
    draw_wave_stroke(cv)
    draw_logo(cv)
    draw_poster_info(cv)
    save_with_crop_marks(cv, _PW, _PH, bleed)
    print(f"Affiche générée : {OUTPUT}")


if __name__ == "__main__":
    gen_poster()
