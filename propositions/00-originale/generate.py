#!/usr/bin/env python3
"""Generate all Original (BASE) assets — Proposition 00."""

import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))
from logoutils import (
    draw_qr_pillow,
    reportlab_crest, pillow_crest,
    BEBAS_PATH, MONTSERRAT_PATH, PLAYFAIR_PATH, INTER_PATH, SPACE_MONO_PATH,
)
from palette import BASE as CFG
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

BLEU = CFG.rl("bleu_seine")
VERT = CFG.rl("vert_eau")
ACCENT = CFG.rl("accent")
VERT_REP = CFG.rl("vert_repere")
BLANC = CFG.rl("blanc")

BLEU_PIL = CFG.pil("bleu_seine")
VERT_PIL = CFG.pil("vert_eau")
ACCENT_PIL = CFG.pil("accent")
BLANC_PIL = (255, 255, 255)

pdfmetrics.registerFont(TTFont("PlayfairDisplay", PLAYFAIR_PATH))
pdfmetrics.registerFont(TTFont("Inter", INTER_PATH))
pdfmetrics.registerFont(TTFont("SpaceMono", SPACE_MONO_PATH))
pdfmetrics.registerFont(TTFont("BebasNeue", BEBAS_PATH))
pdfmetrics.registerFont(TTFont("Montserrat", MONTSERRAT_PATH))

from setlist_data import SETLIST, GREEN_INDICES

# ── Setlist ──

def gen_setlist():
    W, H = A4
    path = os.path.join(PDF, "setlist-original.pdf")
    cv = canvas.Canvas(path, pagesize=(W, H))

    for i in range(120):
        t = i / 119
        r = BLEU.red + (VERT.red - BLEU.red) * t
        g = BLEU.green + (VERT.green - BLEU.green) * t
        b = BLEU.blue + (VERT.blue - BLEU.blue) * t
        cv.setFillColor(Color(r, g, b))
        cv.rect(0, i * H / 120, W, H / 120 + 1, stroke=0, fill=1)

    cv.setFillColor(Color(1, 1, 1, alpha=0.07))
    for row in range(3):
        y_base = 20 + row * 30
        amp = 8 + row * 6
        segs = 300
        sw = W / segs
        p = cv.beginPath()
        p.moveTo(0, y_base)
        for i in range(segs + 1):
            px = i * sw
            py = y_base + amp * math.sin(i * 2 * math.pi / (28 + row * 12))
            p.lineTo(px, py)
        p.lineTo(W, 0)
        p.lineTo(0, 0)
        p.close()
        cv.drawPath(p, fill=1, stroke=0)

    reportlab_crest(cv, W / 2, H - 115, 2.2)

    cv.setFillColor(ACCENT)
    cv.setFont("BebasNeue", 28)
    cv.drawCentredString(W / 2, H - 165, "SETLIST")
    cv.setStrokeColor(Color(1, 1, 1, alpha=0.2))
    cv.setLineWidth(1.5)
    segs = 30
    wl, wy = 160, H - 178
    p = cv.beginPath()
    p.moveTo(W / 2 - wl / 2, wy)
    for i in range(segs + 1):
        t = i / segs
        px = W / 2 - wl / 2 + t * wl
        py = wy + 3.5 * math.sin(t * 2 * math.pi * 4)
        p.lineTo(px, py)
    cv.drawPath(p, stroke=1, fill=0)

    card_w, card_h, card_r = 250, 74, 6
    col_gap = (W - 2 * card_w) / 3
    col_c = [col_gap + card_w / 2, col_gap * 2 + card_w + card_w / 2]
    row_pitch = 86
    rows_top = 610

    def uniform_size():
        longest = max(SETLIST, key=lambda x: len(x[0]))[0]
        mx = card_w - 32 - 24 - 8
        lo, hi = 1, 200
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if pdfmetrics.stringWidth(longest, "BebasNeue", mid) <= mx:
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
        bg = VERT_REP if is_green else ACCENT

        cv.setFillColor(Color(0, 0, 0, alpha=0.15))
        cv.roundRect(cl + 3, cb - 3, card_w, card_h, card_r, stroke=0, fill=1)

        for i in range(30):
            t = i / 29
            l = 0.18 * (1 - t)
            c = Color(min(1, bg.red + l), min(1, bg.green + l), min(1, bg.blue + l))
            cv.setFillColor(c)
            cv.rect(cl, cb + i * card_h / 30, card_w, card_h / 30 + 0.5, stroke=0, fill=1)

        cv.setStrokeColor(Color(1, 1, 1, alpha=0.35))
        cv.setLineWidth(1)
        cv.roundRect(cl, cb, card_w, card_h, card_r, stroke=1, fill=0)

        aw = pdfmetrics.stringWidth(artist, "BebasNeue", us)
        tw = 24 + 8 + aw
        sx = cx - tw / 2

        ncol = ACCENT if is_green else VERT_REP
        bcy = cy + 15
        cv.setFillColor(BLANC)
        cv.circle(sx + 12, bcy, 12, stroke=0, fill=1)
        cv.setFillColor(ncol)
        cv.setFont("Montserrat", 12)
        cv.drawCentredString(sx + 12, bcy - 4.5, f"{idx+1:02d}")

        cv.setFillColor(BLANC)
        cv.setFont("BebasNeue", us)
        cv.drawString(sx + 24 + 8, cy + 6, artist)

        if title:
            cv.setFillColor(Color(1, 1, 1, alpha=0.80))
            ts = 14
            if pdfmetrics.stringWidth(title, "Montserrat", ts) > card_w - 32:
                ts *= (card_w - 32) / pdfmetrics.stringWidth(title, "Montserrat", ts)
            cv.setFont("Montserrat", ts)
            cv.drawCentredString(cx, cy - 17, title)

    cv.setFillColor(Color(1, 1, 1, alpha=0.18))
    cv.setFont("Montserrat", 7)
    text, tr = "R O U E N", 3
    x = W / 2 - (sum(pdfmetrics.stringWidth(c, "Montserrat", 7) for c in text) + tr * (len(text) - 1)) / 2
    for c in text:
        w = pdfmetrics.stringWidth(c, "Montserrat", 7)
        cv.drawString(x, 14, c)
        x += w + tr
    cv.save()
    print(f"[Originale] Setlist → {path}")


