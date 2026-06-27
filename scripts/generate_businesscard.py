#!/usr/bin/env python3
"""Generate Rivers Rock business card (85x55mm, landscape) — Rock Brut."""

import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from logoutils import create_bleed_canvas, save_with_crop_marks, hexagon_logo_reportlab, ANTON_PATH
from palette import ACTIVE, CONFIG_NAMES
from reportlab.lib.units import mm
from reportlab.lib.colors import Color, HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Determine output path from active config
_active_name = ACTIVE.name.lower().replace(" ", "-").replace("é", "e")
_prop_dir = CONFIG_NAMES.get(_active_name, "02-rock-brut")
OUTPUT = os.path.join(os.path.dirname(__file__), "..", "propositions", _prop_dir, "assets", "pdf", "business-card.pdf")

NOIR = HexColor("#0A0A0A")
ORANGE = HexColor("#FF3B00")
BLANC = HexColor("#FFFFFF")
GRIS = Color(0.5, 0.5, 0.5)

pdfmetrics.registerFont(TTFont("Anton", ANTON_PATH))

W = 85 * mm
H = 55 * mm

cv, W_card, H_card, bleed = create_bleed_canvas(OUTPUT, W, H)

# Fond noir mat
cv.setFillColor(NOIR)
cv.rect(0, 0, W, H, stroke=0, fill=1)

# Logo hexagone
hexagon_logo_reportlab(cv, 20 * mm, H / 2 + 2, 14)

cv.setFillColor(BLANC)
cv.setFont("Anton", 12)
cv.drawString(30 * mm, H - 16 * mm, "RIVERS ROCK")

cv.setFillColor(Color(1, 1, 1, alpha=0.4))
cv.setFont("Anton", 7)
cv.drawString(30 * mm, H - 20.5 * mm, "Reprises rock — Rouen")

cv.setFillColor(BLANC)
cv.setFont("Anton", 7)
cv.drawString(30 * mm, H - 32 * mm, "riversrock_rouen@gmail.com")

cv.setFillColor(ORANGE)
cv.setFont("Anton", 6)
cv.drawRightString(W - 5 * mm, 6 * mm, "riversrock.fr")

save_with_crop_marks(cv, W, H, bleed)
print(f"Carte de visite : {OUTPUT}")
