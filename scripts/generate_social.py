#!/usr/bin/env python3
"""Generate Rivers Rock social media templates — Scène & Vintage."""

import os, math
from PIL import Image, ImageDraw, ImageFont
import sys
sys.path.insert(0, os.path.dirname(__file__))
from logoutils import pillow_crest, BEBAS_PATH, MONTSERRAT_PATH, SPACE_MONO_PATH, ANTON_PATH, pillow_grain_overlay, draw_qr_pillow
from palette import ACTIVE as CFG

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "pdf", "templates")
os.makedirs(OUT_DIR, exist_ok=True)

BLEU_SEINE = CFG.pil("bleu_seine")
ACCENT = CFG.pil("accent")
OR = CFG.pil("or_vieilli")
TERRA = CFG.pil("terracotta")
TEAL = CFG.pil("teal_profond")
BLANC = (255, 255, 255)
GRIS = (200, 200, 200)


def lerp_color(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def draw_gradient_radial(draw, w, h, c_center, c_mid, c_edge):
    cx, cy = w / 2, h / 2
    max_r = math.sqrt(cx**2 + cy**2)
    steps = 300
    for i in range(steps):
        t = i / steps
        r = max_r * t
        if t < 0.3:
            color = lerp_color(c_center, c_mid, t / 0.3)
        else:
            color = lerp_color(c_mid, c_edge, (t - 0.3) / 0.7)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)


def draw_logo_glow(draw, cx, cy, scale=1.0):
    for r in range(int(8 * scale), 0, -1):
        glow_a = int(30 * (1 - r / (8 * scale)))
        glow = (OR[0], OR[1], OR[2], glow_a)
    pillow_crest(draw, cx, cy, scale)


def generate_post():
    w, h = 1080, 1080
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    draw_gradient_radial(draw, w, h, OR, TERRA, BLEU_SEINE)

    font_anton_date = ImageFont.truetype(ANTON_PATH, 64) if ANTON_PATH else ImageFont.truetype(BEBAS_PATH, 64)
    font_space = ImageFont.truetype(SPACE_MONO_PATH, 22) if SPACE_MONO_PATH else ImageFont.truetype(MONTSERRAT_PATH, 22)
    font_mont = ImageFont.truetype(MONTSERRAT_PATH, 24)
    font_tag = ImageFont.truetype(SPACE_MONO_PATH, 14) if SPACE_MONO_PATH else ImageFont.truetype(MONTSERRAT_PATH, 14)

    draw_logo_glow(draw, w / 2 - 100, 160, 1.4)
    bbox = draw.textbbox((0, 0), "RIVERS ROCK", font=font_space)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2 + 100, 150), "RIVERS ROCK", fill=BLANC, font=font_space)

    bbox = draw.textbbox((0, 0), "PROCHAIN CONCERT", font=font_space)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 400), "PROCHAIN CONCERT", fill=BLANC, font=font_space)

    bbox = draw.textbbox((0, 0), "VEN 26 JUIN 2026", font=font_anton_date)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 470), "VEN 26 JUIN 2026", fill=OR, font=font_anton_date)

    bbox = draw.textbbox((0, 0), "Montigny · 19h30", font=font_mont)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 560), "Montigny · 19h30", fill=BLANC, font=font_mont)

    qr_x, qr_y, qr_s = w / 2 - 60, 680, 120
    draw.rounded_rectangle([qr_x, qr_y, qr_x + qr_s, qr_y + qr_s], radius=12, fill=BLANC, outline=TERRA, width=3)
    qr_img = draw_qr_pillow(None, 0, 0, qr_s - 12, fill_color=BLEU_SEINE)
    if qr_img:
        img.paste(qr_img, (int(qr_x + 6), int(qr_y + 6)), qr_img if qr_img.mode == 'RGBA' else None)

    tag = "@riversrock.rouen"
    bbox = draw.textbbox((0, 0), tag, font=font_tag)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 870), tag, fill=BLANC, font=font_tag)

    img = pillow_grain_overlay(img, 0.04, seed=10)
    path = os.path.join(OUT_DIR, "instagram-post.png")
    img.save(path)
    print(f"Post généré : {path}")


def generate_story():
    w, h = 1080, 1920
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    draw_gradient_radial(draw, w, h, OR, ACCENT, TEAL)

    font_anton_date = ImageFont.truetype(ANTON_PATH, 120) if ANTON_PATH else ImageFont.truetype(BEBAS_PATH, 120)
    font_space = ImageFont.truetype(SPACE_MONO_PATH, 28) if SPACE_MONO_PATH else ImageFont.truetype(MONTSERRAT_PATH, 28)
    font_tag = ImageFont.truetype(SPACE_MONO_PATH, 18) if SPACE_MONO_PATH else ImageFont.truetype(MONTSERRAT_PATH, 18)

    from logoutils import pillow_crest_timbre
    pillow_crest_timbre(draw, 180, 200, 1.6)

    date_text = "VEN 26 JUIN 2026"
    bbox = draw.textbbox((0, 0), date_text, font=font_anton_date)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 650), date_text, fill=ACCENT, font=font_anton_date)

    lieu_text = "Montigny · 19h30"
    bbox = draw.textbbox((0, 0), lieu_text, font=font_space)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 850), lieu_text, fill=BLANC, font=font_space)

    tag = "@riversrock.rouen"
    bbox = draw.textbbox((0, 0), tag, font=font_tag)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 1750), tag, fill=BLANC, font=font_tag)

    img = pillow_grain_overlay(img, 0.04, seed=20)
    path = os.path.join(OUT_DIR, "instagram-story.png")
    img.save(path)
    print(f"Story générée : {path}")


if __name__ == "__main__":
    generate_post()
    generate_story()
