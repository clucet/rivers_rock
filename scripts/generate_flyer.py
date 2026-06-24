#!/usr/bin/env python3
"""Generate Rivers Rock flyer A6 — Scène & Vintage."""

import os, math, sys
sys.path.insert(0, os.path.dirname(__file__))
from logoutils import create_bleed_canvas, save_with_crop_marks, reportlab_crest, BEBAS_PATH, MONTSERRAT_PATH, draw_qr_reportlab
from palette import ACTIVE as CFG
from reportlab.lib.pagesizes import A4, A6
from reportlab.lib.colors import Color
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

OUTPUT = os.path.join(os.path.dirname(__file__), "..", "pdf", "flyer-a6.pdf")

BLEU_SEINE = CFG.rl("bleu_seine")
TEAL_PROFOND = CFG.rl("teal_profond")
ACCENT = CFG.rl("accent")
OR_VIEILLI = CFG.rl("or_vieilli")
BLANC = CFG.rl("blanc")

pdfmetrics.registerFont(TTFont("BebasNeue", BEBAS_PATH))
pdfmetrics.registerFont(TTFont("Montserrat", MONTSERRAT_PATH))

FW, FH = A6
COLS = 2
ROWS = 2


def gradient(cv, x, y, w, h, c1, c2, steps=60):
    dh = h / steps
    for i in range(steps):
        t = i / (steps - 1)
        r = c1.red + (c2.red - c1.red) * t
        g = c1.green + (c2.green - c1.green) * t
        b = c1.blue + (c2.blue - c1.blue) * t
        cv.setFillColor(Color(r, g, b))
        cv.rect(x, y + i * dh, w, dh + 0.5, stroke=0, fill=1)


def wave_or(cv, x, y, w, h):
    cv.setFillColor(OR_VIEILLI)
    for row in range(2):
        by = y + 8 + row * 18
        amp = 4 + row * 3
        period = 20 + row * 8
        segs = 80
        sw = w / segs
        p = cv.beginPath()
        p.moveTo(x, by)
        for i in range(segs + 1):
            px = x + i * sw
            py = by + amp * math.sin(i * 2 * math.pi / period)
            p.lineTo(px, py)
        p.lineTo(x + w, y)
        p.lineTo(x, y)
        p.close()
        cv.drawPath(p, fill=1, stroke=0)


def draw_recto(cv, ox, oy):
    gradient(cv, ox, oy, FW, FH, BLEU_SEINE, TEAL_PROFOND)
    wave_or(cv, ox, oy, FW, FH)

    cx = ox + FW / 2
    reportlab_crest(cv, cx, oy + FH - 55, 1.0)
    cv.setFillColor(BLANC)
    cv.setFont("BebasNeue", 28)
    cv.drawCentredString(cx, oy + FH - 110, "RIVERS ROCK")

    cv.setFillColor(OR_VIEILLI)
    cv.setFont("BebasNeue", 34)
    cv.drawCentredString(cx, oy + FH - 170, "[DATE]")

    cv.setFillColor(Color(1, 1, 1, alpha=0.7))
    cv.setFont("Montserrat", 10)
    cv.drawCentredString(cx, oy + FH - 200, "[LIEU]")

    cv.setFillColor(Color(1, 1, 1, alpha=0.3))
    cv.setFont("Montserrat", 7)
    cv.drawCentredString(cx, oy + 14, "RIVERS ROCK — Reprises rock — Rouen")


def draw_verso(cv, ox, oy):
    gradient(cv, ox, oy, FW, FH, BLEU_SEINE, TEAL_PROFOND)
    wave_or(cv, ox, oy, FW, FH)

    cx = ox + FW / 2

    cv.setFillColor(BLANC)
    cv.setFont("BebasNeue", 22)
    cv.drawCentredString(cx, oy + FH - 40, "RIVERS ROCK")

    bio = [
        "Groupe rouennais formé en 2024",
        "au centre Éducation et Formation",
        "du Petit-Quevilly.",
        "",
        "Rosaria — batterie",
        "Christophe — basse",
        "Nicolas — guitare",
        "David — guitare / chant",
        "Virginie — chant",
        "",
        "Rock — Pop-Rock — Indé — Alternatif",
    ]

    cv.setFillColor(Color(1, 1, 1, alpha=0.75))
    cv.setFont("Montserrat", 7)
    y = oy + FH - 80
    for line in bio:
        cv.drawCentredString(cx, y, line)
        y -= 12

    cv.setFillColor(ACCENT)
    cv.setFont("Montserrat", 7)
    cv.drawCentredString(cx, y - 6, "Contactez-nous pour programmer un concert")

    qr_size = 30
    qr_x = cx - qr_size / 2
    qr_y = y - 58
    cv.setFillColor(BLANC)
    cv.roundRect(qr_x, qr_y, qr_size, qr_size, 4, stroke=0, fill=1)
    draw_qr_reportlab(cv, cx, qr_y + qr_size / 2, qr_size - 4, fill_color=BLEU_SEINE)

    cv.setFillColor(Color(1, 1, 1, alpha=0.4))
    cv.setFont("Montserrat", 7)
    cv.drawCentredString(cx, qr_y - 8, "@riversrock.rouen — riversrock.fr")

    cv.setFillColor(Color(1, 1, 1, alpha=0.25))
    cv.setFont("Montserrat", 7)
    cv.drawCentredString(cx, oy + 10, "RIVERS ROCK")


def gen_flyer():
    global cv
    cv = canvas.Canvas(OUTPUT, pagesize=A4)

    for page in range(2):
        for row in range(ROWS):
            for col in range(COLS):
                ox = col * FW
                oy = (ROWS - 1 - row) * FH
                if page == 0:
                    draw_recto(cv, ox, oy)
                else:
                    draw_verso(cv, ox, oy)
        if page == 0:
            cv.showPage()

    cv.save()
    print(f"Flyer généré : {OUTPUT}")


if __name__ == "__main__":
    gen_flyer()
