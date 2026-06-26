#!/usr/bin/env python3
"""Generate all Neon Nights assets — Proposition n°5."""
# SVG logo available at: ../propositions/XXX/assets/logo.svg


import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))
from logoutils import (
    create_bleed_canvas, save_with_crop_marks,
    pillow_grain_overlay,
    draw_qr_pillow, BEBAS_PATH, MONTSERRAT_PATH, ORBITRON_PATH, RAJDHANI_PATH, JETBRAINS_PATH,
)
from palette import NEON_NIGHTS as CFG
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

NUIT = CFG.rl("nuit_profonde")
ROSE = CFG.rl("rose_neon")
CYAN = CFG.rl("cyan")
VIOLET = CFG.rl("violet_fonce")
BLANC = CFG.rl("blanc_bleute")

NUIT_PIL = CFG.pil("nuit_profonde")
ROSE_PIL = CFG.pil("rose_neon")
CYAN_PIL = CFG.pil("cyan")
VIOLET_PIL = CFG.pil("violet_fonce")
BLANC_PIL = CFG.pil("blanc_bleute")

pdfmetrics.registerFont(TTFont("Orbitron", ORBITRON_PATH))
pdfmetrics.registerFont(TTFont("Rajdhani", RAJDHANI_PATH))
pdfmetrics.registerFont(TTFont("JetBrainsMono", JETBRAINS_PATH))

from setlist_data import SETLIST, GREEN_INDICES


def logo_neon_reportlab(cv, cx, cy, scale=1.0):
    """Lightning circle logo."""
    r = 20 * scale
    cv.setStrokeColor(CYAN)
    cv.setLineWidth(2 * scale)
    cv.circle(cx, cy, r, stroke=1, fill=0)
    cv.setStrokeColor(ROSE)
    cv.setLineWidth(2 * scale)
    for dx, dy, dx2, dy2 in [(r * 0.7, -r * 0.3, r * 1.6, -r * 0.8),
                              (r * 0.9, r * 0.2, r * 1.4, r * 1.0),
                              (-r * 0.7, -r * 0.5, -r * 1.5, -r * 0.2),
                              (-r * 0.8, r * 0.3, -r * 1.3, r * 0.9)]:
        cv.line(cx + dx, cy + dy, cx + dx2, cy + dy2)
    cv.setFillColor(ROSE)
    cv.circle(cx, cy, r * 0.25, stroke=0, fill=1)


def logo_neon_pillow(draw, cx, cy, scale=1.0):
    """Lightning circle logo for Pillow."""
    r = 20 * scale
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=CYAN_PIL, width=max(1, int(2 * scale)))
    for dx, dy, dx2, dy2 in [(r * 0.7, -r * 0.3, r * 1.6, -r * 0.8),
                              (r * 0.9, r * 0.2, r * 1.4, r * 1.0),
                              (-r * 0.7, -r * 0.5, -r * 1.5, -r * 0.2),
                              (-r * 0.8, r * 0.3, -r * 1.3, r * 0.9)]:
        draw.line([(cx + dx, cy + dy), (cx + dx2, cy + dy2)], fill=ROSE_PIL, width=max(1, int(2 * scale)))
    draw.ellipse([cx - r * 0.25, cy - r * 0.25, cx + r * 0.25, cy + r * 0.25], fill=ROSE_PIL)


def draw_zigzag_waves(cv, W, H):
    cv.setStrokeColor(Color(1, 1, 1, alpha=0.035))
    for row in range(3):
        y_base = 15 + row * 35
        segs = 40
        sw = W / segs
        for i in range(segs):
            x = i * sw
            cv.line(x, y_base, x + sw / 2, y_base + 8 + row * 4)
            cv.line(x + sw / 2, y_base + 8 + row * 4, x + sw, y_base)


def hexagon_badge(cv, cx, cy, r, num):
    hv = [(cx + r * math.cos(math.radians(60 * i - 30)), cy + r * math.sin(math.radians(60 * i - 30))) for i in range(6)]
    cv.setFillColor(ROSE)
    p = cv.beginPath()
    p.moveTo(hv[0][0], hv[0][1])
    for pt in hv[1:]:
        p.lineTo(pt[0], pt[1])
    p.close()
    cv.drawPath(p, fill=1, stroke=0)
    cv.setFillColor(Color(1, 1, 1))
    cv.setFont("Rajdhani", 12)
    cv.drawCentredString(cx, cy - 4.5, f"{num:02d}")


