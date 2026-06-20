#!/usr/bin/env python3
"""Generate Rivers Rock email signature (600x200 PNG)."""

import os
from PIL import Image, ImageDraw, ImageFont
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from logoutils import pillow_crest

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "pdf", "templates")
OUTPUT = os.path.join(OUT_DIR, "email-signature.png")
os.makedirs(OUT_DIR, exist_ok=True)

BLEU_SEINE = (26, 58, 92)
VERT_EAU = (74, 155, 142)
ACCENT = (232, 93, 58)
BLANC = (255, 255, 255)
GRIS = (200, 200, 200)

BEBAS = os.path.expanduser("~/Library/Fonts/BebasNeue-Regular.ttf")
MONTS = os.path.expanduser("~/Library/Fonts/Montserrat-VariableFont_wght.ttf")

W, H = 600, 200


def lerp(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def gradient(draw, steps=80):
    dh = H / steps
    for i in range(steps):
        t = i / (steps - 1)
        draw.rectangle([0, i * dh, W, (i + 1) * dh], fill=lerp(BLEU_SEINE, VERT_EAU, t))


img = Image.new("RGB", (W, H))
draw = ImageDraw.Draw(img)
gradient(draw)

font_logo = ImageFont.truetype(BEBAS, 18)
font_name = ImageFont.truetype(MONTS, 11)
font_info = ImageFont.truetype(MONTS, 9)
font_link = ImageFont.truetype(MONTS, 8)

sym_r = 18
sym_cx = 35
sym_cy = 75
pillow_crest(draw, sym_cx, sym_cy, sym_r/25.0)
draw.text((62, 78), "[Nom]", fill=BLANC, font=font_name)
draw.text((62, 95), "[Téléphone]", fill=GRIS, font=font_info)
draw.text((62, 110), "[Email]", fill=GRIS, font=font_info)

link = "riversrock.fr/setlist"
bbox = draw.textbbox((0, 0), link, font=font_link)
draw.text(((W - (bbox[2] - bbox[0])) / 2, 168), link, fill=ACCENT, font=font_link)

draw.line([(0, 150), (W, 150)], fill=(255, 255, 255, 60), width=1)

img.save(OUTPUT)
print(f"Signature email : {OUTPUT}")
