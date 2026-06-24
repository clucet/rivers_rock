#!/usr/bin/env python3
"""Generate all Fluid Wave assets — Proposition n°1 (refonte identitaire)."""

import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))
from logoutils import (
    draw_qr_pillow,
    pillow_monogramme_wave,
    pillow_crest, pillow_grain_overlay,
    draw_qr_pillow,
    BEBAS_PATH, NUNITO_PATH, PLAYFAIR_PATH,
)
from palette import FLUID_WAVE as CFG
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

VERT_P = CFG.rl("vert_profond")
VERT_E = CFG.rl("vert_eau")
AMBRE = CFG.rl("ambre")
ACCENT = CFG.rl("accent")
BLANC = CFG.rl("blanc")
VERT_REP = CFG.rl("vert_repere")

VERT_P_PIL = CFG.pil("vert_profond")
VERT_E_PIL = CFG.pil("vert_eau")
AMBRE_PIL = CFG.pil("ambre")
ACCENT_PIL = CFG.pil("accent")
BLANC_PIL = (255, 255, 255)

pdfmetrics.registerFont(TTFont("BebasNeue", BEBAS_PATH))
pdfmetrics.registerFont(TTFont("Nunito", NUNITO_PATH))
BEBAS_REG = BEBAS_PATH
NUNITO_REG = NUNITO_PATH
PLAYFAIR_REG = PLAYFAIR_PATH

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


def logo_wave_symbol(draw, cx, cy, scale=1.0):
    """Fluid Wave logo: flowing wave + RIVERS ROCK text."""
    w = 50 * scale
    h = 16 * scale
    segs = 40
    for i in range(segs):
        t0 = i / segs
        t1 = (i + 1) / segs
        x1 = cx - w / 2 + t0 * w
        y1 = cy - h / 2 + h * (math.sin(t0 * 2 * math.pi * 2 - math.pi / 2) + 1) / 2
        x2 = cx - w / 2 + t1 * w
        y2 = cy - h / 2 + h * (math.sin(t1 * 2 * math.pi * 2 - math.pi / 2) + 1) / 2
        draw.line([(x1, y1), (x2, y2)], fill=AMBRE_PIL, width=max(2, int(3 * scale)))


def logo_wave_reportlab(cv, cx, cy, scale=1.0):
    w = 50 * scale
    h = 14 * scale
    segs = 40
    p = cv.beginPath()
    p.moveTo(cx - w / 2, cy)
    for i in range(segs + 1):
        t = i / segs
        px = cx - w / 2 + t * w
        py = cy + h * math.sin(t * 2 * math.pi * 2)
        p.lineTo(px, py)
    cv.setStrokeColor(AMBRE)
    cv.setLineWidth(3 * scale)
    cv.drawPath(p, stroke=1, fill=0)


def draw_bezier_waves(cv, W, H):
    for row in range(4):
        y_base = 10 + row * 28
        amp = 8 + row * 6
        cv.setFillColor(Color(1, 1, 1, alpha=0.04))
        segs = 200
        sw = W / segs
        p = cv.beginPath()
        p.moveTo(0, y_base + amp * math.sin(0))
        for i in range(segs + 1):
            t = i / segs
            px = i * sw
            phase = t * 2 * math.pi * (2.5 + row * 0.4)
            envelope = 1 - abs(t - 0.5) * 1.2
            py = y_base + amp * max(0, envelope) * math.sin(phase)
            p.lineTo(px, py)
        p.lineTo(W, 0)
        p.lineTo(0, 0)
        p.close()
        cv.drawPath(p, fill=1, stroke=0)


def draw_droplet_badge(cv, cx, cy, r, num, color):
    cv.setFillColor(BLANC)
    cv.circle(cx, cy - r * 0.15, r, stroke=0, fill=1)
    cv.setFillColor(color)
    cv.setFont("Nunito", 12)
    cv.drawCentredString(cx, cy - r * 0.15 - 4.5, f"{num:02d}")


# ── Setlist ──

