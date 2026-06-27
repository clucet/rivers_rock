#!/usr/bin/env python3
"""Generate Rivers Rock avatar + monogramme RR — Rock Brut."""

import os
from PIL import Image, ImageDraw, ImageFont
import sys
sys.path.insert(0, os.path.dirname(__file__))
from logoutils import hexagon_logo_pillow, ANTON_PATH

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "pdf", "templates")
os.makedirs(OUT_DIR, exist_ok=True)

SIZE = 500
CX, CY = SIZE / 2, SIZE / 2


def gen_avatar():
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    hexagon_logo_pillow(draw, CX, CY, 100)

    # Add "RIVERS ROCK" below
    font = ImageFont.truetype(ANTON_PATH, 36)
    bbox = draw.textbbox((0, 0), "RIVERS ROCK", font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((SIZE - tw) / 2, CY + 100), "RIVERS ROCK", fill=(255, 255, 255), font=font)

    path = os.path.join(OUT_DIR, "avatar.png")
    img.save(path)
    print(f"Avatar généré : {path}")

    img2 = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw2 = ImageDraw.Draw(img2)
    hexagon_logo_pillow(draw2, CX, CY, 100)

    path2 = os.path.join(OUT_DIR, "monogramme-rr.png")
    img2.save(path2)
    print(f"Monogramme RR généré : {path2}")


if __name__ == "__main__":
    gen_avatar()