# ── Poster ──

def gen_poster():
    W, H = A4
    path = os.path.join(PDF, "poster-original.pdf")
    cv = canvas.Canvas(path, pagesize=(W, H))

    for i in range(120):
        t = i / 119
        r = BLEU.red + (VERT.red - BLEU.red) * t
        g = BLEU.green + (VERT.green - BLEU.green) * t
        b = BLEU.blue + (VERT.blue - BLEU.blue) * t
        cv.setFillColor(Color(r, g, b))
        cv.rect(0, i * H / 120, W, H / 120 + 1, stroke=0, fill=1)

    cv.setFillColor(Color(1, 1, 1, alpha=0.07))
    for row in range(3):
        y = 20 + row * 30
        amp = 8 + row * 6
        segs = 300
        sw = W / segs
        p = cv.beginPath()
        p.moveTo(0, y)
        for i in range(segs + 1):
            px = i * sw
            py = y + amp * math.sin(i * 2 * math.pi / (28 + row * 12))
            p.lineTo(px, py)
        p.lineTo(W, 0)
        p.lineTo(0, 0)
        p.close()
        cv.drawPath(p, fill=1, stroke=0)

    reportlab_crest(cv, W / 2, H - 190, 2.2)

    cv.setFillColor(ACCENT)
    cv.setFont("Montserrat", 12)
    cv.drawCentredString(W / 2, H - 270, "PROCHAIN CONCERT")
    cv.setFillColor(BLANC)
    cv.setFont("BebasNeue", 48)
    cv.drawCentredString(W / 2, H - 340, "[DATE]")
    cv.setFillColor(Color(1, 1, 1, alpha=0.7))
    cv.setFont("Montserrat", 16)
    cv.drawCentredString(W / 2, H - 380, "[LIEU]")

    cv.setStrokeColor(Color(1, 1, 1, alpha=0.2))
    cv.setLineWidth(1.5)
    segs = 30
    wl, wy = 160, H - 410
    p = cv.beginPath()
    p.moveTo(W / 2 - wl / 2, wy)
    for i in range(segs + 1):
        t = i / segs
        px = W / 2 - wl / 2 + t * wl
        py = wy + 3.5 * math.sin(t * 2 * math.pi * 4)
        p.lineTo(px, py)
    cv.drawPath(p, stroke=1, fill=0)

    cv.setFillColor(BLANC)
    cv.setFont("Montserrat", 7)
    text, tr = "R O U E N", 3
    x = W / 2 - (sum(pdfmetrics.stringWidth(c, "Montserrat", 7) for c in text) + tr * (len(text) - 1)) / 2
    for c in text:
        w = pdfmetrics.stringWidth(c, "Montserrat", 7)
        cv.drawString(x, 14, c)
        x += w + tr
    cv.save()
    print(f"[Originale] Poster → {path}")


