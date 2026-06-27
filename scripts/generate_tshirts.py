#!/usr/bin/env python3
"""Generate Rivers Rock t-shirt print file (PDF) + mockup (PNG)."""

import os, math, sys
sys.path.insert(0, os.path.dirname(__file__))
from logoutils import create_bleed_canvas, save_with_crop_marks, hexagon_logo_reportlab, hexagon_logo_pillow, BEBAS_PATH, MONTSERRAT_PATH
from palette import ACTIVE as CFG
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "pdf")
TMPL_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(TMPL_DIR, exist_ok=True)

ACCENT = CFG.rl("accent")
BLANC = CFG.rl("blanc")

pdfmetrics.registerFont(TTFont("BebasNeue", BEBAS_PATH))
pdfmetrics.registerFont(TTFont("Montserrat", MONTSERRAT_PATH))


def draw_design(cv, cx, cy, sym_r, label=""):
    from logoutils import hexagon_logo_reportlab
    hexagon_logo_reportlab(cv, cx, cy, sym_r * 0.8)
    cv.setFillColor(BLANC)
    cv.setFont("Anton", max(10, int(sym_r * 1.6)))
    cv.drawCentredString(cx, cy + sym_r * 0.7 + 4, "RIVERS ROCK")
    if label:
        cv.setFillColor(Color(1, 1, 1, alpha=0.4))
        cv.setFont("Montserrat", 7)
        cv.drawCentredString(cx, cy + sym_r + 60, label)


def draw_crop_marks(cv, x, y, size=8):
    cv.setStrokeColor(Color(0, 0, 0, alpha=0.2))
    cv.setLineWidth(0.5)
    for dx, dy in [(x, y), (x + size, y), (x, y + size)]:
        pass
    cv.line(x - size, y, x + size, y)
    cv.line(x, y - size, x, y + size)


def generate_print():
    w, h = A4
    x_col1 = w / 4
    x_col2 = w * 3 / 4
    y_row1 = h - 200
    y_row2 = h - 440

    sizes = [
        ("S", 22 * mm, x_col1, y_row1),
        ("M", 28 * mm, x_col2, y_row1),
        ("L", 34 * mm, x_col1, y_row2),
        ("XL", 40 * mm, x_col2, y_row2),
    ]

    cv, _, _, bleed = create_bleed_canvas(os.path.join(OUT_DIR, "t-shirt-print.pdf"), A4[0], A4[1])

    cv.setFillColor(Color(0, 0, 0, alpha=0.04))
    cv.rect(0, 0, w, h, stroke=0, fill=1)

    draw_crop_marks(cv, 15, 15)
    draw_crop_marks(cv, w - 15, 15)
    draw_crop_marks(cv, 15, h - 15)
    draw_crop_marks(cv, w - 15, h - 15)

    for label, sym_r, cx, cy in sizes:
        draw_design(cv, cx, cy, sym_r, label=label)

    y_info = 20
    cv.setFillColor(Color(0, 0, 0, alpha=0.3))
    cv.setFont("Montserrat", 7)
    cv.drawString(10, y_info, "T-shirt noir — Design B (poitrine)")
    cv.drawString(10, y_info - 10, "Impression blanc + rouge #E85D3A")
    cv.drawString(10, y_info - 20, "Centrer à ~5 cm sous le col")

    save_with_crop_marks(cv, _, _, bleed)
    print(f"T-shirt print : {os.path.join(OUT_DIR, 't-shirt-print.pdf')}")


def generate_mockup():
    mw, mh = 1200, 1600
    img = Image.new("RGBA", (mw, mh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    NOIR = (20, 20, 22)
    GRIS_F = (35, 35, 38)
    BLANC_T = (255, 255, 255)
    ACCENT_T = (232, 93, 58)

    cx, cy = mw / 2, 400
    tw, th = 700, 820
    rx, ry = cx - tw / 2, cy - th / 2

    def rounded_rect(d, x, y, w, h, r, fill):
        d.rectangle([x + r, y, x + w - r, y + h], fill=fill)
        d.rectangle([x, y + r, x + w, y + h - r], fill=fill)
        d.pieslice([x, y, x + r * 2, y + r * 2], 180, 270, fill=fill)
        d.pieslice([x + w - r * 2, y, x + w, y + r * 2], 270, 360, fill=fill)
        d.pieslice([x, y + h - r * 2, x + r * 2, y + h], 90, 180, fill=fill)
        d.pieslice([x + w - r * 2, y + h - r * 2, x + w, y + h], 0, 90, fill=fill)

    rounded_rect(draw, rx, ry, tw, th, 60, NOIR)
    col_w = tw * 0.2
    enc_w = tw * 0.2
    for side in [-1, 1]:
        cx_e = cx + side * (tw * 0.36)
        y_e = ry + 30
        e_h = th * 0.65
        draw.rectangle([cx_e - enc_w / 2, y_e, cx_e + enc_w / 2, y_e + e_h], fill=NOIR)
        draw.ellipse([cx_e - enc_w / 2 - 5, y_e - 5, cx_e + enc_w / 2 + 5, y_e + 15], fill=NOIR)
        draw.ellipse([cx_e - enc_w / 2 - 5, y_e + e_h - 15, cx_e + enc_w / 2 + 5, y_e + e_h + 5], fill=NOIR)

    draw.ellipse([cx - 40, ry - 20, cx + 40, ry + 30], fill=GRIS_F)

    font_bebas = ImageFont.truetype(BEBAS_PATH, 120)
    font_bebas_sub = ImageFont.truetype(BEBAS_PATH, 72)
    font_mont = ImageFont.truetype(MONTSERRAT_PATH, 18)

    hexagon_logo_pillow(draw, mw / 2, cy - 20, 60)

    draw.text((30, mh - 30), "RIVERS ROCK — T-shirt design B", fill=(255, 255, 255, 80), font=font_mont)

    path = os.path.join(TMPL_DIR, "tshirt-mockup.png")
    img.save(path)
    print(f"Mockup : {path}")


if __name__ == "__main__":
    generate_print()
    generate_mockup()
