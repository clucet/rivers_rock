#!/usr/bin/env python3
"""Generate all Nordik assets — Proposition n°7."""
# SVG logo available at: ../propositions/XXX/assets/logo.svg


import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))
from logoutils import (
    create_bleed_canvas, save_with_crop_marks,
    BEBAS_PATH, MONTSERRAT_PATH, INTER_PATH,
)
from palette import NORDIK as CFG
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

BLANC = CFG.rl("blanc_pur")
GRIS = CFG.rl("gris_ardoise")
NOIR = CFG.rl("noir_doux")
LIN = CFG.rl("accent_lin")
BLANC_PIL = CFG.pil("blanc_pur")
GRIS_PIL = CFG.pil("gris_ardoise")
NOIR_PIL = CFG.pil("noir_doux")
LIN_PIL = CFG.pil("accent_lin")

pdfmetrics.registerFont(TTFont("Inter", INTER_PATH))

from setlist_data import SETLIST, GREEN_INDICES

def nordik_logo_reportlab(cv, cx, cy, scale=1.0):
    w = 60 * scale
    cv.setStrokeColor(LIN)
    cv.setLineWidth(2 * scale)
    cv.line(cx - w, cy, cx + w, cy)

def nordik_logo_pillow(draw, cx, cy, scale=1.0):
    w = 60 * scale
    draw.line([(cx - w, cy), (cx + w, cy)], fill=LIN_PIL, width=max(1, int(2 * scale)))

