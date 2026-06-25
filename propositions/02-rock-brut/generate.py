#!/usr/bin/env python3
"""Generate all Rock Brut assets — Proposition n°2 (refonte identitaire)."""

import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))
from logoutils import (
    create_bleed_canvas, save_with_crop_marks,
    draw_qr_pillow,
    pillow_hexagon_monogramme,
    pillow_crest, pillow_grain_overlay,
    BEBAS_PATH, ANTON_PATH, INTERTIGHT_PATH, JETBRAINS_PATH,
)
from palette import ROCK_BRUT as CFG
from reportlab.lib.pagesizes import A4, A6
from reportlab.lib.colors import Color
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(__file__), "assets")
PDF = os.path.join(OUT, "pdf")
TMPL = os.path.join(OUT, "templates")
for d in (OUT, PDF, TMPL):
    os.makedirs(d, exist_ok=True)

NOIR = CFG.rl("noir")
ACCENT = CFG.rl("accent")
BLANC = CFG.rl("blanc")
VERT = CFG.rl("vert_accent")
FONCE = CFG.rl("gris_fonce")
GRIS_ACIER = CFG.rl("gris_acier")

NOIR_PIL = CFG.pil("noir")
ACCENT_PIL = CFG.pil("accent")
BLANC_PIL = (255, 255, 255)
VERT_PIL = CFG.pil("vert_accent")
FONCE_PIL = CFG.pil("gris_fonce")

pdfmetrics.registerFont(TTFont("Anton", ANTON_PATH))
pdfmetrics.registerFont(TTFont("InterTight", INTERTIGHT_PATH))
pdfmetrics.registerFont(TTFont("JetBrainsMono", JETBRAINS_PATH))

SETLIST = [
    ("NIAGARA", "J'ai vu"),
    ("AC/DC", "You shook me all night long"),
    ("DOLLY", "Je n'veux pas rester sage"),
    ("THE PIXIES", "Where is my mind"),
    ("PJ HARVEY", "Good fortune"),
    ("BELLA CIAO", ""),
    ("SMASHING PUMPKINS", "Today"),
    ("RADIOHEAD", "Creep"),
    ("DESIRELESS", "Voyage, voyage"),
    ("QUEEN", "We will rock you"),
    ("ROLLING STONES", "Jumping jack flash"),
    ("WHITE STRIPES", "Seven nation army"),
]
GREEN_INDICES = {0, 3, 6}


def hexagon_logo_reportlab(cv, cx, cy, size):
    """Draw hexagon + RR text for Rock Brut."""
    r = size
    pts = []
    for i in range(6):
        a = math.radians(60 * i - 30)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    cv.setStrokeColor(ACCENT)
    cv.setLineWidth(3)
    for i in range(6):
        cv.line(pts[i][0], pts[i][1], pts[(i + 1) % 6][0], pts[(i + 1) % 6][1])
    inner = [(cx + (pt[0] - cx) * 0.85, cy + (pt[1] - cy) * 0.85) for pt in pts]
    cv.setStrokeColor(BLANC)
    cv.setLineWidth(1.5)
    for i in range(6):
        cv.line(inner[i][0], inner[i][1], inner[(i + 1) % 6][0], inner[(i + 1) % 6][1])
    cv.setFillColor(BLANC)
    cv.setFont("Anton", max(8, r * 0.9))
    cv.drawCentredString(cx, cy - r * 0.4, "RR")


def hexagon_logo_pillow(draw, cx, cy, size, color=None):
    c = color or BLANC_PIL
    r = size
    pts = []
    for i in range(6):
        a = math.radians(60 * i - 30)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    for i in range(6):
        draw.line([pts[i], pts[(i + 1) % 6]], fill=ACCENT_PIL, width=max(3, int(3 * r / 15)))
    inner = [(cx + (pt[0] - cx) * 0.85, cy + (pt[1] - cy) * 0.85) for pt in pts]
    for i in range(6):
        draw.line([inner[i], inner[(i + 1) % 6]], fill=BLANC_PIL, width=max(1, int(1.5 * r / 15)))
    font = ImageFont.truetype(ANTON_PATH, max(8, int(r * 0.8)))
    bbox = draw.textbbox((0, 0), "RR", font=font)
    tw = bbox[2] - bbox[0]
    draw.text((cx - tw / 2, cy - r * 0.35), "RR", fill=BLANC_PIL, font=font)


def chevron_waves(cv, W, H):
    cv.setStrokeColor(Color(1, 1, 1, alpha=0.04))
    cv.setLineWidth(1)
    for row in range(6):
        y_base = 15 + row * 30
        segs = 20
        sw = W / segs
        for i in range(segs):
            x = i * sw
            cv.line(x, y_base, x + sw / 2, y_base + 6)
            cv.line(x + sw / 2, y_base + 6, x + sw, y_base)


