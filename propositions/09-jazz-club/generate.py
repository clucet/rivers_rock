#!/usr/bin/env python3
"""Generate all Jazz Club assets — Proposition n°9."""

import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))
from logoutils import (
    create_bleed_canvas, save_with_crop_marks,
    pillow_grain_overlay,
    draw_qr_pillow,
    BEBAS_PATH, MONTSERRAT_PATH, DMMONO_PATH, PLAYFAIR_PATH, KARLA_PATH,
)
from palette import JAZZ_CLUB as CFG
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
OR = CFG.rl("or_bruni")
CUIVRE = CFG.rl("cuivre")
ROUGE = CFG.rl("rouge_velours")
IVOIRE = CFG.rl("blanc_ivoire")

NUIT_PIL = CFG.pil("nuit")
OR_PIL = CFG.pil("or_bruni")
CUIVRE_PIL = CFG.pil("cuivre")
ROUGE_PIL = CFG.pil("rouge_velours")
IVOIRE_PIL = CFG.pil("blanc_ivoire")
BLANC_PIL = (255, 255, 255)

pdfmetrics.registerFont(TTFont("PlayfairDisplay", PLAYFAIR_PATH))
pdfmetrics.registerFont(TTFont("Karla", KARLA_PATH))
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


def jazz_logo_reportlab(cv, cx, cy, scale=1.0):
    """Jazz Club logo: circle + arc text + gold line."""
    r = 25 * scale
    cv.setStrokeColor(OR)
    cv.setLineWidth(2 * scale)
    cv.circle(cx, cy, r, stroke=1, fill=0)
    cv.setStrokeColor(Color(1, 1, 1, alpha=0.2))
    cv.setLineWidth(0.5 * scale)
    cv.circle(cx, cy, r + 4 * scale, stroke=1, fill=0)
    cv.line(cx - r * 1.2, cy, cx + r * 1.2, cy)


def jazz_logo_pillow(draw, cx, cy, scale=1.0):
    """Jazz Club logo for Pillow."""
    r = 25 * scale
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=OR_PIL, width=max(1, int(2 * scale)))
    draw.ellipse([cx - r - 4 * scale, cy - r - 4 * scale, cx + r + 4 * scale, cy + r + 4 * scale],
                 outline=(255, 255, 255, 50), width=max(1, int(scale)))
    draw.line([(cx - r * 1.2, cy), (cx + r * 1.2, cy)], fill=OR_PIL, width=max(1, int(scale)))


