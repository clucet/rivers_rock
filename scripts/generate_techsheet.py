#!/usr/bin/env python3
"""Generate Rivers Rock t-shirt technical sheet for screen printer."""

import os, math, sys
sys.path.insert(0, os.path.dirname(__file__))
from logoutils import BEBAS_PATH, MONTSERRAT_PATH
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

OUTPUT = os.path.join(os.path.dirname(__file__), "..", "pdf", "t-shirt-techsheet.pdf")

BLEU_SEINE = HexColor("#1A3A5C")
VERT_EAU = HexColor("#4A9B8E")
ACCENT = HexColor("#E85D3A")
BLANC = HexColor("#FFFFFF")

pdfmetrics.registerFont(TTFont("BebasNeue", BEBAS_PATH))
pdfmetrics.registerFont(TTFont("Montserrat", MONTSERRAT_PATH))

W, H = A4


def draw_symbol(cv, cx, cy, r):
    cv.setStrokeColor(HexColor("#333333"))
    cv.setLineWidth(max(1.5, r * 0.12))
    cv.circle(cx, cy, r, stroke=1, fill=0)
    cv.setStrokeColor(ACCENT)
    cv.setLineWidth(max(1, r * 0.1))
    margin = r * 0.1
    segs = 30
    p = cv.beginPath()
    p.moveTo(cx - r + margin, cy)
    for i in range(segs + 1):
        t = i / segs
        px = cx - r + margin + t * (r * 2 - margin * 2)
        py = cy + r * 0.08 * math.sin(t * 2 * math.pi * 2.5)
        p.lineTo(px, py)
    cv.drawPath(p, stroke=1, fill=0)
    cv.setFillColor(HexColor("#333333"))
    cv.setFont("Montserrat", 7)
    cv.drawCentredString(cx, cy + r + 8, f"∅{r*2/10:.0f} mm")


cv = canvas.Canvas(OUTPUT, pagesize=A4)
cv.setFillColor(Color(0.95, 0.95, 0.93))
cv.rect(0, 0, W, H, stroke=0, fill=1)

cv.setFillColor(HexColor("#222222"))
cv.setFont("BebasNeue", 28)
cv.drawCentredString(W / 2, H - 60, "FICHE TECHNIQUE — T-SHIRT")

cv.setStrokeColor(HexColor("#222222"))
cv.setLineWidth(1)
cv.line(W / 2 - 100, H - 72, W / 2 + 100, H - 72)

cv.setFont("Montserrat", 8)
cv.drawString(30, H - 110, "Design : B (poitrine)")
cv.drawString(30, H - 125, "T-shirt : noir")
cv.drawString(30, H - 140, "Encres : blanc + rouge #E85D3A (≈ Pantone 172)")
cv.drawString(30, H - 155, "Méthode : sérigraphie / flocage")
cv.drawString(30, H - 170, "Placement : centré, ~5 cm sous le col")

cv.setFont("Montserrat", 9)
cv.drawString(30, H - 200, "Tailles :")

sizes = [
    ("S", 22 * mm, 190, 46),
    ("M", 28 * mm, 240, 52),
    ("L", 34 * mm, 290, 58),
    ("XL", 40 * mm, 340, 64),
]

y_table = H - 230
cv.setFont("Montserrat", 7)
cv.setStrokeColor(HexColor("#222222"))
cv.setLineWidth(0.5)
cols_x = [30, 90, 160, 240, 330]
headers = ["Taille", "∅ symbole", "∅ texte", "H. totale", "Dist. col"]
for i, h in enumerate(headers):
    cv.drawString(cols_x[i], y_table, h)
cv.line(25, y_table - 3, 380, y_table - 3)

for row, (label, sym_r, total_h, dist_col) in enumerate(sizes):
    ry = y_table - 14 - row * 14
    cv.drawString(cols_x[0], ry, label)
    cv.drawString(cols_x[1], ry, f"{sym_r * 2 / mm:.0f} mm")
    cv.drawString(cols_x[2], ry, f"{sym_r * 1.4 / mm:.0f} mm")
    cv.drawString(cols_x[3], ry, f"{total_h / mm:.0f} mm")
    cv.drawString(cols_x[4], ry, f"{dist_col / mm:.0f} mm")

y_design = H - 390
cx_design = W / 2

for label, sym_r, cx, cy in sizes:
    draw_symbol(cv, cx_design, y_design + sym_r + 10, sym_r)
    cv.setFillColor(HexColor("#333333"))
    cv.setFont("BebasNeue", max(10, int(sym_r * 0.35)))
    cv.drawCentredString(cx_design, y_design - 2, "RIVERS")
    cv.setFont("BebasNeue", max(8, int(sym_r * 0.3)))
    cv.drawCentredString(cx_design, y_design - 16, "ROCK")
    cv.setFillColor(Color(0, 0, 0, alpha=0.3))
    cv.setFont("Montserrat", 7)
    cv.drawCentredString(cx_design, y_design - 30, label)
    y_design += 90

cv.drawString(30, 30, "RIVERS ROCK — riversrock.fr — @riversrock.rouen")

cv.save()
print(f"Fiche technique : {OUTPUT}")