def pictogram_badge(cv, cx, cy, r, num):
    """Orange square badge with white number, thick border."""
    s = r * 2
    cv.setFillColor(ACCENT)
    cv.rect(cx - s / 2, cy - s / 2, s, s, stroke=0, fill=1)
    cv.setStrokeColor(BLANC)
    cv.setLineWidth(2)
    cv.rect(cx - s / 2, cy - s / 2, s, s, stroke=1, fill=0)
    cv.setFillColor(BLANC)
    cv.setFont("InterTight", 12)
    cv.drawCentredString(cx, cy - 4.5, f"{num:02d}")


# ── Setlist ──

def gen_setlist():
    W, H = int(A4[0]), int(A4[1])
    path = os.path.join(PDF, "setlist-rock-brut.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, W, H)

    cv.setFillColor(NOIR)
    cv.rect(0, 0, W, H, stroke=0, fill=1)

    random.seed(42)
    for _ in range(5000):
        cv.setFillColor(Color(1, 1, 1, alpha=random.uniform(0.03, 0.10)))
        cv.circle(random.uniform(0, W), random.uniform(0, H),
                  random.uniform(0.3, 1.5), stroke=0, fill=1)

    chevron_waves(cv, W, H)

    hexagon_logo_reportlab(cv, W / 2, H - 120, 30)

    cv.setFillColor(BLANC)
    cv.setFont("Anton", 20)
    cv.drawCentredString(W / 2, H - 165, "RIVERS ROCK")

    cv.setFillColor(ACCENT)
    cv.setFont("Anton", 22)
    cv.drawCentredString(W / 2, H - 195, "SETLIST")

    cv.setStrokeColor(Color(1, 1, 1, alpha=0.15))
    cv.setLineWidth(2)
    cv.line(W / 2 - 60, H - 210, W / 2 + 60, H - 210)

    card_w, card_h = 250, 74
    col_gap = (W - 2 * card_w) / 3
    col_c = [col_gap + card_w / 2, col_gap * 2 + card_w + card_w / 2]
    row_pitch = 86
    rows_top = 610

    def uniform_size():
        longest = max(SETLIST, key=lambda x: len(x[0]))[0]
        mx = card_w - 32 - 28 - 8
        lo, hi = 1, 200
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if pdfmetrics.stringWidth(longest, "Anton", mid) <= mx:
                lo = mid
            else:
                hi = mid - 1
        return lo

    us = uniform_size()

    for idx, (artist, title) in enumerate(SETLIST):
        col, row = idx // 6, idx % 6
        cx = col_c[col]
        cy = rows_top - row * row_pitch
        cl, cb = cx - card_w / 2, cy - card_h / 2
        is_green = idx in GREEN_INDICES
        bg = GRIS_ACIER if is_green else FONCE

        cv.setFillColor(bg)
        cv.rect(cl, cb, card_w, card_h, stroke=0, fill=1)

        cv.setStrokeColor(BLANC)
        cv.setLineWidth(1.5)
        cv.rect(cl, cb, card_w, card_h, stroke=1, fill=0)

        aw = pdfmetrics.stringWidth(artist, "Anton", us)
        tw = 28 + 8 + aw
        sx = cx - tw / 2

        bcy = cy + 15
        s = 14
        cv.setFillColor(ACCENT)
        cv.rect(sx, bcy - s / 2, s * 2, s, stroke=0, fill=1)
        cv.setStrokeColor(BLANC)
        cv.setLineWidth(1.5)
        cv.rect(sx, bcy - s / 2, s * 2, s, stroke=1, fill=0)
        cv.setFillColor(BLANC)
        cv.setFont("InterTight", 11)
        cv.drawCentredString(sx + s, bcy - 4, f"{idx+1:02d}")

        cv.setFillColor(BLANC)
        cv.setFont("Anton", us)
        cv.drawString(sx + 28 + 8, cy + 6, artist)

        if title:
            cv.setFillColor(Color(1, 1, 1, alpha=0.70))
            ts = 12
            if pdfmetrics.stringWidth(title, "InterTight", ts) > card_w - 32:
                ts *= (card_w - 32) / pdfmetrics.stringWidth(title, "InterTight", ts)
            cv.setFont("InterTight", ts)
            cv.drawCentredString(cx, cy - 18, title)

    cv.setFillColor(Color(1, 1, 1, alpha=0.25))
    cv.setFont("JetBrainsMono", 7)
    text, tr = "R O U E N", 4
    x = W / 2 - (sum(pdfmetrics.stringWidth(c, "JetBrainsMono", 7) for c in text) + tr * (len(text) - 1)) / 2
    for c in text:
        w = pdfmetrics.stringWidth(c, "JetBrainsMono", 7)
        cv.drawString(x, 14, c)
        x += w + tr
    save_with_crop_marks(cv, _, _, bleed)
    print(f"[Rock Brut] Setlist → {path}")


# ── Poster ──

def gen_poster():
    W, H = int(A4[0]), int(A4[1])
    path = os.path.join(PDF, "poster-rock-brut.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, W, H)

    cv.setFillColor(NOIR)
    cv.rect(0, 0, W, H, stroke=0, fill=1)

    random.seed(42)
    for _ in range(5000):
        cv.setFillColor(Color(1, 1, 1, alpha=random.uniform(0.03, 0.10)))
        cv.circle(random.uniform(0, W), random.uniform(0, H),
                  random.uniform(0.3, 1.5), stroke=0, fill=1)

    cv.setStrokeColor(ACCENT)
    cv.setLineWidth(0.5)
    for y in range(0, H, 30):
        cv.line(0, y, W, y)

    hexagon_logo_reportlab(cv, W / 2, H - 190, 36)

    cv.setFillColor(BLANC)
    cv.setFont("Anton", 22)
    cv.drawCentredString(W / 2, H - 240, "RIVERS ROCK")

    cv.setFillColor(ACCENT)
    cv.setFont("InterTight", 12)
    cv.drawCentredString(W / 2, H - 280, "LES SOIREES NOCTURNES")

    cv.setFillColor(BLANC)
    cv.setFont("Anton", 52)
    cv.drawCentredString(W / 2, H - 350, "VEN 26 JUIN 2026")

    cv.setFillColor(Color(1, 1, 1, alpha=0.6))
    cv.setFont("InterTight", 16)
    cv.drawCentredString(W / 2, H - 390, "Montigny · 19h30")

    cv.setStrokeColor(ACCENT)
    cv.setLineWidth(3)
    cv.line(W / 2 - 80, H - 420, W / 2 + 80, H - 420)

    cv.setFillColor(Color(1, 1, 1, alpha=0.25))
    cv.setFont("JetBrainsMono", 7)
    text, tr = "R O U E N", 4
    x = W / 2 - (sum(pdfmetrics.stringWidth(c, "JetBrainsMono", 7) for c in text) + tr * (len(text) - 1)) / 2
    for c in text:
        w = pdfmetrics.stringWidth(c, "JetBrainsMono", 7)
        cv.drawString(x, 14, c)
        x += w + tr
    save_with_crop_marks(cv, _, _, bleed)
    print(f"[Rock Brut] Poster → {path}")


# ── Flyer ──

def gen_flyer():
    FW, FH = A6
    path = os.path.join(PDF, "flyer-rock-brut.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, A4[0], A4[1])

    def draw_recto(cv, ox, oy):
        cv.setFillColor(NOIR)
        cv.rect(ox, oy, FW, FH, stroke=0, fill=1)
        cv.setStrokeColor(ACCENT)
        cv.setLineWidth(0.3)
        for y in range(int(oy), int(oy + FH), 15):
            cv.line(ox, y, ox + FW, y)
        cx = ox + FW / 2
        hexagon_logo_reportlab(cv, cx, oy + FH - 55, 16)
        cv.setFillColor(BLANC)
        cv.setFont("Anton", 16)
        cv.drawCentredString(cx, oy + FH - 80, "RIVERS ROCK")
        cv.setFillColor(ACCENT)
        cv.setFont("Anton", 28)
        cv.drawCentredString(cx, oy + FH - 150, "VEN 26 JUIN 2026")
        cv.setFillColor(Color(1, 1, 1, alpha=0.6))
        cv.setFont("InterTight", 10)
        cv.drawCentredString(cx, oy + FH - 180, "Montigny · 19h30")

    def draw_verso(cv, ox, oy):
        cv.setFillColor(NOIR)
        cv.rect(ox, oy, FW, FH, stroke=0, fill=1)
        cv.setStrokeColor(ACCENT)
        cv.setLineWidth(0.3)
        for y in range(int(oy), int(oy + FH), 15):
            cv.line(ox, y, ox + FW, y)
        cx = ox + FW / 2
        cv.setFillColor(BLANC)
        cv.setFont("Anton", 16)
        cv.drawCentredString(cx, oy + FH - 40, "RIVERS ROCK")
        bio = ["Groupe rouennais formé en 2024", "au centre Éducation et Formation", "du Petit-Quevilly.",
               "", "Rosaria — batterie", "Christophe — basse", "Nicolas — guitare",
               "David — guitare / chant", "Virginie — chant", "", "Rock — Pop-Rock — Indé — Alternatif"]
        cv.setFillColor(Color(1, 1, 1, alpha=0.7))
        cv.setFont("InterTight", 7)
        y = oy + FH - 80
        for line in bio:
            cv.drawCentredString(cx, y, line)
            y -= 12
        cv.setFillColor(ACCENT)
        cv.setFont("InterTight", 7)
        cv.drawCentredString(cx, y - 6, "Contactez-nous pour programmer un concert")
        cv.setFillColor(Color(1, 1, 1, alpha=0.35))
        cv.setFont("JetBrainsMono", 7)
        cv.drawCentredString(cx, y - 22, "@riversrockrouen — riversrockrouen@gmail.com")

    for page in range(2):
        for row in range(2):
            for col in range(2):
                ox = col * FW
                oy = (1 - row) * FH
                if page == 0:
                    draw_recto(cv, ox, oy)
                else:
                    draw_verso(cv, ox, oy)
        if page == 0:
            cv.showPage()
    save_with_crop_marks(cv, _, _, bleed)
    print(f"[Rock Brut] Flyer → {path}")


# ── Social ──

def gen_social():
    font_anton_l = ImageFont.truetype(ANTON_PATH, 80)
    font_anton_m = ImageFont.truetype(ANTON_PATH, 52)
    font_inter = ImageFont.truetype(INTERTIGHT_PATH, 22)
    font_tag = ImageFont.truetype(JETBRAINS_PATH, 14)

    w, h = 1080, 1080
    img = Image.new("RGB", (w, h), NOIR_PIL)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, w, 3], fill=ACCENT_PIL)

    hexagon_logo_pillow(draw, w / 2 - 140, 160, 35)

    bbox = draw.textbbox((0, 0), "RIVERS ROCK", font=font_anton_l)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2 + 40, 140), "RIVERS ROCK", fill=BLANC_PIL, font=font_anton_l)

    bbox = draw.textbbox((0, 0), "LES SOIREES NOCTURNES", font=font_inter)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 380), "LES SOIREES NOCTURNES", fill=ACCENT_PIL, font=font_inter)
    bbox = draw.textbbox((0, 0), "VEN 26 JUIN 2026", font=font_anton_m)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 440), "VEN 26 JUIN 2026", fill=BLANC_PIL, font=font_anton_m)
    bbox = draw.textbbox((0, 0), "Montigny · 19h30", font=font_inter)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 520), "Montigny · 19h30", fill=(150, 150, 150), font=font_inter)

    qx, qy, qs = w / 2 - 60, 650, 120
    draw.rectangle([qx, qy, qx + qs, qy + qs], fill=BLANC_PIL, outline=ACCENT_PIL, width=4)
    qr_img = draw_qr_pillow(None, 0, 0, qs - 12, fill_color=NOIR_PIL)
    if qr_img:
        img.paste(qr_img, (int(qx + 6), int(qy + 6)), qr_img if qr_img.mode == "RGBA" else None)

    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((qx + (qs - tw) / 2, qy + (qs - th) / 2), "QR", fill=NOIR_PIL, font=font_inter)

    bbox = draw.textbbox((0, 0), "@riversrockrouen", font=font_tag)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 850), "@riversrockrouen", fill=(150, 150, 150), font=font_tag)

    img = pillow_grain_overlay(img, 0.10, seed=10)
    img.save(os.path.join(TMPL, "instagram-post.png"))

    w, h = 1080, 1920
    img = Image.new("RGB", (w, h), NOIR_PIL)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, w, 4], fill=ACCENT_PIL)
    draw.rectangle([0, h - 4, w, h], fill=ACCENT_PIL)

    font_anton_d = ImageFont.truetype(ANTON_PATH, 120)

    hexagon_logo_pillow(draw, w / 2 - 80, 200, 35)
    bbox = draw.textbbox((0, 0), "RIVERS ROCK", font=font_anton_l)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2 + 30, 180), "RIVERS ROCK", fill=BLANC_PIL, font=font_anton_l)

    bbox = draw.textbbox((0, 0), "VEN 26 JUIN 2026", font=font_anton_d)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 650), "VEN 26 JUIN 2026", fill=ACCENT_PIL, font=font_anton_d)
    bbox = draw.textbbox((0, 0), "Montigny · 19h30", font=font_inter)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 830), "Montigny · 19h30", fill=BLANC_PIL, font=font_inter)

    bbox = draw.textbbox((0, 0), "@riversrockrouen", font=font_tag)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 1750), "@riversrockrouen", fill=(150, 150, 150), font=font_tag)

    img = pillow_grain_overlay(img, 0.10, seed=20)
    img.save(os.path.join(TMPL, "instagram-story.png"))
    print(f"[Rock Brut] Social → {TMPL}")