def gen_setlist():
    W, H = A4
    path = os.path.join(PDF, "setlist-neon-nights.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, W, H)

    for i in range(120):
        t = i / 119
        r = NUIT.red + (VIOLET.red - NUIT.red) * t
        g = NUIT.green + (VIOLET.green - NUIT.green) * t
        b = NUIT.blue + (VIOLET.blue - NUIT.blue) * t
        cv.setFillColor(Color(r, g, b))
        cv.rect(0, i * H / 120, W, H / 120 + 1, stroke=0, fill=1)

    random.seed(42)
    for _ in range(3000):
        cv.setFillColor(Color(1, 1, 1, alpha=random.uniform(0.015, 0.04)))
        cv.circle(random.uniform(0, W), random.uniform(0, H), random.uniform(0.3, 1.0), stroke=0, fill=1)

    draw_zigzag_waves(cv, W, H)

    logo_neon_reportlab(cv, W / 2, H - 105, 2.0)
    cv.setFillColor(BLANC)
    cv.setFont("Orbitron", 16)
    cv.drawCentredString(W / 2, H - 150, "RIVERS ROCK")

    cv.setFillColor(ROSE)
    cv.setFont("Orbitron", 22)
    cv.drawCentredString(W / 2, H - 180, "SETLIST")

    card_w, card_h, card_r = 250, 74, 2
    col_gap = (W - 2 * card_w) / 3
    col_c = [col_gap + card_w / 2, col_gap * 2 + card_w + card_w / 2]
    row_pitch = 86
    rows_top = 610

    def uniform_size():
        longest = max(SETLIST, key=lambda x: len(x[0]))[0]
        mx = card_w - 32 - 26 - 8
        lo, hi = 1, 200
        while lo < hi:
            mid = (lo + hi + 1) // 2
            w = pdfmetrics.stringWidth(longest, "Orbitron", mid) or pdfmetrics.stringWidth(longest, "Rajdhani", mid)
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
        bg = VIOLET if is_green else NUIT

        cv.setFillColor(Color(ROSE.red, ROSE.green, ROSE.blue, alpha=0.15))
        cv.roundRect(cl + 3, cb - 3, card_w, card_h, card_r, stroke=0, fill=1)

        for i in range(30):
            t = i / 29
            l = 0.15 * (1 - t)
            c = Color(min(1, bg.red + l), min(1, bg.green + l), min(1, bg.blue + l))
            cv.setFillColor(c)
            cv.rect(cl, cb + i * card_h / 30, card_w, card_h / 30 + 0.5, stroke=0, fill=1)

        cv.setStrokeColor(CYAN)
        cv.setLineWidth(0.5)
        cv.roundRect(cl, cb, card_w, card_h, card_r, stroke=1, fill=0)
        cv.setStrokeColor(ROSE)
        cv.setLineWidth(0.8)
        cv.roundRect(cl - 0.5, cb - 0.5, card_w + 1, card_h + 1, card_r, stroke=1, fill=0)

        aw = pdfmetrics.stringWidth(artist, "Orbitron", us)
        if aw == 0:
            aw = pdfmetrics.stringWidth(artist, "Rajdhani", us)
        tw_ = 26 + 8 + aw
        sx = cx - tw_ / 2

        bcy = cy + 15
        hexagon_badge(cv, sx + 13, bcy, 12, idx + 1)

        cv.setFillColor(BLANC)
        cv.setFont("Orbitron", us)
        cv.drawString(sx + 26 + 8, cy + 6, artist)

        if title:
            cv.setFillColor(Color(1, 1, 1, alpha=0.75))
            ts = 12
            tww = pdfmetrics.stringWidth(title, "Rajdhani", ts)
            if tww > card_w - 32:
                ts *= (card_w - 32) / tww
            cv.setFont("Rajdhani", ts)
            cv.drawCentredString(cx, cy - 18, title)

    cv.setFillColor(Color(1, 1, 1, alpha=0.20))
    cv.setFont("JetBrainsMono", 7)
    text, tr = "R O U E N", 5
    x = W / 2 - (sum(pdfmetrics.stringWidth(c, "JetBrainsMono", 7) for c in text) + tr * (len(text) - 1)) / 2
    for c in text:
        w = pdfmetrics.stringWidth(c, "JetBrainsMono", 7)
        cv.drawString(x, 14, c)
        x += w + tr
    save_with_crop_marks(cv, _, _, bleed)
    print(f"[Neon Nights] Setlist → {path}")


def gen_poster():
    W, H = A4
    path = os.path.join(PDF, "poster-neon-nights.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, W, H)

    for i in range(120):
        t = i / 119
        r = NUIT.red + (VIOLET.red - NUIT.red) * t
        g = NUIT.green + (VIOLET.green - NUIT.green) * t
        b = NUIT.blue + (VIOLET.blue - NUIT.blue) * t
        cv.setFillColor(Color(r, g, b))
        cv.rect(0, i * H / 120, W, H / 120 + 1, stroke=0, fill=1)

    random.seed(42)
    for _ in range(3000):
        cv.setFillColor(Color(1, 1, 1, alpha=random.uniform(0.015, 0.04)))
        cv.circle(random.uniform(0, W), random.uniform(0, H), random.uniform(0.3, 1.0), stroke=0, fill=1)

    draw_zigzag_waves(cv, W, H)
    logo_neon_reportlab(cv, W / 2, H - 190, 2.0)

    cv.setFillColor(BLANC)
    cv.setFont("Orbitron", 12)
    cv.drawCentredString(W / 2, H - 250, "RIVERS ROCK")
    cv.setFillColor(ROSE)
    cv.setFont("Rajdhani", 12)
    cv.drawCentredString(W / 2, H - 275, "LES SOIREES NOCTURNES")
    cv.setFillColor(BLANC)
    cv.setFont("Orbitron", 48)
    cv.drawCentredString(W / 2, H - 340, "VEN 26 JUIN 2026")
    cv.setFillColor(Color(1, 1, 1, alpha=0.7))
    cv.setFont("Rajdhani", 16)
    cv.drawCentredString(W / 2, H - 375, "Montigny · 19h30")

    cv.setStrokeColor(ROSE)
    cv.setLineWidth(0.8)
    cv.line(W / 2 - 60, H - 400, W / 2 + 60, H - 400)

    cv.setFillColor(Color(1, 1, 1, alpha=0.20))
    cv.setFont("JetBrainsMono", 7)
    text, tr = "R O U E N", 5
    x = W / 2 - (sum(pdfmetrics.stringWidth(c, "JetBrainsMono", 7) for c in text) + tr * (len(text) - 1)) / 2
    for c in text:
        w = pdfmetrics.stringWidth(c, "JetBrainsMono", 7)
        cv.drawString(x, 14, c)
        x += w + tr
    save_with_crop_marks(cv, _, _, bleed)
    print(f"[Neon Nights] Poster → {path}")


def gen_flyer():
    FW, FH = A6
    path = os.path.join(PDF, "flyer-neon-nights.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, A4[0], A4[1])

    def grad(cv, x, y, w, h):
        for i in range(60):
            t = i / 59
            r = NUIT.red + (VIOLET.red - NUIT.red) * t
            g = NUIT.green + (VIOLET.green - NUIT.green) * t
            b = NUIT.blue + (VIOLET.blue - NUIT.blue) * t
            cv.setFillColor(Color(r, g, b))
            cv.rect(x, y + i * h / 60, w, h / 60 + 0.5, stroke=0, fill=1)

    def draw_recto(cv, ox, oy):
        grad(cv, ox, oy, FW, FH)
        cx = ox + FW / 2
        logo_neon_reportlab(cv, cx, oy + FH - 50, 1.0)
        cv.setFillColor(BLANC)
        cv.setFont("Orbitron", 14)
        cv.drawCentredString(cx, oy + FH - 80, "RIVERS ROCK")
        cv.setFillColor(ROSE)
        cv.setFont("Orbitron", 28)
        cv.drawCentredString(cx, oy + FH - 145, "VEN 26 JUIN 2026")
        cv.setFillColor(Color(1, 1, 1, alpha=0.7))
        cv.setFont("Rajdhani", 10)
        cv.drawCentredString(cx, oy + FH - 175, "Montigny · 19h30")

    def draw_verso(cv, ox, oy):
        grad(cv, ox, oy, FW, FH)
        cx = ox + FW / 2
        cv.setFillColor(BLANC)
        cv.setFont("Orbitron", 14)
        cv.drawCentredString(cx, oy + FH - 40, "RIVERS ROCK")
        bio = ["Groupe rouennais formé en 2024", "au centre Éducation et Formation", "du Petit-Quevilly.",
               "", "Rosaria - batterie", "Christophe - basse", "Nicolas - guitare",
               "David - guitare / chant", "Virginie - chant", "", "Rock - Pop-Rock - Indé - Alternatif"]
        cv.setFillColor(Color(1, 1, 1, alpha=0.75))
        cv.setFont("Rajdhani", 7)
        y = oy + FH - 80
        for line in bio:
            cv.drawCentredString(cx, y, line)
            y -= 12
        cv.setFillColor(ROSE)
        cv.setFont("Rajdhani", 7)
        cv.drawCentredString(cx, y - 6, "Contactez-nous pour programmer un concert")
        cv.setFillColor(Color(1, 1, 1, alpha=0.4))
        cv.setFont("JetBrainsMono", 7)
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
    print(f"[Neon Nights] Flyer → {path}")


def gen_social():
    def lerp(c1, c2, t):
        return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))

    font_orb = ImageFont.truetype(ORBITRON_PATH, 56)
    font_orb_m = ImageFont.truetype(ORBITRON_PATH, 40)
    font_raj = ImageFont.truetype(RAJDHANI_PATH, 22)
    font_tag = ImageFont.truetype(JETBRAINS_PATH, 14)

    w, h = 1080, 1080
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    for i in range(200):
        t = i / 199
        draw.rectangle([0, i * h / 200, w, (i + 1) * h / 200], fill=lerp(NUIT_PIL, VIOLET_PIL, t))

    img = pillow_grain_overlay(img, 0.03, seed=10)

    logo_neon_pillow(draw, w / 2, 140, 2.5)
    bbox = draw.textbbox((0, 0), "RIVERS ROCK", font=font_orb)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 155), "RIVERS ROCK", fill=ROSE_PIL, font=font_orb)

    bbox = draw.textbbox((0, 0), "LES SOIREES NOCTURNES", font=font_raj)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 380), "LES SOIREES NOCTURNES", fill=CYAN_PIL, font=font_raj)
    bbox = draw.textbbox((0, 0), "VEN 26 JUIN 2026", font=font_orb_m)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 440), "VEN 26 JUIN 2026", fill=BLANC_PIL, font=font_orb_m)
    bbox = draw.textbbox((0, 0), "Montigny · 19h30", font=font_raj)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 520), "Montigny · 19h30", fill=(180, 180, 200), font=font_raj)

    qx, qy, qs = w / 2 - 60, 660, 120
    draw.rectangle([qx, qy, qx + qs, qy + qs], fill=BLANC_PIL, outline=CYAN_PIL, width=3)
    qr_img = draw_qr_pillow(None, 0, 0, qs - 12, fill_color=NUIT_PIL)
    if qr_img:
        img.paste(qr_img, (int(qx + 6), int(qy + 6)), qr_img if qr_img.mode == "RGBA" else None)

    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((qx + (qs - tw) / 2, qy + (qs - th) / 2), "QR", fill=NUIT_PIL, font=font_raj)

    bbox = draw.textbbox((0, 0), "@riversrockrouen", font=font_tag)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 860), "@riversrockrouen", fill=(180, 180, 200), font=font_tag)
    img.save(os.path.join(TMPL, "instagram-post.png"))

    w, h = 1080, 1920
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    cx, cy = w / 2, h / 2
    mr = math.sqrt(cx**2 + cy**2)
    for i in range(300):
        t = i / 299
        r = mr * t
        if t < 0.15:
            c = lerp(CYAN_PIL, ROSE_PIL, t / 0.15)
        elif t < 0.35:
            c = lerp(ROSE_PIL, NUIT_PIL, (t - 0.15) / 0.2)
        else:
            c = lerp(NUIT_PIL, VIOLET_PIL, (t - 0.35) / 0.65)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)

    img = pillow_grain_overlay(img, 0.03, seed=20)

    font_orb_d = ImageFont.truetype(ORBITRON_PATH, 100)
    logo_neon_pillow(draw, w / 2, 180, 3.0)
    bbox = draw.textbbox((0, 0), "RIVERS ROCK", font=font_orb)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2 + 20, 195), "RIVERS ROCK", fill=ROSE_PIL, font=font_orb)

    bbox = draw.textbbox((0, 0), "VEN 26 JUIN 2026", font=font_orb_d)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 650), "VEN 26 JUIN 2026", fill=ROSE_PIL, font=font_orb_d)
    bbox = draw.textbbox((0, 0), "Montigny · 19h30", font=font_raj)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 840), "Montigny · 19h30", fill=BLANC_PIL, font=font_raj)

    bbox = draw.textbbox((0, 0), "@riversrockrouen", font=font_tag)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 1750), "@riversrockrouen", fill=(180, 180, 200), font=font_tag)
    img.save(os.path.join(TMPL, "instagram-story.png"))
    print(f"[Neon Nights] Social → {TMPL}")


