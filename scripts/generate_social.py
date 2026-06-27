#!/usr/bin/env python3
"""Generate Rivers Rock social media templates — Rock Brut."""

import os
from PIL import Image, ImageDraw, ImageFont
import sys
sys.path.insert(0, os.path.dirname(__file__))
from logoutils import hexagon_logo_pillow, ANTON_PATH, pillow_grain_overlay, draw_qr_pillow
from palette import ACTIVE as CFG

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")
os.makedirs(OUT_DIR, exist_ok=True)

NOIR = (10, 10, 10)
ORANGE = (255, 59, 0)
BLANC = (255, 255, 255)
GRIS = (150, 150, 150)


def generate_post():
    w, h = 1080, 1080
    img = Image.new("RGB", (w, h), NOIR)
    draw = ImageDraw.Draw(img)

    hexagon_logo_pillow(draw, w / 2, 200, 60)

    font_anton = ImageFont.truetype(ANTON_PATH, 72)
    bbox = draw.textbbox((0, 0), "RIVERS ROCK", font=font_anton)
    draw.text(((w - (bbox[2] - bbox[0])) / 2, 380), "RIVERS ROCK", fill=BLANC, font=font_anton)

    font_sub = ImageFont.truetype(ANTON_PATH, 32)
    bbox2 = draw.textbbox((0, 0), "REPRISES ROCK — ROUEN", font=font_sub)
    draw.text(((w - (bbox2[2] - bbox2[0])) / 2, 480), "REPRISES ROCK — ROUEN", fill=ORANGE, font=font_sub)

    font_tag = ImageFont.truetype(ANTON_PATH, 18)
    tag = "@riversrock_rouen"
    bbox3 = draw.textbbox((0, 0), tag, font=font_tag)
    draw.text(((w - (bbox3[2] - bbox3[0])) / 2, 1000), tag, fill=GRIS, font=font_tag)

    img = pillow_grain_overlay(img, 0.10)
    path = os.path.join(OUT_DIR, "instagram-post.png")
    img.save(path)
    print(f"Post généré : {path}")


def generate_story():
    w, h = 1080, 1920
    img = Image.new("RGB", (w, h), NOIR)
    draw = ImageDraw.Draw(img)

    hexagon_logo_pillow(draw, w / 2, 300, 80)

    font_anton = ImageFont.truetype(ANTON_PATH, 96)
    bbox = draw.textbbox((0, 0), "RIVERS ROCK", font=font_anton)
    draw.text(((w - (bbox[2] - bbox[0])) / 2, 550), "RIVERS ROCK", fill=BLANC, font=font_anton)

    font_sub = ImageFont.truetype(ANTON_PATH, 40)
    bbox2 = draw.textbbox((0, 0), "REPRISES ROCK — ROUEN", font=font_sub)
    draw.text(((w - (bbox2[2] - bbox2[0])) / 2, 700), "REPRISES ROCK — ROUEN", fill=ORANGE, font=font_sub)

    font_tag = ImageFont.truetype(ANTON_PATH, 22)
    tag = "@riversrock_rouen"
    bbox3 = draw.textbbox((0, 0), tag, font=font_tag)
    draw.text(((w - (bbox3[2] - bbox3[0])) / 2, 1800), tag, fill=GRIS, font=font_tag)

    img = pillow_grain_overlay(img, 0.10)
    path = os.path.join(OUT_DIR, "instagram-story.png")
    img.save(path)
    print(f"Story générée : {path}")


if __name__ == "__main__":
    generate_post()
    generate_story()