def gen_setlist():
    W, H = A4
    path = os.path.join(PDF, "setlist-jazz-club.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, W, H)

    for i in range(120):
        t = i / 119
        r = NUIT.red + (ROUGE.red - NUIT.red) * t
        g = NUIT.green + (ROUGE.green - NUIT.green) * t
        b = NUIT.blue + (ROUGE.blue - NUIT.blue) * t
        cv.setFillColor(Color(r, g, b))
        cv.rect(0, i * H / 120, W, H / 120 + 1, stroke=0, fill=1)

    random.seed(42)
    for _ in range(3000):
        cv.setFillColor(Color(1, 1, 1, alpha=random.uniform(0.03, 0.07)))
        cv.circle(random.uniform(0, W), random.uniform(0, H), random.uniform(0.3, 1.0), stroke=0, fill=1)

    jazz_logo_reportlab(cv, W / 2, H - 110, 2.5)
    cv.setFillColor(IVOIRE)
    cv.setFont("PlayfairDisplay", 18)
    cv.drawCentredString(W / 2, H - 160, "RIVERS ROCK")
    cv.setFillColor(OR)
    cv.setFont("PlayfairDisplay", 24)
    cv.drawCentredString(W / 2, H - 190, "SETLIST")

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
            w = pdfmetrics.stringWidth(longest, "PlayfairDisplay", mid)
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
        bg = ROUGE if is_green else NUIT
        cv.setFillColor(Color(0, 0, 0, alpha=0.20))
        cv.roundRect(cl + 3, cb - 3, card_w, card_h, card_r, stroke=0, fill=1)
        for i in range(30):
            t = i / 29
            l = 0.12 * (1 - t)
            c = Color(min(1, bg.red + l), min(1, bg.green + l), min(1, bg.blue + l))
            cv.setFillColor(c)
            cv.rect(cl, cb + i * card_h / 30, card_w, card_h / 30 + 0.5, stroke=0, fill=1)
        cv.setStrokeColor(OR)
        cv.setLineWidth(0.5)
        cv.roundRect(cl, cb, card_w, card_h, card_r, stroke=1, fill=0)

        aw = pdfmetrics.stringWidth(artist, "PlayfairDisplay", us)
        tw_ = 24 + 8 + aw
        sx = cx - tw_ / 2
        bcy = cy + 15
        cv.setFillColor(IVOIRE)
        cv.circle(sx + 12, bcy, 12, stroke=0, fill=1)
        cv.setFillColor(OR)
        cv.setFont("Karla", 10)
        cv.drawCentredString(sx + 12, bcy - 4.5, f"{idx+1:02d}")
        cv.setFillColor(IVOIRE)
        cv.setFont("PlayfairDisplay", us)
        cv.drawString(sx + 24 + 8, cy + 6, artist)
        if title:
            cv.setFillColor(Color(1, 1, 1, alpha=0.7))
            ts = 12
            tww = pdfmetrics.stringWidth(title, "Karla", ts)
            if tww > card_w - 32:
                ts *= (card_w - 32) / tww
            cv.setFont("Karla", ts)
            cv.drawCentredString(cx, cy - 17, title)

    cv.setFillColor(Color(1, 1, 1, alpha=0.2))
    cv.setFont("DMMono", 7)
    text, tr = "R O U E N", 6
    x = W / 2 - (sum(pdfmetrics.stringWidth(c, "DMMono", 7) for c in text) + tr * (len(text) - 1)) / 2
    for c in text:
        w = pdfmetrics.stringWidth(c, "DMMono", 7)
        cv.drawString(x, 14, c)
        x += w + tr
    save_with_crop_marks(cv, _, _, bleed)
    print(f"[Jazz Club] Setlist → {path}")


def gen_poster():
    W, H = A4
    path = os.path.join(PDF, "poster-jazz-club.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, W, H)
    for i in range(120):
        t = i / 119
        r = NUIT.red + (ROUGE.red - NUIT.red) * t
        g = NUIT.green + (ROUGE.green - NUIT.green) * t
        b = NUIT.blue + (ROUGE.blue - NUIT.blue) * t
        cv.setFillColor(Color(r, g, b))
        cv.rect(0, i * H / 120, W, H / 120 + 1, stroke=0, fill=1)
    random.seed(42)
    for _ in range(3000):
        cv.setFillColor(Color(1, 1, 1, alpha=random.uniform(0.03, 0.07)))
        cv.circle(random.uniform(0, W), random.uniform(0, H), random.uniform(0.3, 1.0), stroke=0, fill=1)

    jazz_logo_reportlab(cv, W / 2, H - 190, 2.5)
    cv.setFillColor(IVOIRE)
    cv.setFont("PlayfairDisplay", 12)
    cv.drawCentredString(W / 2, H - 250, "RIVERS ROCK")
    cv.setFillColor(OR)
    cv.setFont("Karla", 10)
    cv.drawCentredString(W / 2, H - 270, "PROCHAIN CONCERT")
    cv.setFillColor(IVOIRE)
    cv.setFont("PlayfairDisplay", 48)
    cv.drawCentredString(W / 2, H - 340, "VEN 26 JUIN 2026")
    cv.setFillColor(Color(1, 1, 1, alpha=0.6))
    cv.setFont("Karla", 16)
    cv.drawCentredString(W / 2, H - 380, "Montigny · 19h30")
    cv.setStrokeColor(OR)
    cv.setLineWidth(1)
    cv.line(W / 2 - 80, H - 410, W / 2 + 80, H - 410)
    cv.setFillColor(Color(1, 1, 1, alpha=0.2))
    cv.setFont("DMMono", 7)
    text, tr = "R O U E N", 6
    x = W / 2 - (sum(pdfmetrics.stringWidth(c, "DMMono", 7) for c in text) + tr * (len(text) - 1)) / 2
    for c in text:
        w = pdfmetrics.stringWidth(c, "DMMono", 7)
        cv.drawString(x, 14, c)
        x += w + tr
    save_with_crop_marks(cv, _, _, bleed)
    print(f"[Jazz Club] Poster → {path}")


def gen_flyer():
    FW, FH = A6
    path = os.path.join(PDF, "flyer-jazz-club.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, A4[0], A4[1])
    def grad(cv, x, y, w, h):
        for i in range(60):
            t = i / 59
            r = NUIT.red + (ROUGE.red - NUIT.red) * t
            g = NUIT.green + (ROUGE.green - NUIT.green) * t
            b = NUIT.blue + (ROUGE.blue - NUIT.blue) * t
            cv.setFillColor(Color(r, g, b))
            cv.rect(x, y + i * h / 60, w, h / 60 + 0.5, stroke=0, fill=1)

    def draw_recto(cv, ox, oy):
        grad(cv, ox, oy, FW, FH)
        cx = ox + FW / 2
        jazz_logo_reportlab(cv, cx, oy + FH - 50, 1.0)
        cv.setFillColor(IVOIRE)
        cv.setFont("PlayfairDisplay", 14)
        cv.drawCentredString(cx, oy + FH - 80, "RIVERS ROCK")
        cv.setFillColor(OR)
        cv.setFont("PlayfairDisplay", 28)
        cv.drawCentredString(cx, oy + FH - 145, "VEN 26 JUIN")
        cv.setFillColor(Color(1, 1, 1, alpha=0.6))
        cv.setFont("Karla", 10)
        cv.drawCentredString(cx, oy + FH - 175, "Montigny · 19h30")

    def draw_verso(cv, ox, oy):
        grad(cv, ox, oy, FW, FH)
        cx = ox + FW / 2
        cv.setFillColor(IVOIRE)
        cv.setFont("PlayfairDisplay", 14)
        cv.drawCentredString(cx, oy + FH - 40, "RIVERS ROCK")
        bio = ["Groupe rouennais forme en 2024", "au centre Education et Formation", "du Petit-Quevilly.",
               "", "Rosaria - batterie", "Christophe - basse", "Nicolas - guitare",
               "David - guitare / chant", "Virginie - chant", "", "Rock - Pop-Rock - Inde - Alternatif"]
        cv.setFillColor(Color(1, 1, 1, alpha=0.7))
        cv.setFont("Karla", 7)
        y = oy + FH - 80
        for line in bio:
            cv.drawCentredString(cx, y, line)
            y -= 12
        cv.setFillColor(OR)
        cv.setFont("Karla", 7)
        cv.drawCentredString(cx, y - 6, "Contactez-nous pour programmer un concert")
        cv.setFillColor(Color(0, 0, 0, alpha=0.35))
        cv.setFont("DMMono", 6)
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
    cv.save()
    print(f"[Jazz Club] Flyer → {path}")


def gen_social():
    def lerp(c1, c2, t):
        return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))
    font_play = ImageFont.truetype(PLAYFAIR_PATH, 56)
    font_play_m = ImageFont.truetype(PLAYFAIR_PATH, 40)
    font_karla = ImageFont.truetype(KARLA_PATH, 22)
    font_tag = ImageFont.truetype(DMMONO_PATH, 14)

    w, h = 1080, 1080
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    cx, cy = w / 2, h / 2
    mr = math.sqrt(cx**2 + cy**2)
    for i in range(300):
        t = i / 299
        r = mr * t
        if t < 0.15:
            c = lerp(OR_PIL, ROUGE_PIL, t / 0.15)
        elif t < 0.4:
            c = lerp(ROUGE_PIL, NUIT_PIL, (t - 0.15) / 0.25)
        else:
            c = lerp(NUIT_PIL, ROUGE_PIL, (t - 0.4) / 0.6)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)

    img = pillow_grain_overlay(img, 0.08, seed=10)
    jazz_logo_pillow(draw, w / 2, 140, 2.5)
    bbox = draw.textbbox((0, 0), "RIVERS ROCK", font=font_play)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 155), "RIVERS ROCK", fill=IVOIRE_PIL, font=font_play)
    bbox = draw.textbbox((0, 0), "PROCHAIN CONCERT", font=font_karla)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 380), "PROCHAIN CONCERT", fill=OR_PIL, font=font_karla)
    bbox = draw.textbbox((0, 0), "VEN 26 JUIN 2026", font=font_play_m)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 440), "VEN 26 JUIN 2026", fill=IVOIRE_PIL, font=font_play_m)
    bbox = draw.textbbox((0, 0), "Montigny · 19h30", font=font_karla)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 520), "Montigny · 19h30", fill=(180, 170, 160), font=font_karla)

    qx, qy, qs = w / 2 - 60, 660, 120
    draw.rectangle([qx, qy, qx + qs, qy + qs], fill=IVOIRE_PIL, outline=OR_PIL, width=3)
    bbox = draw.textbbox((0, 0), "QR", font=font_karla)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((qx + (qs - tw) / 2, qy + (qs - th) / 2), "QR", fill=NUIT_PIL, font=font_karla)
    bbox = draw.textbbox((0, 0), "@riversrockrouen", font=font_tag)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 860), "@riversrockrouen", fill=(180, 170, 160), font=font_tag)
    img.save(os.path.join(TMPL, "instagram-post.png"))

    w, h = 1080, 1920
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    cx, cy = w / 2, h / 2
    mr = math.sqrt(cx**2 + cy**2)
    for i in range(300):
        t = i / 299
        r = mr * t
        if t < 0.1:
            c = lerp(IVOIRE_PIL, OR_PIL, t / 0.1)
        elif t < 0.3:
            c = lerp(OR_PIL, NUIT_PIL, (t - 0.1) / 0.2)
        else:
            c = lerp(NUIT_PIL, ROUGE_PIL, (t - 0.3) / 0.7)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)

    img = pillow_grain_overlay(img, 0.08, seed=20)
    font_play_d = ImageFont.truetype(PLAYFAIR_PATH, 100)
    jazz_logo_pillow(draw, w / 2, 180, 3.0)
    bbox = draw.textbbox((0, 0), "RIVERS ROCK", font=font_play)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2 + 20, 195), "RIVERS ROCK", fill=IVOIRE_PIL, font=font_play)
    bbox = draw.textbbox((0, 0), "VEN 26 JUIN", font=font_play_d)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 650), "VEN 26 JUIN", fill=OR_PIL, font=font_play_d)
    bbox = draw.textbbox((0, 0), "Montigny · 19h30", font=font_karla)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 840), "Montigny · 19h30", fill=IVOIRE_PIL, font=font_karla)
    bbox = draw.textbbox((0, 0), "@riversrockrouen", font=font_tag)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 1750), "@riversrockrouen", fill=(180, 170, 160), font=font_tag)
    img.save(os.path.join(TMPL, "instagram-story.png"))
    print(f"[Jazz Club] Social → {TMPL}")


