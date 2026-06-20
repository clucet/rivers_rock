#!/usr/bin/env python3
"""Generate Rivers Rock banners (Facebook + YouTube)."""

import os, math
from PIL import Image, ImageDraw, ImageFont
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from logoutils import pillow_crest, BEBAS_PATH_PATH, MONTSERRAT_PATH

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "pdf", "templates")
os.makedirs(OUT_DIR, exist_ok=True)

BLEU_SEINE = (26, 58, 92)
VERT_EAU = (74, 155, 142)
ACCENT = (232, 93, 58)
BLANC = (255, 255, 255)
GRIS = (200, 200, 200)


def lerp(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def gradient(draw, w, h, c1, c2, steps=120):
    dh = h / steps
    for i in range(steps):
        t = i / (steps - 1)
        draw.rectangle([0, i * dh, w, (i + 1) * dh], fill=lerp(c1, c2, t))


def wave(draw, w, h):
    for row in range(3):
        y = 5 + row * 20
        amp = 4 + row * 3
        period = 22 + row * 8
        segs = 200
        sw = w / segs
        pts = []
        for i in range(segs + 1):
            px = i * sw
            py = y + amp * math.sin(i * 2 * math.pi / period)
            pts.append((px, py))
        pts.append((w, 0))
        pts.append((0, 0))
        draw.polygon(pts, fill=(255, 255, 255, 18))


def make_banner(w, h, logo_size, sub_size, path):
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    gradient(draw, w, h, BLEU_SEINE, VERT_EAU)
    wave(draw, w, h)

    font_logo = ImageFont.truetype(BEBAS_PATH, logo_size)
    font_sub = ImageFont.truetype(MONTS, sub_size)

    sym_r = logo_size * 0.45
    bbox = draw.textbbox((0, 0), "RIVERS ROCK", font=font_logo)
    tw = bbox[2] - bbox[0]
    gap = sym_r * 0.4
    total_w = sym_r * 2 + gap + tw
    start_x = (w - total_w) / 2
    sym_cx = start_x + sym_r
    text_x = start_x + sym_r * 2 + gap
    text_y = h / 2 - (bbox[3] - bbox[1]) / 2
    sym_cy = text_y + (bbox[3] - bbox[1]) * 0.3

    pillow_crest(draw, sym_cx, sym_cy, sym_r/25.0)

    img.save(path)
    return path


fb = make_banner(1640, 624, 56, 14, os.path.join(OUT_DIR, "facebook-banner.png"))
yt = make_banner(2560, 1440, 86, 20, os.path.join(OUT_DIR, "youtube-banner.png"))
print(f"Bannière FB : {fb}\nBannière YT : {yt}")
