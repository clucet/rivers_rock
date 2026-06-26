#!/usr/bin/env python3
"""Generate all Scène & Vintage assets — Proposition 03 (retenue)."""
# SVG logo available at: ../propositions/XXX/assets/logo.svg


import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))
from logoutils import (
    create_bleed_canvas, save_with_crop_marks,
    draw_qr_pillow,
    reportlab_crest, pillow_crest, pillow_crest_timbre,
    pillow_grain_overlay,
    draw_qr_reportlab,
    pillow_monogramme_rr,
    BEBAS_PATH, MONTSERRAT_PATH, SPACE_MONO_PATH, ANTON_PATH,
)
from palette import SCENE_VINTAGE as CFG
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
TEAL = CFG.rl("teal_profond")
ACCENT = CFG.rl("accent")
TERRA = CFG.rl("terracotta")
OR = CFG.rl("or_vieilli")
BLANC = CFG.rl("blanc")

BLEU_PIL = CFG.pil("bleu_seine")
TEAL_PIL = CFG.pil("teal_profond")
ACCENT_PIL = CFG.pil("accent")
TERRA_PIL = CFG.pil("terracotta")
OR_PIL = CFG.pil("or_vieilli")
BLANC_PIL = (255, 255, 255)

pdfmetrics.registerFont(TTFont("BebasNeue", BEBAS_PATH))
pdfmetrics.registerFont(TTFont("Montserrat", MONTSERRAT_PATH))

from setlist_data import SETLIST, GREEN_INDICES

# ── Setlist ──

