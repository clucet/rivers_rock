#!/usr/bin/env python3
"""Generate all Sable & Bronze assets — Proposition n°6."""

import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))
from logoutils import (
    create_bleed_canvas, save_with_crop_marks,
    pillow_grain_overlay,
    draw_qr_pillow, BEBAS_PATH, MONTSERRAT_PATH, CINZEL_PATH, LATO_PATH, CORMORANT_PATH,
)
from palette import SABLE_BRONZE as CFG
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

SABLE = CFG.rl("sable")
TERRE = CFG.rl("terre_cuite")
BRONZE = CFG.rl("bronze")
VERT = CFG.rl("vert_palmier")
CREME = CFG.rl("creme")

SABLE_PIL = CFG.pil("sable")
TERRE_PIL = CFG.pil("terre_cuite")
BRONZE_PIL = CFG.pil("bronze")
VERT_PIL = CFG.pil("vert_palmier")
CREME_PIL = CFG.pil("creme")
BLANC_PIL = (255, 255, 255)

pdfmetrics.registerFont(TTFont("Cinzel", CINZEL_PATH))
pdfmetrics.registerFont(TTFont("Lato", LATO_PATH))
pdfmetrics.registerFont(TTFont("Cormorant", CORMORANT_PATH))

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


def sun_logo_reportlab(cv, cx, cy, scale=1.0):
    """Sun circle with radiating triangles."""
    r = 20 * scale
    cv.setFillColor(BRONZE)
    cv.circle(cx, cy, r, stroke=0, fill=1)
    cv.setStrokeColor(Color(1, 1, 1, alpha=0.4))
    cv.setLineWidth(0.5 * scale)
    cv.circle(cx, cy, r + 3 * scale, stroke=1, fill=0)
    for i in range(8):
        a = math.radians(45 * i)
        pts = [(cx + r * 0.6 * math.cos(a), cy + r * 0.6 * math.sin(a)),
               (cx + r * 2.0 * math.cos(a - 0.2), cy + r * 2.0 * math.sin(a - 0.2)),
               (cx + r * 2.0 * math.cos(a + 0.2), cy + r * 2.0 * math.sin(a + 0.2))]
        cv.setFillColor(BRONZE)
        p = cv.beginPath()
        p.moveTo(pts[0][0], pts[0][1])
        p.lineTo(pts[1][0], pts[1][1])
        p.lineTo(pts[2][0], pts[2][1])
        p.close()
        cv.drawPath(p, fill=1, stroke=0)


def sun_logo_pillow(draw, cx, cy, scale=1.0):
    """Sun circle for Pillow."""
    r = 20 * scale
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BRONZE_PIL)
    draw.ellipse([cx - r - 3 * scale, cy - r - 3 * scale, cx + r + 3 * scale, cy + r + 3 * scale],
                 outline=(255, 255, 255, 100), width=max(1, int(scale)))
    for i in range(8):
        a = math.radians(45 * i)
        pts = [(cx + r * 0.6 * math.cos(a), cy + r * 0.6 * math.sin(a)),
               (cx + r * 2.0 * math.cos(a - 0.15), cy + r * 2.0 * math.sin(a - 0.15)),
               (cx + r * 2.0 * math.cos(a + 0.15), cy + r * 2.0 * math.sin(a + 0.15))]
        draw.polygon(pts, fill=BRONZE_PIL)


def draw_geometric_waves(cv, W, H):
    cv.setStrokeColor(Color(0, 0, 0, alpha=0.03))
    for row in range(2):
        y_base = 20 + row * 50
        for x in range(0, int(W), 40):
            cv.line(x, y_base, x + 20, y_base + 15)
            cv.line(x + 20, y_base + 15, x + 40, y_base)