def gen_setlist():
    W, H = A4
    path = os.path.join(PDF, "setlist-fluid-wave.pdf")
    cv = canvas.Canvas(path, pagesize=(W, H))

    for i in range(120):
        t = i / 119
        r = VERT_P.red + (VERT_E.red - VERT_P.red) * t
        g = VERT_P.green + (VERT_E.green - VERT_P.green) * t
        b = VERT_P.blue + (VERT_E.blue - VERT_P.blue) * t
        cv.setFillColor(Color(r, g, b))
        cv.rect(0, i * H / 120, W, H / 120 + 1, stroke=0, fill=1)

    random.seed(42)
    for _ in range(2000):
        cv.setFillColor(Color(1, 1, 1, alpha=random.uniform(0.015, 0.04)))
        cv.circle(random.uniform(0, W), random.uniform(0, H),
                  random.uniform(0.5, 1.5), stroke=0, fill=1)

    draw_bezier_waves(cv, W, H)

    logo_wave_reportlab(cv, W / 2, H - 110, 2.5)
    cv.setFillColor(BLANC)
    cv.setFont("BebasNeue", 22)
    cv.drawCentredString(W / 2, H - 145, "RIVERS ROCK")

    cv.setFillColor(ACCENT)
    cv.setFont("BebasNeue", 26)
    cv.drawCentredString(W / 2, H - 175, "SETLIST")
    cv.setStrokeColor(Color(1, 1, 1, alpha=0.15))
    cv.setLineWidth(1)
    segs = 30
    wl, wy = 120, H - 188
    p = cv.beginPath()
    p.moveTo(W / 2 - wl / 2, wy)
    for i in range(segs + 1):
        t = i / segs
        px = W / 2 - wl / 2 + t * wl
        py = wy + 2.5 * math.sin(t * 2 * math.pi * 4)
        p.lineTo(px, py)
    cv.drawPath(p, stroke=1, fill=0)

    card_w, card_h, card_r = 250, 74, 14
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
        bg = VERT_P if is_green else ACCENT

        cv.setFillColor(Color(0, 0, 0, alpha=0.10))
        cv.roundRect(cl + 4, cb - 4, card_w, card_h, card_r, stroke=0, fill=1)

        for i in range(30):
            t = i / 29
            l = 0.20 * (1 - t)
            c = Color(min(1, bg.red + l), min(1, bg.green + l), min(1, bg.blue + l))
            cv.setFillColor(c)
            cv.rect(cl, cb + i * card_h / 30, card_w, card_h / 30 + 0.5, stroke=0, fill=1)

        cv.setStrokeColor(Color(1, 1, 1, alpha=0.25))
        cv.setLineWidth(0.8)
        cv.roundRect(cl, cb, card_w, card_h, card_r, stroke=1, fill=0)

        aw = pdfmetrics.stringWidth(artist, "BebasNeue", us)
        tw = 24 + 8 + aw
        sx = cx - tw / 2

        ncol = AMBRE if is_green else BLANC
        bcy = cy + 15
        cv.setFillColor(BLANC)
        cv.circle(sx + 12, bcy, 12, stroke=0, fill=1)
        cv.setFillColor(ncol)
        cv.setFont("Nunito", 12)
        cv.drawCentredString(sx + 12, bcy - 4.5, f"{idx+1:02d}")

        cv.setFillColor(BLANC)
        cv.setFont("BebasNeue", us)
        cv.drawString(sx + 24 + 8, cy + 6, artist)

        if title:
            cv.setFillColor(Color(1, 1, 1, alpha=0.75))
            ts = 13
            if pdfmetrics.stringWidth(title, "Nunito", ts) > card_w - 32:
                ts *= (card_w - 32) / pdfmetrics.stringWidth(title, "Nunito", ts)
            cv.setFont("Nunito", ts)
            cv.drawCentredString(cx, cy - 17, title)

    cv.setFillColor(Color(1, 1, 1, alpha=0.15))
    cv.setFont("Nunito", 7)
    text, tr = "R O U E N", 3
    x = W / 2 - (sum(pdfmetrics.stringWidth(c, "Nunito", 6) for c in text) + tr * (len(text) - 1)) / 2
    for c in text:
        w = pdfmetrics.stringWidth(c, "Nunito", 6)
        cv.drawString(x, 14, c)
        x += w + tr
    cv.save()
    print(f"[Fluid Wave] Setlist → {path}")


