#!/usr/bin/env python3
"""Generate Rivers Rock banners — Rock Brut (Facebook + YouTube)."""

import os
from PIL import Image, ImageDraw, ImageFont
import sys
sys.path.insert(0, os.path.dirname(__file__))
from logoutils import hexagon_logo_pillow, ANTON_PATH, pillow_grain_overlay

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")
os.makedirs(OUT_DIR, exist_ok=True)

NOIR = (10, 10, 10)
ORANGE = (255, 59, 0)
BLANC = (255, 255, 255)
GRIS = (150, 150, 150)


def make_banner(w, h, logo_size, sub_size, path):
    img = Image.new("RGBA", (w, h), NOIR)
    draw = ImageDraw.Draw(img)

    font_logo = ImageFont.truetype(ANTON_PATH, logo_size)
    font_sub = ImageFont.truetype(ANTON_PATH, sub_size)

    hexagon_logo_pillow(draw, w / 2, h / 2 - 20, logo_size * 0.5)

    bbox = draw.textbbox((0, 0), "RIVERS ROCK", font=font_logo)
    draw.text(((w - (bbox[2] - bbox[0])) / 2, h / 2 + 40), "RIVERS ROCK", fill=BLANC, font=font_logo)

    sub = "Reprises rock — Rouen"
    bbox2 = draw.textbbox((0, 0), sub, font=font_sub)
    draw.text(((w - (bbox2[2] - bbox2[0])) / 2, h - 60), sub, fill=ORANGE, font=font_sub)

    img_rgb = img.convert("RGB")
    grain = pillow_grain_overlay(img_rgb, 0.10, seed=30)
    grain.save(path)
    return path


def gen_banners():
    fb = make_banner(1640, 624, 72, 20, os.path.join(OUT_DIR, "facebook-banner.png"))
    yt = make_banner(2560, 1440, 120, 32, os.path.join(OUT_DIR, "youtube-banner.png"))
    print(f"Bannière FB : {fb}\nBannière YT : {yt}")


if __name__ == "__main__":
    gen_banners()