# ── Flyer ──

def gen_flyer():
    FW, FH = A6
    path = os.path.join(PDF, "flyer-original.pdf")
    cv = canvas.Canvas(path, pagesize=A4)

    def grad(cv, x, y, w, h):
        for i in range(60):
            t = i / 59
            r = BLEU.red + (VERT.red - BLEU.red) * t
            g = BLEU.green + (VERT.green - BLEU.green) * t
            b = BLEU.blue + (VERT.blue - BLEU.blue) * t
            cv.setFillColor(Color(r, g, b))
            cv.rect(x, y + i * h / 60, w, h / 60 + 0.5, stroke=0, fill=1)

    def draw_recto(cv, ox, oy):
        grad(cv, ox, oy, FW, FH)
        cx = ox + FW / 2
        reportlab_crest(cv, cx, oy + FH - 55, 1.0)
        cv.setFillColor(BLANC)
        cv.setFont("BebasNeue", 28)
        cv.drawCentredString(cx, oy + FH - 110, "RIVERS ROCK")
        cv.setFillColor(ACCENT)
        cv.setFont("BebasNeue", 34)
        cv.drawCentredString(cx, oy + FH - 175, "[DATE]")
        cv.setFillColor(Color(1, 1, 1, alpha=0.7))
        cv.setFont("Montserrat", 10)
        cv.drawCentredString(cx, oy + FH - 205, "[LIEU]")

    def draw_verso(cv, ox, oy):
        grad(cv, ox, oy, FW, FH)
        cx = ox + FW / 2
        cv.setFillColor(BLANC)
        cv.setFont("BebasNeue", 22)
        cv.drawCentredString(cx, oy + FH - 40, "RIVERS ROCK")
        bio = ["Groupe rouennais formé en 2024", "au centre Éducation et Formation", "du Petit-Quevilly.",
               "", "Rosaria — batterie", "Christophe — basse", "Nicolas — guitare",
               "David — guitare / chant", "Virginie — chant", "", "Rock — Pop-Rock — Indé — Alternatif"]
        cv.setFillColor(Color(1, 1, 1, alpha=0.75))
        cv.setFont("Montserrat", 7)
        y = oy + FH - 80
        for line in bio:
            cv.drawCentredString(cx, y, line)
            y -= 12
        cv.setFillColor(ACCENT)
        cv.setFont("Montserrat", 7)
        cv.drawCentredString(cx, y - 6, "Contactez-nous pour programmer un concert")
        cv.setFillColor(Color(1, 1, 1, alpha=0.4))
        cv.setFont("Montserrat", 7)
        cv.drawCentredString(cx, y - 22, "@riversrock.rouen — riversrock.fr")

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
    print(f"[Originale] Flyer → {path}")


# ── Social ──