# ── Poster ──

def gen_poster():
    W, H = A4
    path = os.path.join(PDF, "poster-fluid-wave.pdf")
    cv = canvas.Canvas(path, pagesize=(W, H))

    for i in range(120):
        t = i / 119
        r = VERT_P.red + (VERT_E.red - VERT_P.red) * t
        g = VERT_P.green + (VERT_E.green - VERT_P.green) * t
        b = VERT_P.blue + (VERT_E.blue - VERT_P.blue) * t
        cv.setFillColor(Color(r, g, b))
        cv.rect(0, i * H / 120, W, H / 120 + 1, stroke=0, fill=1)

    random.seed(42)
    for _ in range(2000):
        cv.setFillColor(Color(1, 1, 1, alpha=random.uniform(0.015, 0.04)))
        cv.circle(random.uniform(0, W), random.uniform(0, H),
                  random.uniform(0.5, 1.5), stroke=0, fill=1)

    draw_bezier_waves(cv, W, H)

    logo_wave_reportlab(cv, W / 2, H - 190, 2.5)
    cv.setFillColor(BLANC)
    cv.setFont("BebasNeue", 22)
    cv.drawCentredString(W / 2, H - 225, "RIVERS ROCK")

    cv.setFillColor(AMBRE)
    cv.setFont("Nunito", 12)
    cv.drawCentredString(W / 2, H - 280, "LES SOIREES NOCTURNES")

    cv.setFillColor(BLANC)
    cv.setFont("BebasNeue", 48)
    cv.drawCentredString(W / 2, H - 340, "SAM 26 JUIN 2026")

    cv.setFillColor(Color(1, 1, 1, alpha=0.7))
    cv.setFont("Nunito", 16)
    cv.drawCentredString(W / 2, H - 375, "Montigny · 19h30")

    cv.setStrokeColor(Color(1, 1, 1, alpha=0.15))
    cv.setLineWidth(1)
    segs = 30
    wl, wy = 120, H - 400
    p = cv.beginPath()
    p.moveTo(W / 2 - wl / 2, wy)
    for i in range(segs + 1):
        t = i / segs
        px = W / 2 - wl / 2 + t * wl
        py = wy + 2.5 * math.sin(t * 2 * math.pi * 4)
        p.lineTo(px, py)
    cv.drawPath(p, stroke=1, fill=0)

    cv.setFillColor(BLANC)
    cv.setFont("Nunito", 7)
    text, tr = "R O U E N", 3
    x = W / 2 - (sum(pdfmetrics.stringWidth(c, "Nunito", 7) for c in text) + tr * (len(text) - 1)) / 2
    for c in text:
        w = pdfmetrics.stringWidth(c, "Nunito", 7)
        cv.drawString(x, 14, c)
        x += w + tr
    cv.save()
    print(f"[Fluid Wave] Poster → {path}")


# ── Flyer ──

