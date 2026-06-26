#!/usr/bin/env python3
"""Generate Rivers Rock business card (85x55mm, landscape, without QR)."""

import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from logoutils import create_bleed_canvas, save_with_crop_marks, reportlab_crest, BEBAS_PATH, MONTSERRAT_PATH
from logoutils import draw_gradient_pdf
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

OUTPUT = os.path.join(os.path.dirname(__file__), "..", "pdf", "business-card.pdf")

BLEU_SEINE = HexColor("#1A3A5C")
VERT_EAU = HexColor("#4A9B8E")
ACCENT = HexColor("#E85D3A")
BLANC = HexColor("#FFFFFF")

pdfmetrics.registerFont(TTFont("BebasNeue", BEBAS_PATH))
pdfmetrics.registerFont(TTFont("Montserrat", MONTSERRAT_PATH))

W = 85 * mm
H = 55 * mm


cv, W_card, H_card, bleed = create_bleed_canvas(OUTPUT, W, H)
draw_gradient_pdf(cv, W, H, BLEU_SEINE, VERT_EAU, steps=60)

reportlab_crest(cv, 24 * mm, H / 2 + 4, 0.45)
cv.setFillColor(BLANC)
cv.setFont("BebasNeue", 14)
cv.drawString(31 * mm, H - 16 * mm, "RIVERS ROCK")
cv.setFillColor(Color(1, 1, 1, alpha=0.5))
cv.setFont("Montserrat", 7)
cv.drawString(31 * mm, H - 20 * mm, "Reprises rock — Rouen")

cv.setFillColor(BLANC)
cv.setFont("Montserrat", 7)
contact_y = H - 31 * mm
cv.drawString(33 * mm, contact_y, "[Nom]")
cv.drawString(33 * mm, contact_y - 4 * mm, "[Téléphone]")
cv.drawString(33 * mm, contact_y - 8 * mm, "[Email]")

cv.setFillColor(Color(1, 1, 1, alpha=0.5))
cv.setFont("Montserrat", 7)
cv.drawRightString(W - 5 * mm, 6 * mm, "riversrock.fr")

save_with_crop_marks(cv, W, H, bleed)
print(f"Carte de visite : {OUTPUT}")
