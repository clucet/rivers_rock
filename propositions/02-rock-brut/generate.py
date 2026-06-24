#!/usr/bin/env python3
"""Generate all Rock Brut assets — Proposition n°2 (refonte identitaire)."""

import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))
from logoutils import (
    draw_qr_pillow,
    pillow_hexagon_monogramme,
    pillow_crest, pillow_grain_overlay,
    draw_qr_pillow,
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
    cv = canvas.Canvas(path, pagesize=(W, H))

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
    cv.save()
    print(f"[Rock Brut] Setlist → {path}")


# ── Poster ──

def gen_poster():
    W, H = int(A4[0]), int(A4[1])
    path = os.path.join(PDF, "poster-rock-brut.pdf")
    cv = canvas.Canvas(path, pagesize=(W, H))

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
    cv.drawCentredString(W / 2, H - 280, "PROCHAIN CONCERT")

    cv.setFillColor(BLANC)
    cv.setFont("Anton", 52)
    cv.drawCentredString(W / 2, H - 350, "[DATE]")

    cv.setFillColor(Color(1, 1, 1, alpha=0.6))
    cv.setFont("InterTight", 16)
    cv.drawCentredString(W / 2, H - 390, "[LIEU]")

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
    cv.save()
    print(f"[Rock Brut] Poster → {path}")


# ── Flyer ──

def gen_flyer():
    FW, FH = A6
    path = os.path.join(PDF, "flyer-rock-brut.pdf")
    cv = canvas.Canvas(path, pagesize=A4)

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
        cv.drawCentredString(cx, oy + FH - 150, "[DATE]")
        cv.setFillColor(Color(1, 1, 1, alpha=0.6))
        cv.setFont("InterTight", 10)
        cv.drawCentredString(cx, oy + FH - 180, "[LIEU]")

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
    cv.save()
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

    bbox = draw.textbbox((0, 0), "PROCHAIN CONCERT", font=font_inter)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 380), "PROCHAIN CONCERT", fill=ACCENT_PIL, font=font_inter)
    bbox = draw.textbbox((0, 0), "[DATE]", font=font_anton_m)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 440), "[DATE]", fill=BLANC_PIL, font=font_anton_m)
    bbox = draw.textbbox((0, 0), "[LIEU]", font=font_inter)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 520), "[LIEU]", fill=(150, 150, 150), font=font_inter)

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

    bbox = draw.textbbox((0, 0), "[DATE]", font=font_anton_d)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 650), "[DATE]", fill=ACCENT_PIL, font=font_anton_d)
    bbox = draw.textbbox((0, 0), "[LIEU]", font=font_inter)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 830), "[LIEU]", fill=BLANC_PIL, font=font_inter)

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
    cv = canvas.Canvas(path, pagesize=A4)

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
    cv.save()
    print(f"[Rock Brut] Stickers → {path}")


# ── T-shirt ──

def gen_tshirt():
    from reportlab.lib.units import mm
    w, h = A4
    sizes = [("S", 22 * mm, w / 4, h - 200), ("M", 28 * mm, w * 3 / 4, h - 200),
             ("L", 34 * mm, w / 4, h - 440), ("XL", 40 * mm, w * 3 / 4, h - 440)]
    path = os.path.join(PDF, "tshirt-rock-brut.pdf")
    cv = canvas.Canvas(path, pagesize=A4)
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
    cv.save()
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
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Inter Tight','Montserrat',sans-serif;background:#0A0A0A;color:#fff;min-height:100vh}
.accent-bar{position:fixed;top:0;left:0;width:100%;height:4px;background:#FF3B00;z-index:100}
.container{max-width:680px;margin:0 auto;padding:80px 24px;text-align:center}
.logo{margin-bottom:16px}
.logo svg{width:90px;height:90px}
.logo svg polygon{fill:none;stroke:#fff;stroke-width:4}
.logo svg polyline{fill:none;stroke:#FF3B00;stroke-width:3}
h1{font-family:'Anton','Helvetica Neue',sans-serif;font-size:72px;letter-spacing:3px;color:#fff;text-transform:uppercase;margin-bottom:4px}
.tagline{font-family:'JetBrains Mono',monospace;font-size:12px;color:#FF3B00;letter-spacing:2px;text-transform:uppercase;margin-bottom:28px}
p,li{font-size:14px;line-height:1.7;color:rgba(255,255,255,0.85)}
h2{font-family:'Anton','Helvetica Neue',sans-serif;font-size:32px;letter-spacing:3px;color:#FF3B00;margin:48px 0 16px;text-transform:uppercase}
h2::after{content:'';display:block;width:40px;height:3px;background:#FF3B00;margin:8px auto 0}
.members{list-style:none;padding:0}
.members li{padding:8px 0;font-size:15px;border-bottom:1px solid rgba(255,255,255,0.04)}
.members li:last-child{border-bottom:none}
.highlight{color:#FF3B00;font-weight:600}
.band{width:100%;height:4px;background:#FF3B00;margin:40px 0}
.links{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:24px}
.links a{color:rgba(255,255,255,0.78);text-decoration:none;font-family:'Inter Tight',sans-serif;font-size:12px;padding:10px 20px;border:2px solid rgba(255,59,0,0.3);transition:.2s;text-transform:uppercase;letter-spacing:1px}
.links a:hover{color:#fff;border-color:#FF3B00;background:rgba(255,59,0,0.15)}
.footer{font-family:'JetBrains Mono',monospace;font-size:11px;color:rgba(255,255,255,0.45);margin-top:48px;letter-spacing:4px;border-top:1px solid rgba(255,59,0,0.15);padding-top:24px}
@media(max-width:640px){
  h1{font-size:42px}
  .container{padding:40px 16px}
  nav a{display:none}
}
</style>
</head>
<body>
<div class="accent-bar"></div>
<div class="container">
  <div class="logo">
    <svg viewBox="0 0 100 100">
      <polygon points="50,8 86.4,29 86.4,71 50,92 13.6,71 13.6,29"/>
      <polyline points="35,60 50,45 65,60"/>
    </svg>
  </div>
  <h1>Rivers Rock</h1>
  <div class="tagline">Reprises rock — Rouen</div>
  <p>Groupe rouennais formé en 2024. Rock, pop-rock, indé, alternatif.</p>
  <div class="band"></div>
  <h2>Les membres</h2>
  <ul class="members">
    <li><span class="highlight">Rosaria</span> — batterie</li>
    <li><span class="highlight">Christophe</span> — basse</li>
    <li><span class="highlight">Nicolas</span> — guitare</li>
    <li><span class="highlight">David</span> — guitare / chant</li>
    <li><span class="highlight">Virginie</span> — chant</li>
  </ul>
  <div class="band"></div>
  <h2>Concerts</h2>
  <p>Contactez-nous pour programmer un concert.</p>
  <div class="band"></div>
  <h2>Contact</h2>
  <p>riversrockrouen@gmail.com</p>
  <div class="links">
    <a href="https://www.instagram.com/riversrockrouen" target="_blank">Instagram</a>
    <a href="https://www.facebook.com/RiversRockRouen" target="_blank">Facebook</a>
    <a href="https://www.youtube.com/@RiversRockRouen" target="_blank">YouTube</a>
  </div>
  <p class="footer">R O U E N</p>
</div>
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