def gen_flyer():
    FW, FH = A6
    path = os.path.join(PDF, "flyer-fluid-wave.pdf")
    cv = canvas.Canvas(path, pagesize=A4)

    def grad(cv, x, y, w, h):
        for i in range(60):
            t = i / 59
            r = VERT_P.red + (VERT_E.red - VERT_P.red) * t
            g = VERT_P.green + (VERT_E.green - VERT_P.green) * t
            b = VERT_P.blue + (VERT_E.blue - VERT_P.blue) * t
            cv.setFillColor(Color(r, g, b))
            cv.rect(x, y + i * h / 60, w, h / 60 + 0.5, stroke=0, fill=1)

    def draw_recto(cv, ox, oy):
        grad(cv, ox, oy, FW, FH)
        cx = ox + FW / 2
        logo_wave_reportlab(cv, cx, oy + FH - 55, 1.2)
        cv.setFillColor(BLANC)
        cv.setFont("BebasNeue", 16)
        cv.drawCentredString(cx, oy + FH - 75, "RIVERS ROCK")
        cv.setFillColor(AMBRE)
        cv.setFont("BebasNeue", 34)
        cv.drawCentredString(cx, oy + FH - 145, "SAM 26 JUIN 2026")
        cv.setFillColor(Color(1, 1, 1, alpha=0.7))
        cv.setFont("Nunito", 10)
        cv.drawCentredString(cx, oy + FH - 175, "Montigny · 19h30")

    def draw_verso(cv, ox, oy):
        grad(cv, ox, oy, FW, FH)
        cx = ox + FW / 2
        cv.setFillColor(BLANC)
        cv.setFont("BebasNeue", 16)
        cv.drawCentredString(cx, oy + FH - 40, "RIVERS ROCK")
        bio = ["Groupe rouennais formé en 2024", "au centre Éducation et Formation", "du Petit-Quevilly.",
               "", "Rosaria — batterie", "Christophe — basse", "Nicolas — guitare",
               "David — guitare / chant", "Virginie — chant", "", "Rock — Pop-Rock — Indé — Alternatif"]
        cv.setFillColor(Color(1, 1, 1, alpha=0.75))
        cv.setFont("Nunito", 7)
        y = oy + FH - 80
        for line in bio:
            cv.drawCentredString(cx, y, line)
            y -= 12
        cv.setFillColor(AMBRE)
        cv.setFont("Nunito", 7)
        cv.drawCentredString(cx, y - 6, "Contactez-nous pour programmer un concert")
        cv.setFillColor(Color(1, 1, 1, alpha=0.4))
        cv.setFont("Nunito", 7)
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
    print(f"[Fluid Wave] Flyer → {path}")


# ── Social ──

def gen_social():
    def lerp(c1, c2, t):
        return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))

    font_bebas = ImageFont.truetype(BEBAS_REG, 60)
    font_bebas_m = ImageFont.truetype(BEBAS_REG, 44)
    font_nunito = ImageFont.truetype(NUNITO_REG, 24)
    font_tag = ImageFont.truetype(NUNITO_REG, 16)
    font_play = ImageFont.truetype(PLAYFAIR_REG, 28) if PLAYFAIR_REG else font_bebas

    w, h = 1080, 1080
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    for i in range(200):
        t = i / 199
        draw.rectangle([0, i * h / 200, w, (i + 1) * h / 200],
                       fill=lerp(VERT_P_PIL, VERT_E_PIL, t))

    img = pillow_grain_overlay(img, 0.03, seed=10)

    # Wave logo
    logo_wave_symbol(draw, w / 2, 150, 2.5)
    bbox = draw.textbbox((0, 0), "RIVERS ROCK", font=font_bebas)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 165), "RIVERS ROCK", fill=ACCENT_PIL, font=font_bebas)

    bbox = draw.textbbox((0, 0), "LES SOIREES NOCTURNES", font=font_play)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 380), "LES SOIREES NOCTURNES", fill=AMBRE_PIL, font=font_play)
    bbox = draw.textbbox((0, 0), "SAM 26 JUIN 2026", font=font_bebas_m)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 440), "SAM 26 JUIN 2026", fill=BLANC_PIL, font=font_bebas_m)
    bbox = draw.textbbox((0, 0), "Montigny · 19h30", font=font_nunito)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 510), "Montigny · 19h30", fill=(200, 200, 200), font=font_nunito)

    qx, qy, qs = w / 2 - 60, 650, 120
    draw.rounded_rectangle([qx, qy, qx + qs, qy + qs], radius=16, fill=BLANC_PIL, outline=AMBRE_PIL, width=3)
    qr_img = draw_qr_pillow(None, 0, 0, qs - 12, fill_color=VERT_P_PIL)
    if qr_img:
        img.paste(qr_img, (int(qx + 6), int(qy + 6)), qr_img if qr_img.mode == "RGBA" else None)

    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((qx + (qs - tw) / 2, qy + (qs - th) / 2), "QR", fill=VERT_P_PIL, font=font_nunito)

    bbox = draw.textbbox((0, 0), "@riversrockrouen", font=font_tag)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 850), "@riversrockrouen", fill=(200, 200, 200), font=font_tag)
    img.save(os.path.join(TMPL, "instagram-post.png"))

    w, h = 1080, 1920
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    for i in range(300):
        t = i / 299
        draw.rectangle([0, i * h / 300, w, (i + 1) * h / 300],
                       fill=lerp(VERT_P_PIL, VERT_E_PIL, t))

    img = pillow_grain_overlay(img, 0.03, seed=20)

    font_bebas_d = ImageFont.truetype(BEBAS_REG, 120)
    font_play_l = ImageFont.truetype(PLAYFAIR_REG, 26) if PLAYFAIR_REG else font_nunito

    logo_wave_symbol(draw, w / 2, 180, 3.0)
    bbox = draw.textbbox((0, 0), "RIVERS ROCK", font=font_bebas)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 200), "RIVERS ROCK", fill=ACCENT_PIL, font=font_bebas)

    bbox = draw.textbbox((0, 0), "SAM 26 JUIN 2026", font=font_bebas_d)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 650), "SAM 26 JUIN 2026", fill=AMBRE_PIL, font=font_bebas_d)
    bbox = draw.textbbox((0, 0), "Montigny · 19h30", font=font_play_l)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 830), "Montigny · 19h30", fill=BLANC_PIL, font=font_play_l)

    bbox = draw.textbbox((0, 0), "@riversrockrouen", font=font_tag)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 1750), "@riversrockrouen", fill=(200, 200, 200), font=font_tag)
    img.save(os.path.join(TMPL, "instagram-story.png"))
    print(f"[Fluid Wave] Social → {TMPL}")