# ── Banners ──

def gen_banners():
    for name, w, h, logo_s in [
        ("facebook-banner.png", 1640, 624, 56),
        ("youtube-banner.png", 2560, 1440, 86),
    ]:
        img = Image.new("RGB", (w, h), NOIR_PIL)
        draw = ImageDraw.Draw(img)

        bar_h = max(6, int(h * 0.05))
        draw.rectangle([0, 0, w, bar_h], fill=ACCENT_PIL)
        draw.rectangle([0, h - bar_h, w, h], fill=ACCENT_PIL)

        img = pillow_grain_overlay(img, 0.10, seed=30)

        font_logo = ImageFont.truetype(ANTON_PATH, logo_s)
        tw = draw.textbbox((0, 0), "RIVERS ROCK", font=font_logo)[2]
        sym_r = logo_s * 0.5
        gap = sym_r * 0.3
        sx = (w - (sym_r * 2 + gap + tw)) / 2
        hexagon_logo_pillow(draw, sx + sym_r, h / 2, sym_r / 2.5)
        draw.text((sx + sym_r * 2 + gap, h / 2 - tw * 0.25), "RIVERS ROCK", fill=BLANC_PIL, font=font_logo)

        font_sub = ImageFont.truetype(INTERTIGHT_PATH, 14)
        sub = "Reprises rock — Rouen"
        sb = draw.textbbox((0, 0), sub, font=font_sub)
        draw.text(((w - (sb[2] - sb[0])) / 2, h - 50), sub, fill=(150, 150, 150), font=font_sub)

        img.save(os.path.join(TMPL, name))
    print(f"[Rock Brut] Banners → {TMPL}")