def gen_banners():
    for name, w, h, logo_s in [("facebook-banner.png", 1640, 624, 48), ("youtube-banner.png", 2560, 1440, 72)]:
        img = Image.new("RGB", (w, h))
        draw = ImageDraw.Draw(img)
        for i in range(120):
            t = i / 119
            c = tuple(int(a + (b - a) * t) for a, b in zip(NUIT_PIL, ROUGE_PIL))
            draw.rectangle([0, i * h / 120, w, (i + 1) * h / 120], fill=c)
        img = pillow_grain_overlay(img, 0.08, seed=30)
        font_logo = ImageFont.truetype(PLAYFAIR_PATH, logo_s)
        tw = draw.textbbox((0, 0), "RIVERS ROCK", font=font_logo)[2]
        sym_r = logo_s * 0.5
        gap = sym_r * 0.3
        sx = (w - (sym_r * 2 + gap + tw)) / 2
        jazz_logo_pillow(draw, sx + sym_r, h / 2, sym_r / 22.0)
        draw.text((sx + sym_r * 2 + gap, h / 2 - tw * 0.25), "RIVERS ROCK", fill=IVOIRE_PIL, font=font_logo)
        font_sub = ImageFont.truetype(KARLA_PATH, 14)
        draw.text(((w - (bbox := draw.textbbox((0, 0), "Reprises rock - Rouen", font=font_sub))[2] + bbox[0]) / 2, h - 50), "Reprises rock - Rouen", fill=OR_PIL, font=font_sub)
        img.save(os.path.join(TMPL, name))
    print(f"[Jazz Club] Banners → {TMPL}")


