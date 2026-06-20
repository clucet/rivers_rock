#!/usr/bin/env python3
"""Generate Rivers Rock sticker sheet (6 x ∅80mm circles on A4)."""

import os, math
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from logoutils import BEBAS_PATH

OUTPUT = os.path.join(os.path.dirname(__file__), "..", "pdf", "stickers.pdf")

BLEU_SEINE = HexColor("#1A3A5C")
VERT_EAU = HexColor("#4A9B8E")
ACCENT = HexColor("#E85D3A")
BLANC = HexColor("#FFFFFF")

pdfmetrics.registerFont(TTFont("BebasNeue", BEBAS_PATH))

W, H = A4
STICKER_R = 40 * mm
MARGIN_X = (W - 2 * STICKER_R * 2) / 3
MARGIN_Y = (H - 3 * STICKER_R * 2) / 4

CENTERS = []
for col in range(2):
    for row in range(3):
        cx = MARGIN_X + STICKER_R + col * (MARGIN_X + STICKER_R * 2)
        cy = MARGIN_Y + STICKER_R + row * (MARGIN_Y + STICKER_R * 2)
        CENTERS.append((cx, cy))


def draw_gradient_in_circle(cv, cx, cy, r):
    steps = 60
    dh = r * 2 / steps
    for i in range(steps):
        t = i / (steps - 1)
        rcol = BLEU_SEINE.red + (VERT_EAU.red - BLEU_SEINE.red) * t
        gcol = BLEU_SEINE.green + (VERT_EAU.green - BLEU_SEINE.green) * t
        bcol = BLEU_SEINE.blue + (VERT_EAU.blue - BLEU_SEINE.blue) * t
        cv.setFillColor(Color(rcol, gcol, bcol))
        y = cy - r + i * dh
        cv.rect(cx - r, y, r * 2, dh + 0.5, stroke=0, fill=1)
    cv.setStrokeColor(BLANC)
    cv.setLineWidth(2)
    cv.circle(cx, cy, r, stroke=1, fill=0)


def draw_symbol(cv, cx, cy, r):
    cv.setStrokeColor(BLANC)
    cv.setLineWidth(2)
    cv.circle(cx, cy, r, stroke=1, fill=0)
    cv.setStrokeColor(ACCENT)
    cv.setLineWidth(1.5)
    margin = r * 0.08
    segs = 30
    p = cv.beginPath()
    p.moveTo(cx - r + margin, cy)
    for i in range(segs + 1):
        t = i / segs
        px = cx - r + margin + t * (r * 2 - margin * 2)
        py = cy + r * 0.06 * math.sin(t * 2 * math.pi * 2.5)
        p.lineTo(px, py)
    cv.drawPath(p, stroke=1, fill=0)


def draw_crop_marks(cv, cx, cy, r):
    ext = 4
    cv.setStrokeColor(Color(0, 0, 0, alpha=0.3))
    cv.setLineWidth(0.5)
    d = r * 1.05
    for dx, dy in [(-d, 0), (d, 0), (0, -d), (0, d)]:
        cv.line(cx + dx - ext * (1 if dx > 0 else -1), cy + dy,
                cx + dx + ext * (1 if dx > 0 else -1), cy + dy)
        cv.line(cx + dx, cy + dy - ext * (1 if dy > 0 else -1),
                cx + dx, cy + dy + ext * (1 if dy > 0 else -1))


cv = canvas.Canvas(OUTPUT, pagesize=A4)

for i, (cx, cy) in enumerate(CENTERS):
    draw_gradient_in_circle(cv, cx, cy, STICKER_R)
    sym_r = STICKER_R * 0.55
    draw_symbol(cv, cx, cy, sym_r)
    draw_crop_marks(cv, cx, cy, STICKER_R)

    cv.setFillColor(BLANC)
    cv.setFont("BebasNeue", 12)
    cv.drawCentredString(cx, cy - STICKER_R - 10, f"Sticker {i + 1}")

cv.save()
print(f"Stickers : {OUTPUT}")