def gen_banners():
    for name, w, h, logo_s in [
        ("facebook-banner.png", 1640, 624, 48),
        ("youtube-banner.png", 2560, 1440, 72),
    ]:
        img = Image.new("RGB", (w, h))
        draw = ImageDraw.Draw(img)
        for i in range(120):
            t = i / 119
            c = tuple(int(a + (b - a) * t) for a, b in zip(NUIT_PIL, VIOLET_PIL))
            draw.rectangle([0, i * h / 120, w, (i + 1) * h / 120], fill=c)

        img = pillow_grain_overlay(img, 0.03, seed=30)

        font_logo = ImageFont.truetype(ORBITRON_PATH, logo_s)
        tw = draw.textbbox((0, 0), "RIVERS ROCK", font=font_logo)[2]
        sym_r = logo_s * 0.5
        gap = sym_r * 0.3
        sx = (w - (sym_r * 2 + gap + tw)) / 2
        logo_neon_pillow(draw, sx + sym_r, h / 2, sym_r / 22.0)
        draw.text((sx + sym_r * 2 + gap, h / 2 - tw * 0.25), "RIVERS ROCK", fill=BLANC_PIL, font=font_logo)

        font_sub = ImageFont.truetype(RAJDHANI_PATH, 14)
        sub = "Reprises rock - Rouen"
        sb = draw.textbbox((0, 0), sub, font=font_sub)
        draw.text(((w - (sb[2] - sb[0])) / 2, h - 50), sub, fill=CYAN_PIL, font=font_sub)
        img.save(os.path.join(TMPL, name))
    print(f"[Neon Nights] Banners → {TMPL}")