def gen_social():
    def lerp(c1, c2, t):
        return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))

    font_bebas = ImageFont.truetype(BEBAS_PATH, 80)
    font_bebas_m = ImageFont.truetype(BEBAS_PATH, 52)
    font_mont = ImageFont.truetype(MONTSERRAT_PATH, 28)
    font_tag = ImageFont.truetype(MONTSERRAT_PATH, 18)

    w, h = 1080, 1080
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    for i in range(200):
        t = i / 199
        draw.rectangle([0, i * h / 200, w, (i + 1) * h / 200],
                       fill=lerp(BLEU_PIL, VERT_PIL, t))

    pillow_crest(draw, w / 2 - 140, 160, 1.4)

    bbox = draw.textbbox((0, 0), "RIVERS ROCK", font=font_bebas)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2 + 40, 150), "RIVERS ROCK", fill=BLANC_PIL, font=font_bebas)

    bbox = draw.textbbox((0, 0), "PROCHAIN CONCERT", font=font_mont)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 400), "PROCHAIN CONCERT", fill=ACCENT_PIL, font=font_mont)
    bbox = draw.textbbox((0, 0), "[DATE]", font=font_bebas_m)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 470), "[DATE]", fill=BLANC_PIL, font=font_bebas_m)
    bbox = draw.textbbox((0, 0), "[LIEU]", font=font_mont)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 550), "[LIEU]", fill=(200, 200, 200), font=font_mont)

    qr_x, qr_y, qr_s = w / 2 - 60, 680, 120
    draw.rounded_rectangle([qr_x, qr_y, qr_x + qr_s, qr_y + qr_s], radius=12, fill=BLANC_PIL, outline=ACCENT_PIL, width=3)
    qr_img = draw_qr_pillow(None, 0, 0, qs - 12, fill_color=BLEU_PIL)
    if qr_img:
        img.paste(qr_img, (int(qx + 6), int(qy + 6)), qr_img if qr_img.mode == "RGBA" else None)

    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((qr_x + (qr_s - tw) / 2, qr_y + (qr_s - th) / 2), "QR", fill=BLEU_PIL, font=font_mont)

    bbox = draw.textbbox((0, 0), "@riversrock.rouen", font=font_tag)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 870), "@riversrock.rouen", fill=(200, 200, 200), font=font_tag)
    img.save(os.path.join(TMPL, "instagram-post.png"))

    w, h = 1080, 1920
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    for i in range(300):
        t = i / 299
        draw.rectangle([0, i * h / 300, w, (i + 1) * h / 300],
                       fill=lerp(BLEU_PIL, VERT_PIL, t))

    font_bebas_l = ImageFont.truetype(BEBAS_PATH, 60)
    font_bebas_d = ImageFont.truetype(BEBAS_PATH, 140)
    pillow_crest(draw, w / 2 - 100, 200, 1.2)
    bbox = draw.textbbox((0, 0), "RIVERS ROCK", font=font_bebas_l)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2 + 30, 190), "RIVERS ROCK", fill=BLANC_PIL, font=font_bebas_l)

    bbox = draw.textbbox((0, 0), "[DATE]", font=font_bebas_d)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 650), "[DATE]", fill=ACCENT_PIL, font=font_bebas_d)
    bbox = draw.textbbox((0, 0), "[LIEU]", font=font_mont)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 850), "[LIEU]", fill=BLANC_PIL, font=font_mont)
    bbox = draw.textbbox((0, 0), "@riversrock.rouen", font=font_mont)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 1750), "@riversrock.rouen", fill=(200, 200, 200), font=font_mont)
    img.save(os.path.join(TMPL, "instagram-story.png"))
    print(f"[Originale] Social → {TMPL}")


# ── Banners ──

def gen_banners():
    for name, w, h, logo_s in [
        ("facebook-banner.png", 1640, 624, 56),
        ("youtube-banner.png", 2560, 1440, 86),
    ]:
        img = Image.new("RGB", (w, h))
        draw = ImageDraw.Draw(img)
        for i in range(120):
            t = i / 119
            draw.rectangle([0, i * h / 120, w, (i + 1) * h / 120],
                           fill=tuple(int(a + (b - a) * t) for a, b in zip(BLEU_PIL, VERT_PIL)))

        font_logo = ImageFont.truetype(BEBAS_PATH, logo_s)
        tw = draw.textbbox((0, 0), "RIVERS ROCK", font=font_logo)[2]
        sym_r = logo_s * 0.45
        gap = sym_r * 0.4
        sx = (w - (sym_r * 2 + gap + tw)) / 2
        pillow_crest(draw, sx + sym_r, h / 2, sym_r / 25.0)
        draw.text((sx + sym_r * 2 + gap, h / 2 - tw * 0.2), "RIVERS ROCK", fill=BLANC_PIL, font=font_logo)
        img.save(os.path.join(TMPL, name))
    print(f"[Originale] Banners → {TMPL}")