# ── Banners ──

def gen_banners():
    for name, w, h, logo_s in [
        ("facebook-banner.png", 1640, 624, 48),
        ("youtube-banner.png", 2560, 1440, 72),
    ]:
        img = Image.new("RGB", (w, h))
        draw = ImageDraw.Draw(img)
        for i in range(120):
            t = i / 119
            c = tuple(int(a + (b - a) * t) for a, b in zip(VERT_P_PIL, VERT_E_PIL))
            draw.rectangle([0, i * h / 120, w, (i + 1) * h / 120], fill=c)

        img = pillow_grain_overlay(img, 0.03, seed=30)

        font_logo = ImageFont.truetype(BEBAS_REG, logo_s)
        tw = draw.textbbox((0, 0), "RIVERS ROCK", font=font_logo)[2]
        sym_r = logo_s * 0.5
        gap = sym_r * 0.3
        sx = (w - (sym_r * 2 + gap + tw)) / 2
        logo_wave_symbol(draw, sx + sym_r, h / 2, sym_r / 20.0)
        draw.text((sx + sym_r * 2 + gap, h / 2 - tw * 0.25), "RIVERS ROCK", fill=BLANC_PIL, font=font_logo)

        font_sub = ImageFont.truetype(NUNITO_REG, 14)
        sub = "Reprises rock — Rouen"
        sb = draw.textbbox((0, 0), sub, font=font_sub)
        draw.text(((w - (sb[2] - sb[0])) / 2, h - 50), sub, fill=AMBRE_PIL, font=font_sub)
        img.save(os.path.join(TMPL, name))
    print(f"[Fluid Wave] Banners → {TMPL}")


# ── Avatar ──

def gen_avatar():
    S = 500
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    logo_wave_symbol(draw, S / 2, S / 2, 6.0)
    font = ImageFont.truetype(BEBAS_REG, 36)
    bbox = draw.textbbox((0, 0), "RR", font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((S - tw) / 2, S / 2 + 50), "RR", fill=ACCENT_PIL, font=font)
    img.save(os.path.join(TMPL, "avatar.png"))
    print(f"[Fluid Wave] Avatar → {TMPL}")


# ── Stickers ──