def gen_setlist():
    W, H = A4
    path = os.path.join(PDF, "setlist-sable-bronze.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, W, H)

    for i in range(120):
        t = i / 119
        r = CREME.red / 255 + (SABLE.red / 255 - CREME.red / 255) * t
        g = CREME.green / 255 + (SABLE.green / 255 - CREME.green / 255) * t
        b = CREME.blue / 255 + (SABLE.blue / 255 - CREME.blue / 255) * t
        cv.setFillColor(Color(r, g, b))
        cv.rect(0, i * H / 120, W, H / 120 + 1, stroke=0, fill=1)

    random.seed(42)
    for _ in range(2000):
        cv.setFillColor(Color(0, 0, 0, alpha=random.uniform(0.02, 0.05)))
        cv.circle(random.uniform(0, W), random.uniform(0, H), random.uniform(0.5, 1.5), stroke=0, fill=1)

    draw_geometric_waves(cv, W, H)

    sun_logo_reportlab(cv, W / 2, H - 110, 2.0)
    cv.setFillColor(VERT)
    cv.setFont("Cinzel", 16)
    cv.drawCentredString(W / 2, H - 155, "RIVERS ROCK")
    cv.setFillColor(TERRE)
    cv.setFont("Cinzel", 22)
    cv.drawCentredString(W / 2, H - 185, "SETLIST")

    card_w, card_h, card_r = 250, 74, 8
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
            w = pdfmetrics.stringWidth(longest, "Cinzel", mid) or pdfmetrics.stringWidth(longest, "Lato", mid)
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
        bg = TERRE if is_green else BRONZE

        cv.setFillColor(Color(0, 0, 0, alpha=0.08))
        cv.roundRect(cl + 3, cb - 3, card_w, card_h, card_r, stroke=0, fill=1)

        for i in range(30):
            t = i / 29
            l = 0.15 * (1 - t)
            c = Color(min(1, bg.red + l), min(1, bg.green + l), min(1, bg.blue + l))
            cv.setFillColor(c)
            cv.rect(cl, cb + i * card_h / 30, card_w, card_h / 30 + 0.5, stroke=0, fill=1)

        cv.setStrokeColor(Color(1, 1, 1, alpha=0.35))
        cv.setLineWidth(0.8)
        cv.roundRect(cl, cb, card_w, card_h, card_r, stroke=1, fill=0)

        aw = pdfmetrics.stringWidth(artist, "Cinzel", us)
        if aw == 0:
            aw = pdfmetrics.stringWidth(artist, "Lato", us)
        tw_ = 24 + 8 + aw
        sx = cx - tw_ / 2

        bcy = cy + 15
        cv.setFillColor(CREME)
        cv.circle(sx + 12, bcy, 12, stroke=0, fill=1)
        cv.setFillColor(TERRE)
        cv.setFont("Lato", 12)
        cv.drawCentredString(sx + 12, bcy - 4.5, f"{idx+1:02d}")

        cv.setFillColor(VERT)
        cv.setFont("Cinzel", us)
        cv.drawString(sx + 24 + 8, cy + 6, artist)

        if title:
            cv.setFillColor(Color(0, 0, 0, alpha=0.55))
            ts = 13
            tww = pdfmetrics.stringWidth(title, "Lato", ts)
            if tww > card_w - 32:
                ts *= (card_w - 32) / tww
            cv.setFont("Lato", ts)
            cv.drawCentredString(cx, cy - 17, title)

    cv.setFillColor(Color(0, 0, 0, alpha=0.15))
    cv.setFont("Cormorant", 7)
    text, tr = "R O U E N", 3
    x = W / 2 - (sum(pdfmetrics.stringWidth(c, "Cormorant", 7) for c in text) + tr * (len(text) - 1)) / 2
    for c in text:
        w = pdfmetrics.stringWidth(c, "Cormorant", 7)
        cv.drawString(x, 14, c)
        x += w + tr
    save_with_crop_marks(cv, _, _, bleed)
    print(f"[Sable & Bronze] Setlist → {path}")


def gen_poster():
    W, H = A4
    path = os.path.join(PDF, "poster-sable-bronze.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, W, H)

    for i in range(120):
        t = i / 119
        r = CREME.red / 255 + (SABLE.red / 255 - CREME.red / 255) * t
        g = CREME.green / 255 + (SABLE.green / 255 - CREME.green / 255) * t
        b = CREME.blue / 255 + (SABLE.blue / 255 - CREME.blue / 255) * t
        cv.setFillColor(Color(r, g, b))
        cv.rect(0, i * H / 120, W, H / 120 + 1, stroke=0, fill=1)

    random.seed(42)
    for _ in range(2000):
        cv.setFillColor(Color(0, 0, 0, alpha=random.uniform(0.02, 0.05)))
        cv.circle(random.uniform(0, W), random.uniform(0, H), random.uniform(0.5, 1.5), stroke=0, fill=1)

    sun_logo_reportlab(cv, W / 2, H - 190, 2.0)
    cv.setFillColor(VERT)
    cv.setFont("Cinzel", 12)
    cv.drawCentredString(W / 2, H - 250, "RIVERS ROCK")
    cv.setFillColor(TERRE)
    cv.setFont("Lato", 12)
    cv.drawCentredString(W / 2, H - 275, "LES SOIREES NOCTURNES")
    cv.setFillColor(VERT)
    cv.setFont("Cinzel", 48)
    cv.drawCentredString(W / 2, H - 340, "SAM 26 JUIN 2026")
    cv.setFillColor(Color(0, 0, 0, alpha=0.5))
    cv.setFont("Lato", 16)
    cv.drawCentredString(W / 2, H - 375, "Montigny · 19h30")
    cv.setStrokeColor(TERRE)
    cv.setLineWidth(0.8)
    cv.line(W / 2 - 60, H - 400, W / 2 + 60, H - 400)
    cv.setFillColor(Color(0, 0, 0, alpha=0.15))
    cv.setFont("Cormorant", 7)
    text, tr = "R O U E N", 3
    x = W / 2 - (sum(pdfmetrics.stringWidth(c, "Cormorant", 7) for c in text) + tr * (len(text) - 1)) / 2
    for c in text:
        w = pdfmetrics.stringWidth(c, "Cormorant", 7)
        cv.drawString(x, 14, c)
        x += w + tr
    save_with_crop_marks(cv, _, _, bleed)
    print(f"[Sable & Bronze] Poster → {path}")


def gen_flyer():
    FW, FH = A6
    path = os.path.join(PDF, "flyer-sable-bronze.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, A4[0], A4[1])

    def grad(cv, x, y, w, h):
        for i in range(60):
            t = i / 59
            r = CREME.red / 255 + (SABLE.red / 255 - CREME.red / 255) * t
            g = CREME.green / 255 + (SABLE.green / 255 - CREME.green / 255) * t
            b = CREME.blue / 255 + (SABLE.blue / 255 - CREME.blue / 255) * t
            cv.setFillColor(Color(r, g, b))
            cv.rect(x, y + i * h / 60, w, h / 60 + 0.5, stroke=0, fill=1)

    def draw_recto(cv, ox, oy):
        grad(cv, ox, oy, FW, FH)
        cx = ox + FW / 2
        sun_logo_reportlab(cv, cx, oy + FH - 50, 1.0)
        cv.setFillColor(VERT)
        cv.setFont("Cinzel", 14)
        cv.drawCentredString(cx, oy + FH - 80, "RIVERS ROCK")
        cv.setFillColor(TERRE)
        cv.setFont("Cinzel", 28)
        cv.drawCentredString(cx, oy + FH - 145, "SAM 26 JUIN 2026")
        cv.setFillColor(Color(0, 0, 0, alpha=0.5))
        cv.setFont("Lato", 10)
        cv.drawCentredString(cx, oy + FH - 175, "Montigny · 19h30")

    def draw_verso(cv, ox, oy):
        grad(cv, ox, oy, FW, FH)
        cx = ox + FW / 2
        cv.setFillColor(VERT)
        cv.setFont("Cinzel", 14)
        cv.drawCentredString(cx, oy + FH - 40, "RIVERS ROCK")
        bio = ["Groupe rouennais formé en 2024", "au centre Éducation et Formation", "du Petit-Quevilly.",
               "", "Rosaria - batterie", "Christophe - basse", "Nicolas - guitare",
               "David - guitare / chant", "Virginie - chant", "", "Rock - Pop-Rock - Indé - Alternatif"]
        cv.setFillColor(Color(0, 0, 0, alpha=0.65))
        cv.setFont("Lato", 7)
        y = oy + FH - 80
        for line in bio:
            cv.drawCentredString(cx, y, line)
            y -= 12
        cv.setFillColor(TERRE)
        cv.setFont("Lato", 7)
        cv.drawCentredString(cx, y - 6, "Contactez-nous pour programmer un concert")
        cv.setFillColor(Color(0, 0, 0, alpha=0.35))
        cv.setFont("Cormorant", 7)
        cv.drawCentredString(cx, y - 22, "@riversrockrouen - riversrockrouen@gmail.com")

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
    print(f"[Sable & Bronze] Flyer → {path}")


def gen_social():
    def lerp(c1, c2, t):
        return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))

    font_cinzel = ImageFont.truetype(CINZEL_PATH, 56)
    font_cinzel_m = ImageFont.truetype(CINZEL_PATH, 40)
    font_lato = ImageFont.truetype(LATO_PATH, 22)
    font_tag = ImageFont.truetype(LATO_PATH, 14)

    w, h = 1080, 1080
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    for i in range(200):
        t = i / 199
        draw.rectangle([0, i * h / 200, w, (i + 1) * h / 200], fill=lerp(CREME_PIL, SABLE_PIL, t))

    img = pillow_grain_overlay(img, 0.05, seed=10)

    sun_logo_pillow(draw, w / 2, 140, 2.5)
    bbox = draw.textbbox((0, 0), "RIVERS ROCK", font=font_cinzel)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 155), "RIVERS ROCK", fill=VERT_PIL, font=font_cinzel)

    bbox = draw.textbbox((0, 0), "LES SOIREES NOCTURNES", font=font_lato)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 380), "LES SOIREES NOCTURNES", fill=TERRE_PIL, font=font_lato)
    bbox = draw.textbbox((0, 0), "SAM 26 JUIN 2026", font=font_cinzel_m)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 440), "SAM 26 JUIN 2026", fill=VERT_PIL, font=font_cinzel_m)
    bbox = draw.textbbox((0, 0), "Montigny · 19h30", font=font_lato)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 520), "Montigny · 19h30", fill=(100, 80, 60), font=font_lato)

    qx, qy, qs = w / 2 - 60, 660, 120
    draw.rectangle([qx, qy, qx + qs, qy + qs], fill=BLANC_PIL, outline=TERRE_PIL, width=3)
    qr_img = draw_qr_pillow(None, 0, 0, qs - 12, fill_color=VERT_PIL)
    if qr_img:
        img.paste(qr_img, (int(qx + 6), int(qy + 6)), qr_img if qr_img.mode == "RGBA" else None)

    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((qx + (qs - tw) / 2, qy + (qs - th) / 2), "QR", fill=VERT_PIL, font=font_lato)

    bbox = draw.textbbox((0, 0), "@riversrockrouen", font=font_tag)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 860), "@riversrockrouen", fill=(100, 80, 60), font=font_tag)
    img.save(os.path.join(TMPL, "instagram-post.png"))

    w, h = 1080, 1920
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    cx, cy = w / 2, h / 2
    mr = math.sqrt(cx**2 + cy**2)
    for i in range(300):
        t = i / 299
        r = mr * t
        if t < 0.2:
            c = lerp(TERRE_PIL, BRONZE_PIL, t / 0.2)
        else:
            c = lerp(BRONZE_PIL, SABLE_PIL, (t - 0.2) / 0.8)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)

    img = pillow_grain_overlay(img, 0.05, seed=20)

    font_cinzel_d = ImageFont.truetype(CINZEL_PATH, 100)
    sun_logo_pillow(draw, w / 2, 180, 3.0)
    bbox = draw.textbbox((0, 0), "RIVERS ROCK", font=font_cinzel)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2 + 20, 195), "RIVERS ROCK", fill=VERT_PIL, font=font_cinzel)

    bbox = draw.textbbox((0, 0), "SAM 26 JUIN 2026", font=font_cinzel_d)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 650), "SAM 26 JUIN 2026", fill=TERRE_PIL, font=font_cinzel_d)
    bbox = draw.textbbox((0, 0), "Montigny · 19h30", font=font_lato)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 840), "Montigny · 19h30", fill=(100, 80, 60), font=font_lato)

    bbox = draw.textbbox((0, 0), "@riversrockrouen", font=font_tag)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 1750), "@riversrockrouen", fill=(100, 80, 60), font=font_tag)
    img.save(os.path.join(TMPL, "instagram-story.png"))
    print(f"[Sable & Bronze] Social → {TMPL}")