def gen_setlist():
    W, H = A4
    path = os.path.join(PDF, "setlist-scene-vintage.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, W, H)

    for i in range(120):
        t = i / 119
        r = BLEU.red + (TEAL.red - BLEU.red) * t
        g = BLEU.green + (TEAL.green - BLEU.green) * t
        b = BLEU.blue + (TEAL.blue - BLEU.blue) * t
        cv.setFillColor(Color(r, g, b))
        cv.rect(0, i * H / 120, W, H / 120 + 1, stroke=0, fill=1)

    random.seed(42)
    for _ in range(3000):
        cv.setFillColor(Color(1, 1, 1, alpha=random.uniform(0.02, 0.06)))
        cv.circle(random.uniform(0, W), random.uniform(0, H),
                  random.uniform(0.3, 1.0), stroke=0, fill=1)

    cv.setFillColor(Color(1, 1, 1, alpha=0.06))
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

    cv.setStrokeColor(OR)
    cv.setLineWidth(1.5)
    segs = 200
    sw = W / segs
    p = cv.beginPath()
    p.moveTo(0, H - 45)
    for i in range(segs + 1):
        px = i * sw
        py = H - 45 + 8 * math.sin(i * 2 * math.pi / 32)
        p.lineTo(px, py)
    cv.drawPath(p, stroke=1, fill=0)

    reportlab_crest(cv, W / 2, H - 115, 2.2)

    cv.setFillColor(ACCENT)
    cv.setFont("BebasNeue", 28)
    cv.drawCentredString(W / 2, H - 165, "SETLIST")
    cv.setStrokeColor(OR)
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
        bg = TEAL if is_green else TERRA

        cv.setFillColor(Color(0, 0, 0, alpha=0.20))
        cv.roundRect(cl + 4, cb - 4, card_w, card_h, card_r, stroke=0, fill=1)

        for i in range(30):
            t = i / 29
            l = 0.18 * (1 - t)
            c = Color(min(1, bg.red + l), min(1, bg.green + l), min(1, bg.blue + l))
            cv.setFillColor(c)
            cv.rect(cl, cb + i * card_h / 30, card_w, card_h / 30 + 0.5, stroke=0, fill=1)

        cv.setStrokeColor(Color(1, 1, 1, alpha=0.50))
        cv.setLineWidth(0.5)
        cv.roundRect(cl, cb, card_w, card_h, card_r, stroke=1, fill=0)
        cv.setStrokeColor(OR)
        cv.setLineWidth(0.8)
        cv.roundRect(cl - 0.5, cb - 0.5, card_w + 1, card_h + 1, card_r, stroke=1, fill=0)

        aw = pdfmetrics.stringWidth(artist, "BebasNeue", us)
        tw = 24 + 8 + aw
        sx = cx - tw / 2

        ncol = OR if is_green else ACCENT
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
    save_with_crop_marks(cv, _, _, bleed)
    print(f"[Scène & Vintage] Setlist → {path}")


# ── Poster ──

def gen_poster():
    W, H = int(A4[0]), int(A4[1])
    path = os.path.join(PDF, "poster-scene-vintage.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, W, H)

    for i in range(120):
        t = i / 119
        r = BLEU.red + (TEAL.red - BLEU.red) * t
        g = BLEU.green + (TEAL.green - BLEU.green) * t
        b = BLEU.blue + (TEAL.blue - BLEU.blue) * t
        cv.setFillColor(Color(r, g, b))
        cv.rect(0, i * H / 120, W, H / 120 + 1, stroke=0, fill=1)

    random.seed(42)
    for _ in range(3000):
        cv.setFillColor(Color(1, 1, 1, alpha=random.uniform(0.02, 0.06)))
        cv.circle(random.uniform(0, W), random.uniform(0, H),
                  random.uniform(0.3, 1.0), stroke=0, fill=1)

    cv.setFillColor(Color(1, 1, 1, alpha=0.04))
    for y in range(20, H - 20, 8):
        for x in range(20, W - 20, 8):
            d = min(x, W - x, y, H - y)
            if d < 100:
                cv.setFillColor(Color(1, 1, 1, alpha=random.uniform(0.02, 0.06)))
                cv.circle(x, y, random.uniform(0.5, 1.5), stroke=0, fill=1)

    cv.setFillColor(Color(1, 1, 1, alpha=0.06))
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

    cv.setStrokeColor(OR)
    cv.setLineWidth(1.5)
    segs = 200
    sw = W / segs
    p = cv.beginPath()
    p.moveTo(0, H - 45)
    for i in range(segs + 1):
        px = i * sw
        py = H - 45 + 8 * math.sin(i * 2 * math.pi / 32)
        p.lineTo(px, py)
    cv.drawPath(p, stroke=1, fill=0)

    reportlab_crest(cv, W / 2, H - 190, 2.2)

    cv.setFillColor(OR)
    cv.setFont("Montserrat", 12)
    cv.drawCentredString(W / 2, H - 270, "LES SOIREES NOCTURNES")
    cv.setFillColor(BLANC)
    cv.setFont("BebasNeue", 56)
    cv.drawCentredString(W / 2, H - 340, "VEN 26 JUIN 2026")
    cv.setFillColor(Color(1, 1, 1, alpha=0.7))
    cv.setFont("Montserrat", 18)
    cv.drawCentredString(W / 2, H - 385, "Montigny · 19h30")

    cv.setStrokeColor(OR)
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
    save_with_crop_marks(cv, _, _, bleed)
    print(f"[Scène & Vintage] Poster → {path}")


# ── Flyer ──

def gen_flyer():
    FW, FH = A6
    path = os.path.join(PDF, "flyer-scene-vintage.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, A4[0], A4[1])

    def grad(cv, x, y, w, h):
        for i in range(60):
            t = i / 59
            r = BLEU.red + (TEAL.red - BLEU.red) * t
            g = BLEU.green + (TEAL.green - BLEU.green) * t
            b = BLEU.blue + (TEAL.blue - BLEU.blue) * t
            cv.setFillColor(Color(r, g, b))
            cv.rect(x, y + i * h / 60, w, h / 60 + 0.5, stroke=0, fill=1)

    def draw_recto(cv, ox, oy):
        grad(cv, ox, oy, FW, FH)
        cx = ox + FW / 2
        reportlab_crest(cv, cx, oy + FH - 55, 1.0)
        cv.setFillColor(BLANC)
        cv.setFont("BebasNeue", 28)
        cv.drawCentredString(cx, oy + FH - 110, "RIVERS ROCK")
        cv.setFillColor(OR)
        cv.setFont("BebasNeue", 34)
        cv.drawCentredString(cx, oy + FH - 170, "VEN 26 JUIN 2026")
        cv.setFillColor(Color(1, 1, 1, alpha=0.7))
        cv.setFont("Montserrat", 10)
        cv.drawCentredString(cx, oy + FH - 200, "Montigny · 19h30")

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

        qs = 30
        qx, qy2 = cx - qs / 2, y - 58
        cv.setFillColor(BLANC)
        cv.roundRect(qx, qy2, qs, qs, 4, stroke=0, fill=1)
        cv.setStrokeColor(OR)
        cv.setLineWidth(0.8)
        cv.roundRect(qx, qy2, qs, qs, 4, stroke=1, fill=0)
        cv.setFillColor(BLEU)
        cv.setFont("Montserrat", 7)
        draw_qr_reportlab(cv, cx, qy2 + qs / 2, qs - 4, fill_color=BLEU)

        cv.setFillColor(Color(1, 1, 1, alpha=0.4))
        cv.setFont("Montserrat", 7)
        cv.drawCentredString(cx, qy2 - 8, "@riversrock_rouen — riversrock.fr")

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
    print(f"[Scène & Vintage] Flyer → {path}")


# ── Social ──

def gen_social():
    def lerp(c1, c2, t):
        return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))

    font_anton = ImageFont.truetype(ANTON_PATH, 64) if ANTON_PATH else ImageFont.truetype(BEBAS_PATH, 64)
    font_space = ImageFont.truetype(SPACE_MONO_PATH, 22) if SPACE_MONO_PATH else ImageFont.truetype(MONTSERRAT_PATH, 22)
    font_mont = ImageFont.truetype(MONTSERRAT_PATH, 24)
    font_tag = ImageFont.truetype(SPACE_MONO_PATH, 14) if SPACE_MONO_PATH else ImageFont.truetype(MONTSERRAT_PATH, 14)

    w, h = 1080, 1080
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    cx, cy = w / 2, h / 2
    mr = math.sqrt(cx**2 + cy**2)
    for i in range(200):
        t = i / 199
        r = mr * t
        if t < 0.3:
            c = lerp(OR_PIL, TERRA_PIL, t / 0.3)
        else:
            c = lerp(TERRA_PIL, BLEU_PIL, (t - 0.3) / 0.7)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)

    pillow_crest(draw, w / 2 - 100, 160, 1.4)
    bbox = draw.textbbox((0, 0), "RIVERS ROCK", font=font_space)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2 + 100, 150), "RIVERS ROCK", fill=BLANC_PIL, font=font_space)

    bbox = draw.textbbox((0, 0), "LES SOIREES NOCTURNES", font=font_space)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 400), "LES SOIREES NOCTURNES", fill=BLANC_PIL, font=font_space)
    bbox = draw.textbbox((0, 0), "VEN 26 JUIN 2026", font=font_anton)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 470), "VEN 26 JUIN 2026", fill=OR_PIL, font=font_anton)
    bbox = draw.textbbox((0, 0), "Montigny · 19h30", font=font_mont)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 560), "Montigny · 19h30", fill=BLANC_PIL, font=font_mont)

    qx, qy, qs = w / 2 - 60, 680, 120
    draw.rounded_rectangle([qx, qy, qx + qs, qy + qs], radius=12, fill=BLANC_PIL, outline=TERRA_PIL, width=3)
    qr_img = draw_qr_pillow(None, 0, 0, qs - 12, fill_color=BLEU_PIL)
    if qr_img:
        img.paste(qr_img, (int(qx + 6), int(qy + 6)), qr_img if qr_img.mode == "RGBA" else None)

    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((qx + (qs - tw) / 2, qy + (qs - th) / 2), "QR", fill=BLEU_PIL, font=font_space)

    bbox = draw.textbbox((0, 0), "@riversrock_rouen", font=font_tag)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 870), "@riversrock_rouen", fill=BLANC_PIL, font=font_tag)

    img = pillow_grain_overlay(img, 0.04, seed=10)
    img.save(os.path.join(TMPL, "instagram-post.png"))

    # Story
    w, h = 1080, 1920
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    cx, cy = w / 2, h / 2
    mr = math.sqrt(cx**2 + cy**2)
    for i in range(300):
        t = i / 299
        r = mr * t
        if t < 0.3:
            c = lerp(OR_PIL, ACCENT_PIL, t / 0.3)
        else:
            c = lerp(ACCENT_PIL, TEAL_PIL, (t - 0.3) / 0.7)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)

    font_anton_d = ImageFont.truetype(ANTON_PATH, 120) if ANTON_PATH else ImageFont.truetype(BEBAS_PATH, 120)
    font_space_l = ImageFont.truetype(SPACE_MONO_PATH, 28) if SPACE_MONO_PATH else ImageFont.truetype(MONTSERRAT_PATH, 28)

    pillow_crest_timbre(draw, 180, 200, 1.6)

    bbox = draw.textbbox((0, 0), "VEN 26 JUIN 2026", font=font_anton_d)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 650), "VEN 26 JUIN 2026", fill=ACCENT_PIL, font=font_anton_d)
    bbox = draw.textbbox((0, 0), "Montigny · 19h30", font=font_space_l)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 850), "Montigny · 19h30", fill=BLANC_PIL, font=font_space_l)

    bbox = draw.textbbox((0, 0), "@riversrock_rouen", font=font_space_l)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, 1750), "@riversrock_rouen", fill=BLANC_PIL, font=font_space_l)

    img = pillow_grain_overlay(img, 0.04, seed=20)
    img.save(os.path.join(TMPL, "instagram-story.png"))
    print(f"[Scène & Vintage] Social → {TMPL}")