# ── Avatar ──

def gen_avatar():
    S = 500
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    pillow_crest(draw, S / 2, S / 2, 180 / 25.0)
    img.save(os.path.join(TMPL, "avatar.png"))
    print(f"[Originale] Avatar → {TMPL}")


# ── Stickers ──

def gen_stickers():
    from reportlab.lib.units import mm
    W, H = A4
    SR = 40 * mm
    MX = (W - 2 * SR * 2) / 3
    MY = (H - 3 * SR * 2) / 4
    centers = [(MX + SR + c * (MX + SR * 2), MY + SR + r * (MY + SR * 2)) for c in range(2) for r in range(3)]

    path = os.path.join(PDF, "stickers-original.pdf")
    cv = canvas.Canvas(path, pagesize=A4)

    for cx, cy in centers:
        for i in range(60):
            t = i / 59
            r = BLEU.red + (VERT.red - BLEU.red) * t
            g = BLEU.green + (VERT.green - BLEU.green) * t
            b = BLEU.blue + (VERT.blue - BLEU.blue) * t
            cv.setFillColor(Color(r, g, b))
            y = cy - SR + i * SR * 2 / 60
            cv.rect(cx - SR, y, SR * 2, SR * 2 / 60 + 0.5, stroke=0, fill=1)
        cv.setStrokeColor(BLANC)
        cv.setLineWidth(2)
        cv.circle(cx, cy, SR, stroke=1, fill=0)

        sr = SR * 0.55
        cv.setStrokeColor(BLANC)
        cv.setLineWidth(2)
        cv.circle(cx, cy, sr, stroke=1, fill=0)
        cv.setStrokeColor(ACCENT)
        cv.setLineWidth(1.5)
        m = sr * 0.08
        segs = 30
        p = cv.beginPath()
        p.moveTo(cx - sr + m, cy)
        for i in range(segs + 1):
            t = i / segs
            px = cx - sr + m + t * (sr * 2 - m * 2)
            py = cy + sr * 0.06 * math.sin(t * 2 * math.pi * 2.5)
            p.lineTo(px, py)
        cv.drawPath(p, stroke=1, fill=0)
    cv.save()
    print(f"[Originale] Stickers → {path}")


# ── T-shirt ──

def gen_tshirt():
    from reportlab.lib.units import mm
    w, h = A4
    sizes = [("S", 22 * mm, w / 4, h - 200), ("M", 28 * mm, w * 3 / 4, h - 200),
             ("L", 34 * mm, w / 4, h - 440), ("XL", 40 * mm, w * 3 / 4, h - 440)]
    path = os.path.join(PDF, "tshirt-original.pdf")
    cv = canvas.Canvas(path, pagesize=A4)
    cv.setFillColor(Color(0, 0, 0, alpha=0.04))
    cv.rect(0, 0, w, h, stroke=0, fill=1)
    for label, sr, cx, cy in sizes:
        reportlab_crest(cv, cx, cy, sr / 25.0)
        cv.setFillColor(BLANC)
        cv.setFont("BebasNeue", max(14, int(sr * 2.2)))
        cv.drawCentredString(cx, cy - sr - max(10, sr * 0.6), "RIVERS")
        cv.drawCentredString(cx, cy - sr - max(24, sr * 1.3), "ROCK")
        if label:
            cv.setFillColor(Color(1, 1, 1, alpha=0.4))
            cv.setFont("Montserrat", 7)
            cv.drawCentredString(cx, cy + sr + 60, label)
    cv.save()
    print(f"[Originale] T-shirt → {path}")


# ── Animated logo ──

