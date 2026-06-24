#!/usr/bin/env python3
"""Generate all Original (BASE) assets — Proposition 00."""

import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))
from logoutils import (
    reportlab_crest, pillow_crest,
    BEBAS_PATH, MONTSERRAT_PATH,
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

pdfmetrics.registerFont(TTFont("BebasNeue", BEBAS_PATH))
pdfmetrics.registerFont(TTFont("Montserrat", MONTSERRAT_PATH))

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
    bbox = draw.textbbox((0, 0), "QR", font=font_mont)
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
<title>Rivers Rock — Logo</title>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0}
body{width:1080px;height:1920px;overflow:hidden;background:#1A3A5C;display:flex;align-items:center;justify-content:center}
canvas{position:absolute;top:0;left:0;width:1080px;height:1920px}
svg{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:400px;height:400px;overflow:visible}
.outer{fill:none;stroke:rgba(255,255,255,0.25);stroke-width:2}
.inner{fill:none;stroke:#fff;stroke-width:5;stroke-dasharray:300;stroke-dashoffset:300;animation:drawC .8s ease-out .3s forwards}
.wave{fill:none;stroke:#E85D3A;stroke-width:4;stroke-linecap:round;opacity:0;animation:fadeW .5s ease-out 1.5s forwards}
@keyframes drawC{to{stroke-dashoffset:0}}
@keyframes fadeW{to{opacity:1}}
.letter{font-family:'Helvetica Neue',Arial,sans-serif;font-weight:700;font-size:32px;fill:#fff;opacity:0}
.lR{animation:drop .4s ease-out 1.0s forwards}
.lI{animation:drop .4s ease-out 1.1s forwards}
.lV{animation:drop .4s ease-out 1.2s forwards}
.lE1{animation:drop .4s ease-out 1.3s forwards}
.lR2{animation:drop .4s ease-out 1.4s forwards}
.lS{animation:drop .4s ease-out 1.5s forwards}
.lROCK_R{animation:slide .4s ease-out 1.9s forwards}
.lROCK_O{animation:slide .4s ease-out 2.0s forwards}
.lROCK_C{animation:slide .4s ease-out 2.1s forwards}
.lROCK_K{animation:slide .4s ease-out 2.2s forwards}
@keyframes drop{0%{opacity:0;transform:translateY(-40px)}100%{opacity:1;transform:translateY(0)}}
@keyframes slide{0%{opacity:0;transform:translateX(200px)}100%{opacity:1;transform:translateX(0)}}
@media(max-width:640px){
  .container{padding:40px 16px}
  .logo svg{width:70px;height:70px}
}
</style>
</head>
<body>
<canvas id="p"></canvas>
<svg viewBox="-200 -200 400 400">
  <circle class="outer" cx="0" cy="0" r="165"/>
  <circle class="inner" cx="0" cy="0" r="80"/>
  <path class="wave" d="M-72,0 Q-40,-20 0,0 Q40,20 72,0">
    <animate attributeName="d" dur="3s" repeatCount="indefinite" values="M-72,0 Q-40,-20 0,0 Q40,20 72,0;M-72,0 Q-40,20 0,0 Q40,-20 72,0;M-72,0 Q-40,-20 0,0 Q40,20 72,0"/>
  </path>
  <text x="-60" y="-52.9" text-anchor="middle" class="letter lR">R</text>
  <text x="-36" y="-71.4" text-anchor="middle" class="letter lI">I</text>
  <text x="-12" y="-79.1" text-anchor="middle" class="letter lV">V</text>
  <text x="12" y="-79.1" text-anchor="middle" class="letter lE1">E</text>
  <text x="36" y="-71.4" text-anchor="middle" class="letter lR2">R</text>
  <text x="60" y="-52.9" text-anchor="middle" class="letter lS">S</text>
  <text x="-30" y="74.2" text-anchor="middle" class="letter lROCK_R" font-size="26">R</text>
  <text x="-10" y="79.4" text-anchor="middle" class="letter lROCK_O" font-size="26">O</text>
  <text x="10" y="79.4" text-anchor="middle" class="letter lROCK_C" font-size="26">C</text>
  <text x="30" y="74.2" text-anchor="middle" class="letter lROCK_K" font-size="26">K</text>
</svg>
<script>
const c=document.getElementById('p'),ctx=c.getContext('2d');
c.width=1080;c.height=1920;
const ps=[];
for(let i=0;i<25;i++){ps.push({x:Math.random()*1080,y:Math.random()*1920,s:Math.random()*2+1,a:Math.random()*0.08+0.02})}
const grad=ctx.createLinearGradient(0,0,0,1920);grad.addColorStop(0,'#1A3A5C');grad.addColorStop(1,'#4A9B8E');
function draw(){ctx.clearRect(0,0,1080,1920);ctx.fillStyle=grad;ctx.fillRect(0,0,1080,1920);
for(const p of ps){ctx.beginPath();ctx.arc(p.x,p.y,p.s,0,Math.PI*2);ctx.fillStyle='rgba(255,255,255,'+p.a+')';ctx.fill();p.y-=0.3;if(p.y<0){p.y=1920;p.x=Math.random()*1080}}
requestAnimationFrame(draw)}draw();
</script>
</body>
</html>'''
    path = os.path.join(TMPL, "logo-animated-original.html")
    with open(path, "w") as f:
        f.write(html)
    print(f"[Originale] Animated logo → {path}")


# ── Site ──

def gen_site():
    html = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rivers Rock — Logo</title>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:system-ui,-apple-system,sans-serif;background:linear-gradient(135deg,#1A3A5C,#4A9B8E);color:#fff;min-height:100vh;display:flex;flex-direction:column;align-items:center}
.container{max-width:640px;width:100%;padding:60px 24px;text-align:center}
.logo{margin-bottom:32px}
.logo svg{width:100px;height:100px}
.logo svg circle{fill:none;stroke:#fff;stroke-width:4}
.logo svg path{fill:none;stroke:#E85D3A;stroke-width:3.5}
h1{font-family:'Helvetica Neue',Arial,sans-serif;font-weight:700;font-size:clamp(36px,8vw,48px);letter-spacing:2px;margin-top:8px;text-transform:uppercase}
h2{font-size:clamp(20px,5vw,28px);font-weight:400;letter-spacing:4px;text-transform:uppercase;color:#E85D3A;margin:32px 0 12px}
p,li{font-size:15px;line-height:1.7;color:rgba(255,255,255,.8)}
.members{list-style:none;padding:0}
.members li{padding:4px 0}
.highlight{color:#E85D3A;font-weight:600}
hr{border:none;border-top:1px solid rgba(255,255,255,.15);margin:32px 0}
.links{display:flex;gap:16px;justify-content:center;flex-wrap:wrap;margin-top:24px}
.links a{color:rgba(255,255,255,.82);text-decoration:none;font-size:14px;padding:8px 16px;border:1px solid rgba(255,255,255,.2);border-radius:6px;transition:.2s}
.links a:hover{color:#fff;border-color:#fff}
.footer{font-size:12px;color:rgba(255,255,255,.3);margin-top:48px}
@media(max-width:640px){
  .container{padding:40px 16px}
  .logo svg{width:70px;height:70px}
}
</style>
</head>
<body>
<div class="container">
  <div class="logo">
    <svg viewBox="0 0 100 100">
      <circle cx="50" cy="50" r="42"/>
      <path d="M18,50 Q30,42 42,50 Q54,58 66,50 Q78,42 90,50"/>
    </svg>
    <h1>RIVERS ROCK</h1>
  </div>
  <p>Groupe rouennais formé en 2024 au centre Éducation et Formation du Petit-Quevilly.<br>Rock — Pop-Rock — Indé — Alternatif</p>
  <hr>
  <h2>Les membres</h2>
  <ul class="members">
    <li><span class="highlight">Rosaria</span> — batterie</li>
    <li><span class="highlight">Christophe</span> — basse</li>
    <li><span class="highlight">Nicolas</span> — guitare</li>
    <li><span class="highlight">David</span> — guitare / chant</li>
    <li><span class="highlight">Virginie</span> — chant</li>
  </ul>
  <hr>
  <h2>Concerts</h2>
  <p>Contactez-nous pour programmer un concert.</p>
  <hr>
  <h2>Contact</h2>
  <p>riversrockrouen@gmail.com</p>
  <div class="links">
    <a href="https://www.instagram.com/riversrock.rouen" target="_blank">Instagram</a>
    <a href="https://www.facebook.com/RiversRockRouen" target="_blank">Facebook</a>
    <a href="https://www.youtube.com/@RiversRockRouen" target="_blank">YouTube</a>
  </div>
  <p class="footer">RIVERS ROCK — Rouen</p>
</div>
</body>
</html>'''
    path = os.path.join(OUT, "index.html")
    with open(path, "w") as f:
        f.write(html)
    print(f"[Originale] Site → {path}")


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