def gen_banners():
    for name, w, h, logo_s in [
        ("facebook-banner.png", 1640, 624, 48),
        ("youtube-banner.png", 2560, 1440, 72),
    ]:
        img = Image.new("RGB", (w, h))
        draw = ImageDraw.Draw(img)
        for i in range(120):
            t = i / 119
            c = tuple(int(a + (b - a) * t) for a, b in zip(SABLE_PIL, CREME_PIL))
            draw.rectangle([0, i * h / 120, w, (i + 1) * h / 120], fill=c)

        img = pillow_grain_overlay(img, 0.05, seed=30)

        font_logo = ImageFont.truetype(CINZEL_PATH, logo_s)
        tw = draw.textbbox((0, 0), "RIVERS ROCK", font=font_logo)[2]
        sym_r = logo_s * 0.5
        gap = sym_r * 0.3
        sx = (w - (sym_r * 2 + gap + tw)) / 2
        sun_logo_pillow(draw, sx + sym_r, h / 2, sym_r / 22.0)
        draw.text((sx + sym_r * 2 + gap, h / 2 - tw * 0.25), "RIVERS ROCK", fill=VERT_PIL, font=font_logo)

        font_sub = ImageFont.truetype(LATO_PATH, 14)
        sub = "Reprises rock - Rouen"
        sb = draw.textbbox((0, 0), sub, font=font_sub)
        draw.text(((w - (sb[2] - sb[0])) / 2, h - 50), sub, fill=TERRE_PIL, font=font_sub)
        img.save(os.path.join(TMPL, name))
    print(f"[Sable & Bronze] Banners → {TMPL}")


