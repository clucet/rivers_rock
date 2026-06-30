#!/usr/bin/env python3
"""Generate Rivers Rock avatar + monogramme RR — Rock Brut."""

import os
from PIL import Image, ImageDraw, ImageFont
import sys
sys.path.insert(0, os.path.dirname(__file__))
from logoutils import hexagon_logo_pillow, ANTON_PATH

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")
os.makedirs(OUT_DIR, exist_ok=True)

SIZE = 500
CX, CY = SIZE / 2, SIZE / 2


def gen_avatar():
    # Version fond noir opaque (YouTube, reseaux)
    img = Image.new("RGB", (SIZE, SIZE), (10, 10, 10))
    draw = ImageDraw.Draw(img)
    hexagon_logo_pillow(draw, CX, CY, 100)
    path = os.path.join(OUT_DIR, "avatar.png")
    img.save(path)
    print(f"Avatar généré : {path}")

    # Version fond transparent (superposition, watermark)
    img_t = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw_t = ImageDraw.Draw(img_t)
    hexagon_logo_pillow(draw_t, CX, CY, 100)
    path_t = os.path.join(OUT_DIR, "avatar-transparent.png")
    img_t.save(path_t)
    print(f"Avatar transparent généré : {path_t}")

    img2 = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw2 = ImageDraw.Draw(img2)
    hexagon_logo_pillow(draw2, CX, CY, 100)
    path2 = os.path.join(OUT_DIR, "monogramme-rr.png")
    img2.save(path2)
    print(f"Monogramme RR généré : {path2}")


if __name__ == "__main__":
    gen_avatar()