def gen_stickers():
    from reportlab.lib.units import mm
    W, H = A4
    SR = 40 * mm
    MX = (W - 2 * SR * 2) / 3
    MY = (H - 3 * SR * 2) / 4
    centers = [(MX + SR + c * (MX + SR * 2), MY + SR + r * (MY + SR * 2)) for c in range(2) for r in range(3)]

    path = os.path.join(PDF, "stickers-fluid-wave.pdf")
    cv = canvas.Canvas(path, pagesize=A4)

    for cx, cy in centers:
        for i in range(60):
            t = i / 59
            r = VERT_P.red + (VERT_E.red - VERT_P.red) * t
            g = VERT_P.green + (VERT_E.green - VERT_P.green) * t
            b = VERT_P.blue + (VERT_E.blue - VERT_P.blue) * t
            cv.setFillColor(Color(r, g, b))
            y = cy - SR + i * SR * 2 / 60
            cv.rect(cx - SR, y, SR * 2, SR * 2 / 60 + 0.5, stroke=0, fill=1)
        cv.setStrokeColor(Color(1, 1, 1, alpha=0.5))
        cv.setLineWidth(1.5)
        cv.circle(cx, cy, SR, stroke=1, fill=0)
        sr = SR * 0.50
        logo_wave_reportlab(cv, cx, cy, sr / 22.0)
        cv.setFillColor(BLANC)
        cv.setFont("BebasNeue", 7)
        cv.drawCentredString(cx, cy + sr + 8, "RIVERS ROCK")
    cv.save()
    print(f"[Fluid Wave] Stickers → {path}")


# ── T-shirt ──

def gen_tshirt():
    from reportlab.lib.units import mm
    w, h = A4
    sizes = [("S", 22 * mm, w / 4, h - 200), ("M", 28 * mm, w * 3 / 4, h - 200),
             ("L", 34 * mm, w / 4, h - 440), ("XL", 40 * mm, w * 3 / 4, h - 440)]
    path = os.path.join(PDF, "tshirt-fluid-wave.pdf")
    cv = canvas.Canvas(path, pagesize=A4)
    cv.setFillColor(Color(0, 0, 0, alpha=0.04))
    cv.rect(0, 0, w, h, stroke=0, fill=1)
    for label, sr, cx, cy in sizes:
        logo_wave_reportlab(cv, cx, cy, sr / 22.0)
        cv.setFillColor(BLANC)
        cv.setFont("BebasNeue", max(12, int(sr * 1.8)))
        cv.drawCentredString(cx, cy + sr * 0.6 + 6, "RIVERS ROCK")
        if label:
            cv.setFillColor(Color(0, 0, 0, alpha=0.3))
            cv.setFont("Nunito", 7)
            cv.drawCentredString(cx, cy + sr + 60, label)
    cv.save()
    print(f"[Fluid Wave] T-shirt → {path}")


# ── Animated logo ──

def gen_animated():
    html = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rivers Rock — Fluid Wave</title>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0}
