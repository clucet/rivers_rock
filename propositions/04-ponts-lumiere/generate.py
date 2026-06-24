#!/usr/bin/env python3
"""Generate all Ponts & Lumière assets — Proposition n°5."""

import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))
from logoutils import (
    draw_qr_pillow,
    pillow_bridge_silhouette,
    pillow_grain_overlay,
    draw_qr_pillow, BEBAS_PATH, MONTSERRAT_PATH,
    TEKO_PATH, RALEWAY_PATH, DMMONO_PATH,
)
from palette import PONTS_LUMIERE as CFG
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

NUIT = CFG.rl("nuit")
ACIER = CFG.rl("acier")
LUMIERE = CFG.rl("lumiere")
SEINE = CFG.rl("seine")
BROU = CFG.rl("brouillard")
BLANC = CFG.rl("blanc")

NUIT_PIL = CFG.pil("nuit")
ACIER_PIL = CFG.pil("acier")
LUMIERE_PIL = CFG.pil("lumiere")
SEINE_PIL = CFG.pil("seine")
BROU_PIL = CFG.pil("brouillard")
BLANC_PIL = (255, 255, 255)

pdfmetrics.registerFont(TTFont("Teko", TEKO_PATH))
pdfmetrics.registerFont(TTFont("Raleway", RALEWAY_PATH))
pdfmetrics.registerFont(TTFont("DMMono", DMMONO_PATH))

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


def bridge_logo_reportlab(cv, cx, cy, scale=1.0):
    """Draw bridge silhouette logo."""
    r = 25 * scale
    w = 60 * scale
    segs = 30
    for arc_offset, stroke_c, lw in [(0, BROU, 1.5), (-10, LUMIERE, 1.0)]:
        cv.setStrokeColor(stroke_c)
        cv.setLineWidth(lw * scale)
        p = cv.beginPath()
        p.moveTo(cx - w, cy + arc_offset)
        for i in range(segs + 1):
            t = i / segs
            px = cx - w + t * w * 2
            py = cy + arc_offset - 30 * scale * ((t - 0.5) ** 2 - 0.25)
            p.lineTo(px, py)
        cv.drawPath(p, stroke=1, fill=0)
    cv.setFillColor(LUMIERE)
    cv.circle(cx, cy - 7 * scale, 4 * scale, stroke=0, fill=1)
    cv.setFillColor(BLANC)
    cv.setFont("Teko", max(8, int(10 * scale)))
    cv.drawCentredString(cx, cy + 18 * scale, "RIVERS")
    cv.drawCentredString(cx + 15 * scale, cy + 28 * scale, "ROCK")


def bridge_logo_pillow(draw, cx, cy, scale=1.0):
    """Draw bridge silhouette logo with Pillow."""
    r = 25 * scale
    w = 60 * scale
    segs = 30
    for arc_offset, stroke_c, lw in [(0, BROU_PIL, 2), (-10, LUMIERE_PIL, 1)]:
        for i in range(segs):
            t0 = i / segs
            t1 = (i + 1) / segs
            x1 = cx - w + t0 * w * 2
            y1 = cy + arc_offset - 30 * scale * ((t0 - 0.5) ** 2 - 0.25)
            x2 = cx - w + t1 * w * 2
            y2 = cy + arc_offset - 30 * scale * ((t1 - 0.5) ** 2 - 0.25)
            draw.line([(x1, y1), (x2, y2)], fill=stroke_c, width=max(1, int(lw * scale)))
    draw.ellipse([cx - 4 * scale, cy - 7 * scale - 4 * scale,
                  cx + 4 * scale, cy - 7 * scale + 4 * scale],
                 fill=LUMIERE_PIL)
    font = ImageFont.truetype(BEBAS_PATH, max(8, int(10 * scale)))
    bbox = draw.textbbox((0, 0), "RIVERS", font=font)
    tw = bbox[2] - bbox[0]
    draw.text((cx - tw / 2, cy + 18 * scale - bbox[1]), "RIVERS", fill=BLANC_PIL, font=font)
    bbox2 = draw.textbbox((0, 0), "ROCK", font=font)
    tw2 = bbox2[2] - bbox2[0]
    draw.text((cx + 15 * scale - tw2 / 2, cy + 28 * scale - bbox2[1]), "ROCK", fill=BLANC_PIL, font=font)


def draw_catenary_waves(cv, W, H):
    """Draw catenary curve decorative elements."""
    cv.setStrokeColor(Color(1, 1, 1, alpha=0.03))
    for row in range(3):
        y_base = 15 + row * 35
        amp = 30 + row * 15
        cv.setLineWidth(0.5 + row * 0.3)
        segs = 100
        sw = W / segs
        p = cv.beginPath()
        p.moveTo(0, y_base)
        for i in range(segs + 1):
            t = i / segs
            px = i * sw
            py = y_base + amp * ((t - 0.5) ** 2 - 0.25) * 4
            p.lineTo(px, py)
        cv.drawPath(p, stroke=1, fill=0)


