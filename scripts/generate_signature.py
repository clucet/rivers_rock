#!/usr/bin/env python3
"""Generate Rivers Rock email signature — Rock Brut."""

import os
from PIL import Image, ImageDraw, ImageFont
import sys
sys.path.insert(0, os.path.dirname(__file__))
from logoutils import hexagon_logo_pillow, ANTON_PATH

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")
OUTPUT = os.path.join(OUT_DIR, "email-signature.png")
os.makedirs(OUT_DIR, exist_ok=True)

ORANGE = (255, 59, 0)
BLANC = (255, 255, 255)
GRIS = (150, 150, 150)
NOIR = (10, 10, 10)

W, H = 600, 200


def gen_signature():
    img = Image.new("RGB", (W, H), NOIR)
    draw = ImageDraw.Draw(img)

    font_logo = ImageFont.truetype(ANTON_PATH, 20)
    font_name = ImageFont.truetype(ANTON_PATH, 12)
    font_text = ImageFont.truetype(ANTON_PATH, 10)

    hexagon_logo_pillow(draw, 40, 75, 28)
    draw.text((68, 62), "[Nom]", fill=BLANC, font=font_name)
    draw.text((68, 80), "[Téléphone]", fill=GRIS, font=font_text)
    draw.text((68, 96), "[Email]", fill=GRIS, font=font_text)

    draw.text((20, 166), "RIVERS ROCK", fill=ORANGE, font=font_text)

    img.save(OUTPUT)
    print(f"Signature email : {OUTPUT}")


if __name__ == "__main__":
    gen_signature()
