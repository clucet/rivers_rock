#!/usr/bin/env python3
"""Generate Rivers Rock avatar (500x500 PNG, symbol only)."""

import os
from PIL import Image, ImageDraw
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from logoutils import pillow_crest

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "pdf", "templates")
os.makedirs(OUT_DIR, exist_ok=True)

ACCENT = (232, 93, 58)
BLANC = (255, 255, 255)
TRANS = (0, 0, 0, 0)

SIZE = 500
CX, CY = SIZE / 2, SIZE / 2
R = 180
WAVE_COLOR = ACCENT
STROKE_COLOR = BLANC
STROKE_W = 12
WAVE_W = 9


img = Image.new("RGBA", (SIZE, SIZE), TRANS)
draw = ImageDraw.Draw(img)
pillow_crest(draw, CX, CY, R/25.0)

path = os.path.join(OUT_DIR, "avatar.png")
img.save(path)
print(f"Avatar généré : {path}")