# ── Setlist ──

def gen_setlist():
    W, H = A4
    path = os.path.join(PDF, "setlist-ponts-lumiere.pdf")
    cv = canvas.Canvas(path, pagesize=(W, H))

    for i in range(120):
        t = i / 119
        r = NUIT.red + (SEINE.red - NUIT.red) * t
        g = NUIT.green + (SEINE.green - NUIT.green) * t
        b = NUIT.blue + (SEINE.blue - NUIT.blue) * t
        cv.setFillColor(Color(r, g, b))
        cv.rect(0, i * H / 120, W, H / 120 + 1, stroke=0, fill=1)

    random.seed(42)
    for _ in range(3000):
        cv.setFillColor(Color(1, 1, 1, alpha=random.uniform(0.02, 0.05)))
        cv.circle(random.uniform(0, W), random.uniform(0, H),
                  random.uniform(0.3, 1.0), stroke=0, fill=1)

    draw_catenary_waves(cv, W, H)

    bridge_logo_reportlab(cv, W / 2, H - 105, 2.0)

    cv.setFillColor(LUMIERE)
    cv.setFont("Teko", 26)
    cv.drawCentredString(W / 2, H - 165, "SETLIST")
    cv.setStrokeColor(Color(1, 1, 1, alpha=0.15))
    cv.setLineWidth(1)
    segs = 30
    wl, wy = 120, H - 180
    p = cv.beginPath()
    p.moveTo(W / 2 - wl / 2, wy)
    for i in range(segs + 1):
        t = i / segs
        px = W / 2 - wl / 2 + t * wl
        py = wy - 8 * ((t - 0.5) ** 2 - 0.25)
        p.lineTo(px, py)
    cv.drawPath(p, stroke=1, fill=0)

    card_w, card_h, card_r = 250, 74, 4
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
            w = pdfmetrics.stringWidth(longest, "Teko", mid)
            if not w:
                w = pdfmetrics.stringWidth(longest, "Raleway", mid)
            if w <= mx:
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
        bg = SEINE if is_green else ACIER

        cv.setFillColor(Color(0, 0, 0, alpha=0.25))
        cv.roundRect(cl + 3, cb - 3, card_w, card_h, card_r, stroke=0, fill=1)

        for i in range(30):
            t = i / 29
            l = 0.15 * (1 - t)
            c = Color(min(1, bg.red + l), min(1, bg.green + l), min(1, bg.blue + l))
            cv.setFillColor(c)
            cv.rect(cl, cb + i * card_h / 30, card_w, card_h / 30 + 0.5, stroke=0, fill=1)

        cv.setStrokeColor(Color(1, 1, 1, alpha=0.40))
        cv.setLineWidth(0.8)
        cv.roundRect(cl, cb, card_w, card_h, card_r, stroke=1, fill=0)

        aw = pdfmetrics.stringWidth(artist, "Teko", us)
        if aw == 0:
            aw = pdfmetrics.stringWidth(artist, "Raleway", us)
        tw_ = 24 + 8 + aw
        sx = cx - tw_ / 2

        bcy = cy + 15
        cv.setFillColor(BLANC)
        cv.circle(sx + 12, bcy, 12, stroke=0, fill=1)
        cv.setFillColor(LUMIERE)
        cv.setFont("Raleway", 12)
        cv.drawCentredString(sx + 12, bcy - 4.5, f"{idx+1:02d}")

        cv.setFillColor(BLANC)
        cv.setFont("Teko", us)
        cv.drawString(sx + 24 + 8, cy + 6, artist)

        if title:
            cv.setFillColor(Color(1, 1, 1, alpha=0.75))
            ts = 13
            tww = pdfmetrics.stringWidth(title, "Raleway", ts)
            if tww > card_w - 32:
                ts *= (card_w - 32) / tww
            cv.setFont("Raleway", ts)
            cv.drawCentredString(cx, cy - 17, title)

    cv.setFillColor(Color(1, 1, 1, alpha=0.20))
    cv.setFont("Raleway", 7)
    text, tr = "R O U E N", 4
    x = 0
    for c in text:
        w = pdfmetrics.stringWidth(c, "Raleway", 7)
        if x == 0:
            x = W / 2 - (sum(pdfmetrics.stringWidth(c2, "Raleway", 7) for c2 in text) + tr * (len(text) - 1)) / 2
        cv.drawString(x, 14, c)
        x += w + tr
    cv.save()
    print(f"[Ponts & Lumière] Setlist → {path}")


# ── Poster ──