def gen_avatar():
    S = 500
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    logo_neon_pillow(draw, S / 2, S / 2, 6.0)
    font = ImageFont.truetype(ORBITRON_PATH, 28)
    bbox = draw.textbbox((0, 0), "RR", font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((S - tw) / 2, S / 2 + 60), "RR", fill=ROSE_PIL, font=font)
    img.save(os.path.join(TMPL, "avatar.png"))
    print(f"[Neon Nights] Avatar → {TMPL}")


def gen_stickers():
    from reportlab.lib.units import mm
    W, H = A4
    SR = 40 * mm
    MX = (W - 2 * SR * 2) / 3
    MY = (H - 3 * SR * 2) / 4
    centers = [(MX + SR + c * (MX + SR * 2), MY + SR + r * (MY + SR * 2)) for c in range(2) for r in range(3)]

    path = os.path.join(PDF, "stickers-neon-nights.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, A4[0], A4[1])

    for cx, cy in centers:
        for i in range(60):
            t = i / 59
            r = NUIT.red + (VIOLET.red - NUIT.red) * t
            g = NUIT.green + (VIOLET.green - NUIT.green) * t
            b = NUIT.blue + (VIOLET.blue - NUIT.blue) * t
            cv.setFillColor(Color(r, g, b))
            y = cy - SR + i * SR * 2 / 60
            cv.rect(cx - SR, y, SR * 2, SR * 2 / 60 + 0.5, stroke=0, fill=1)
        cv.setStrokeColor(ROSE)
        cv.setLineWidth(2)
        cv.circle(cx, cy, SR, stroke=1, fill=0)
        sr = SR * 0.50
        logo_neon_reportlab(cv, cx, cy, sr / 22.0)
        cv.setFillColor(BLANC)
        cv.setFont("Orbitron", 7)
        cv.drawCentredString(cx, cy + sr + 8, "RIVERS ROCK")
    save_with_crop_marks(cv, _, _, bleed)
    print(f"[Neon Nights] Stickers → {path}")


def gen_tshirt():
    from reportlab.lib.units import mm
    w, h = A4
    sizes = [("S", 22 * mm, w / 4, h - 200), ("M", 28 * mm, w * 3 / 4, h - 200),
             ("L", 34 * mm, w / 4, h - 440), ("XL", 40 * mm, w * 3 / 4, h - 440)]
    path = os.path.join(PDF, "tshirt-neon-nights.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, A4[0], A4[1])
    cv.setFillColor(Color(0, 0, 0, alpha=0.04))
    cv.rect(0, 0, w, h, stroke=0, fill=1)
    for label, sr, cx, cy in sizes:
        logo_neon_reportlab(cv, cx, cy, sr / 22.0)
        cv.setFillColor(BLANC)
        cv.setFont("Orbitron", max(8, int(sr * 1.4)))
        cv.drawCentredString(cx, cy + sr * 0.6 + 4, "RIVERS ROCK")
        if label:
            cv.setFillColor(Color(0, 0, 0, alpha=0.3))
            cv.setFont("Rajdhani", 7)
            cv.drawCentredString(cx, cy + sr + 60, label)
    save_with_crop_marks(cv, _, _, bleed)
    print(f"[Neon Nights] T-shirt → {path}")


def gen_animated():
    html = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rivers Rock — Neon Nights</title>
<link rel="icon" type="image/png" sizes="32x32" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAONJREFUWEft1r0NgzAQBeD/FYyAWIAJYAQKOkZgBEZgBDoWYARGYAQK4khBtuWf+CJFJMqV3vfpneMEAf4PQAiAEAChIyA6AqIj4D8AlNJ3rfU2TdNr2/dfPn+PcRzBmga01gBQSgEAtVaMMQAAay0A5JyL53meIYQAAJxzAECTJAHGGADUWk3T3QFKKQDAWosxxhCCz/N8TdP0zvN83/u+xBjfi8Jrreb7PgC01ng8Hk3TfI/j+AFCSvmZpunVdd0r5/ytlPoqpV5KKRBCAEBKCQApJQCEENbaW84Z5pz3AFrrb845zjkjhAAAnHMQQvjvfQFCCOGHEEIIIRBC+I/vB0RPRM90HYzWAAAAAElFTkSuQmCC">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0}
body{width:1080px;height:1920px;overflow:hidden;background:#0F0B1A;display:flex;align-items:center;justify-content:center}
canvas{position:absolute;top:0;left:0;width:1080px;height:1920px}
svg{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:400px;height:400px;overflow:visible}
.flash{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(255,255,255,0.85);opacity:0;z-index:10;pointer-events:none;animation:flashBang .1s ease-out .9s forwards}
@keyframes flashBang{0%{opacity:1}100%{opacity:0}}
.buzz{animation:buzz .15s ease-in-out 5;transform-origin:center}
@keyframes buzz{0%{transform:scale(1)}50%{transform:scale(1.06)}100%{transform:scale(1)}}
.circle{fill:none;stroke:#00F5FF;stroke-width:3;animation:fadeIn .2s ease-out .3s forwards;filter:drop-shadow(0 0 15px rgba(0,245,255,0.7))}
@keyframes fadeIn{to{opacity:1}}
.lightning{fill:none;stroke:#FFF;stroke-width:3;stroke-linecap:round;stroke-dasharray:100;stroke-dashoffset:100;animation:strike .12s ease-out .95s forwards}
.lightning-a{animation-delay:.95s}
.lightning-b{animation-delay:.98s}
@keyframes strike{to{stroke-dashoffset:0}}
.lightning-fill{fill:none;stroke:#FF2D95;stroke-width:3;opacity:0;animation:glowOn .3s ease-out 1.15s forwards;filter:drop-shadow(0 0 10px rgba(255,45,149,0.9))}
@keyframes glowOn{to{opacity:1}}
.center-fill{opacity:0;animation:fadeIn .2s ease-out 1.3s forwards}
.letter{font-family:'Orbitron',sans-serif;font-size:28px;fill:#E8E0F0;opacity:0}
.lR{animation:flicker .6s ease-out 2.0s forwards}
.lI{animation:flicker .6s ease-out 2.12s forwards}
.lV{animation:flicker .6s ease-out 2.24s forwards}
.lE{animation:flicker .6s ease-out 2.36s forwards}
.lR2{animation:flicker .6s ease-out 2.48s forwards}
.lS{animation:flicker .6s ease-out 2.6s forwards}
@keyframes flicker{0%{opacity:1}15%{opacity:0}30%{opacity:1}45%{opacity:0}60%{opacity:1}70%{opacity:0.3}85%{opacity:1}100%{opacity:1}}
.lROCK_R{animation:slideBlur .4s ease-out 3.0s forwards}
.lROCK_O{animation:slideBlur .4s ease-out 3.12s forwards}
.lROCK_C{animation:slideBlur .4s ease-out 3.24s forwards}
.lROCK_K{animation:slideBlur .4s ease-out 3.36s forwards}
@keyframes slideBlur{0%{opacity:0;transform:translateX(100px);filter:blur(6px)}100%{opacity:1;transform:translateX(0);filter:blur(0)}}
@media(prefers-reduced-motion){*{animation:none!important;transition:none!important}}
</style>
</head>
<body>
<div class="flash"></div>
<canvas id="p"></canvas>
<svg viewBox="-200 -200 400 400">
  <g class="buzz">
    <circle class="circle" cx="0" cy="0" r="45"/>
  </g>
  <polyline class="lightning lightning-a" points="35,-20 55,-10 42,5 60,15"/>
  <polyline class="lightning lightning-b" points="-35,-20 -50,-10 -40,5 -55,15"/>
  <polyline class="lightning-fill" points="35,-20 55,-10 42,5 60,15"/>
  <polyline class="lightning-fill" points="-35,-20 -50,-10 -40,5 -55,15"/>
  <circle class="center-fill" cx="0" cy="0" r="10" fill="#FF2D95"/>
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
for(let i=0;i<30;i++){ps.push({x:Math.random()*1080,y:Math.random()*1920,s:Math.random()*3+1,a:Math.random()*0.04+0.01})}
function draw(){ctx.clearRect(0,0,1080,1920);
ctx.fillStyle='#0F0B1A';ctx.fillRect(0,0,1080,1920);
const g=ctx.createRadialGradient(540,860,0,540,860,1200);
g.addColorStop(0,'rgba(255,45,149,0.08)');g.addColorStop(0.5,'rgba(0,245,255,0.03)');g.addColorStop(1,'rgba(15,11,26,0)');
ctx.fillStyle=g;ctx.fillRect(0,0,1080,1920);
for(const p of ps){ctx.beginPath();ctx.arc(p.x,p.y,p.s,0,Math.PI*2);ctx.fillStyle='rgba(0,245,255,'+p.a+')';ctx.fill();p.y-=0.3;if(p.y<0){p.y=1920;p.x=Math.random()*1080}}
requestAnimationFrame(draw)}draw();
</script>
</body>
</html>'''
    path = os.path.join(TMPL, "logo-animated-neon-nights.html")
    with open(path, "w") as f:
        f.write(html)
    print(f"[Neon Nights] Animated logo → {path}")
def gen_site():
    html = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rivers Rock — Neon Nights</title>
<link rel="preload" href="assets/logo.svg" as="image" type="image/svg+xml">
<link rel="icon" type="image/png" sizes="32x32" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAONJREFUWEft1r0NgzAQBeD/FYyAWIAJYAQKOkZgBEZgBDoWYARGYAQK4khBtuWf+CJFJMqV3vfpneMEAf4PQAiAEAChIyA6AqIj4D8AlNJ3rfU2TdNr2/dfPn+PcRzBmga01gBQSgEAtVaMMQAAay0A5JyL53meIYQAAJxzAECTJAHGGADUWk3T3QFKKQDAWosxxhCCz/N8TdP0zvN83/u+xBjfi8Jrreb7PgC01ng8Hk3TfI/j+AFCSvmZpunVdd0r5/ytlPoqpV5KKRBCAEBKCQApJQCEENbaW84Z5pz3AFrrb845zjkjhAAAnHMQQvjvfQFCCOGHEEIIIRBC+I/vB0RPRM90HYzWAAAAAElFTkSuQmCC">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700&family=Rajdhani:wght@300;400;600&family=JetBrains+Mono&display=swap" rel="stylesheet">
<style>
:root{--nuit:#0F0B1A;--rose:#FF2D95;--cyan:#00F5FF;--violet:#1A0B2E;--blanc:#E8E0F0}@media(prefers-color-scheme:dark){:root{--nuit:#06030A;--violet:#0B0415}}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:'Rajdhani',sans-serif;font-weight:300;color:var(--blanc);min-height:100vh;background:linear-gradient(135deg,var(--nuit),var(--violet))}
.bg-grain{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23g)' opacity='0.03'/%3E%3C/svg%3E")}
nav{position:fixed;top:0;width:100%;padding:14px 32px;display:flex;justify-content:space-between;align-items:center;z-index:100;background:rgba(15,11,26,0.9);backdrop-filter:blur(8px);border-bottom:1px solid rgba(255,45,149,0.15)}
nav .logo-small{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--blanc)}
nav .logo-small span{font-family:'Orbitron',sans-serif;font-size:14px;letter-spacing:2px}
nav a{color:rgba(232,224,240,0.5);text-decoration:none;font-size:12px;font-weight:400;letter-spacing:1px;text-transform:uppercase;padding:6px 14px;transition:.3s}
nav a:hover{color:var(--rose);text-shadow:0 0 8px rgba(255,45,149,0.4)}
.hero{position:relative;z-index:1;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:120px 24px 80px;background:radial-gradient(ellipse at 50% 35%, rgba(255,45,149,0.08) 0%, rgba(0,245,255,0.03) 50%, transparent 70%)}
.hero .logo-hero svg{width:130px;height:130px;margin-bottom:12px}
.hero h1{font-family:'Orbitron',sans-serif;font-size:clamp(36px,8vw,72px);letter-spacing:4px;color:var(--blanc);margin-bottom:4px}
.hero .tagline{font-family:'JetBrains Mono',monospace;font-size:12px;color:#FF69B4;letter-spacing:3px;text-transform:uppercase;margin-bottom:28px;text-shadow:0 0 10px rgba(255,45,149,0.3)}
.hero p{font-size:16px;line-height:1.7;color:rgba(232,224,240,0.6);max-width:500px}
.section{position:relative;z-index:1;padding:80px 24px;max-width:700px;margin:0 auto}
.section h2{font-family:'Orbitron',sans-serif;font-size:26px;letter-spacing:2px;text-transform:uppercase;color:#FF69B4;margin-bottom:32px;text-align:center}
.section h2::after{content:'';display:block;width:60px;height:1px;background:var(--cyan);margin:8px auto 0}
.section p{font-size:16px;line-height:1.8;color:rgba(232,224,240,0.7);margin-bottom:20px}
.section-alt{background:rgba(26,11,46,0.2);border-top:1px solid rgba(255,45,149,0.06);border-bottom:1px solid rgba(255,45,149,0.06)}
.members-grid{display:flex;flex-wrap:wrap;justify-content:center;gap:20px;margin-top:20px}
.member-card{flex:0 0 180px;text-align:center;padding:24px 12px;background:rgba(26,11,46,0.3);border-radius:2px;border:1px solid rgba(0,245,255,0.08);transition:.25s}
.member-card:hover{border-color:rgba(255,45,149,0.3);transform:scale(1.03)}
.member-card .avatar-circle{width:68px;height:68px;border-radius:50%;background:linear-gradient(135deg,var(--rose),var(--cyan));margin:0 auto 10px;display:flex;align-items:center;justify-content:center;font-family:'Orbitron',sans-serif;font-size:24px;color:var(--blanc)}
.member-card h3{font-family:'Orbitron',sans-serif;font-size:15px;letter-spacing:1px;color:var(--rose);margin-bottom:3px}
.member-card p{font-family:'Rajdhani',sans-serif;font-size:13px;color:rgba(232,224,240,0.4)}
.concerts-list{list-style:none;padding:0}
.concerts-list li{padding:14px 20px;margin-bottom:10px;background:rgba(26,11,46,0.3);border-radius:2px;border-left:3px solid var(--cyan);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px}
.concerts-list .date{font-family:'JetBrains Mono',monospace;font-size:13px;color:var(--rose)}
.concerts-list .lieu{font-size:14px;color:rgba(232,224,240,0.5)}
.concerts-list .status{font-size:10px;padding:3px 10px;border-radius:2px;background:rgba(255,45,149,0.1);color:var(--rose)}
.contact-info{text-align:center;margin-top:16px}
.contact-info p{font-size:16px;margin-bottom:6px}
.contact-info .email{font-family:'JetBrains Mono',monospace;font-size:14px;color:#00D4E0;text-decoration:none;transition:.2s}
.contact-info .email:hover{color:var(--rose)}
.links-social{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:24px}
.links-social a{color:rgba(232,224,240,0.5);text-decoration:none;font-family:'JetBrains Mono',monospace;font-size:11px;padding:8px 18px;border:1px solid rgba(255,45,149,0.2);border-radius:2px;transition:.3s;letter-spacing:1px;text-transform:uppercase}
.links-social a:hover{color:var(--blanc);border-color:var(--rose);background:rgba(255,45,149,0.06)}
.footer{position:relative;z-index:1;text-align:center;padding:44px 24px;border-top:1px solid rgba(255,45,149,0.06)}
.footer p{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:5px;color:rgba(232,224,240,0.2)}
.footer .logo-footer svg{width:50px;height:50px;margin-bottom:8px;opacity:0.3}
.scroll-indicator{position:absolute;bottom:32px;left:50%;transform:translateX(-50%);width:24px;height:40px;border:2px solid rgba(255,255,255,0.15);border-radius:12px}
.scroll-indicator::after{content:'';position:absolute;top:6px;left:50%;transform:translateX(-50%);width:3px;height:8px;background:var(--rose);border-radius:2px;animation:scrollDown 2s infinite}
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
      <circle cx="50" cy="50" r="35" fill="none" stroke="#00F5FF" stroke-width="2.5"/>
      <polyline points="68,28 78,20 74,35 80,42" fill="none" stroke="#FF2D95" stroke-width="2.5"/>
      <polyline points="68,72 78,64 74,79 80,86" fill="none" stroke="#FF2D95" stroke-width="2"/>
      <circle cx="50" cy="50" r="8" fill="#FF2D95"/>
    </svg>
  </div>
  <h1>RIVERS ROCK</h1>
  <div class="tagline">Reprises rock - Rouen</div>
  <p>Groupe rouennais forme en 2024. Rock, pop-rock, inde et alternatif. La Seine la nuit.</p>
  <a href="#groupe" style="text-decoration:none;color:inherit"><div class="scroll-indicator"></div></a>
</section>
<section id="groupe" class="section">
  <h2>Le groupe</h2>
  <p>Cinq musiciens, une passion commune : faire vibrer la scene rouennaise.</p>
  <div class="members-grid">
    <div class="member-card"><div class="avatar-circle" style="background:linear-gradient(135deg,#ccc,#999);font-size:20px;font-weight:bold">R</div><h3>Rosaria</h3><p>Batterie</p></div>
    <div class="member-card"><div class="avatar-circle">C</div><h3>Christophe</h3><p>Basse</p></div>
    <div class="member-card"><div class="avatar-circle">N</div><h3>Nicolas</h3><p>Guitare</p></div>
    <div class="member-card"><div class="avatar-circle">D</div><h3>David</h3><p>Guitare / Chant</p></div>
    <div class="member-card"><div class="avatar-circle">V</div><h3>Virginie</h3><p>Chant</p></div>
  </div>
</section>
<section id="concerts" class="section section-alt">
  <h2>Concerts</h2>
  <p>Contactez-nous pour programmer un concert.</p>
  <ul class="concerts-list"><li><span class="date">A venir</span><span class="lieu">Contactez-nous</span><span class="status">Sur demande</span></li></ul>
  <div style="margin-top:20px;border-radius:8px;overflow:hidden;max-width:400px;margin-left:auto;margin-right:auto">
    <img src="../../../images/IMG-20260620-WA0001.jpg" style="width:100%;height:auto;display:block;border-radius:8px" alt="Affiche Soirees Nocturnes - VEN 26 JUIN 2026 - Montigny">
  </div>
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
  
  <form action="mailto:riversrockrouen@gmail.com" method="POST" enctype="text/plain" style="max-width:400px;margin:20px auto">
    <input type="text" name="nom" placeholder="Votre nom" required style="width:100%;padding:10px;margin-bottom:8px;border:1px solid rgba(255,255,255,0.15);border-radius:6px;background:rgba(255,255,255,0.05);color:#fff;font-family:inherit;font-size:14px">
    <input type="email" name="email" placeholder="Votre email" required style="width:100%;padding:10px;margin-bottom:8px;border:1px solid rgba(255,255,255,0.15);border-radius:6px;background:rgba(255,255,255,0.05);color:#fff;font-family:inherit;font-size:14px">
    <textarea name="message" placeholder="Votre message" required rows="3" style="width:100%;padding:10px;margin-bottom:8px;border:1px solid rgba(255,255,255,0.15);border-radius:6px;background:rgba(255,255,255,0.05);color:#fff;font-family:inherit;font-size:14px;resize:vertical"></textarea>
    <button type="submit" style="width:100%;padding:10px;border:none;border-radius:6px;background:var(--accent, #E85D3A);color:#fff;font-family:inherit;font-size:14px;font-weight:600;cursor:pointer">Envoyer</button>
  </form><div class="links-social">
    <a href="https://www.instagram.com/riversrockrouen" target="_blank">Instagram</a>
    <a href="https://www.facebook.com/RiversRockRouen" target="_blank">Facebook</a>
    <a href="https://www.youtube.com/@RiversRockRouen" target="_blank">YouTube</a>
  </div>
</section>
<footer class="footer">
  <div class="logo-footer">
    <svg viewBox="0 0 100 100">
      <circle cx="50" cy="50" r="35" fill="none" stroke="#00F5FF" stroke-width="2"/>
      <polyline points="68,28 78,20 74,35 80,42" fill="none" stroke="#FF2D95" stroke-width="2"/>
      <circle cx="50" cy="50" r="8" fill="#FF2D95"/>
    </svg>
  </div>
  <p>R O U E N</p>
</footer>
</body>
</html>'''
    dst = os.path.join(OUT, "index.html")
    with open(dst, "w") as f:
        f.write(html)
    print(f"[Neon Nights] Site → {dst}")


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