body{width:1080px;height:1920px;overflow:hidden;background:radial-gradient(ellipse at 50% 45%, #1A4A3A 0%, #4A9B8E 100%);display:flex;align-items:center;justify-content:center}
canvas{position:absolute;top:0;left:0;width:1080px;height:1920px}
svg{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:400px;height:400px;overflow:visible}
.wave{fill:none;stroke:#D4A843;stroke-width:4;stroke-linecap:round;opacity:0;animation:fadeW .8s ease-out .5s forwards;filter:drop-shadow(0 0 6px rgba(212,168,67,0.5))}
.wave2{fill:none;stroke:rgba(212,168,67,0.25);stroke-width:2;stroke-linecap:round;opacity:0;animation:fadeW 1s ease-out .9s forwards}
@keyframes fadeW{to{opacity:1}}
.bubble{fill:rgba(212,168,67,0.3);opacity:0}
.b1{animation:bubbleUp 1.2s ease-out .3s forwards}
.b2{animation:bubbleUp 1.0s ease-out .6s forwards}
.b3{animation:bubbleUp 1.4s ease-out .9s forwards}
.b4{animation:bubbleUp 0.9s ease-out 1.2s forwards}
.b5{animation:bubbleUp 1.1s ease-out 1.5s forwards}
@keyframes bubbleUp{0%{opacity:0;transform:translateY(100px)}50%{opacity:0.4}100%{opacity:0;transform:translateY(-60px)}}
.letter{font-family:'Bebas Neue','Helvetica Neue',sans-serif;font-size:36px;fill:#fff;opacity:0}
.lR{animation:floatUp .5s ease-out 1.8s forwards}
.lI{animation:floatUp .5s ease-out 1.95s forwards}
.lV{animation:floatUp .5s ease-out 2.1s forwards}
.lE{animation:floatUp .5s ease-out 2.25s forwards}
.lR2{animation:floatUp .5s ease-out 2.4s forwards}
.lS{animation:floatUp .5s ease-out 2.55s forwards}
@keyframes floatUp{0%{opacity:0;transform:translateY(80px)}100%{opacity:1;transform:translateY(0)}}
.text-roc{font-family:'Bebas Neue',sans-serif;font-size:28px;fill:#E85D3A;opacity:0;animation:fadeW .6s ease-out 2.8s forwards}
</style>
</head>
<body>
<canvas id="p"></canvas>
<svg viewBox="-200 -200 400 400">
  <circle class="bubble b1" cx="-80" cy="40" r="6"/>
  <circle class="bubble b2" cx="-40" cy="20" r="4"/>
  <circle class="bubble b3" cx="20" cy="60" r="8"/>
  <circle class="bubble b4" cx="70" cy="30" r="5"/>
  <circle class="bubble b5" cx="100" cy="50" r="3"/>
  <path class="wave" d="M-140,0 C-100,-40 -60,40 -20,0 C20,-40 60,40 100,0 C140,-40 180,40 200,0">
    <animate attributeName="d" dur="3s" repeatCount="indefinite"
      values="M-140,0 C-100,-40 -60,40 -20,0 C20,-40 60,40 100,0 C140,-40 180,40 200,0;
              M-140,8 C-100,-32 -60,48 -20,8 C20,-32 60,48 100,8 C140,-32 180,48 200,8;
              M-140,-4 C-100,-44 -60,36 -20,-4 C20,-44 60,36 100,-4 C140,-44 180,36 200,-4;
              M-140,0 C-100,-40 -60,40 -20,0 C20,-40 60,40 100,0 C140,-40 180,40 200,0"/>
  </path>
  <path class="wave2" d="M-140,12 C-100,-28 -60,52 -20,12 C20,-28 60,52 100,12 C140,-28 180,52 200,12"/>
  <text x="-60" y="-52.9" text-anchor="middle" class="letter lR">R</text>
  <text x="-36" y="-71.4" text-anchor="middle" class="letter lI">I</text>
  <text x="-12" y="-79.1" text-anchor="middle" class="letter lV">V</text>
  <text x="12" y="-79.1" text-anchor="middle" class="letter lE">E</text>
  <text x="36" y="-71.4" text-anchor="middle" class="letter lR2">R</text>
  <text x="60" y="-52.9" text-anchor="middle" class="letter lS">S</text>
  <text x="0" y="90" text-anchor="middle" class="text-roc">ROCK</text>
</svg>
<script>
const c=document.getElementById('p'),ctx=c.getContext('2d');
c.width=1080;c.height=1920;
const ps=[];
for(let i=0;i<25;i++){ps.push({x:Math.random()*1080,y:Math.random()*1920,s:Math.random()*2+1,a:Math.random()*0.04+0.01})}
function draw(){ctx.clearRect(0,0,1080,1920);
for(const p of ps){ctx.beginPath();ctx.arc(p.x,p.y,p.s,0,Math.PI*2);ctx.fillStyle='rgba(212,168,67,'+p.a+')';ctx.fill();p.y-=0.25;if(p.y<0){p.y=1920;p.x=Math.random()*1080}}
requestAnimationFrame(draw)}draw();
</script>
</body>
</html>'''
    path = os.path.join(TMPL, "logo-animated-fluid-wave.html")
    with open(path, "w") as f:
        f.write(html)
    print(f"[Fluid Wave] Animated logo → {path}")


# ── Site ──

def gen_site():
    html = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rivers Rock — Fluid Wave</title>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Playfair+Display:ital@0;1&family=Nunito:wght@300;400;600&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Nunito','Montserrat',sans-serif;background:linear-gradient(135deg,#1A4A3A,#4A9B8E);color:#fff;min-height:100vh;overflow-x:hidden}
.waves-bg{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;opacity:0.07}
.waves-bg svg{width:100%;height:100%}
.container{position:relative;z-index:1;max-width:640px;margin:0 auto;padding:80px 24px;text-align:center}
.logo-wave{margin-bottom:8px}
.logo-wave svg{width:120px;height:40px}
h1{font-family:'Playfair Display',serif;font-size:52px;font-weight:400;color:#fff;margin-bottom:4px}
.tagline{font-family:'Nunito',sans-serif;font-size:16px;color:#D4A843;margin-bottom:32px;letter-spacing:1px}
p,li{font-size:15px;line-height:1.8;color:rgba(255,255,255,0.8)}
h2{font-family:'Playfair Display',serif;font-size:30px;font-weight:400;color:#D4A843;margin:48px 0 16px;text-align:center}
h2::after{content:'';display:block;width:60px;height:1px;background:rgba(212,168,67,0.4);margin:8px auto 0}
.members{list-style:none;padding:0;display:flex;flex-wrap:wrap;justify-content:center;gap:12px}
.members li{padding:6px 16px;background:rgba(255,255,255,0.06);border-radius:20px;font-size:14px}
.highlight{color:#D4A843;font-weight:600}
hr{border:none;border-top:1px solid rgba(212,168,67,0.15);margin:40px 0}
.links{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:24px}
.links a{color:rgba(255,255,255,0.78);text-decoration:none;font-family:'Nunito',sans-serif;font-size:13px;padding:10px 24px;border:1px solid rgba(212,168,67,0.3);border-radius:24px;transition:.3s}
.links a:hover{color:#fff;border-color:#D4A843;background:rgba(212,168,67,0.1)}
.footer{font-family:'Nunito',sans-serif;font-size:12px;color:rgba(255,255,255,0.3);margin-top:48px;letter-spacing:3px}
@media(max-width:640px){
  .container{padding:48px 16px}
  h1{font-size:36px}
  .members li{flex:1 1 100%}
}
</style>
</head>
<body>
<div class="waves-bg">
  <svg viewBox="0 0 1440 900" preserveAspectRatio="none">
    <path d="M0,450 C360,300 720,600 1080,450 C1260,375 1440,450 1440,450 L1440,900 L0,900 Z" fill="rgba(255,255,255,0.03)"/>
    <path d="M0,500 C360,650 720,350 1080,500 C1260,575 1440,500 1440,500 L1440,900 L0,900 Z" fill="rgba(255,255,255,0.02)"/>
  </svg>
</div>
<div class="container">
  <div class="logo-wave">
    <svg viewBox="0 0 200 40" xmlns="http://www.w3.org/2000/svg">
      <path d="M10,20 C40,0 70,40 100,20 C130,0 160,40 190,20" fill="none" stroke="#D4A843" stroke-width="3" stroke-linecap="round"/>
    </svg>
  </div>
  <h1>Rivers Rock</h1>
  <div class="tagline">Reprises rock — Rouen</div>
  <p>Groupe rouennais formé en 2024. Rock, pop-rock, indé, alternatif. La Seine qui coule derrière le 106.</p>
  <hr>
  <h2>Les membres</h2>
  <ul class="members">
    <li><span class="highlight">Rosaria</span> batterie</li>
    <li><span class="highlight">Christophe</span> basse</li>
    <li><span class="highlight">Nicolas</span> guitare</li>
    <li><span class="highlight">David</span> guitare / chant</li>
    <li><span class="highlight">Virginie</span> chant</li>
  </ul>
  <hr>
  <h2>Concerts</h2>
  <p>Contactez-nous pour programmer un concert.</p>
  <hr>
  <h2>Musique</h2>
  <p>Decouvrez Rivers Rock en action &mdash; extraits live et playlist a venir.</p>
  <div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:8px;margin-top:16px">
    <iframe src="https://www.youtube.com/embed/" style="position:absolute;top:0;left:0;width:100%;height:100%;border:none" allowfullscreen></iframe>
  </div>
  <hr>
  <h2>Contact</h2>
  <p>riversrockrouen@gmail.com</p>
  <div class="links">
    <a href="https://www.instagram.com/riversrockrouen" target="_blank">Instagram</a>
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
    print(f"[Fluid Wave] Site → {path}")


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