def gen_poster():
    W, H = A4
    path = os.path.join(PDF, "poster-ponts-lumiere.pdf")
    cv = canvas.Canvas(path, pagesize=(W, H))

    for i in range(120):
        t = i / 119
        r = NUIT.red + (SEINE.red - NUIT.red) * t
        g = NUIT.green + (SEINE.green - NUIT.green) * t
        b = NUIT.blue + (SEINE.blue - NUIT.blue) * t
        cv.setFillColor(Color(r, g, b))
        cv.rect(0, i * H / 120, W, H / 120 + 1, stroke=0, fill=1)

    random.seed(42)
    for _ in range(3000):
        cv.setFillColor(Color(1, 1, 1, alpha=random.uniform(0.02, 0.05)))
        cv.circle(random.uniform(0, W), random.uniform(0, H),
                  random.uniform(0.3, 1.0), stroke=0, fill=1)

    draw_catenary_waves(cv, W, H)
    bridge_logo_reportlab(cv, W / 2, H - 190, 2.0)

    cv.setFillColor(LUMIERE)
    cv.setFont("Raleway", 12)
    cv.drawCentredString(W / 2, H - 270, "PROCHAIN CONCERT")
    cv.setFillColor(BLANC)
    cv.setFont("Teko", 52)
    cv.drawCentredString(W / 2, H - 340, "[DATE]")
    cv.setFillColor(Color(1, 1, 1, alpha=0.7))
    cv.setFont("Raleway", 16)
    cv.drawCentredString(W / 2, H - 385, "[LIEU]")

    cv.setStrokeColor(Color(1, 1, 1, alpha=0.15))
    cv.setLineWidth(1)
    segs = 30
    wl, wy = 120, H - 410
    p = cv.beginPath()
    p.moveTo(W / 2 - wl / 2, wy)
    for i in range(segs + 1):
        t = i / segs
        px = W / 2 - wl / 2 + t * wl
        py = wy - 8 * ((t - 0.5) ** 2 - 0.25)
        p.lineTo(px, py)
    cv.drawPath(p, stroke=1, fill=0)

    cv.setFillColor(BLANC)
    cv.setFont("Raleway", 7)
    text, tr = "R O U E N", 4
    x = 0
    for c in text:
        w = pdfmetrics.stringWidth(c, "Raleway", 7)
        if x == 0:
            x = W / 2 - (sum(pdfmetrics.stringWidth(c2, "Raleway", 7) for c2 in text) + tr * (len(text) - 1)) / 2
        cv.drawString(x, 14, c)
        x += w + tr
    cv.save()
    print(f"[Ponts & Lumière] Poster → {path}")


# ── Flyer ──

def gen_flyer():
    FW, FH = A6
    path = os.path.join(PDF, "flyer-ponts-lumiere.pdf")
    cv = canvas.Canvas(path, pagesize=A4)

    def grad(cv, x, y, w, h):
        for i in range(60):
            t = i / 59
            r = NUIT.red + (SEINE.red - NUIT.red) * t
            g = NUIT.green + (SEINE.green - NUIT.green) * t
            b = NUIT.blue + (SEINE.blue - NUIT.blue) * t
            cv.setFillColor(Color(r, g, b))
            cv.rect(x, y + i * h / 60, w, h / 60 + 0.5, stroke=0, fill=1)

    def draw_recto(cv, ox, oy):
        grad(cv, ox, oy, FW, FH)
        cx = ox + FW / 2
        bridge_logo_reportlab(cv, cx, oy + FH - 50, 1.0)
        cv.setFillColor(BLANC)
        cv.setFont("Teko", 16)
        cv.drawCentredString(cx, oy + FH - 75, "RIVERS ROCK")
        cv.setFillColor(LUMIERE)
        cv.setFont("Teko", 34)
        cv.drawCentredString(cx, oy + FH - 145, "[DATE]")
        cv.setFillColor(Color(1, 1, 1, alpha=0.7))
        cv.setFont("Raleway", 10)
        cv.drawCentredString(cx, oy + FH - 175, "[LIEU]")

    def draw_verso(cv, ox, oy):
        grad(cv, ox, oy, FW, FH)
        cx = ox + FW / 2
        cv.setFillColor(BLANC)
        cv.setFont("Teko", 16)
        cv.drawCentredString(cx, oy + FH - 40, "RIVERS ROCK")
        bio = ["Groupe rouennais formé en 2024", "au centre Éducation et Formation", "du Petit-Quevilly.",
               "", "Rosaria — batterie", "Christophe — basse", "Nicolas — guitare",
               "David — guitare / chant", "Virginie — chant", "", "Rock — Pop-Rock — Indé — Alternatif"]
        cv.setFillColor(Color(1, 1, 1, alpha=0.75))
        cv.setFont("Raleway", 7)
        y = oy + FH - 80
        for line in bio:
            cv.drawCentredString(cx, y, line)
            y -= 12
        cv.setFillColor(LUMIERE)
        cv.setFont("Raleway", 7)
        cv.drawCentredString(cx, y - 6, "Contactez-nous pour programmer un concert")
        cv.setFillColor(Color(1, 1, 1, alpha=0.4))
        cv.setFont("Raleway", 6)
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
    print(f"[Ponts & Lumière] Flyer → {path}")


