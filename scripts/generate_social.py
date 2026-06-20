#!/usr/bin/env python3
"""Generate Rivers Rock social media templates (Instagram Post + Story)."""

import os
from PIL import Image, ImageDraw, ImageFont
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from logoutils import pillow_crest, BEBAS_PATH, MONTSERRAT_PATH

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "pdf", "templates")
os.makedirs(OUT_DIR, exist_ok=True)

BLEU_SEINE = (26, 58, 92)
VERT_EAU = (74, 155, 142)
ACCENT = (232, 93, 58)
VERT_REPERE = (45, 138, 110)
BLANC = (255, 255, 255)
GRIS = (200, 200, 200)


def lerp_color(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def draw_gradient_bg(draw, w, h, c1, c2):
    steps = 200
    dh = h / steps
    for i in range(steps):
        t = i / (steps - 1)
        color = lerp_color(c1, c2, t)
        draw.rectangle([0, i * dh, w, (i + 1) * dh], fill=color)


def draw_logo_horizontal(draw, font_bebas, base_x, base_y, sym_r, gap, text, size):
    font = ImageFont.truetype(BEBAS_PATH, size)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    total_w = sym_r * 2 + gap + text_w
    start_x = base_x - total_w / 2
    sym_cx = start_x + sym_r
    text_x = start_x + sym_r * 2 + gap
    text_y_offset = (bbox[3] - bbox[1]) * 0.35
    sym_cy = base_y + (bbox[3] - bbox[1]) / 2 - text_y_offset
    pillow_crest(draw, sym_cx, sym_cy, sym_r/25.0)
    return total_w


def generate_post():
    w, h = 1080, 1080
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    draw_gradient_bg(draw, w, h, BLEU_SEINE, VERT_EAU)

    font_bebas_large = ImageFont.truetype(BEBAS_PATH, 80)
    font_bebas_med = ImageFont.truetype(BEBAS_PATH, 52)
    font_mont = ImageFont.truetype(MONTSERRAT_PATH, 28)

    draw_logo_horizontal(draw, font_bebas_large, w / 2, 160, 34, 16, "RIVERS ROCK", 80)

    bbox = draw.textbbox((0, 0), "PROCHAIN CONCERT", font=font_mont)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 400), "PROCHAIN CONCERT", fill=ACCENT, font=font_mont)

    bbox = draw.textbbox((0, 0), "[DATE]", font=font_bebas_med)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 470), "[DATE]", fill=BLANC, font=font_bebas_med)

    bbox = draw.textbbox((0, 0), "[LIEU]", font=font_mont)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 550), "[LIEU]", fill=GRIS, font=font_mont)

    qr_x, qr_y, qr_s = w / 2 - 60, 680, 120
    draw.rounded_rectangle([qr_x, qr_y, qr_x + qr_s, qr_y + qr_s], radius=12, fill=BLANC, outline=ACCENT, width=3)
    bbox = draw.textbbox((0, 0), "QR", font=font_mont)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((qr_x + (qr_s - tw) / 2, qr_y + (qr_s - th) / 2), "QR", fill=BLEU_SEINE, font=font_mont)

    font_tag = ImageFont.truetype(MONTSERRAT_PATH, 18)
    tag = "@riversrock.rouen"
    bbox = draw.textbbox((0, 0), tag, font=font_tag)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 870), tag, fill=GRIS, font=font_tag)

    path = os.path.join(OUT_DIR, "instagram-post.png")
    img.save(path)
    print(f"Post généré : {path}")


def generate_story():
    w, h = 1080, 1920
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    draw_gradient_bg(draw, w, h, BLEU_SEINE, VERT_EAU)

    font_bebas_logo = ImageFont.truetype(BEBAS_PATH, 60)
    font_bebas_date = ImageFont.truetype(BEBAS_PATH, 140)
    font_mont = ImageFont.truetype(MONTSERRAT_PATH, 26)

    draw_logo_horizontal(draw, font_bebas_logo, w / 2, 200, 26, 12, "RIVERS ROCK", 60)

    date_text = "[DATE]"
    bbox = draw.textbbox((0, 0), date_text, font=font_bebas_date)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 650), date_text, fill=ACCENT, font=font_bebas_date)

    lieu_text = "[LIEU]"
    bbox = draw.textbbox((0, 0), lieu_text, font=font_mont)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 850), lieu_text, fill=BLANC, font=font_mont)

    tag = "@riversrock.rouen"
    bbox = draw.textbbox((0, 0), tag, font=font_mont)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 1750), tag, fill=GRIS, font=font_mont)

    path = os.path.join(OUT_DIR, "instagram-story.png")
    img.save(path)
    print(f"Story générée : {path}")


if __name__ == "__main__":
    generate_post()
    generate_story()