# ── Banners ──

def gen_banners():
    def lerp(c1, c2, t):
        return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))

    for name, w, h, logo_s in [
        ("facebook-banner.png", 1640, 624, 48),
        ("youtube-banner.png", 2560, 1440, 72),
    ]:
        img = Image.new("RGB", (w, h))
        draw = ImageDraw.Draw(img)
        for i in range(120):
            t = i / 119
            draw.rectangle([0, i * h / 120, w, (i + 1) * h / 120],
                           fill=lerp(BLEU_PIL, TEAL_PIL, t))

        cx, cy = w / 2, h / 2
        mr = math.sqrt(cx**2 + cy**2)
        for i in range(100):
            t = i / 99
            r = mr * t
            a = int(60 * (1 - t))
            draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                        fill=(OR_PIL[0], OR_PIL[1], OR_PIL[2], max(0, a)))

        font_logo = ImageFont.truetype(ANTON_PATH, logo_s) if ANTON_PATH else ImageFont.truetype(BEBAS_PATH, logo_s)
        tw = draw.textbbox((0, 0), "RIVERS ROCK", font=font_logo)[2]
        sym_r = logo_s * 0.45
        gap = sym_r * 0.4
        sx = (w - (sym_r * 2 + gap + tw)) / 2
        pillow_crest(draw, sx + sym_r, h / 2, sym_r / 25.0)
        draw.text((sx + sym_r * 2 + gap, h / 2 - tw * 0.2), "RIVERS ROCK", fill=BLANC_PIL, font=font_logo)

        font_sub = ImageFont.truetype(MONTSERRAT_PATH, 14)
        sub = "Reprises rock — Rouen"
        sb = draw.textbbox((0, 0), sub, font=font_sub)
        draw.text(((w - (sb[2] - sb[0])) / 2, h - 60), sub, fill=BLANC_PIL, font=font_sub)

        img_rgb = img.convert("RGB")
        grain = pillow_grain_overlay(img_rgb, 0.04, seed=30)
        grain.save(os.path.join(TMPL, name))
    print(f"[Scène & Vintage] Banners → {TMPL}")


# ── Avatar + Monogramme ──

def gen_avatar():
    S = 500
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    pillow_crest(draw, S / 2, S / 2, 180 / 25.0)
    img.save(os.path.join(TMPL, "avatar.png"))

    img2 = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw2 = ImageDraw.Draw(img2)
    pillow_monogramme_rr(draw2, S / 2, S / 2, 6.0)
    img2.save(os.path.join(TMPL, "monogramme-rr.png"))
    print(f"[Scène & Vintage] Avatar → {TMPL}")


# ── Stickers ──