# ── Social ──

def gen_social():
    def lerp(c1, c2, t):
        return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))

    font_teko = ImageFont.truetype(BEBAS_PATH, 64)
    font_teko_m = ImageFont.truetype(BEBAS_PATH, 46)
    font_raleway = ImageFont.truetype(MONTSERRAT_PATH, 24)
    font_tag = ImageFont.truetype(MONTSERRAT_PATH, 16)

    w, h = 1080, 1080
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    for i in range(200):
        t = i / 199
        draw.rectangle([0, i * h / 200, w, (i + 1) * h / 200],
                       fill=lerp(NUIT_PIL, SEINE_PIL, t))

    img = pillow_grain_overlay(img, 0.04, seed=10)

    bridge_logo_pillow(draw, w / 2, 140, 2.5)
    bbox = draw.textbbox((0, 0), "RIVERS ROCK", font=font_teko)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 155), "RIVERS ROCK", fill=LUMIERE_PIL, font=font_teko)

    bbox = draw.textbbox((0, 0), "PROCHAIN CONCERT", font=font_raleway)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 380), "PROCHAIN CONCERT", fill=LUMIERE_PIL, font=font_raleway)
    bbox = draw.textbbox((0, 0), "[DATE]", font=font_teko_m)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 440), "[DATE]", fill=BLANC_PIL, font=font_teko_m)
    bbox = draw.textbbox((0, 0), "[LIEU]", font=font_raleway)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 520), "[LIEU]", fill=(180, 180, 180), font=font_raleway)

    qx, qy, qs = w / 2 - 60, 660, 120
    draw.rectangle([qx, qy, qx + qs, qy + qs], fill=BLANC_PIL, outline=LUMIERE_PIL, width=3)
    qr_img = draw_qr_pillow(None, 0, 0, qs - 12, fill_color=NUIT_PIL)
    if qr_img:
        img.paste(qr_img, (int(qx + 6), int(qy + 6)), qr_img if qr_img.mode == "RGBA" else None)

    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((qx + (qs - tw) / 2, qy + (qs - th) / 2), "QR", fill=NUIT_PIL, font=font_raleway)

    bbox = draw.textbbox((0, 0), "@riversrockrouen", font=font_tag)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 860), "@riversrockrouen", fill=(180, 180, 180), font=font_tag)
    img.save(os.path.join(TMPL, "instagram-post.png"))

    w, h = 1080, 1920
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    cx, cy = w / 2, h / 2
    max_r = math.sqrt(cx**2 + cy**2)
    for i in range(300):
        t = i / 299
        r = max_r * t
        if t < 0.2:
            c = lerp(LUMIERE_PIL, ACIER_PIL, t / 0.2)
        else:
            c = lerp(ACIER_PIL, NUIT_PIL, (t - 0.2) / 0.8)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)

    img = pillow_grain_overlay(img, 0.04, seed=20)

    font_teko_d = ImageFont.truetype(BEBAS_PATH, 120)
    bridge_logo_pillow(draw, w / 2, 180, 3.0)
    bbox = draw.textbbox((0, 0), "RIVERS ROCK", font=font_teko)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 195), "RIVERS ROCK", fill=LUMIERE_PIL, font=font_teko)

    bbox = draw.textbbox((0, 0), "[DATE]", font=font_teko_d)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 650), "[DATE]", fill=LUMIERE_PIL, font=font_teko_d)
    bbox = draw.textbbox((0, 0), "[LIEU]", font=font_raleway)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 840), "[LIEU]", fill=BLANC_PIL, font=font_raleway)

    bbox = draw.textbbox((0, 0), "@riversrockrouen", font=font_tag)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 1750), "@riversrockrouen", fill=(180, 180, 180), font=font_tag)
    img.save(os.path.join(TMPL, "instagram-story.png"))
    print(f"[Ponts & Lumière] Social → {TMPL}")


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
            c = tuple(int(a + (b - a) * t) for a, b in zip(NUIT_PIL, SEINE_PIL))
            draw.rectangle([0, i * h / 120, w, (i + 1) * h / 120], fill=c)

        img = pillow_grain_overlay(img, 0.04, seed=30)

        font_logo = ImageFont.truetype(BEBAS_PATH, logo_s)
        tw = draw.textbbox((0, 0), "RIVERS ROCK", font=font_logo)[2]
        sym_r = logo_s * 0.5
        gap = sym_r * 0.3
        sx = (w - (sym_r * 2 + gap + tw)) / 2
        bridge_logo_pillow(draw, sx + sym_r, h / 2, sym_r / 22.0)
        draw.text((sx + sym_r * 2 + gap, h / 2 - tw * 0.25), "RIVERS ROCK", fill=BLANC_PIL, font=font_logo)

        font_sub = ImageFont.truetype(MONTSERRAT_PATH, 14)
        sub = "Reprises rock — Rouen"
        sb = draw.textbbox((0, 0), sub, font=font_sub)
        draw.text(((w - (sb[2] - sb[0])) / 2, h - 50), sub, fill=LUMIERE_PIL, font=font_sub)
        img.save(os.path.join(TMPL, name))
    print(f"[Ponts & Lumière] Banners → {TMPL}")