def gen_avatar():
    S = 500
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    sun_logo_pillow(draw, S / 2, S / 2, 6.0)
    font = ImageFont.truetype(CINZEL_PATH, 28)
    bbox = draw.textbbox((0, 0), "RR", font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((S - tw) / 2, S / 2 + 60), "RR", fill=TERRE_PIL, font=font)
    img.save(os.path.join(TMPL, "avatar.png"))
    print(f"[Sable & Bronze] Avatar → {TMPL}")


def gen_stickers():
    from reportlab.lib.units import mm
    W, H = A4
    SR = 40 * mm
    MX = (W - 2 * SR * 2) / 3
    MY = (H - 3 * SR * 2) / 4
    centers = [(MX + SR + c * (MX + SR * 2), MY + SR + r * (MY + SR * 2)) for c in range(2) for r in range(3)]

    path = os.path.join(PDF, "stickers-sable-bronze.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, A4[0], A4[1])

    for cx, cy in centers:
        for i in range(60):
            t = i / 59
            r = SABLE.red / 255 + (BRONZE.red / 255 - SABLE.red / 255) * t
            g = SABLE.green / 255 + (BRONZE.green / 255 - SABLE.green / 255) * t
            b = SABLE.blue / 255 + (BRONZE.blue / 255 - SABLE.blue / 255) * t
            cv.setFillColor(Color(r, g, b))
            y = cy - SR + i * SR * 2 / 60
            cv.rect(cx - SR, y, SR * 2, SR * 2 / 60 + 0.5, stroke=0, fill=1)
        cv.setStrokeColor(TERRE)
        cv.setLineWidth(2)
        cv.circle(cx, cy, SR, stroke=1, fill=0)
        sr = SR * 0.50
        sun_logo_reportlab(cv, cx, cy, sr / 22.0)
        cv.setFillColor(VERT)
        cv.setFont("Cinzel", 7)
        cv.drawCentredString(cx, cy + sr + 8, "RIVERS ROCK")
    save_with_crop_marks(cv, _, _, bleed)
    print(f"[Sable & Bronze] Stickers → {path}")


def gen_tshirt():
    from reportlab.lib.units import mm
    w, h = A4
    sizes = [("S", 22 * mm, w / 4, h - 200), ("M", 28 * mm, w * 3 / 4, h - 200),
             ("L", 34 * mm, w / 4, h - 440), ("XL", 40 * mm, w * 3 / 4, h - 440)]
    path = os.path.join(PDF, "tshirt-sable-bronze.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, A4[0], A4[1])
    cv.setFillColor(Color(0, 0, 0, alpha=0.04))
    cv.rect(0, 0, w, h, stroke=0, fill=1)
    for label, sr, cx, cy in sizes:
        sun_logo_reportlab(cv, cx, cy, sr / 22.0)
        cv.setFillColor(VERT)
        cv.setFont("Cinzel", max(8, int(sr * 1.4)))
        cv.drawCentredString(cx, cy + sr * 0.6 + 4, "RIVERS ROCK")
        if label:
            cv.setFillColor(Color(0, 0, 0, alpha=0.3))
            cv.setFont("Lato", 7)
            cv.drawCentredString(cx, cy + sr + 60, label)
    save_with_crop_marks(cv, _, _, bleed)
    print(f"[Sable & Bronze] T-shirt → {path}")


def gen_animated():
    html = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rivers Rock — Sable &amp; Bronze</title>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0}
body{width:1080px;height:1920px;overflow:hidden;background:linear-gradient(135deg,#D4A373,#FEFAE0);display:flex;align-items:center;justify-content:center}
canvas{position:absolute;top:0;left:0;width:1080px;height:1920px}
svg{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:400px;height:400px;overflow:visible}
.sun-group{opacity:0;animation:sunRise .8s ease-out .3s forwards}
@keyframes sunRise{0%{opacity:0;transform:translateY(120px)}100%{opacity:1;transform:translateY(0)}}
.sun{fill:#B5835A}
.ring{fill:none;stroke:rgba(0,0,0,0.06);stroke-width:1.5;stroke-dasharray:3 3}
.ray{fill:#B5835A;opacity:0}
.r1{animation:raySpread .5s ease-out .8s forwards}
.r2{animation:raySpread .5s ease-out .95s forwards}
.r3{animation:raySpread .5s ease-out 1.1s forwards}
.r4{animation:raySpread .5s ease-out 1.25s forwards}
@keyframes raySpread{0%{opacity:0;transform:scale(0)}100%{opacity:1;transform:scale(1)}}
.glow{position:absolute;top:50%;left:50%;width:400px;height:400px;margin:-200px;background:radial-gradient(circle,rgba(255,255,255,0.12) 0%,transparent 70%);opacity:0;animation:glowSpread 1s ease-out 1.5s forwards}
@keyframes glowSpread{0%{opacity:0;transform:scale(0.5)}100%{opacity:1;transform:scale(1)}}
.letter{font-family:'Cinzel',serif;font-size:28px;fill:#2D6A4F;opacity:0}
.lR{animation:riseBlur .5s ease-out 2.0s forwards}
.lI{animation:riseBlur .5s ease-out 2.15s forwards}
.lV{animation:riseBlur .5s ease-out 2.3s forwards}
.lE{animation:riseBlur .5s ease-out 2.45s forwards}
.lR2{animation:riseBlur .5s ease-out 2.6s forwards}
.lS{animation:riseBlur .5s ease-out 2.75s forwards}
@keyframes riseBlur{0%{opacity:0;transform:translateY(40px);filter:blur(8px)}100%{opacity:1;transform:translateY(0);filter:blur(0)}}
.lROCK_R{animation:slide .4s ease-out 3.1s forwards}
.lROCK_O{animation:slide .4s ease-out 3.25s forwards}
.lROCK_C{animation:slide .4s ease-out 3.4s forwards}
.lROCK_K{animation:slide .4s ease-out 3.55s forwards}
@keyframes slide{0%{opacity:0;transform:translateX(150px)}100%{opacity:1;transform:translateX(0)}}
.rays-rotate{animation:spinSlow 25s linear infinite;transform-origin:0 0}
@keyframes spinSlow{0%{transform:rotate(0deg)}100%{transform:rotate(360deg)}}
@media(prefers-reduced-motion){*{animation:none!important;transition:none!important}}
</style>
</head>
<body>
<div class="glow"></div>
<canvas id="p"></canvas>
<svg viewBox="-200 -200 400 400">
  <g class="sun-group">
    <circle class="sun" cx="0" cy="0" r="35"/>
    <circle class="ring" cx="0" cy="0" r="40"/>
    <g class="rays-rotate">
      <polygon class="ray r1" points="10,-10 45,-35 30,-5"/>
      <polygon class="ray r2" points="-10,-10 -35,-45 -5,-30"/>
      <polygon class="ray r3" points="10,10 35,45 5,30"/>
      <polygon class="ray r4" points="-10,10 -45,35 -30,5"/>
      <polygon class="ray r1" points="0,-15 0,-50 0,-30" style="animation-delay:1.0s"/>
      <polygon class="ray r2" points="0,15 0,50 0,30" style="animation-delay:1.15s"/>
      <polygon class="ray r3" points="15,0 50,0 30,0" style="animation-delay:1.0s"/>
      <polygon class="ray r4" points="-15,0 -50,0 -30,0" style="animation-delay:1.15s"/>
    </g>
  </g>
  <text x="-60" y="-52.9" text-anchor="middle" class="letter lR">R</text>
  <text x="-36" y="-71.4" text-anchor="middle" class="letter lI">I</text>
  <text x="-12" y="-79.1" text-anchor="middle" class="letter lV">V</text>
  <text x="12" y="-79.1" text-anchor="middle" class="letter lE">E</text>
  <text x="36" y="-71.4" text-anchor="middle" class="letter lR2">R</text>
  <text x="60" y="-52.9" text-anchor="middle" class="letter lS">S</text>
  <text x="-30" y="74.2" text-anchor="middle" class="letter lROCK_R" font-size="22">R</text>
  <text x="-10" y="79.4" text-anchor="middle" class="letter lROCK_O" font-size="22">O</text>
  <text x="10" y="79.4" text-anchor="middle" class="letter lROCK_C" font-size="22">C</text>
  <text x="30" y="74.2" text-anchor="middle" class="letter lROCK_K" font-size="22">K</text>
</svg>
<script>
const c=document.getElementById('p'),ctx=c.getContext('2d');
c.width=1080;c.height=1920;
const ps=[];
for(let i=0;i<25;i++){ps.push({x:Math.random()*1080,y:Math.random()*1920,s:Math.random()*3+1,a:Math.random()*0.04+0.01})}
function draw(){ctx.clearRect(0,0,1080,1920);
ctx.fillStyle='#D4A373';ctx.fillRect(0,0,1080,1920);
const g=ctx.createRadialGradient(540,860,0,540,860,1200);
g.addColorStop(0,'rgba(204,107,73,0.06)');g.addColorStop(1,'rgba(212,163,115,0)');
ctx.fillStyle=g;ctx.fillRect(0,0,1080,1920);
for(const p of ps){ctx.beginPath();ctx.arc(p.x,p.y,p.s,0,Math.PI*2);ctx.fillStyle='rgba(204,107,73,'+p.a+')';ctx.fill();p.y-=0.2;if(p.y<0){p.y=1920;p.x=Math.random()*1080}}
requestAnimationFrame(draw)}draw();
</script>
</body>
</html>'''
    path = os.path.join(TMPL, "logo-animated-sable-bronze.html")
    with open(path, "w") as f:
        f.write(html)
    print(f"[Sable & Bronze] Animated logo → {path}")
def gen_site():
    html = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rivers Rock — Sable &amp; Bronze</title>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600&family=Lato:wght@300;400;600&family=Cormorant:ital@1&display=swap" rel="stylesheet">
<style>
:root{--sable:#D4A373;--terre:#CC6B49;--bronze:#B5835A;--vert:#2D6A4F;--creme:#FEFAE0}@media(prefers-color-scheme:dark){:root{--sable:#A07440;--creme:#D4C8A0;--terre:#A04D3D}}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:'Lato',sans-serif;font-weight:300;color:#1A4A3A;min-height:100vh;background:linear-gradient(135deg,var(--creme),var(--sable))}
.bg-grain{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23g)' opacity='0.04'/%3E%3C/svg%3E")}
nav{position:fixed;top:0;width:100%;padding:14px 32px;display:flex;justify-content:space-between;align-items:center;z-index:100;background:rgba(254,250,224,0.9);backdrop-filter:blur(8px);border-bottom:1px solid rgba(45,106,79,0.1)}
nav .logo-small{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--vert)}
nav .logo-small span{font-family:'Cinzel',serif;font-size:14px;letter-spacing:1px}
nav a{color:#1A4A3A;text-decoration:none;font-size:12px;font-weight:400;letter-spacing:1px;text-transform:uppercase;padding:6px 14px;transition:.3s}
nav a:hover{color:var(--terre)}
.hero{position:relative;z-index:1;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:120px 24px 80px}
.hero .logo-hero svg{width:120px;height:120px;margin-bottom:12px}
.hero h1{font-family:'Cinzel',serif;font-size:clamp(36px,8vw,72px);letter-spacing:3px;color:#1A3A2A;margin-bottom:4px}
.hero .tagline{font-family:'Cormorant',serif;font-style:italic;font-size:18px;color:#8B4513;margin-bottom:28px}
.hero p{font-size:16px;line-height:1.7;color:#1A4A3A;max-width:500px}
.section{position:relative;z-index:1;padding:80px 24px;max-width:700px;margin:0 auto}
.section h2{font-family:'Cinzel',serif;font-size:26px;letter-spacing:2px;color:#8B4513;margin-bottom:32px;text-align:center}
.section h2::after{content:'';display:block;width:60px;height:1px;background:var(--bronze);margin:8px auto 0}
.section p{font-size:16px;line-height:1.8;color:#1A4A3A;margin-bottom:20px}
.section-alt{background:rgba(212,163,115,0.12);border-top:1px solid rgba(45,106,79,0.06);border-bottom:1px solid rgba(45,106,79,0.06)}
.members-grid{display:flex;flex-wrap:wrap;justify-content:center;gap:20px;margin-top:20px}
.member-card{flex:0 0 180px;text-align:center;padding:24px 12px;background:rgba(254,250,224,0.3);border-radius:8px;border:1px solid rgba(181,131,90,0.15);transition:.25s}
.member-card:hover{background:rgba(254,250,224,0.5);transform:scale(1.03)}
.member-card .avatar-circle{width:68px;height:68px;border-radius:50%;background:linear-gradient(135deg,var(--bronze),var(--terre));margin:0 auto 10px;display:flex;align-items:center;justify-content:center;font-family:'Cinzel',serif;font-size:24px;color:var(--creme)}
.member-card h3{font-family:'Cinzel',serif;font-size:15px;letter-spacing:1px;color:var(--terre);margin-bottom:3px}
.member-card p{font-family:'Lato',sans-serif;font-size:13px;color:#3A5A4A}
.concerts-list{list-style:none;padding:0}
.concerts-list li{padding:14px 20px;margin-bottom:10px;background:rgba(254,250,224,0.3);border-radius:6px;border-left:3px solid var(--bronze);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px}
.concerts-list .date{font-family:'Cormorant',serif;font-size:15px;color:var(--terre)}
.concerts-list .lieu{font-size:14px;color:#1A4A3A}
.concerts-list .status{font-size:10px;padding:3px 10px;border-radius:10px;background:rgba(204,107,73,0.1);color:var(--terre)}
.contact-info{text-align:center;margin-top:16px}
.contact-info p{font-size:16px;margin-bottom:6px}
.contact-info .email{font-family:'Lato',sans-serif;font-size:16px;color:var(--terre);text-decoration:none;transition:.2s}
.contact-info .email:hover{color:var(--vert)}
.links-social{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:24px}
.links-social a{color:#1A4A3A;text-decoration:none;font-family:'Lato',sans-serif;font-size:12px;padding:8px 18px;border:1px solid rgba(181,131,90,0.2);border-radius:6px;transition:.3s;letter-spacing:1px;text-transform:uppercase}
.links-social a:hover{color:var(--vert);border-color:var(--terre);background:rgba(204,107,73,0.04)}
.footer{position:relative;z-index:1;text-align:center;padding:44px 24px;border-top:1px solid rgba(45,106,79,0.06)}
.footer p{font-family:'Cormorant',serif;font-size:11px;letter-spacing:3px;color:#3A5A4A}
.footer .logo-footer svg{width:60px;height:60px;margin-bottom:8px;opacity:0.3}
.scroll-indicator{position:absolute;bottom:32px;left:50%;transform:translateX(-50%);width:24px;height:40px;border:2px solid rgba(0,0,0,0.12);border-radius:12px}
.scroll-indicator::after{content:'';position:absolute;top:6px;left:50%;transform:translateX(-50%);width:3px;height:8px;background:var(--bronze);border-radius:2px;animation:scrollDown 2s infinite}
@keyframes scrollDown{0%{opacity:1;transform:translateX(-50%) translateY(0)}100%{opacity:0;transform:translateX(-50%) translateY(16px)}}
@media(max-width:640px){
  nav{padding:12px 16px}
  nav a{font-size:11px;padding:4px 10px}
  .hero{padding:100px 16px 60px}
  .section{padding:60px 16px}
  .member-card{flex:0 0 150px}
}
@media(max-width:400px){
  .hero h1{font-size:36px}
  .member-card{flex:0 0 140px}
  .section{padding:40px 12px}
}
@media(prefers-reduced-motion){*{animation:none!important;transition:none!important}}
</style>
</head>
<body>
<div class="bg-grain"></div>
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
  <div class="logo-hero">
    <svg viewBox="0 0 100 100">
      <circle cx="50" cy="50" r="28" fill="#B5835A"/>
      <circle cx="50" cy="50" r="32" fill="none" stroke="rgba(0,0,0,0.06)" stroke-width="1.5" stroke-dasharray="3 3"/>
      <polygon points="50,22 58,40 42,40" fill="#B5835A"/>
      <polygon points="50,78 42,60 58,60" fill="#B5835A"/>
      <polygon points="22,50 40,42 40,58" fill="#B5835A"/>
      <polygon points="78,50 60,42 60,58" fill="#B5835A"/>
    </svg>
  </div>
  <h1>RIVERS ROCK</h1>
  <div class="tagline">Reprises rock — Rouen</div>
  <p>Groupe rouennais formé en 2024. Rock, pop-rock, indé et alternatif. Chaleur et évasion.</p>
  <a href="#groupe" style="text-decoration:none;color:inherit"><div class="scroll-indicator"></div></a>
</section>
<section id="groupe" class="section">
  <h2>Le groupe</h2>
  <p>Cinq musiciens, une passion commune : faire vibrer la scène rouennaise.</p>
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
    <div style="position:absolute;top:0;left:0;width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,0.05);border-radius:8px;font-family:sans-serif;font-size:16px;color:rgba(0,0,0,0.3)">Video a venir</div>
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
  <div class="logo-footer">
    <svg viewBox="0 0 100 100">
      <circle cx="50" cy="50" r="28" fill="#B5835A"/>
      <polygon points="50,22 58,40 42,40" fill="#B5835A"/>
      <polygon points="50,78 42,60 58,60" fill="#B5835A"/>
      <polygon points="22,50 40,42 40,58" fill="#B5835A"/>
      <polygon points="78,50 60,42 60,58" fill="#B5835A"/>
    </svg>
  </div>
  <p>R O U E N</p>
</footer>
</body>
</html>'''
    dst = os.path.join(OUT, "index.html")
    with open(dst, "w") as f:
        f.write(html)
    print(f"[Sable & Bronze] Site → {dst}")


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