def gen_stickers():
    from reportlab.lib.units import mm
    W, H = A4
    SR = 40 * mm
    MX = (W - 2 * SR * 2) / 3
    MY = (H - 3 * SR * 2) / 4
    centers = [(MX + SR + c * (MX + SR * 2), MY + SR + r * (MY + SR * 2)) for c in range(2) for r in range(3)]

    path = os.path.join(PDF, "stickers-scene-vintage.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, A4[0], A4[1])

    for cx, cy in centers:
        for i in range(60):
            t = i / 59
            r = TERRA.red + (OR.red - TERRA.red) * t
            g = TERRA.green + (OR.green - TERRA.green) * t
            b = TERRA.blue + (OR.blue - TERRA.blue) * t
            cv.setFillColor(Color(r, g, b))
            y = cy - SR + i * SR * 2 / 60
            cv.rect(cx - SR, y, SR * 2, SR * 2 / 60 + 0.5, stroke=0, fill=1)
        cv.setStrokeColor(BLANC)
        cv.setLineWidth(2)
        cv.circle(cx, cy, SR, stroke=1, fill=0)

        sr = SR * 0.50
        ring_r = sr + sr * 0.15
        cv.setStrokeColor(BLANC)
        cv.setLineWidth(0.8)
        cv.circle(cx, cy, ring_r, stroke=1, fill=0)
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
        cv.setFillColor(BLANC)
        cv.setFont("BebasNeue", 8)
        cv.drawCentredString(cx, cy + sr + 6, "RIVERS ROCK")
    save_with_crop_marks(cv, _, _, bleed)
    print(f"[Scène & Vintage] Stickers → {path}")


# ── T-shirt ──

def gen_tshirt():
    from reportlab.lib.units import mm
    w, h = A4
    sizes = [("S", 22 * mm, w / 4, h - 200), ("M", 28 * mm, w * 3 / 4, h - 200),
             ("L", 34 * mm, w / 4, h - 440), ("XL", 40 * mm, w * 3 / 4, h - 440)]
    path = os.path.join(PDF, "tshirt-scene-vintage.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, A4[0], A4[1])
    cv.setFillColor(Color(0, 0, 0, alpha=0.04))
    cv.rect(0, 0, w, h, stroke=0, fill=1)
    for label, sr, cx, cy in sizes:
        from logoutils import reportlab_crest_vintage
        reportlab_crest_vintage(cv, cx, cy, sr / 25.0)
        cv.setFillColor(BLANC)
        cv.setFont("BebasNeue", max(14, int(sr * 2.2)))
        cv.drawCentredString(cx, cy - sr - max(10, sr * 0.6), "RIVERS")
        cv.drawCentredString(cx, cy - sr - max(24, sr * 1.3), "ROCK")
        if label:
            cv.setFillColor(Color(1, 1, 1, alpha=0.4))
            cv.setFont("Montserrat", 7)
            cv.drawCentredString(cx, cy + sr + 60, label)
    save_with_crop_marks(cv, _, _, bleed)
    print(f"[Scène & Vintage] T-shirt → {path}")


# ── Animated logo ──

def gen_animated():
    html = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rivers Rock — Scène &amp; Vintage</title>
<meta name="description" content="Rivers Rock — Scène &amp; Vintage — Rivers Rock, groupe de reprises rock base a Rouen. Rock, pop-rock, inde et alternatif — 5 musiciens, 12 titres.">
<meta property="og:title" content="Rivers Rock — Scène &amp; Vintage">
<meta property="og:description" content="Rivers Rock — Scène &amp; Vintage — Rivers Rock, groupe de reprises rock base a Rouen. Rock, pop-rock, inde et alternatif — 5 musiciens, 12 titres.">
<meta property="og:type" content="music.group">
<meta property="og:url" content="https://clucet.github.io/rivers_rock/propositions/03-scene-vintage/">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="Rivers Rock — Scène &amp; Vintage">
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Bebas+Neue&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0}
body{width:1080px;height:1920px;overflow:hidden;background:radial-gradient(ellipse at 50% 42%, #C96D4D 0%, #1A3A5C 55%, #1A5C5C 100%);display:flex;align-items:center;justify-content:center}
canvas{position:absolute;top:0;left:0;width:1080px;height:1920px}
svg{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:420px;height:420px;overflow:visible}
.vinyl{opacity:0;animation:vinylAppear .3s ease-out .3s forwards}
.vinyl-ring{fill:none;stroke:rgba(0,0,0,0.15);stroke-width:2}
.vinyl-spin{animation:spin 1.2s linear .3s forwards;transform-origin:0 0}
@keyframes spin{0%{transform:rotate(0deg)}100%{transform:rotate(360deg)}}
@keyframes vinylAppear{to{opacity:1}}
.vinyl-fade{opacity:0;animation:fadeVinyl .4s ease-out 1.3s forwards}
@keyframes fadeVinyl{to{opacity:0}}
.crest-group{opacity:0;animation:fadeCrest .5s ease-out 1.6s forwards}
@keyframes fadeCrest{to{opacity:1}}
.outer{fill:none;stroke:rgba(212,184,90,0.2);stroke-width:1.5}
.inner{fill:none;stroke:#fff;stroke-width:5;stroke-dasharray:300;stroke-dashoffset:300;animation:drawC .6s ease-out 1.6s forwards;filter:drop-shadow(0 0 15px rgba(232,93,58,0.7))}
.timbre{fill:none;stroke:rgba(255,255,255,0.15);stroke-width:1.5;stroke-dasharray:6 4;opacity:0;animation:fadeT .4s ease-out 1.8s forwards}
.wave{fill:none;stroke:#E85D3A;stroke-width:4;stroke-linecap:round;opacity:0;animation:fadeW .4s ease-out 2.0s forwards;filter:drop-shadow(0 0 10px rgba(232,93,58,0.9))}
@keyframes drawC{to{stroke-dashoffset:0}}
@keyframes fadeW{to{opacity:1}}
@keyframes fadeT{to{opacity:1}}
.letter{font-family:'Anton',sans-serif;font-size:34px;fill:#fff;opacity:0;filter:drop-shadow(0 0 4px rgba(255,255,255,0.3))}
.lR{animation:dropCurve .5s ease-out 2.2s forwards}
.lI{animation:dropCurve .5s ease-out 2.35s forwards}
.lV{animation:dropCurve .5s ease-out 2.5s forwards}
.lE1{animation:dropCurve .5s ease-out 2.65s forwards}
.lR2{animation:dropCurve .5s ease-out 2.8s forwards}
.lS{animation:dropCurve .5s ease-out 2.95s forwards}
@keyframes dropCurve{0%{opacity:0;transform:translateY(-50px) translateX(-10px)}100%{opacity:1;transform:translateY(0) translateX(0)}}
.lROCK_R{animation:slide .4s ease-out 3.3s forwards}
.lROCK_O{animation:slide .4s ease-out 3.45s forwards}
.lROCK_C{animation:slide .4s ease-out 3.6s forwards}
.lROCK_K{animation:slide .4s ease-out 3.75s forwards}
@keyframes slide{0%{opacity:0;transform:translateX(200px)}100%{opacity:1;transform:translateX(0)}}
.neon-pulse{animation:pulse 2s ease-in-out infinite alternate}
@keyframes pulse{0%{filter:drop-shadow(0 0 8px rgba(232,93,58,0.4))}100%{filter:drop-shadow(0 0 25px rgba(232,93,58,0.9))}}
@media(prefers-reduced-motion){*{animation:none!important;transition:none!important}}

a:focus-visible{outline:2px solid var(--accent,#E85D3A);outline-offset:2px}
button:focus-visible{outline:2px solid var(--accent,#E85D3A);outline-offset:2px}</style>
</head>
<body>
<canvas id="p"></canvas>
<svg viewBox="-200 -200 400 400">
  <g class="vinyl vinyl-fade">
    <g class="vinyl-spin">
      <circle class="vinyl-ring" cx="0" cy="0" r="140"/>
      <circle class="vinyl-ring" cx="0" cy="0" r="120" stroke-dasharray="4 6"/>
      <circle class="vinyl-ring" cx="0" cy="0" r="100" stroke-dasharray="2 8"/>
      <circle class="vinyl-ring" cx="0" cy="0" r="80"/>
      <circle cx="0" cy="0" r="30" fill="rgba(200,60,40,0.3)"/>
      <circle cx="0" cy="0" r="6" fill="#333"/>
    </g>
  </g>
  <g class="crest-group">
    <circle class="outer" cx="0" cy="0" r="165"/>
    <circle class="timbre" cx="0" cy="0" r="90"/>
    <circle class="inner neon-pulse" cx="0" cy="0" r="80"/>
    <path class="wave" d="M-72,0 Q-40,-20 0,0 Q40,20 72,0">
      <animate attributeName="d" dur="3s" repeatCount="indefinite"
        values="M-72,0 Q-40,-20 0,0 Q40,20 72,0;M-72,0 Q-40,20 0,0 Q40,-20 72,0;M-72,0 Q-40,-20 0,0 Q40,20 72,0"/>
    </path>
    <text x="-55" y="-52.9" text-anchor="middle" class="letter lR">R</text>
    <text x="-33" y="-71.4" text-anchor="middle" class="letter lI">I</text>
    <text x="-11" y="-79.1" text-anchor="middle" class="letter lV">V</text>
    <text x="11" y="-79.1" text-anchor="middle" class="letter lE1">E</text>
    <text x="33" y="-71.4" text-anchor="middle" class="letter lR2">R</text>
    <text x="55" y="-52.9" text-anchor="middle" class="letter lS">S</text>
    <text x="-30" y="74.2" text-anchor="middle" class="letter lROCK_R" font-size="28">R</text>
    <text x="-10" y="79.4" text-anchor="middle" class="letter lROCK_O" font-size="28">O</text>
    <text x="10" y="79.4" text-anchor="middle" class="letter lROCK_C" font-size="28">C</text>
    <text x="30" y="74.2" text-anchor="middle" class="letter lROCK_K" font-size="28">K</text>
  </g>
</svg>
<script>
const c=document.getElementById('p'),ctx=c.getContext('2d');
c.width=1080;c.height=1920;
const ps=[];
for(let i=0;i<35;i++){ps.push({x:Math.random()*1080,y:Math.random()*1920,s:Math.random()*3+1,a:Math.random()*0.06+0.01})}
function draw(){ctx.clearRect(0,0,1080,1920);
ctx.fillStyle='#1A3A5C';ctx.fillRect(0,0,1080,1920);
const g=ctx.createRadialGradient(540,860,0,540,860,1200);
g.addColorStop(0,'rgba(212,184,90,0.25)');g.addColorStop(0.4,'rgba(201,109,77,0.12)');g.addColorStop(1,'rgba(26,58,92,0)');
ctx.fillStyle=g;ctx.fillRect(0,0,1080,1920);
for(const p of ps){ctx.beginPath();ctx.arc(p.x,p.y,p.s,0,Math.PI*2);ctx.fillStyle='rgba(232,93,58,'+p.a+')';ctx.fill();p.y-=0.35;if(p.y<0){p.y=1920;p.x=Math.random()*1080}}
requestAnimationFrame(draw)}draw();
</script>
</body>
</html>'''
    path = os.path.join(TMPL, "logo-animated-scene-vintage.html")
    with open(path, "w") as f:
        f.write(html)
    print(f"[Scène & Vintage] Animated logo → {path}")


# ── Site ──

def gen_site():
    html = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Rivers Rock — Scène &amp; Vintage</title>
<meta name="description" content="Rivers Rock — Scène &amp; Vintage — Rivers Rock, groupe de reprises rock base a Rouen. Rock, pop-rock, inde et alternatif — 5 musiciens, 12 titres.">
<meta property="og:title" content="Rivers Rock — Scène &amp; Vintage">
<meta property="og:description" content="Rivers Rock — Scène &amp; Vintage — Rivers Rock, groupe de reprises rock base a Rouen. Rock, pop-rock, inde et alternatif — 5 musiciens, 12 titres.">
<meta property="og:type" content="music.group">
<meta property="og:url" content="https://clucet.github.io/rivers_rock/propositions/03-scene-vintage/">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="Rivers Rock — Scène &amp; Vintage">
<link rel="preload" href="assets/logo.svg" as="image" type="image/svg+xml">
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Bebas+Neue&display=swap" rel="stylesheet">
<link rel="icon" type="image/svg+xml" sizes="32x32" href="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzMiAzMiI+PGNpcmNsZSBjeD0iMTYiIGN5PSIxNiIgcj0iMTUiIGZpbGw9IiNFODVEM0EiLz48dGV4dCB4PSIxNiIgeT0iMjIiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtZmFtaWx5PSJzYW5zLXNlcmlmIiBmb250LXNpemU9IjE2IiBmaWxsPSIjZmZmIiBmb250LXdlaWdodD0iYm9sZCI+UzwvdGV4dD48L3N2Zz4=">
<link rel="icon" type="image/png" sizes="16x16" href="templates/monogramme-rr.png">
<link rel="apple-touch-icon" href="templates/monogramme-rr.png">
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Bebas+Neue&family=Montserrat:wght@300;400;600&family=Space+Mono&display=swap" rel="stylesheet">
<style>
:root{--bleu:#1A3A5C;--teal:#1A5C5C;--accent:#E85D3A;--or:#C9A84C;--terracotta:#C96D4D;--blanc:#fff}@media(prefers-color-scheme:dark){:root{--bleu:#0A1A2A;--teal:#0A2A2A;--accent:#E85D3A;--or:#B8943A;--terracotta:#A04D3D;--blanc:#E0E0E0}}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:70px}
body{font-family:'Montserrat',system-ui,sans-serif;font-weight:300;color:var(--blanc);min-height:100vh;background:linear-gradient(135deg,var(--bleu),var(--teal))}
.bg-grain{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23g)' opacity='0.05'/%3E%3C/svg%3E")}
nav{position:fixed;top:0;width:100%;padding:14px 32px;display:flex;justify-content:space-between;align-items:center;z-index:100;background:rgba(26,58,92,0.88);backdrop-filter:blur(8px);border-bottom:1px solid rgba(201,168,76,0.15)}
nav .logo-small{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--blanc)}
nav .logo-small svg{width:30px;height:30px}
nav .logo-small svg circle{fill:none;stroke:var(--or);stroke-width:2.5}
nav .logo-small svg path{fill:none;stroke:var(--accent);stroke-width:2}
nav .logo-small span{font-family:'Anton',sans-serif;font-size:16px;letter-spacing:1px;text-transform:uppercase}
nav a{color:rgba(255,255,255,0.82);text-decoration:none;font-size:12px;font-weight:400;letter-spacing:1px;text-transform:uppercase;padding:6px 14px;border-radius:4px;transition:.3s}
nav a:hover{color:var(--or);background:rgba(201,168,76,0.08)}
.hero{position:relative;z-index:1;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:120px 24px 80px;background:radial-gradient(ellipse at 50% 38%, rgba(201,168,76,0.18) 0%, rgba(201,109,77,0.08) 45%, transparent 70%)}
.hero .logo-glow{margin-bottom:12px}
.hero .logo-glow svg{width:130px;height:130px}
.hero .logo-glow svg circle{fill:none;stroke:var(--blanc);stroke-width:4;filter:drop-shadow(0 0 14px rgba(232,93,58,0.5))}
.hero .logo-glow svg path{fill:none;stroke:var(--accent);stroke-width:3.5;filter:drop-shadow(0 0 12px rgba(232,93,58,0.7))}
.hero h1{font-family:'Anton',sans-serif;font-size:clamp(48px,10vw,96px);letter-spacing:3px;text-transform:uppercase;color:var(--blanc);margin-bottom:6px}
.hero .tagline{font-family:'Space Mono',monospace;font-size:14px;color:var(--or);letter-spacing:2px;text-transform:uppercase;margin-bottom:32px}
.hero p{font-size:15px;line-height:1.7;color:rgba(255,255,255,0.7);max-width:500px}
.hero .scroll-indicator{position:absolute;bottom:32px;left:50%;transform:translateX(-50%);width:24px;height:40px;border:2px solid rgba(255,255,255,0.15);border-radius:12px}
.hero .scroll-indicator::after{content:"";position:absolute;top:6px;left:50%;transform:translateX(-50%);width:3px;height:8px;background:var(--or);border-radius:2px;animation:scrollDown 2s infinite}
@keyframes scrollDown{0%{opacity:1;transform:translateX(-50%) translateY(0)}100%{opacity:0;transform:translateX(-50%) translateY(16px)}}
.section{position:relative;z-index:1;padding:80px 24px;max-width:700px;margin:0 auto}
.section h2{font-family:'Anton',sans-serif;font-size:34px;letter-spacing:2px;text-transform:uppercase;color:var(--or);margin-bottom:36px;text-align:center}
.section h2::after{content:"";display:block;width:80px;height:2px;background:var(--accent);margin:10px auto 0}
.section p{font-size:15px;line-height:1.8;color:rgba(255,255,255,0.75);margin-bottom:20px}
.section-alt{background:rgba(26,92,92,0.12);border-top:1px solid rgba(201,168,76,0.08);border-bottom:1px solid rgba(201,168,76,0.08)}
.members-grid{display:flex;flex-wrap:wrap;justify-content:center;gap:20px;margin-top:20px}
.member-card{flex:0 0 180px;text-align:center;padding:24px 12px;background:rgba(255,255,255,0.04);border-radius:8px;border:1px solid rgba(255,255,255,0.06);transition:.25s}
.member-card:hover{background:rgba(255,255,255,0.08);transform:scale(1.03)}
.member-card .avatar-circle{width:68px;height:68px;border-radius:50%;background:linear-gradient(135deg,var(--terracotta),var(--or));margin:0 auto 10px;display:flex;align-items:center;justify-content:center;font-family:'Anton',sans-serif;font-size:26px;color:var(--blanc)}
.member-card h3{font-family:'Anton',sans-serif;font-size:17px;letter-spacing:1px;color:var(--accent);margin-bottom:3px}
.member-card p{font-family:'Space Mono',monospace;font-size:11px;color:rgba(255,255,255,0.45);letter-spacing:1px;text-transform:uppercase}
.concerts-list{list-style:none;padding:0}
.concerts-list li{padding:14px 20px;margin-bottom:10px;background:rgba(255,255,255,0.03);border-radius:6px;border-left:3px solid var(--or);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px}
.concerts-list .date{font-family:'Space Mono',monospace;font-size:14px;color:var(--or)}
.concerts-list .lieu{font-size:14px;color:rgba(255,255,255,0.78)}
.concerts-list .status{font-size:11px;padding:3px 10px;border-radius:10px;background:rgba(201,109,77,0.15);color:var(--terracotta);text-transform:uppercase}
.contact-info{text-align:center;margin-top:16px}
.contact-info p{font-size:15px;margin-bottom:6px}
.contact-info .email{font-family:'Space Mono',monospace;font-size:16px;color:var(--or);text-decoration:none;transition:.2s}
.contact-info .email:hover{color:var(--accent)}
.links-social{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:24px}
.links-social a{color:rgba(255,255,255,0.78);text-decoration:none;font-family:'Space Mono',monospace;font-size:12px;padding:8px 18px;border:1px solid rgba(201,168,76,0.3);border-radius:6px;transition:.3s;letter-spacing:1px;text-transform:uppercase}
.links-social a:hover{color:var(--blanc);border-color:var(--or);background:rgba(201,168,76,0.08)}
.footer{position:relative;z-index:1;text-align:center;padding:44px 24px;border-top:1px solid rgba(201,168,76,0.08)}
.footer .logo-timbre svg{width:56px;height:56px;margin-bottom:10px;opacity:0.5}
.footer .logo-timbre svg circle:nth-child(1){fill:none;stroke:rgba(255,255,255,0.12);stroke-width:1;stroke-dasharray:3 3}
.footer .logo-timbre svg circle:nth-child(2){fill:none;stroke:rgba(255,255,255,0.2);stroke-width:2}
.footer .logo-timbre svg path{fill:none;stroke:var(--accent);stroke-width:2.5;opacity:0.5}
.footer p{font-family:'Montserrat',sans-serif;font-size:11px;letter-spacing:4px;color:rgba(255,255,255,0.2);text-transform:uppercase}
@media(max-width:640px){
  nav{padding:12px 16px}
  nav a{font-size:11px;padding:4px 10px}
  .hero{padding:100px 16px 60px}
  .section{padding:60px 16px}
  .member-card{flex:0 0 150px}
}
@media(max-width:400px){
  nav{padding:10px 12px}
  nav .logo-small span{font-size:14px}
  nav a{font-size:10px;padding:4px 8px}
  .hero h1{font-size:36px}
  .member-card{flex:0 0 140px}
  .member-card .avatar-circle{width:56px;height:56px;font-size:22px}
  .section{padding:40px 12px}
  .section h2{font-size:26px}
}
@media(prefers-reduced-motion){*{animation:none!important;transition:none!important}}

a:focus-visible{outline:2px solid var(--accent,#E85D3A);outline-offset:2px}
button:focus-visible{outline:2px solid var(--accent,#E85D3A);outline-offset:2px}</style>
</head>
<body>
<div class="bg-grain"></div>
<nav>
  <a href="#" class="logo-small">
    <svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="42"/><path d="M18,50 Q30,42 42,50 Q54,58 66,50 Q78,42 90,50"/></svg>
    <span>Rivers Rock</span>
  </a>
  <div>
    <a href="#groupe">Le groupe</a>
    <a href="#concerts">Concerts</a>
    <a href="#musique">Musique</a>
    <a href="#contact">Contact</a>
  </div>
</nav>
<section class="hero">
  <div class="logo-glow">
    <svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="42"/><path d="M18,50 Q30,42 42,50 Q54,58 66,50 Q78,42 90,50"/></svg>
  </div>
  <h1>RIVERS ROCK</h1>
  <div class="tagline">Reprises rock — Rouen</div>
  <p>Groupe rouennais formé en 2024. Rock, pop-rock, indé et alternatif. La Seine qui coule derrière le 106.</p>
  <a href="#groupe" style="text-decoration:none;color:inherit"><div class="scroll-indicator"></div></a>
</section>
<section id="groupe" class="section">
  <h2>Le groupe</h2>
  <p>Cinq musiciens, une passion commune : faire vibrer la scène rouennaise avec des reprises qui décoiffent. Du rock à l\'alternatif, du pop-rock à l\'indé, Rivers Rock met le feu à chaque concert.</p>
  <p>Notre nom ? La Seine qui coule derrière le 106, notre lieu de répétition. L\'eau vive et l\'énergie rock, en un seul nom.</p>
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
  <p>Contactez-nous pour programmer un concert. Notre setlist de 12 titres traverse les époques : de Queen aux White Stripes, en passant par Radiohead, AC/DC et Bella Ciao.</p>
  <ul class="concerts-list"><li><span class="date">À venir</span><span class="lieu">Contactez-nous</span><span class="status">Sur demande</span></li></ul>
  <div style="margin-top:20px;border-radius:8px;overflow:hidden;max-width:400px;margin-left:auto;margin-right:auto">
    <img src="../../../images/IMG-20260620-WA0001.jpg" style="width:100%;height:auto;display:block;border-radius:8px" alt="Affiche Soirees Nocturnes - VEN 26 JUIN 2026 - Montigny">
  </div>
</section>
<section id="musique" class="section">
  <h2>Musique</h2>
  <p>Découvrez Rivers Rock en action — extraits live et playlist à venir.</p>
  <div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:8px;margin-top:16px">
    <div style="position:absolute;top:0;left:0;width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,0.05);border-radius:8px;font-family:sans-serif;font-size:16px;color:rgba(0,0,0,0.3)"><div style="text-align:center;padding:30px 20px;background:rgba(128,128,128,0.04);border-radius:8px"><p style="color:rgba(128,128,128,0.5);font-size:14px;margin-bottom:12px;font-family:sans-serif">Playlist musicale a venir</p><a href="https://www.youtube.com/@RiversRockRouen" target="_blank" style="display:inline-block;padding:10px 24px;border-radius:6px;background:var(--accent,#E85D3A);color:#fff;text-decoration:none;font-size:13px">Suivre sur YouTube</a></div></div>
  </div>
</section>
<section id="contact" class="section section-alt">
  <h2>Contact</h2>
  <div class="contact-info"><p>Pour toute demande de concert :</p><a class="email" href="mailto:riversrock_rouen@gmail.com">riversrock_rouen@gmail.com</a></div>
  
  <form action="https://formsubmit.co/riversrock_rouen@gmail.com" method="POST" enctype="text/plain" style="max-width:400px;margin:20px auto">
    <input type="text" name="nom" placeholder="Votre nom" required style="width:100%;padding:10px;margin-bottom:8px;border:1px solid rgba(255,255,255,0.15);border-radius:6px;background:rgba(255,255,255,0.05);color:#fff;font-family:inherit;font-size:14px">
    <input type="email" name="email" placeholder="Votre email" required style="width:100%;padding:10px;margin-bottom:8px;border:1px solid rgba(255,255,255,0.15);border-radius:6px;background:rgba(255,255,255,0.05);color:#fff;font-family:inherit;font-size:14px">
    <textarea name="message" placeholder="Votre message" required rows="3" style="width:100%;padding:10px;margin-bottom:8px;border:1px solid rgba(255,255,255,0.15);border-radius:6px;background:rgba(255,255,255,0.05);color:#fff;font-family:inherit;font-size:14px;resize:vertical"></textarea>
    <button type="submit" style="width:100%;padding:10px;border:none;border-radius:6px;background:var(--accent, #E85D3A);color:#fff;font-family:inherit;font-size:14px;font-weight:600;cursor:pointer">Envoyer</button>
  </form><div class="links-social">
    <a href="https://www.instagram.com/riversrock_rouen" target="_blank">Instagram</a>
    <a href="https://www.facebook.com/RiversRockRouen" target="_blank">Facebook</a>
    <a href="https://www.youtube.com/@RiversRockRouen" target="_blank">YouTube</a>
  </div>
</section>
<footer class="footer">
  <div class="logo-timbre">
    <svg viewBox="0 0 120 120"><circle cx="60" cy="60" r="54"/><circle cx="60" cy="60" r="46"/><path d="M32,60 Q42,50 52,60 Q62,70 72,60 Q82,50 92,60"/></svg>
  </div>
  <p>R O U E N</p>
</footer>
</body>
</html>'''
    dst = os.path.join(OUT, "index.html")
    with open(dst, "w") as f:
        f.write(html)
    print(f"[Scène & Vintage] Site → {dst}")


def gen_animated_mp4():
    """Render animated logo to MP4 via render_animation.py."""
    try:
        import subprocess, sys
        script = os.path.join(os.path.dirname(__file__), "..", "..", "scripts", "render_animation.py")
        out = os.path.join(TMPL, "logo-animated-scene-vintage.mp4")
        subprocess.run([sys.executable, script, "--output", out, "--render-scale", "0.5"],
                       check=True, timeout=120)
        print(f"[Scène & Vintage] MP4 → {out}")
    except Exception as e:
        print(f"[Scène & Vintage] MP4 skipped: {e}")


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
    # gen_animated_mp4()
    gen_site()