# ── Avatar ──

def gen_avatar():
    S = 500
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    bridge_logo_pillow(draw, S / 2, S / 2, 6.0)
    font = ImageFont.truetype(BEBAS_PATH, 30)
    bbox = draw.textbbox((0, 0), "RR", font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((S - tw) / 2, S / 2 + 60), "RR", fill=LUMIERE_PIL, font=font)
    img.save(os.path.join(TMPL, "avatar.png"))
    print(f"[Ponts & Lumière] Avatar → {TMPL}")


# ── Stickers ──

def gen_stickers():
    from reportlab.lib.units import mm
    W, H = A4
    SR = 40 * mm
    MX = (W - 2 * SR * 2) / 3
    MY = (H - 3 * SR * 2) / 4
    centers = [(MX + SR + c * (MX + SR * 2), MY + SR + r * (MY + SR * 2)) for c in range(2) for r in range(3)]

    path = os.path.join(PDF, "stickers-ponts-lumiere.pdf")
    cv = canvas.Canvas(path, pagesize=A4)

    for cx, cy in centers:
        for i in range(60):
            t = i / 59
            r = NUIT.red + (SEINE.red - NUIT.red) * t
            g = NUIT.green + (SEINE.green - NUIT.green) * t
            b = NUIT.blue + (SEINE.blue - NUIT.blue) * t
            cv.setFillColor(Color(r, g, b))
            y = cy - SR + i * SR * 2 / 60
            cv.rect(cx - SR, y, SR * 2, SR * 2 / 60 + 0.5, stroke=0, fill=1)
        cv.setStrokeColor(BLANC)
        cv.setLineWidth(1.5)
        cv.circle(cx, cy, SR, stroke=1, fill=0)
        sr = SR * 0.50
        bridge_logo_reportlab(cv, cx, cy, sr / 22.0)
        cv.setFillColor(BLANC)
        cv.setFont("Teko", 7)
        cv.drawCentredString(cx, cy + sr + 8, "RIVERS ROCK")
    cv.save()
    print(f"[Ponts & Lumière] Stickers → {path}")


# ── T-shirt ──

def gen_tshirt():
    from reportlab.lib.units import mm
    w, h = A4
    sizes = [("S", 22 * mm, w / 4, h - 200), ("M", 28 * mm, w * 3 / 4, h - 200),
             ("L", 34 * mm, w / 4, h - 440), ("XL", 40 * mm, w * 3 / 4, h - 440)]
    path = os.path.join(PDF, "tshirt-ponts-lumiere.pdf")
    cv = canvas.Canvas(path, pagesize=A4)
    cv.setFillColor(Color(0, 0, 0, alpha=0.04))
    cv.rect(0, 0, w, h, stroke=0, fill=1)
    for label, sr, cx, cy in sizes:
        bridge_logo_reportlab(cv, cx, cy, sr / 22.0)
        cv.setFillColor(BLANC)
        cv.setFont("Teko", max(10, int(sr * 1.6)))
        cv.drawCentredString(cx, cy + sr * 0.6 + 4, "RIVERS ROCK")
        if label:
            cv.setFillColor(Color(0, 0, 0, alpha=0.3))
            cv.setFont("Raleway", 7)
            cv.drawCentredString(cx, cy + sr + 60, label)
    cv.save()
    print(f"[Ponts & Lumière] T-shirt → {path}")


# ── Animated logo ──

def gen_animated():
    html = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rivers Rock — Ponts &amp; Lumiere</title>