def gen_setlist():
    W, H = A4
    path = os.path.join(PDF, "setlist-nordik.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, W, H)
    cv.setFillColor(BLANC)
    cv.rect(0, 0, W, H, stroke=0, fill=1)
    nordik_logo_reportlab(cv, W / 2, H - 105, 2.5)
    cv.setFillColor(NOIR)
    cv.setFont("Inter", 16)
    cv.drawCentredString(W / 2, H - 155, "rivers rock")
    cv.setFont("Inter", 22)
    cv.drawCentredString(W / 2, H - 185, "SETLIST")
    cv.setStrokeColor(LIN)
    cv.setLineWidth(0.5)
    cv.line(W / 2 - 40, H - 200, W / 2 + 40, H - 200)
    card_w, card_h, card_r = 250, 74, 2
    col_gap = (W - 2 * card_w) / 3
    col_c = [col_gap + card_w / 2, col_gap * 2 + card_w + card_w / 2]
    row_pitch = 86
    rows_top = 610
    us = 24
    for idx, (artist, title) in enumerate(SETLIST):
        col, row = idx // 6, idx % 6
        cx = col_c[col]
        cy = rows_top - row * row_pitch
        cl, cb = cx - card_w / 2, cy - card_h / 2
        cv.setFillColor(Color(0, 0, 0, alpha=0.05))
        cv.roundRect(cl + 2, cb - 2, card_w, card_h, card_r, stroke=0, fill=1)
        cv.setFillColor(BLANC)
        cv.rect(cl, cb, card_w, card_h, stroke=0, fill=1)
        cv.setStrokeColor(Color(0, 0, 0, alpha=0.08))
        cv.setLineWidth(0.5)
        cv.roundRect(cl, cb, card_w, card_h, card_r, stroke=1, fill=0)
        aw = pdfmetrics.stringWidth(artist, "Inter", us)
        sx = cx - (20 + 4 + aw) / 2 + 12
        cv.setFillColor(NOIR)
        cv.setFont("Inter", us)
        cv.drawString(sx + 20 + 4, cy + 6, artist)
        cv.setFillColor(Color(0, 0, 0, alpha=0.15))
        cv.setFont("Inter", 9)
        cv.drawCentredString(sx + 10, cy + 16, f"{idx+1:02d}")
        if title:
            cv.setFillColor(Color(0, 0, 0, alpha=0.5))
            cv.setFont("Inter", 11)
            cv.drawCentredString(cx, cy - 17, title)
    cv.setFillColor(Color(0, 0, 0, alpha=0.12))
    cv.setFont("Inter", 7)
    text, tr = "R O U E N", 8
    x = W / 2 - (sum(pdfmetrics.stringWidth(c, "Inter", 7) for c in text) + tr * (len(text) - 1)) / 2
    for c in text:
        w = pdfmetrics.stringWidth(c, "Inter", 7)
        cv.drawString(x, 14, c)
        x += w + tr
    save_with_crop_marks(cv, _, _, bleed)
    print(f"[Nordik] Setlist > {path}")

def gen_poster():
    W, H = A4
    path = os.path.join(PDF, "poster-nordik.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, W, H)
    cv.setFillColor(BLANC)
    cv.rect(0, 0, W, H, stroke=0, fill=1)
    nordik_logo_reportlab(cv, W / 2, H - 190, 2.5)
    cv.setFillColor(NOIR)
    cv.setFont("Inter", 12)
    cv.drawCentredString(W / 2, H - 250, "rivers rock")
    cv.setFillColor(GRIS)
    cv.setFont("Inter", 10)
    cv.drawCentredString(W / 2, H - 270, "concert")
    cv.setFillColor(NOIR)
    cv.setFont("Inter", 42)
    cv.drawCentredString(W / 2, H - 340, "VEN 26 JUIN 2026")
    cv.setFillColor(Color(0, 0, 0, alpha=0.4))
    cv.setFont("Inter", 14)
    cv.drawCentredString(W / 2, H - 380, "Montigny . 19h30")
    cv.setStrokeColor(Color(0, 0, 0, alpha=0.15))
    cv.setLineWidth(0.5)
    cv.line(W / 2 - 80, H - 410, W / 2 + 80, H - 410)
    cv.setFillColor(Color(0, 0, 0, alpha=0.12))
    cv.setFont("Inter", 7)
    text, tr = "R O U E N", 8
    x = W / 2 - (sum(pdfmetrics.stringWidth(c, "Inter", 7) for c in text) + tr * (len(text) - 1)) / 2
    for c in text:
        w = pdfmetrics.stringWidth(c, "Inter", 7)
        cv.drawString(x, 14, c)
        x += w + tr
    save_with_crop_marks(cv, _, _, bleed)
    print(f"[Nordik] Poster > {path}")

# Remaining generators: flyer, social, banners, avatar, stickers, tshirt, animated, site
def gen_flyer():
    FW, FH = A6
    path = os.path.join(PDF, "flyer-nordik.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, A4[0], A4[1])
    def draw_recto(cv, ox, oy):
        cv.setFillColor(BLANC)
        cv.rect(ox, oy, FW, FH, stroke=0, fill=1)
        cx = ox + FW / 2
        nordik_logo_reportlab(cv, cx, oy + FH - 50, 1.0)
        cv.setFillColor(NOIR)
        cv.setFont("Inter", 14)
        cv.drawCentredString(cx, oy + FH - 80, "rivers rock")
        cv.setFont("Inter", 28)
        cv.drawCentredString(cx, oy + FH - 145, "VEN 26 JUIN")
        cv.setFillColor(Color(0, 0, 0, alpha=0.4))
        cv.setFont("Inter", 10)
        cv.drawCentredString(cx, oy + FH - 175, "Montigny . 19h30")
    def draw_verso(cv, ox, oy):
        cv.setFillColor(BLANC)
        cv.rect(ox, oy, FW, FH, stroke=0, fill=1)
        cx = ox + FW / 2
        cv.setFillColor(NOIR)
        cv.setFont("Inter", 14)
        cv.drawCentredString(cx, oy + FH - 40, "rivers rock")
        bio = ["Groupe rouennais forme en 2024", "au centre Education et Formation", "du Petit-Quevilly.",
               "", "Rosaria - batterie", "Christophe - basse", "Nicolas - guitare",
               "David - guitare / chant", "Virginie - chant", "", "Rock - Pop-Rock - Inde - Alternatif"]
        cv.setFillColor(Color(0, 0, 0, alpha=0.6))
        cv.setFont("Inter", 7)
        y = oy + FH - 80
        for line in bio:
            cv.drawCentredString(cx, y, line)
            y -= 12
        cv.setFillColor(LIN)
        cv.setFont("Inter", 7)
        cv.drawCentredString(cx, y - 6, "Contactez-nous")
        cv.setFillColor(Color(0, 0, 0, alpha=0.3))
        cv.setFont("Inter", 7)
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
    print(f"[Nordik] Flyer > {path}")

def gen_social():
    font_l = ImageFont.truetype(INTER_PATH, 64)
    font_m = ImageFont.truetype(INTER_PATH, 44)
    font_s = ImageFont.truetype(INTER_PATH, 20)
    w, h = 1080, 1080
    img = Image.new("RGB", (w, h), BLANC_PIL)
    draw = ImageDraw.Draw(img)
    nordik_logo_pillow(draw, w / 2, 140, 2.5)
    bbox = draw.textbbox((0,0), "rivers rock", font=font_l); tw=bbox[2]-bbox[0]
    draw.text(((w-tw)/2,150), "rivers rock", fill=NOIR_PIL, font=font_l)
    bbox = draw.textbbox((0,0), "VEN 26 JUIN 2026", font=font_m); tw=bbox[2]-bbox[0]
    draw.text(((w-tw)/2,440), "VEN 26 JUIN 2026", fill=NOIR_PIL, font=font_m)
    bbox = draw.textbbox((0,0), "Montigny . 19h30", font=font_s); tw=bbox[2]-bbox[0]
    draw.text(((w-tw)/2,520), "Montigny . 19h30", fill=GRIS_PIL, font=font_s)
    bbox = draw.textbbox((0,0), "@riversrockrouen", font=font_s); tw=bbox[2]-bbox[0]
    draw.text(((w-tw)/2,860), "@riversrockrouen", fill=GRIS_PIL, font=font_s)
    img.save(os.path.join(TMPL, "instagram-post.png"))
    w, h = 1080, 1920
    img = Image.new("RGB", (w, h), BLANC_PIL)
    draw = ImageDraw.Draw(img)
    font_big = ImageFont.truetype(INTER_PATH, 110)
    nordik_logo_pillow(draw, w / 2, 180, 3.0)
    bbox = draw.textbbox((0,0), "rivers rock", font=font_l); tw=bbox[2]-bbox[0]
    draw.text(((w-tw)/2,190), "rivers rock", fill=NOIR_PIL, font=font_l)
    bbox = draw.textbbox((0,0), "VEN 26 JUIN", font=font_big); tw=bbox[2]-bbox[0]
    draw.text(((w-tw)/2,650), "VEN 26 JUIN", fill=NOIR_PIL, font=font_big)
    bbox = draw.textbbox((0,0), "Montigny . 19h30", font=font_s); tw=bbox[2]-bbox[0]
    draw.text(((w-tw)/2,840), "Montigny . 19h30", fill=GRIS_PIL, font=font_s)
    img.save(os.path.join(TMPL, "instagram-story.png"))
    print(f"[Nordik] Social > {TMPL}")

def gen_banners():
    for name, w, h, logo_s in [("facebook-banner.png",1640,624,48),("youtube-banner.png",2560,1440,72)]:
        img = Image.new("RGB", (w, h), BLANC_PIL)
        draw = ImageDraw.Draw(img)
        font_logo = ImageFont.truetype(INTER_PATH, logo_s)
        tw = draw.textbbox((0,0), "rivers rock", font=font_logo)[2]
        sym_r = logo_s * 0.5; gap = sym_r * 0.3
        sx = (w - (sym_r*2+gap+tw))/2
        nordik_logo_pillow(draw, sx+sym_r, h/2, sym_r/22.0)
        draw.text((sx+sym_r*2+gap, h/2-tw*0.25), "rivers rock", fill=NOIR_PIL, font=font_logo)
        font_sub = ImageFont.truetype(INTER_PATH, 14)
        draw.text(((w-(sb:=draw.textbbox((0,0),"Reprises rock - Rouen",font=font_sub))[2]+sb[0])/2,h-50),"Reprises rock - Rouen",fill=GRIS_PIL,font=font_sub)
        img.save(os.path.join(TMPL, name))
    print(f"[Nordik] Banners > {TMPL}")

def gen_avatar():
    S = 500
    img = Image.new("RGBA", (S, S), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    nordik_logo_pillow(draw, S/2, S/2, 6.0)
    font = ImageFont.truetype(INTER_PATH, 36)
    bbox = draw.textbbox((0,0), "rr", font=font); tw = bbox[2]-bbox[0]
    draw.text(((S-tw)/2, S/2+50), "rr", fill=LIN_PIL, font=font)
    img.save(os.path.join(TMPL, "avatar.png"))
    print(f"[Nordik] Avatar > {TMPL}")

def gen_stickers():
    from reportlab.lib.units import mm
    W, H = A4; SR = 40*mm; MX = (W-2*SR*2)/3; MY = (H-3*SR*2)/4
    centers = [(MX+SR+c*(MX+SR*2), MY+SR+r*(MY+SR*2)) for c in range(2) for r in range(3)]
    path = os.path.join(PDF, "stickers-nordik.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, A4[0], A4[1])
    for cx, cy in centers:
        cv.setFillColor(BLANC)
        cv.circle(cx, cy, SR, stroke=0, fill=1)
        cv.setStrokeColor(Color(0,0,0,alpha=0.1))
        cv.setLineWidth(1)
        cv.circle(cx, cy, SR, stroke=1, fill=0)
        sr = SR * 0.50
        nordik_logo_reportlab(cv, cx, cy, sr/22.0)
        cv.setFillColor(NOIR)
        cv.setFont("Inter", 7)
        cv.drawCentredString(cx, cy+sr+8, "rivers rock")
    cv.save()
    print(f"[Nordik] Stickers > {path}")

def gen_tshirt():
    from reportlab.lib.units import mm
    w, h = A4
    sizes = [("S",22*mm,w/4,h-200),("M",28*mm,w*3/4,h-200),("L",34*mm,w/4,h-440),("XL",40*mm,w*3/4,h-440)]
    path = os.path.join(PDF, "tshirt-nordik.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, A4[0], A4[1])
    cv.setFillColor(Color(0,0,0,alpha=0.04))
    cv.rect(0,0,w,h,stroke=0,fill=1)
    for label, sr, cx, cy in sizes:
        nordik_logo_reportlab(cv, cx, cy, sr/22.0)
        cv.setFillColor(NOIR)
        cv.setFont("Inter", max(8,int(sr*1.4)))
        cv.drawCentredString(cx, cy+sr*0.6+4, "rivers rock")
        if label:
            cv.setFillColor(Color(0,0,0,alpha=0.3))
            cv.setFont("Inter", 7)
            cv.drawCentredString(cx, cy+sr+60, label)
    cv.save()
    print(f"[Nordik] T-shirt > {path}")

def gen_animated():
    path = os.path.join(TMPL, "logo-animated-nordik.html")
    with open(path, "w") as f:
        f.write('''<!DOCTYPE html>
<html lang="fr">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rivers Rock \u2014 Nordik</title>
<link rel="icon" type="image/png" sizes="32x32" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAMlJREFUWEft1rENwjAQBdD/FYyAWIAJYAQKOkZgBEZgBDoWYARGYAQK4kiWLNnxnU8UKZLr/Pd9thMEAf4PQAiAEAChIyA6AgI7ArLWPuc8zjnnC85a+5xzHgEgBEAIAOrA3Xsf9z17ZgBIfYAx5hVjrN77z3ffH4DVByClBICttV+t3bee1gcgpQQAay0B7L0TAOYcBPAcB3NODPCe0DHG5xhjA0AIgBAAoSMgOgICOwKy1j7nnMec8wsnhHDOeRxjjACEEADhCAgBEB0BgR0BWWufc85jzvmFE8Kccx5jjACEEADhCEgIAOgICAEQHQH/Ab3+V/+tKtRsAAAAAElFTkSuQmCC">
<style>
*{margin:0;padding:0}
body{width:1080px;height:1920px;overflow:hidden;background:#FAFAFA;display:flex;align-items:center;justify-content:center}
.line{stroke:#B8B5A8;stroke-width:2;stroke-dasharray:120;stroke-dashoffset:120;animation:drawLine 2s ease-out .5s forwards}
@keyframes drawLine{to{stroke-dashoffset:0}}
.letter{font-family:'Inter',sans-serif;font-weight:200;font-size:44px;fill:#2B2B2B;opacity:0}
.lR{animation:fadeL .3s ease-out 2.5s forwards}
.lI{animation:fadeL .3s ease-out 2.8s forwards}
.lV{animation:fadeL .3s ease-out 3.1s forwards}
.lE{animation:fadeL .3s ease-out 3.4s forwards}
.lR2{animation:fadeL .3s ease-out 3.7s forwards}
.lS{animation:fadeL .3s ease-out 4.0s forwards}
.lROCK_R{animation:fadeL .3s ease-out 4.3s forwards}
.lROCK_O{animation:fadeL .3s ease-out 4.6s forwards}
.lROCK_C{animation:fadeL .3s ease-out 4.9s forwards}
.lROCK_K{animation:fadeL .3s ease-out 5.2s forwards}
@keyframes fadeL{0%{opacity:0;transform:translateY(-10px);letter-spacing:20px}100%{opacity:1;transform:translateY(0);letter-spacing:4px}}
</style></head>
<body>
<svg viewBox="-200 -200 400 400">
  <line class="line" x1="-60" y1="0" x2="60" y2="0"/>
  <text x="-60" y="-52.9" text-anchor="middle" class="letter lR">r</text>
  <text x="-36" y="-71.4" text-anchor="middle" class="letter lI">i</text>
  <text x="-12" y="-79.1" text-anchor="middle" class="letter lV">v</text>
  <text x="12" y="-79.1" text-anchor="middle" class="letter lE">e</text>
  <text x="36" y="-71.4" text-anchor="middle" class="letter lR2">r</text>
  <text x="60" y="-52.9" text-anchor="middle" class="letter lS">s</text>
  <text x="-45" y="74.2" text-anchor="middle" class="letter lROCK_R" font-size="30">r</text>
  <text x="-15" y="79.4" text-anchor="middle" class="letter lROCK_O" font-size="30">o</text>
  <text x="15" y="79.4" text-anchor="middle" class="letter lROCK_C" font-size="30">c</text>
  <text x="45" y="74.2" text-anchor="middle" class="letter lROCK_K" font-size="30">k</text>
</svg>
</body>
</html>''')
    print(f"[Nordik] Animated logo > {path}")

def gen_site():
    path = os.path.join(OUT, "index.html")
    with open(path, "w") as f:
        f.write('''<!DOCTYPE html>
<html lang="fr">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rivers Rock \u2014 Nordik</title>
<link rel="preload" href="assets/logo.svg" as="image" type="image/svg+xml">
<link rel="icon" type="image/png" sizes="32x32" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAMlJREFUWEft1rENwjAQBdD/FYyAWIAJYAQKOkZgBEZgBDoWYARGYAQK4kiWLNnxnU8UKZLr/Pd9thMEAf4PQAiAEAChIyA6AgI7ArLWPuc8zjnnC85a+5xzHgEgBEAIAOrA3Xsf9z17ZgBIfYAx5hVjrN77z3ffH4DVByClBICttV+t3bee1gcgpQQAay0B7L0TAOYcBPAcB3NODPCe0DHG5xhjA0AIgBAAoSMgOgICOwKy1j7nnMec8wsnhHDOeRxjjACEEADhCAgBEB0BgR0BWWufc85jzvmFE8Kccx5jjACEEADhCEgIAOgICAEQHQH/Ab3+V/+tKtRsAAAAAElFTkSuQmCC">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;600&display=swap" rel="stylesheet">
<style>
:root{--b:#FAFAFA;--g:#E8E8E4;--a:#4A4A4A;--n:#2B2B2B;--l:#B8B5A8;--nav:rgba(250,250,250,0.9)}
@media(prefers-color-scheme:dark){:root{--b:#1A1A1A;--g:#2A2A2A;--a:#B8B5A8;--n:#E8E8E4;--l:#6A6A5A;--nav:rgba(26,26,26,0.9)}}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:60px}
body{font-family:'Inter',sans-serif;font-weight:300;color:var(--a);background:var(--b)}
nav{position:fixed;top:0;width:100%;padding:12px 32px;display:flex;justify-content:space-between;align-items:center;z-index:100;background:var(--nav);backdrop-filter:blur(8px);border-bottom:1px solid var(--g)}
nav .logo-small{text-decoration:none;color:var(--n);font-weight:200;font-size:14px;letter-spacing:4px;text-transform:lowercase}
nav a{color:var(--a);text-decoration:none;font-size:11px;font-weight:300;letter-spacing:1px;padding:4px 12px;transition:.3s}
nav a:hover{color:var(--l)}
.hero{min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:100px 24px 60px}
.hero .line{width:80px;height:2px;background:var(--l);margin-bottom:20px}
.hero h1{font-weight:200;font-size:clamp(32px,7vw,56px);color:var(--n);letter-spacing:4px;text-transform:lowercase;margin-bottom:4px}
.hero .tagline{font-weight:200;font-size:14px;color:var(--l);letter-spacing:2px;margin-bottom:24px}
.hero p{font-weight:300;font-size:14px;color:var(--a);max-width:440px;line-height:1.7}
.section{padding:80px 24px;max-width:680px;margin:0 auto}
.section h2{font-weight:200;font-size:24px;color:var(--n);letter-spacing:3px;margin-bottom:24px;text-align:center}
.section p{font-weight:300;font-size:14px;color:var(--a);line-height:1.8;margin-bottom:16px}
.mgrid{display:flex;flex-wrap:wrap;justify-content:center;gap:12px}
.mcard{flex:0 0 160px;text-align:center;padding:16px 8px}
.mcard h3{font-weight:400;font-size:15px;color:var(--n);margin-bottom:2px}
.mcard p{font-weight:200;font-size:11px;color:var(--a)}
.clist{list-style:none;padding:0}
.clist li{padding:10px 0;border-bottom:1px solid var(--g);display:flex;justify-content:space-between}
.clist .date{font-weight:400;color:var(--n)}
.clist .lieu{font-weight:200;color:var(--a)}
.ci{text-align:center;margin-top:16px}
.ci .email{color:var(--n);text-decoration:none;font-weight:300;border-bottom:1px solid var(--l)}
.links{display:flex;gap:12px;justify-content:center;margin-top:24px}
.links a{color:var(--a);text-decoration:none;font-size:11px;font-weight:200;padding:4px 12px;transition:.3s}
.links a:hover{color:var(--l)}
footer{text-align:center;padding:40px 24px;border-top:1px solid var(--g)}
footer .line{width:40px;height:1px;background:var(--l);margin:0 auto 8px}
footer p{font-weight:200;font-size:10px;color:var(--a);letter-spacing:8px;text-transform:lowercase}
</style></head>
<body>
<nav><a href="#" class="logo-small">rivers rock</a>
<div><a href="#groupe">groupe</a><a href="#concerts">concerts</a><a href="#musique">musique</a><a href="#contact">contact</a></div></nav>
<section class="hero"><div class="line"></div><h1>rivers rock</h1><div class="tagline">Reprises rock \u2014 Rouen</div>
<p>Groupe rouennais forme en 2024. Rock, pop-rock, inde, alternatif.</p></section>
<section id="groupe" class="section"><h2>groupe</h2>
<div class="mgrid">
<div class="mcard"><h3>Rosaria</h3><p>batterie</p></div>
<div class="mcard"><h3>Christophe</h3><p>basse</p></div>
<div class="mcard"><h3>Nicolas</h3><p>guitare</p></div>
<div class="mcard"><h3>David</h3><p>guitare / chant</p></div>
<div class="mcard"><h3>Virginie</h3><p>chant</p></div></div></section>
<section id="concerts" class="section"><h2>concerts</h2>
<ul class="clist"><li><span class="date">VEN 26 JUIN 2026</span><span class="lieu">Montigny . 19h30</span></li></ul>
<div style="margin-top:16px;max-width:300px;margin-left:auto;margin-right:auto"><img src="../../../images/IMG-20260620-WA0001.jpg" style="width:100%;height:auto;display:block" alt="Affiche"></div></section>
<section id="musique" class="section"><h2>musique</h2>
<p>Decouvrez Rivers Rock en action</p>
<div style="position:relative;padding-bottom:56.25%;height:0;background:var(--g);margin-top:16px"><div style="position:absolute;top:0;left:0;width:100%;height:100%;display:flex;align-items:center;justify-content:center;color:var(--a);font-weight:200"><iframe src="https://open.spotify.com/embed/playlist/REMPLACER_PAR_ID" width="100%" height="380" frameborder="0" allow="encrypted-media" style="border-radius:8px" title="Playlist Rivers Rock"></iframe></div></div></section>
<section id="contact" class="section"><h2>contact</h2>
<div class="ci"><a class="email" href="mailto:riversrockrouen@gmail.com">riversrockrouen@gmail.com</a></div>
<div class="links">
<a href="https://www.instagram.com/riversrockrouen">Instagram</a>
<a href="https://www.facebook.com/RiversRockRouen">Facebook</a>
<a href="https://www.youtube.com/@RiversRockRouen">YouTube</a></div>
  <form action="mailto:riversrockrouen@gmail.com" method="POST" enctype="text/plain" style="max-width:360px;margin:16px auto">
    <input type="text" name="nom" placeholder="votre nom" required style="width:100%;padding:8px 0;margin-bottom:8px;border:none;border-bottom:1px solid var(--g);background:transparent;color:var(--noir);font-family:inherit;font-size:13px;font-weight:200">
    <input type="email" name="email" placeholder="votre email" required style="width:100%;padding:8px 0;margin-bottom:8px;border:none;border-bottom:1px solid var(--g);background:transparent;color:var(--noir);font-family:inherit;font-size:13px;font-weight:200">
    <textarea name="message" placeholder="votre message" required rows="2" style="width:100%;padding:8px 0;margin-bottom:8px;border:none;border-bottom:1px solid var(--g);background:transparent;color:var(--noir);font-family:inherit;font-size:13px;font-weight:200;resize:vertical"></textarea>
    <button type="submit" style="width:100%;padding:8px;border:1px solid var(--l);background:transparent;color:var(--a);font-family:inherit;font-size:12px;font-weight:200;cursor:pointer;letter-spacing:2px">envoyer</button>
  </form>
</section>
<footer><div class="line"></div><p>rouen</p></footer>
</body>
</html>''')
    print(f"[Nordik] Site > {path}")

if __name__ == "__main__":
    gen_setlist(); gen_poster(); gen_flyer()
    gen_social(); gen_banners(); gen_avatar()
    gen_stickers(); gen_tshirt(); gen_animated(); gen_site()