# ── Avatar ──

def gen_avatar():
    S = 500
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    hexagon_logo_pillow(draw, S / 2, S / 2, 100)
    font = ImageFont.truetype(ANTON_PATH, 80)
    bbox = draw.textbbox((0, 0), "RR", font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((S - tw) / 2, 340), "RR", fill=BLANC_PIL, font=font)
    img.save(os.path.join(TMPL, "avatar.png"))
    print(f"[Rock Brut] Avatar → {TMPL}")


# ── Stickers ──

def gen_stickers():
    from reportlab.lib.units import mm
    W, H = A4
    SR = 40 * mm
    MX = (W - 2 * SR * 2) / 3
    MY = (H - 3 * SR * 2) / 4
    centers = [(MX + SR + c * (MX + SR * 2), MY + SR + r * (MY + SR * 2)) for c in range(2) for r in range(3)]

    path = os.path.join(PDF, "stickers-rock-brut.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, A4[0], A4[1])

    for cx, cy in centers:
        cv.setFillColor(NOIR)
        cv.circle(cx, cy, SR, stroke=0, fill=1)
        cv.setStrokeColor(ACCENT)
        cv.setLineWidth(3)
        cv.circle(cx, cy, SR, stroke=1, fill=0)
        sr = SR * 0.50
        hexagon_logo_reportlab(cv, cx, cy, sr * 0.8)
        cv.setFillColor(BLANC)
        cv.setFont("Anton", 7)
        cv.drawCentredString(cx, cy + sr * 0.9 + 8, "RIVERS ROCK")
    save_with_crop_marks(cv, _, _, bleed)
    print(f"[Rock Brut] Stickers → {path}")


# ── T-shirt ──

def gen_tshirt():
    from reportlab.lib.units import mm
    w, h = A4
    sizes = [("S", 22 * mm, w / 4, h - 200), ("M", 28 * mm, w * 3 / 4, h - 200),
             ("L", 34 * mm, w / 4, h - 440), ("XL", 40 * mm, w * 3 / 4, h - 440)]
    path = os.path.join(PDF, "tshirt-rock-brut.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, A4[0], A4[1])
    cv.setFillColor(Color(0, 0, 0, alpha=0.04))
    cv.rect(0, 0, w, h, stroke=0, fill=1)
    for label, sr, cx, cy in sizes:
        hexagon_logo_reportlab(cv, cx, cy, sr * 0.8)
        cv.setFillColor(BLANC)
        cv.setFont("Anton", max(10, int(sr * 1.6)))
        cv.drawCentredString(cx, cy + sr * 0.7 + 4, "RIVERS ROCK")
        if label:
            cv.setFillColor(Color(0, 0, 0, alpha=0.3))
            cv.setFont("InterTight", 7)
            cv.drawCentredString(cx, cy + sr + 60, label)
    save_with_crop_marks(cv, _, _, bleed)
    print(f"[Rock Brut] T-shirt → {path}")


# ── Animated logo ──

def gen_animated():
    html = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rivers Rock — Rock Brut</title>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter+Tight&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0}
body{width:1080px;height:1920px;overflow:hidden;background:#0A0A0A;display:flex;align-items:center;justify-content:center}
canvas{position:absolute;top:0;left:0;width:1080px;height:1920px}
svg{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:400px;height:400px;overflow:visible}
.hex{fill:none;stroke:#fff;stroke-width:4;stroke-dasharray:400;stroke-dashoffset:400;animation:drawHex .6s cubic-bezier(0.34,1.56,0.64,1) .3s forwards}
@keyframes drawHex{0%{stroke-dashoffset:400;transform:scale(0)}60%{transform:scale(1.15)}100%{stroke-dashoffset:0;transform:scale(1)}}
.hex-inner{fill:none;stroke:#FF3B00;stroke-width:2.5;opacity:0;animation:fadeH .2s ease-out 1.0s forwards}
@keyframes fadeH{to{opacity:1}}
.shake{animation:shake .3s ease-out 1.1s forwards}
@keyframes shake{0%{transform:translateX(0)}20%{transform:translateX(-5px)}40%{transform:translateX(5px)}60%{transform:translateX(-3px)}80%{transform:translateX(3px)}100%{transform:translateX(0)}}
.rr-left{font-family:'Anton',sans-serif;font-size:40px;fill:#fff;opacity:0}
.rr-right{font-family:'Anton',sans-serif;font-size:40px;fill:#fff;opacity:0}
.lR1{animation:clapLeft .4s cubic-bezier(0.34,1.56,0.64,1) 1.4s forwards}
.lR2{animation:clapRight .4s cubic-bezier(0.34,1.56,0.64,1) 1.55s forwards}
@keyframes clapLeft{0%{opacity:0;transform:translateX(-40px)}100%{opacity:1;transform:translateX(0)}}
@keyframes clapRight{0%{opacity:0;transform:translateX(40px)}100%{opacity:1;transform:translateX(0)}}
.chev{fill:none;stroke:rgba(255,59,0,0.3);stroke-width:2.5;stroke-linecap:round;opacity:0;animation:fadeH .3s ease-out 1.9s forwards}
.chev2{fill:none;stroke:rgba(255,59,0,0.15);stroke-width:1.5;opacity:0;animation:fadeH .4s ease-out 2.1s forwards}
.text-sub{font-family:'Inter Tight',sans-serif;font-size:14px;fill:#fff;opacity:0;animation:fadeH .5s ease-out 2.4s forwards}
@media(prefers-reduced-motion){*{animation:none!important;transition:none!important}}
</style>
</head>
<body>
<canvas id="p"></canvas>
<svg viewBox="-200 -200 400 400">
  <polygon class="hex" points="0,-80 69.3,-40 69.3,40 0,80 -69.3,40 -69.3,-40"/>
  <g class="shake">
    <polygon class="hex-inner" points="0,-60 52,-30 52,30 0,60 -52,30 -52,-30"/>
  </g>
  <text x="-15" y="12" text-anchor="middle" class="rr-left lR1">R</text>
  <text x="15" y="12" text-anchor="middle" class="rr-right lR2">R</text>
  <polyline class="chev" points="-40,50 -25,35 -10,50"/>
  <polyline class="chev2" points="10,50 25,35 40,50"/>
  <text x="0" y="100" text-anchor="middle" class="text-sub">RIVERS ROCK</text>
</svg>
<script>
const c=document.getElementById('p'),ctx=c.getContext('2d');
c.width=1080;c.height=1920;
const ps=[];
for(let i=0;i<20;i++){ps.push({x:Math.random()*1080,y:Math.random()*1920,s:Math.random()*2+1,a:Math.random()*0.12+0.04})}
function draw(){ctx.clearRect(0,0,1080,1920);ctx.fillStyle='#0A0A0A';ctx.fillRect(0,0,1080,1920);
for(const p of ps){ctx.beginPath();ctx.arc(p.x,p.y,p.s,0,Math.PI*2);ctx.fillStyle='rgba(255,59,0,'+p.a+')';ctx.fill();p.y-=0.6;if(p.y<0){p.y=1920;p.x=Math.random()*1080}}
requestAnimationFrame(draw)}draw();
</script>
</body>
</html>'''
    path = os.path.join(TMPL, "logo-animated-rock-brut.html")
    with open(path, "w") as f:
        f.write(html)
    print(f"[Rock Brut] Animated logo → {path}")


# ── Site ──

def gen_site():
    html = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rivers Rock — Rock Brut</title>
<link href="https://fonts.googleapis.com/css2?family=Anton&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter+Tight:wght@300;400;600&family=JetBrains+Mono&display=swap" rel="stylesheet">
<style>
:root{--noir:#0A0A0A;--accent:#FF3B00;--blanc:#fff;--gris:#222}@media(prefers-color-scheme:dark){:root{--noir:#000;--gris:#111}}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:70px}
body{font-family:'Inter Tight','Montserrat',sans-serif;background:var(--noir);color:var(--blanc);min-height:100vh}
.bg-grain{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23g)' opacity='0.05'/%3E%3C/svg%3E")}
.accent-bar{position:fixed;top:0;left:0;width:100%;height:4px;background:var(--accent);z-index:101}
nav{position:fixed;top:0;left:0;right:0;height:56px;display:flex;justify-content:space-between;align-items:center;padding:0 32px;z-index:100;background:rgba(10,10,10,0.9);backdrop-filter:blur(8px);border-bottom:1px solid rgba(255,59,0,0.1)}
nav .logo-small{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--blanc)}
nav .logo-small span{font-family:'Anton',sans-serif;font-size:16px;letter-spacing:2px;text-transform:uppercase}
nav a{color:rgba(255,255,255,0.6);text-decoration:none;font-size:12px;font-weight:400;letter-spacing:1px;text-transform:uppercase;padding:6px 14px;transition:.2s}
nav a:hover{color:var(--accent)}
.hero{position:relative;z-index:1;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:100px 24px 60px}
.hero .logo-svg svg{width:100px;height:100px;margin-bottom:12px}
.hero .logo-svg svg polygon{fill:none;stroke:#fff;stroke-width:4}
.hero .logo-svg svg polyline{fill:none;stroke:var(--accent);stroke-width:3}
.hero h1{font-family:'Anton',sans-serif;font-size:clamp(42px,10vw,72px);letter-spacing:3px;color:var(--blanc);text-transform:uppercase;margin-bottom:4px}
.hero .tagline{font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--accent);letter-spacing:2px;text-transform:uppercase;margin-bottom:24px}
.hero p{font-size:14px;line-height:1.7;color:rgba(255,255,255,0.6);max-width:500px}
.section{position:relative;z-index:1;padding:80px 24px;max-width:700px;margin:0 auto}
.section h2{font-family:'Anton',sans-serif;font-size:clamp(24px,6vw,32px);letter-spacing:3px;color:var(--accent);margin-bottom:24px;text-transform:uppercase;text-align:center}
.section h2::after{content:'';display:block;width:40px;height:3px;background:var(--accent);margin:8px auto 0}
.section p{font-size:14px;line-height:1.7;color:rgba(255,255,255,0.6);margin-bottom:16px}
.band{width:100%;height:4px;background:var(--accent);margin:40px 0}
.members-grid{display:flex;flex-wrap:wrap;justify-content:center;gap:20px;margin-top:20px}
.member-card{flex:0 0 180px;text-align:center;padding:24px 12px;background:rgba(34,34,34,0.5);border:1px solid rgba(255,255,255,0.04);transition:.2s}
.member-card:hover{background:rgba(255,59,0,0.06);border-color:rgba(255,59,0,0.15)}
.member-card .avatar-circle{width:68px;height:68px;border-radius:2px;background:rgba(255,59,0,0.15);margin:0 auto 10px;display:flex;align-items:center;justify-content:center;font-family:'Anton',sans-serif;font-size:26px;color:var(--accent)}
.member-card h3{font-family:'Anton',sans-serif;font-size:16px;letter-spacing:1px;color:var(--blanc);margin-bottom:3px}
.member-card p{font-family:'Inter Tight',sans-serif;font-size:12px;text-transform:uppercase;color:rgba(255,255,255,0.3)}
.concerts-list{list-style:none;padding:0}
.concerts-list li{padding:14px 20px;margin-bottom:10px;background:rgba(34,34,34,0.4);border-left:3px solid var(--accent);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px}
.concerts-list .date{font-family:'JetBrains Mono',monospace;font-size:13px;color:var(--accent)}
.concerts-list .lieu{font-size:13px;color:rgba(255,255,255,0.4)}
.concerts-list .status{font-size:10px;padding:3px 10px;background:rgba(255,59,0,0.1);color:var(--accent)}
.contact-info{text-align:center;margin-top:16px}
.contact-info p{font-size:14px;margin-bottom:6px;color:rgba(255,255,255,0.6)}
.contact-info .email{font-family:'JetBrains Mono',monospace;font-size:14px;color:var(--accent);text-decoration:none;transition:.2s}
.contact-info .email:hover{color:var(--blanc)}
.links{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:24px}
.links a{color:rgba(255,255,255,0.6);text-decoration:none;font-family:'Inter Tight',sans-serif;font-size:12px;padding:10px 20px;border:2px solid rgba(255,59,0,0.3);transition:.2s;text-transform:uppercase;letter-spacing:1px}
.links a:hover{color:#fff;border-color:var(--accent);background:rgba(255,59,0,0.15)}
.footer{position:relative;z-index:1;text-align:center;padding:44px 24px;border-top:1px solid rgba(255,59,0,0.1)}
.footer .logo-footer svg{width:60px;height:60px;margin-bottom:8px;opacity:0.3}
.footer .logo-footer svg polygon{fill:none;stroke:rgba(255,255,255,0.2);stroke-width:3}
.footer .logo-footer svg polyline{fill:none;stroke:rgba(255,59,0,0.2);stroke-width:2}
.footer p{font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:4px;color:rgba(255,255,255,0.25)}
.scroll-indicator{position:absolute;bottom:20px;left:50%;transform:translateX(-50%);width:24px;height:40px;border:2px solid rgba(255,255,255,0.1);border-radius:12px}
.scroll-indicator::after{content:'';position:absolute;top:6px;left:50%;transform:translateX(-50%);width:3px;height:8px;background:var(--accent);border-radius:2px;animation:scrollDown 2s infinite}
@keyframes scrollDown{0%{opacity:1;transform:translateX(-50%) translateY(0)}100%{opacity:0;transform:translateX(-50%) translateY(16px)}}
@media(max-width:640px){
  h1{font-size:42px}
  nav{padding:0 16px}
  nav a{font-size:10px;padding:4px 8px}
  .hero{padding:80px 16px 40px}
  .section{padding:60px 16px}
  .member-card{flex:0 0 150px}
}
@media(max-width:400px){
  .hero h1{font-size:32px}
  .member-card{flex:0 0 140px}
  .section{padding:40px 12px}
}
@media(prefers-reduced-motion){*{animation:none!important;transition:none!important}}
</style>
</head>
<body>
<div class="bg-grain"></div>
<div class="accent-bar"></div>
<nav>
  <a href="#" class="logo-small"><span>RIVERS ROCK</span></a>
  <div>
    <a href="#groupe">Groupe</a>
    <a href="#concerts">Concerts</a>
    <a href="#musique">Musique</a>
    <a href="#contact">Contact</a>
  </div>
</nav>
<section class="hero">
  <div class="logo-svg">
    <svg viewBox="0 0 100 100">
      <polygon points="50,8 86.4,29 86.4,71 50,92 13.6,71 13.6,29"/>
      <polyline points="35,60 50,45 65,60"/>
    </svg>
  </div>
  <h1>Rivers Rock</h1>
  <div class="tagline">Reprises rock — Rouen</div>
  <p>Groupe rouennais forme en 2024. Rock, pop-rock, inde, alternatif.</p>
  <a href="#groupe" style="text-decoration:none;color:inherit"><div class="scroll-indicator"></div></a>
</section>
<section id="groupe" class="section">
  <h2>Le groupe</h2>
  <p>Cinq musiciens, une passion commune : faire vibrer la scene rouennaise.</p>
  <div class="members-grid">
    <div class="member-card"><div class="avatar-circle">R</div><h3>Rosaria</h3><p>Batterie</p></div>
    <div class="member-card"><div class="avatar-circle">C</div><h3>Christophe</h3><p>Basse</p></div>
    <div class="member-card"><div class="avatar-circle">N</div><h3>Nicolas</h3><p>Guitare</p></div>
    <div class="member-card"><div class="avatar-circle">D</div><h3>David</h3><p>Guitare / Chant</p></div>
    <div class="member-card"><div class="avatar-circle">V</div><h3>Virginie</h3><p>Chant</p></div>
  </div>
</section>
<section id="concerts" class="section">
  <div class="band"></div>
  <h2>Concerts</h2>
  <p>Contactez-nous pour programmer un concert. Notre setlist de 12 titres traverse les epoques.</p>
  <div class="concerts-list"><li><span class="date">VEN 26 JUIN 2026</span><span class="lieu">Montigny · 19h30</span><span class="status">Concert</span></li></div>
  <div class="band"></div>
  <div style="margin-top:16px;border-radius:8px;overflow:hidden;max-width:400px;margin-left:auto;margin-right:auto"><img src="../../images/IMG-20260620-WA0001.jpg" style="width:100%;height:auto;display:block;border-radius:8px" alt="Affiche"></div>
</section>
<section id="musique" class="section">
  <h2>Musique</h2>
  <p>Decouvrez Rivers Rock en action — extraits live et playlist a venir.</p>
  <div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:4px;margin-top:16px">
    <div style="position:absolute;top:0;left:0;width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,0.3);border-radius:4px;font-family:sans-serif;font-size:16px;color:rgba(255,255,255,0.3)">Video a venir</div>
  </div>
</section>
<section id="contact" class="section">
  <h2>Contact</h2>
  <div class="contact-info"><p>Pour toute demande :</p><a class="email" href="mailto:riversrockrouen@gmail.com">riversrockrouen@gmail.com</a></div>
  <div class="links">
    <a href="https://www.instagram.com/riversrockrouen" target="_blank">Instagram</a>
    <a href="https://www.facebook.com/RiversRockRouen" target="_blank">Facebook</a>
    <a href="https://www.youtube.com/@RiversRockRouen" target="_blank">YouTube</a>
  </div>
</section>
<footer class="footer">
  <div class="logo-footer">
    <svg viewBox="0 0 100 100">
      <polygon points="50,16 78.1,33.5 78.1,66.5 50,84 21.9,66.5 21.9,33.5"/>
      <polyline points="40,65 50,55 60,65"/>
    </svg>
  </div>
  <p>R O U E N</p>
</footer>
</body>
</html>'''
    path = os.path.join(OUT, "index.html")
    with open(path, "w") as f:
        f.write(html)
    print(f"[Rock Brut] Site → {path}")


if __name__ == "__main__":
    gen_setlist()
    gen_poster()
    gen_flyer()
    gen_social()
    gen_banners()
    gen_avatar()
    gen_stickers()
    gen_tshirt()
    gen_animated()
    gen_site()