<link href="https://fonts.googleapis.com/css2?family=Teko:wght@400;600&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0}
body{width:1080px;height:1920px;overflow:hidden;background:#0D1B2A;display:flex;align-items:center;justify-content:center}
canvas{position:absolute;top:0;left:0;width:1080px;height:1920px}
svg{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:400px;height:400px;overflow:visible}
.cable-l{fill:none;stroke:#E0E1DD;stroke-width:2;stroke-dasharray:300;stroke-dashoffset:300;animation:drawCableL 1s ease-out .3s forwards}
.cable-r{fill:none;stroke:#E0E1DD;stroke-width:2;stroke-dasharray:300;stroke-dashoffset:300;animation:drawCableR 1s ease-out .3s forwards}
.cable-accent-l{fill:none;stroke:#FFB703;stroke-width:1.5;stroke-dasharray:300;stroke-dashoffset:300;animation:drawCableL 1.2s ease-out .7s forwards}
.cable-accent-r{fill:none;stroke:#FFB703;stroke-width:1.5;stroke-dasharray:300;stroke-dashoffset:300;animation:drawCableR 1.2s ease-out .7s forwards}
@keyframes drawCableL{to{stroke-dashoffset:0}}
@keyframes drawCableR{to{stroke-dashoffset:0}}
.flare{opacity:0;animation:flareOn .4s ease-out 1.6s forwards}
.flare circle{animation:pulseLight 2s ease-in-out infinite alternate}
@keyframes flareOn{to{opacity:1}}
@keyframes pulseLight{0%{r:3;opacity:1}100%{r:6;opacity:0.5}}
.letter{font-family:'Teko',sans-serif;font-size:40px;font-weight:600;fill:#fff;opacity:0}
.lRI{animation:slideFrom .5s ease-out 2.2s forwards}
.lV{animation:slideFrom .5s ease-out 2.35s forwards}
.lE{animation:slideFrom .5s ease-out 2.5s forwards}
.lR2{animation:slideFrom .5s ease-out 2.65s forwards}
.lS{animation:slideFromR .5s ease-out 2.2s forwards}
.lR{animation:slideFromR .5s ease-out 2.35s forwards}
@keyframes slideFrom{0%{opacity:0;transform:translateX(-60px)}100%{opacity:1;transform:translateX(0)}}
@keyframes slideFromR{0%{opacity:0;transform:translateX(60px)}100%{opacity:1;transform:translateX(0)}}
.lROCK_R{animation:slide .4s ease-out 2.9s forwards}
.lROCK_O{animation:slide .4s ease-out 3.0s forwards}
.lROCK_C{animation:slide .4s ease-out 3.1s forwards}
.lROCK_K{animation:slide .4s ease-out 3.2s forwards}
@keyframes slide{0%{opacity:0;transform:translateX(150px)}100%{opacity:1;transform:translateX(0)}}
</style>
</head>
<body>
<canvas id="p"></canvas>
<svg viewBox="-200 -200 400 400">
  <path class="cable-l" d="M-160,80 Q-80,-20 0,30"/>
  <path class="cable-r" d="M160,80 Q80,-20 0,30"/>
  <path class="cable-accent-l" d="M-160,90 Q-80,-10 0,40"/>
  <path class="cable-accent-r" d="M160,90 Q80,-10 0,40"/>
  <g class="flare">
    <circle cx="0" cy="35" r="3" fill="#FFB703"/>
    <circle cx="0" cy="35" r="8" fill="rgba(255,183,3,0.2)"/>
  </g>
  <text x="-80" y="-52.9" text-anchor="middle" class="letter lRI">R</text>
  <text x="-45" y="-71.4" text-anchor="middle" class="letter lV">V</text>
  <text x="-10" y="-79.1" text-anchor="middle" class="letter lE">E</text>
  <text x="25" y="-71.4" text-anchor="middle" class="letter lR2">R</text>
  <text x="50" y="-52.9" text-anchor="middle" class="letter lS">S</text>
  <text x="-25" y="60" text-anchor="middle" class="letter lR">R</text>
  <text x="0" y="65" text-anchor="middle" class="letter lI">I</text>
  <text x="-30" y="80" text-anchor="middle" class="letter lROCK_R" font-size="32">R</text>
  <text x="-10" y="84" text-anchor="middle" class="letter lROCK_O" font-size="32">O</text>
  <text x="10" y="84" text-anchor="middle" class="letter lROCK_C" font-size="32">C</text>
  <text x="30" y="80" text-anchor="middle" class="letter lROCK_K" font-size="32">K</text>
</svg>
<script>
const c=document.getElementById('p'),ctx=c.getContext('2d');
c.width=1080;c.height=1920;
const ps=[];
for(let i=0;i<30;i++){ps.push({x:Math.random()*1080,y:Math.random()*1920,s:Math.random()*3+1,a:Math.random()*0.04+0.01})}
function draw(){ctx.clearRect(0,0,1080,1920);
ctx.fillStyle='#0D1B2A';ctx.fillRect(0,0,1080,1920);
const g=ctx.createRadialGradient(540,860,0,540,860,1200);
g.addColorStop(0,'rgba(255,183,3,0.08)');g.addColorStop(1,'rgba(13,27,42,0)');
ctx.fillStyle=g;ctx.fillRect(0,0,1080,1920);
for(const p of ps){ctx.beginPath();ctx.arc(p.x,p.y,p.s,0,Math.PI*2);ctx.fillStyle='rgba(255,183,3,'+p.a+')';ctx.fill();p.y-=0.3;if(p.y<0){p.y=1920;p.x=Math.random()*1080}}
requestAnimationFrame(draw)}draw();
</script>
</body>
</html>'''
    path = os.path.join(TMPL, "logo-animated-ponts-lumiere.html")
    with open(path, "w") as f:
        f.write(html)
    print(f"[Ponts & Lumiere] Animated logo → {path}")
def gen_site():
    html = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rivers Rock — Ponts &amp; Lumière</title>
<link href="https://fonts.googleapis.com/css2?family=Teko:wght@400;600&family=Raleway:wght@300;400;600&family=DM+Mono&display=swap" rel="stylesheet">
<style>
:root{--nuit:#0D1B2A;--acier:#415A77;--lumiere:#FFB703;--seine:#1B263B;--brouillard:#E0E1DD;--blanc:#fff}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:'Raleway',sans-serif;font-weight:300;color:var(--blanc);min-height:100vh;background:linear-gradient(135deg,var(--nuit),var(--seine))}
.bg-grain{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23g)' opacity='0.04'/%3E%3C/svg%3E")}
nav{position:fixed;top:0;width:100%;padding:14px 32px;display:flex;justify-content:space-between;align-items:center;z-index:100;background:rgba(13,27,42,0.9);backdrop-filter:blur(8px);border-bottom:1px solid rgba(255,183,3,0.12)}
nav .logo-small{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--blanc)}
nav .logo-small svg{width:28px;height:28px}
nav .logo-small span{font-family:'Teko',sans-serif;font-size:18px;letter-spacing:1px;text-transform:uppercase}
nav a{color:rgba(255,255,255,0.78);text-decoration:none;font-size:12px;font-weight:400;letter-spacing:1px;text-transform:uppercase;padding:6px 14px;transition:.3s}
nav a:hover{color:var(--lumiere)}
.hero{position:relative;z-index:1;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:120px 24px 80px;background:radial-gradient(ellipse at 50% 38%, rgba(255,183,3,0.08) 0%, transparent 60%)}
.hero .logo-hero svg{width:200px;height:80px;margin-bottom:12px}
.hero h1{font-family:'Teko',sans-serif;font-size:clamp(48px,10vw,80px);letter-spacing:4px;text-transform:uppercase;color:var(--blanc);margin-bottom:4px}
.hero .tagline{font-family:'DM Mono',monospace;font-size:13px;color:var(--lumiere);letter-spacing:2px;text-transform:uppercase;margin-bottom:28px}
.hero p{font-size:15px;line-height:1.7;color:rgba(255,255,255,0.82);max-width:500px}
.section{position:relative;z-index:1;padding:80px 24px;max-width:700px;margin:0 auto}
.section h2{font-family:'Teko',sans-serif;font-size:38px;letter-spacing:2px;text-transform:uppercase;color:var(--lumiere);margin-bottom:32px;text-align:center}
.section h2::after{content:'';display:block;width:60px;height:2px;background:var(--lumiere);margin:8px auto 0}
.section p{font-size:15px;line-height:1.8;color:rgba(255,255,255,0.7);margin-bottom:20px}
.section-alt{background:rgba(27,38,59,0.2);border-top:1px solid rgba(255,183,3,0.06);border-bottom:1px solid rgba(255,183,3,0.06)}
.members-grid{display:flex;flex-wrap:wrap;justify-content:center;gap:20px;margin-top:20px}
.member-card{flex:0 0 180px;text-align:center;padding:24px 12px;background:rgba(65,90,119,0.12);border-radius:4px;border:1px solid rgba(255,255,255,0.06);transition:.25s}
.member-card:hover{background:rgba(65,90,119,0.2);transform:scale(1.03)}
.member-card .avatar-circle{width:68px;height:68px;border-radius:50%;background:linear-gradient(135deg,var(--acier),var(--seine));margin:0 auto 10px;display:flex;align-items:center;justify-content:center;font-family:'Teko',sans-serif;font-size:28px;color:var(--lumiere)}
.member-card h3{font-family:'Teko',sans-serif;font-size:18px;letter-spacing:1px;color:var(--lumiere);margin-bottom:3px}
.member-card p{font-family:'Raleway',sans-serif;font-size:11px;color:rgba(255,255,255,0.4);letter-spacing:1px;text-transform:uppercase}
.concerts-list{list-style:none;padding:0}
.concerts-list li{padding:14px 20px;margin-bottom:10px;background:rgba(27,38,59,0.3);border-radius:4px;border-left:3px solid var(--lumiere);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px}
.concerts-list .date{font-family:'DM Mono',monospace;font-size:14px;color:var(--lumiere)}
.concerts-list .lieu{font-size:14px;color:rgba(255,255,255,0.78)}
.concerts-list .status{font-size:11px;padding:3px 10px;border-radius:4px;background:rgba(255,183,3,0.1);color:var(--lumiere)}
.contact-info{text-align:center;margin-top:16px}
.contact-info p{font-size:15px;margin-bottom:6px}
.contact-info .email{font-family:'DM Mono',monospace;font-size:16px;color:var(--lumiere);text-decoration:none;transition:.2s}
.contact-info .email:hover{color:var(--brouillard)}
.links-social{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:24px}
.links-social a{color:rgba(255,255,255,0.78);text-decoration:none;font-family:'DM Mono',monospace;font-size:12px;padding:8px 18px;border:1px solid rgba(255,183,3,0.25);border-radius:4px;transition:.3s;letter-spacing:1px;text-transform:uppercase}
.links-social a:hover{color:var(--blanc);border-color:var(--lumiere);background:rgba(255,183,3,0.06)}
.footer{position:relative;z-index:1;text-align:center;padding:44px 24px;border-top:1px solid rgba(255,183,3,0.06)}
.footer svg{width:120px;height:40px;margin-bottom:10px;opacity:0.3}
.footer p{font-family:'DM Mono',monospace;font-size:11px;letter-spacing:4px;color:rgba(255,255,255,0.45)}@media(max-width:400px){
  .hero h1{font-size:36px}
  .member-card{flex:0 0 140px}
  nav a{font-size:10px}
  .section{padding:40px 12px}
}
</style>
</head>
<body>
<div class="bg-grain"></div>
<nav>
  <a href="#" class="logo-small">
    <svg viewBox="0 0 100 40"><path d="M0,35 Q25,5 50,20 Q75,5 100,35" fill="none" stroke="#FFB703" stroke-width="2"/><path d="M0,38 Q25,8 50,23 Q75,8 100,38" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="1.5"/></svg>
    <span>Rivers Rock</span>
  </a>
  <div>
    <a href="#groupe">Le groupe</a>
    <a href="#concerts">Concerts</a>
    <a href="#contact">Contact</a>
  </div>
</nav>
<section class="hero">
  <div class="logo-hero">
    <svg viewBox="0 0 200 80"><path d="M10,70 Q50,10 100,30 Q150,10 190,70" fill="none" stroke="#E0E1DD" stroke-width="2"/><path d="M10,76 Q50,16 100,36 Q150,16 190,76" fill="none" stroke="#FFB703" stroke-width="1.5"/><circle cx="100" cy="33" r="4" fill="#FFB703"/></svg>
  </div>
  <h1>RIVERS ROCK</h1>
  <div class="tagline">Reprises rock — Rouen</div>
  <p>Groupe rouennais formé en 2024. Rock, pop-rock, indé et alternatif. La Seine et ses ponts, la nuit.</p>
</section>
<section id="groupe" class="section">
  <h2>Le groupe</h2>
  <p>Cinq musiciens, une passion commune : faire vibrer la scène rouennaise avec des reprises qui décoiffent.</p>
  <div class="members-grid">
    <div class="member-card"><div class="avatar-circle">R</div><h3>Rosaria</h3><p>Batterie</p></div>
    <div class="member-card"><div class="avatar-circle">C</div><h3>Christophe</h3><p>Basse</p></div>
    <div class="member-card"><div class="avatar-circle">N</div><h3>Nicolas</h3><p>Guitare</p></div>
    <div class="member-card"><div class="avatar-circle">D</div><h3>David</h3><p>Guitare / Chant</p></div>
    <div class="member-card"><div class="avatar-circle">V</div><h3>Virginie</h3><p>Chant</p></div>
  </div>
</section>
<section id="concerts" class="section section-alt">
  <h2>Concerts</h2>
  <p>Contactez-nous pour programmer un concert.</p>
  <ul class="concerts-list"><li><span class="date">À venir</span><span class="lieu">Contactez-nous</span><span class="status">Sur demande</span></li></ul>
</section>
<section id="musique" class="section">
  <h2>Musique</h2>
  <p>Decouvrez Rivers Rock en action &mdash; extraits live et playlist a venir.</p>
  <div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:8px;margin-top:16px">
    <iframe src="https://www.youtube.com/embed/" style="position:absolute;top:0;left:0;width:100%;height:100%;border:none" allowfullscreen></iframe>
  </div>
</section>
<section id="contact" class="section section-alt">
  <h2>Contact</h2>
  <div class="contact-info"><p>Pour toute demande :</p><a class="email" href="mailto:riversrockrouen@gmail.com">riversrockrouen@gmail.com</a></div>
  <div class="links-social">
    <a href="https://www.instagram.com/riversrockrouen" target="_blank">Instagram</a>
    <a href="https://www.facebook.com/RiversRockRouen" target="_blank">Facebook</a>
    <a href="https://www.youtube.com/@RiversRockRouen" target="_blank">YouTube</a>
  </div>
</section>
<footer class="footer">
  <svg viewBox="0 0 120 40"><path d="M10,35 Q30,10 60,25 Q90,10 110,35" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="1"/></svg>
  <p>R O U E N</p>
</footer>
</body>
</html>'''
    dst = os.path.join(OUT, "index.html")
    with open(dst, "w") as f:
        f.write(html)
    print(f"[Ponts & Lumière] Site → {dst}")


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