def gen_animated():
    html = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rivers Rock — Ombre & Lumiere</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0}
body{width:1080px;height:1920px;overflow:hidden;background:#0A0A0A;display:flex;align-items:center;justify-content:center}
canvas{position:absolute;top:0;left:0;width:1080px;height:1920px}
svg{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:360px;height:360px;overflow:visible}
.circle{fill:none;stroke:rgba(255,255,255,0.12);stroke-width:2;animation:fadeIn 1s ease-out .3s forwards;opacity:0}
.diaphragm{stroke:#BDBDBD;stroke-width:4;stroke-linecap:round;opacity:0;animation:fadeIn .6s ease-out .8s forwards}
.dot{fill:#BDBDBD;opacity:0;animation:expand 1s ease-out 1.4s forwards}
@keyframes fadeIn{to{opacity:1}}
@keyframes expand{0%{opacity:0;r:0}100%{opacity:1;r:8}}
.text{font-family:'Playfair Display',serif;font-size:34px;fill:#F5F0E8;opacity:0;letter-spacing:6}
.t1{animation:appearText .8s ease-out 2.0s forwards}
.t2{animation:appearText .8s ease-out 2.6s forwards}
@keyframes appearText{0%{opacity:0;transform:translateY(20px)}100%{opacity:1;transform:translateY(0)}}
@media(prefers-reduced-motion){*{animation:none!important;transition:none!important}}
</style></head><body>
<canvas id="c"></canvas>
<svg viewBox="-200 -200 400 400">
  <circle class="circle" cx="0" cy="0" r="160"/>
  <circle class="circle" cx="0" cy="0" r="145" style="animation-delay:.6s"/>
  <line class="diaphragm" x1="0" y1="-160" x2="0" y2="-50"/>
  <line class="diaphragm" x1="0" y1="50" x2="0" y2="160" style="animation-delay:1.0s"/>
  <circle class="dot" cx="0" cy="0" r="8"/>
  <text class="text t1" x="0" y="65" text-anchor="middle">RIVERS ROCK</text>
  <text class="text t2" x="0" y="105" text-anchor="middle" font-size="14" fill="#6B6B6B" letter-spacing="9">OMBRE & LUMIERE</text>
</svg>
<script>
const c=document.getElementById('c'),ctx=c.getContext('2d');c.width=1080;c.height=1920;
const ps=[];
for(let i=0;i<60;i++){ps.push({x:Math.random()*1080,y:Math.random()*1920,s:Math.random()*2+0.5,a:Math.random()*0.03+0.01})}
function draw(){ctx.clearRect(0,0,1080,1920);
const g=ctx.createRadialGradient(540,960,0,540,960,1200);
g.addColorStop(0,'rgba(255,255,255,0.03)');g.addColorStop(1,'rgba(0,0,0,0)');
ctx.fillStyle=g;ctx.fillRect(0,0,1080,1920);
for(const p of ps){ctx.beginPath();ctx.arc(p.x,p.y,p.s,0,Math.PI*2);ctx.fillStyle='rgba(255,255,255,'+p.a+')';ctx.fill();p.y-=0.15;if(p.y<0){p.y=1920;p.x=Math.random()*1080}}
requestAnimationFrame(draw)}draw();
</script>
</body></html>'''
    path = os.path.join(TMPL, "logo-animated-original.html")
    with open(path, "w") as f:
        f.write(html)
    print(f"[Ombre & Lumiere] Animated logo → {path}")

# ── Site ──
def gen_site():
    html = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rivers Rock — Ombre & Lumiere</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600&family=Inter:wght@300;400;600&family=Space+Mono&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--noir:#0A0A0A;--gris-fonce:#2B2B2B;--gris-moyen:#6B6B6B;--gris-clair:#BDBDBD;--blanc:#FFFFFF}
body{font-family:Inter,system-ui,sans-serif;background:var(--noir);color:var(--blanc);min-height:100vh;display:flex;flex-direction:column;align-items:center}
.bg-grain{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256'%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23g)' opacity='0.08'/%3E%3C/svg%3E")}
.container{max-width:640px;width:100%;padding:60px 24px;text-align:center;position:relative;z-index:1}
.logo{margin-bottom:32px}
.logo svg{width:80px;height:80px}
.logo svg circle{fill:none;stroke:var(--gris-clair);stroke-width:2.5}
.logo svg line{stroke:var(--gris-clair);stroke-width:3;stroke-linecap:round}
h1{font-family:Playfair Display,serif;font-weight:400;font-size:clamp(32px,7vw,44px);letter-spacing:4px;margin-top:8px;color:var(--gris-clair)}
.tagline{font-family:Space Mono,monospace;font-size:11px;color:var(--gris-moyen);letter-spacing:3px;margin-top:4px;text-transform:uppercase}
h2{font-family:Playfair Display,serif;font-size:clamp(18px,4vw,24px);font-weight:400;letter-spacing:3px;color:var(--gris-clair);margin:40px 0 16px}
p{font-size:14px;line-height:1.7;color:var(--gris-moyen)}
.members{list-style:none;padding:0}
.members li{padding:4px 0;font-size:14px;color:var(--gris-clair)}
.members li span{color:var(--blanc)}
hr{border:none;border-top:1px solid rgba(255,255,255,0.06);margin:32px 0}
.links{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:24px}
.links a{color:var(--gris-moyen);text-decoration:none;font-size:12px;font-family:Space Mono,monospace;padding:8px 18px;border:1px solid rgba(255,255,255,0.1);border-radius:6px;transition:.3s}
.links a:hover{color:var(--blanc);border-color:var(--gris-clair)}
.footer{font-size:10px;font-family:Space Mono,monospace;color:var(--gris-moyen);margin-top:48px;letter-spacing:3px;text-transform:uppercase}
@media(max-width:640px){.container{padding:40px 16px}.logo svg{width:60px;height:60px}h1{font-size:28px}}
@media(prefers-color-scheme:light){:root{--noir:#FAFAFA;--gris-fonce:#E8E8E4;--gris-moyen:#666;--gris-clair:#333;--blanc:#1A1A1A}}
a:focus-visible,button:focus-visible{outline:2px solid var(--gris-clair);outline-offset:2px}
</style>
</head>
<body>
<div class="bg-grain"></div>
<div class="container">
  <div class="logo">
    <svg viewBox="0 0 100 100">
      <circle cx="50" cy="50" r="42"/>
      <circle cx="50" cy="50" r="38"/>
      <line x1="50" y1="8" x2="50" y2="42"/>
      <line x1="50" y1="58" x2="50" y2="92"/>
      <circle cx="50" cy="50" r="5" fill="var(--noir)"/>
    </svg>
    <h1>RIVERS ROCK</h1>
    <div class="tagline">Ombre &amp; Lumiere</div>
  </div>
  <p>Clair-obscur, argentique, lessentiel.<br>Groupe rouennais forme en 2024.</p>
  <hr>
  <h2>Membres</h2>
  <ul class="members">
    <li><span>Rosaria</span> -- batterie</li>
    <li><span>Christophe</span> -- basse</li>
    <li><span>Nicolas</span> -- guitare</li>
    <li><span>David</span> -- guitare / chant</li>
    <li><span>Virginie</span> -- chant</li>
  </ul>
  <hr>
  <h2>Concerts</h2>
  <p>Contactez-nous pour programmer un concert.</p>
  <hr>
  <h2>Musique</h2>
  <p>Playlist a venir -- suivez-nous sur YouTube.</p>
  <hr>
  <h2>Contact</h2>
  <p>riversrock_rouen@gmail.com</p>
  <div class="links">
    <a href="https://www.instagram.com/riversrock_rouen">Instagram</a>
    <a href="https://www.facebook.com/RiversRockRouen">Facebook</a>
    <a href="https://www.youtube.com/@RiversRockRouen">YouTube</a>
  </div>
  <p class="footer">RIVERS ROCK -- Rouen</p>
</div>
</body>
</html>'''
    path = os.path.join(OUT, "index.html")
    with open(path, "w") as f:
        f.write(html)
    print(f"[Ombre & Lumiere] Site > {path}")

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
