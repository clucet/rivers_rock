#!/usr/bin/env python3
"""Generate Rivers Rock banners — Scène & Vintage (Facebook + YouTube)."""

import os, math
from PIL import Image, ImageDraw, ImageFont
import sys
sys.path.insert(0, os.path.dirname(__file__))
from logoutils import pillow_crest, BEBAS_PATH, MONTSERRAT_PATH, ANTON_PATH, pillow_grain_overlay
from palette import ACTIVE as CFG

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "pdf", "templates")
os.makedirs(OUT_DIR, exist_ok=True)

BLEU_SEINE = CFG.pil("bleu_seine")
TEAL = CFG.pil("teal_profond")
ACCENT = CFG.pil("accent")
OR = CFG.pil("or_vieilli")
BLANC = (255, 255, 255)


def lerp(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def gradient_duotone(draw, w, h):
    steps = 120
    dh = h / steps
    for i in range(steps):
        t = i / (steps - 1)
        draw.rectangle([0, i * dh, w, (i + 1) * dh], fill=lerp(BLEU_SEINE, TEAL, t))


def wave_gold(draw, w, h):
    for row in range(2):
        y = 5 + row * 20
        amp = 4 + row * 3
        period = 22 + row * 8
        segs = 200
        pts = []
        for i in range(segs + 1):
            px = i * w / segs
            py = y + amp * math.sin(i * 2 * math.pi / period)
            pts.append((px, py))
        pts.append((w, 0))
        pts.append((0, 0))
        color = (OR[0], OR[1], OR[2], 12)
        draw.polygon(pts, fill=color)


def flare(draw, w, h):
    cx, cy = w / 2, h / 2
    max_r = math.sqrt(cx**2 + cy**2)
    steps = 100
    for i in range(steps):
        t = i / steps
        r = max_r * t
        a = int(60 * (1 - t))
        color = (OR[0], OR[1], OR[2], max(0, a))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)


def make_banner(w, h, logo_size, sub_size, path):
    img = Image.new("RGBA", (w, h))
    draw = ImageDraw.Draw(img)
    gradient_duotone(draw, w, h)
    wave_gold(draw, w, h)
    flare(draw, w, h)

    font_logo = ImageFont.truetype(ANTON_PATH, logo_size) if ANTON_PATH else ImageFont.truetype(BEBAS_PATH, logo_size)
    font_sub = ImageFont.truetype(MONTSERRAT_PATH, sub_size)

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
    draw.text((text_x, text_y), "RIVERS ROCK", fill=BLANC, font=font_logo)

    sub = "Reprises rock — Rouen"
    bbox2 = draw.textbbox((0, 0), sub, font=font_sub)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((w - tw2) / 2, h - 60), sub, fill=BLANC, font=font_sub)

    img_rgb = img.convert("RGB")
    grain = pillow_grain_overlay(img_rgb, 0.04, seed=30)
    grain.save(path)
    return path


def gen_banners():
    fb = make_banner(1640, 624, 48, 14, os.path.join(OUT_DIR, "facebook-banner.png"))
    yt = make_banner(2560, 1440, 72, 20, os.path.join(OUT_DIR, "youtube-banner.png"))
    print(f"Bannière FB : {fb}\nBannière YT : {yt}")


if __name__ == "__main__":
    gen_banners()