def gen_avatar():
    S = 500
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    jazz_logo_pillow(draw, S / 2, S / 2, 6.0)
    font = ImageFont.truetype(PLAYFAIR_PATH, 28)
    bbox = draw.textbbox((0, 0), "RR", font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((S - tw) / 2, S / 2 + 60), "RR", fill=OR_PIL, font=font)
    img.save(os.path.join(TMPL, "avatar.png"))
    print(f"[Jazz Club] Avatar → {TMPL}")


def gen_stickers():
    from reportlab.lib.units import mm
    W, H = A4
    SR = 40 * mm
    MX = (W - 2 * SR * 2) / 3
    MY = (H - 3 * SR * 2) / 4
    centers = [(MX + SR + c * (MX + SR * 2), MY + SR + r * (MY + SR * 2)) for c in range(2) for r in range(3)]
    path = os.path.join(PDF, "stickers-jazz-club.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, A4[0], A4[1])
    for cx, cy in centers:
        for i in range(60):
            t = i / 59
            r = NUIT.red + (ROUGE.red - NUIT.red) * t
            g = NUIT.green + (ROUGE.green - NUIT.green) * t
            b = NUIT.blue + (ROUGE.blue - NUIT.blue) * t
            cv.setFillColor(Color(r, g, b))
            y = cy - SR + i * SR * 2 / 60
            cv.rect(cx - SR, y, SR * 2, SR * 2 / 60 + 0.5, stroke=0, fill=1)
        cv.setStrokeColor(OR)
        cv.setLineWidth(2)
        cv.circle(cx, cy, SR, stroke=1, fill=0)
        sr = SR * 0.50
        cv.setStrokeColor(Color(1, 1, 1, alpha=0.2))
        cv.setLineWidth(0.5)
        cv.circle(cx, cy, sr + 4, stroke=1, fill=0)
        jazz_logo_reportlab(cv, cx, cy, sr / 22.0)
        cv.setFillColor(IVOIRE)
        cv.setFont("PlayfairDisplay", 7)
        cv.drawCentredString(cx, cy + sr + 8, "RIVERS ROCK")
    cv.save()
    print(f"[Jazz Club] Stickers → {path}")


def gen_tshirt():
    from reportlab.lib.units import mm
    w, h = A4
    sizes = [("S", 22 * mm, w / 4, h - 200), ("M", 28 * mm, w * 3 / 4, h - 200),
             ("L", 34 * mm, w / 4, h - 440), ("XL", 40 * mm, w * 3 / 4, h - 440)]
    path = os.path.join(PDF, "tshirt-jazz-club.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, A4[0], A4[1])
    cv.setFillColor(Color(0, 0, 0, alpha=0.04))
    cv.rect(0, 0, w, h, stroke=0, fill=1)
    for label, sr, cx, cy in sizes:
        jazz_logo_reportlab(cv, cx, cy, sr / 22.0)
        cv.setFillColor(IVOIRE)
        cv.setFont("PlayfairDisplay", max(8, int(sr * 1.4)))
        cv.drawCentredString(cx, cy + sr * 0.6 + 4, "RIVERS ROCK")
        if label:
            cv.setFillColor(Color(0, 0, 0, alpha=0.3))
            cv.setFont("Karla", 7)
            cv.drawCentredString(cx, cy + sr + 60, label)
    cv.save()
    print(f"[Jazz Club] T-shirt → {path}")


def gen_animated():
    html = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rivers Rock — Jazz Club</title>
<link rel="icon" type="image/png" sizes="32x32" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAMlJREFUWEft1rENwjAQBdD/FYyAWIAJYAQKOkZgBEZgBDoWYARGYAQK4kiWLNnxnU8UKZLr/Pd9thMEAf4PQAiAEAChIyA6AgI7ArLWPuc8zjnnC85a+5xzHgEgBEAIAOrA3Xsf9z17ZgBIfYAx5hVjrN77z3ffH4DVByClBICttV+t3bee1gcgpQQAay0B7L0TAOYcBPAcB3NODPCe0DHG5xhjA0AIgBAAoSMgOgICOwKy1j7nnMec8wsnhHDOeRxjjACEEADhCAgBEB0BgR0BWWufc85jzvmFE8Kccx5jjACEEADhCEgIAOgICAEQHQH/Ab3+V/+tKtRsAAAAAElFTkSuQmCC">
<style>
*{margin:0;padding:0}
body{width:1080px;height:1920px;overflow:hidden;background:#0A0A0A;display:flex;align-items:center;justify-content:center}
canvas{position:absolute;top:0;left:0;width:1080px;height:1920px}
svg{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:400px;height:400px;overflow:visible}
.spolight{position:fixed;top:0;left:0;width:100%;height:100%;background:radial-gradient(ellipse at 50% 40%, rgba(201,168,108,0.04) 0%, transparent 60%);pointer-events:none;z-index:0}
.circle{fill:none;stroke:#C9A86C;stroke-width:2.5;stroke-dasharray:250;stroke-dashoffset:250;animation:drawC 1.5s ease-out .3s forwards;filter:drop-shadow(0 0 15px rgba(201,168,108,0.3))}
.inner{fill:none;stroke:rgba(255,255,255,0.08);stroke-width:1;stroke-dasharray:4 4;opacity:0;animation:fadeT .6s ease-out 1.2s forwards}
@keyframes drawC{to{stroke-dashoffset:0}}
@keyframes fadeT{to{opacity:1}}
.letter{font-family:'Playfair Display','Georgia',serif;font-size:32px;fill:#F5F0E8;opacity:0}
.lR{animation:drop .3s ease-out 2.0s forwards}
.lI{animation:drop .3s ease-out 2.15s forwards}
.lV{animation:drop .3s ease-out 2.3s forwards}
.lE{animation:drop .3s ease-out 2.45s forwards}
.lR2{animation:drop .3s ease-out 2.6s forwards}
.lS{animation:drop .3s ease-out 2.75s forwards}
.lROCK_R{animation:slide .4s ease-out 3.0s forwards}
.lROCK_O{animation:slide .4s ease-out 3.15s forwards}
.lROCK_C{animation:slide .4s ease-out 3.3s forwards}
.lROCK_K{animation:slide .4s ease-out 3.45s forwards}
@keyframes drop{0%{opacity:0;transform:translateY(-20px)}100%{opacity:1;transform:translateY(0)}}
@keyframes slide{0%{opacity:0;transform:translateX(120px)}100%{opacity:1;transform:translateX(0)}}
@media(prefers-reduced-motion){*{animation:none!important}}
</style>
</head>
<body>
<div class="spolight"></div>
<canvas id="p"></canvas>
<svg viewBox="-200 -200 400 400">
  <circle class="circle" cx="0" cy="0" r="50"/>
  <circle class="inner" cx="0" cy="0" r="56"/>
  <line x1="-65" y1="0" x2="65" y2="0" stroke="#C9A86C" stroke-width="1.5" opacity="0"/>
  <text x="-60" y="-52.9" text-anchor="middle" class="letter lR">R</text>
  <text x="-36" y="-71.4" text-anchor="middle" class="letter lI">I</text>
  <text x="-12" y="-79.1" text-anchor="middle" class="letter lV">V</text>
  <text x="12" y="-79.1" text-anchor="middle" class="letter lE">E</text>
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
for(let i=0;i<15;i++){ps.push({x:Math.random()*1080,y:Math.random()*1920,s:Math.random()*1+0.3,a:Math.random()*0.04+0.01})}
function draw(){ctx.clearRect(0,0,1080,1920);
ctx.fillStyle='#0A0A0A';ctx.fillRect(0,0,1080,1920);
for(const p of ps){ctx.beginPath();ctx.arc(p.x,p.y,p.s,0,Math.PI*2);ctx.fillStyle='rgba(201,168,108,'+p.a+')';ctx.fill();p.y-=0.1;if(p.y<0){p.y=1920;p.x=Math.random()*1080}}
requestAnimationFrame(draw)}draw();
</script>
</body>
</html>'''
    path = os.path.join(TMPL, "logo-animated-jazz-club.html")
    with open(path, "w") as f:
        f.write(html)
    print(f"[Jazz Club] Animated logo → {path}")


def gen_site():
    html = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rivers Rock — Jazz Club</title>
<link rel="icon" type="image/png" sizes="32x32" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAMlJREFUWEft1rENwjAQBdD/FYyAWIAJYAQKOkZgBEZgBDoWYARGYAQK4kiWLNnxnU8UKZLr/Pd9thMEAf4PQAiAEAChIyA6AgI7ArLWPuc8zjnnC85a+5xzHgEgBEAIAOrA3Xsf9z17ZgBIfYAx5hVjrN77z3ffH4DVByClBICttV+t3bee1gcgpQQAay0B7L0TAOYcBPAcB3NODPCe0DHG5xhjA0AIgBAAoSMgOgICOwKy1j7nnMec8wsnhHDOeRxjjACEEADhCAgBEB0BgR0BWWufc85jzvmFE8Kccx5jjACEEADhCEgIAOgICAEQHQH/Ab3+V/+tKtRsAAAAAElFTkSuQmCC">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600&family=Karla:wght@300;400;600&family=DM+Mono&display=swap" rel="stylesheet">
<style>
:root{--nuit:#0A0A0A;--or:#C9A86C;--cuivre:#B87333;--rouge:#8B1A1A;--ivoire:#F5F0E8}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:70px}
body{font-family:'Karla',sans-serif;font-weight:300;color:var(--ivoire);min-height:100vh;background:var(--nuit)}
.bg-grain{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23g)' opacity='0.05'/%3E%3C/svg%3E")}
nav{position:fixed;top:0;width:100%;padding:14px 32px;display:flex;justify-content:space-between;align-items:center;z-index:100;background:rgba(10,10,10,0.95);backdrop-filter:blur(8px);border-bottom:1px solid rgba(201,168,108,0.12)}
nav .logo-small{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--ivoire)}
nav .logo-small span{font-family:'Playfair Display',serif;font-size:16px;letter-spacing:1px;text-transform:uppercase}
nav a{color:rgba(245,240,232,0.5);text-decoration:none;font-size:12px;letter-spacing:1px;padding:6px 14px;transition:.3s}
nav a:hover{color:var(--or)}
.hero{position:relative;z-index:1;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:120px 24px 80px;background:radial-gradient(ellipse at 50% 35%, rgba(201,168,108,0.06) 0%, transparent 60%)}
.hero .logo-hero svg{width:120px;height:120px;margin-bottom:12px}
.hero h1{font-family:'Playfair Display',serif;font-size:clamp(36px,8vw,72px);letter-spacing:2px;color:var(--ivoire);margin-bottom:4px}
.hero .tagline{font-family:'Karla',sans-serif;font-size:14px;color:var(--or);letter-spacing:2px;text-transform:uppercase;margin-bottom:24px}
.hero p{font-size:15px;line-height:1.7;color:rgba(245,240,232,0.5);max-width:500px}
.section{position:relative;z-index:1;padding:80px 24px;max-width:700px;margin:0 auto}
.section h2{font-family:'Playfair Display',serif;font-size:28px;letter-spacing:1px;color:var(--or);margin-bottom:32px;text-align:center}
.section h2::after{content:'';display:block;width:60px;height:1px;background:var(--or);margin:8px auto 0}
.section p{font-size:15px;line-height:1.8;color:rgba(245,240,232,0.55);margin-bottom:20px}
.section-alt{background:rgba(139,26,26,0.06);border-top:1px solid rgba(201,168,108,0.04);border-bottom:1px solid rgba(201,168,108,0.04)}
.members-grid{display:flex;flex-wrap:wrap;justify-content:center;gap:20px;margin-top:20px}
.member-card{flex:0 0 180px;text-align:center;padding:24px 12px;background:rgba(139,26,26,0.06);border-radius:6px;border:1px solid rgba(201,168,108,0.08);transition:.25s}
.member-card:hover{background:rgba(201,168,108,0.04);border-color:var(--or)}
.member-card .avatar-circle{width:68px;height:68px;border-radius:50%;background:linear-gradient(135deg,var(--or),var(--cuivre));margin:0 auto 10px;display:flex;align-items:center;justify-content:center;font-family:'Playfair Display',serif;font-size:24px;color:var(--nuit)}
.member-card h3{font-family:'Playfair Display',serif;font-size:16px;color:var(--or);margin-bottom:3px}
.member-card p{font-family:'Karla',sans-serif;font-size:12px;color:rgba(245,240,232,0.35)}
.concerts-list{list-style:none;padding:0}
.concerts-list li{padding:14px 20px;margin-bottom:10px;background:rgba(139,26,26,0.05);border-left:3px solid var(--or);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px}
.concerts-list .date{font-family:'Playfair Display',serif;font-size:15px;color:var(--or)}
.concerts-list .lieu{font-size:14px;color:rgba(245,240,232,0.45)}
.concerts-list .status{font-size:10px;padding:3px 10px;background:rgba(201,168,108,0.08);color:var(--or)}
.contact-info{text-align:center;margin-top:16px}
.contact-info p{font-size:15px;margin-bottom:6px;color:rgba(245,240,232,0.5)}
.contact-info .email{font-family:'DM Mono',monospace;font-size:14px;color:var(--or);text-decoration:none;transition:.2s}
.contact-info .email:hover{color:var(--ivoire)}
.links-social{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:24px}
.links-social a{color:rgba(245,240,232,0.4);text-decoration:none;font-size:11px;padding:8px 18px;border:1px solid rgba(201,168,108,0.15);transition:.3s;letter-spacing:1px}
.links-social a:hover{color:var(--ivoire);border-color:var(--or)}
.footer{position:relative;z-index:1;text-align:center;padding:44px 24px;border-top:1px solid rgba(201,168,108,0.05)}
.footer svg{width:80px;height:80px;margin-bottom:8px;opacity:0.25}
.footer p{font-family:'DM Mono',monospace;font-size:10px;letter-spacing:6px;color:rgba(245,240,232,0.15)}
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
      <circle cx="50" cy="50" r="35" fill="none" stroke="#C9A86C" stroke-width="2"/>
      <circle cx="50" cy="50" r="40" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="1" stroke-dasharray="3 3"/>
      <line x1="15" y1="50" x2="85" y2="50" stroke="#C9A86C" stroke-width="1"/>
    </svg>
  </div>
  <h1>RIVERS ROCK</h1>
  <div class="tagline">Reprises rock — Rouen</div>
  <p>Groupe rouennais forme en 2024. Rock, pop-rock, inde et alternatif. La Seine la nuit, le club, l'atmosphere.</p>
</section>
<section id="groupe" class="section">
  <h2>Le groupe</h2>
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
  <div class="concerts-list"><li><span class="date">VEN 26 JUIN 2026</span><span class="lieu">Montigny · 19h30</span><span class="status">Concert</span></li></div>
  <div style="margin-top:16px;border-radius:8px;overflow:hidden;max-width:400px;margin-left:auto;margin-right:auto"><img src="../../../images/IMG-20260620-WA0001.jpg" style="width:100%;height:auto;display:block;border-radius:8px" alt="Affiche"></div>
</section>
<section id="musique" class="section">
  <h2>Musique</h2>
  <p>Decouvrez Rivers Rock en action — extraits live et playlist a venir.</p>
  <div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border:1px solid rgba(201,168,108,0.15);margin-top:16px">
    <div style="position:absolute;top:0;left:0;width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,0.3);color:rgba(245,240,232,0.2);font-family:sans-serif">Video a venir</div>
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
  <svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="35" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="1"/><line x1="20" y1="50" x2="80" y2="50" stroke="rgba(255,255,255,0.1)" stroke-width="1"/></svg>
  <p>R O U E N</p>
</footer>
</body>
</html>'''
    dst = os.path.join(OUT, "index.html")
    with open(dst, "w") as f:
        f.write(html)
    print(f"[Jazz Club] Site → {dst}")


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
