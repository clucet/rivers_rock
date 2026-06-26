#!/usr/bin/env python3
"""Generate all Grunge assets — Proposition n°8."""
# SVG logo available at: ../propositions/XXX/assets/logo.svg


import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))
from logoutils import (
    create_bleed_canvas, save_with_crop_marks,
    pillow_grain_overlay,
    draw_qr_pillow,
    BEBAS_PATH, MONTSERRAT_PATH, SPACE_MONO_PATH, RUBIK_PATH, SYNEMONO_PATH,
)
from palette import GRUNGE as CFG
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

PAPIER = CFG.rl("papier")
TONER = CFG.rl("toner")
MARQ = CFG.rl("marqueur")
CORR = CFG.rl("correcteur")

PAPIER_PIL = CFG.pil("papier")
TONER_PIL = CFG.pil("toner")
MARQ_PIL = CFG.pil("marqueur")
CORR_PIL = CFG.pil("correcteur")

pdfmetrics.registerFont(TTFont("RubikGlitch", RUBIK_PATH))
pdfmetrics.registerFont(TTFont("SpaceMono", SPACE_MONO_PATH))
pdfmetrics.registerFont(TTFont("SyneMono", SYNEMONO_PATH))

from setlist_data import SETLIST

GREEN_INDICES = {0, 3, 6}

def logo_grunge_rl(cv, cx, cy, scale=1.0):
    cv.setFillColor(Color(1, 51/255, 102/255))
    cv.circle(cx + 15 * scale, cy - 5 * scale, 8 * scale, stroke=0, fill=1)
    cv.setFillColor(TONER)
    cv.setFont("RubikGlitch", max(8, int(14 * scale)))
    cv.drawCentredString(cx - 5 * scale, cy - 6 * scale, "rIVERS rOCK")

def logo_grunge_pil(draw, cx, cy, scale=1.0):
    r = 8 * scale
    draw.ellipse([cx + 15*scale - r, cy - 5*scale - r, cx + 15*scale + r, cy - 5*scale + r], fill=MARQ_PIL)
    font = ImageFont.truetype(RUBIK_PATH or SPACE_MONO_PATH, max(8, int(14 * scale)))
    draw.text((cx - 5*scale, cy - 6*scale), "rIVERS rOCK", fill=TONER_PIL, font=font)

def gen_setlist():
    W, H = A4; path = os.path.join(PDF, "setlist-grunge.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, W, H)
    cv.setFillColor(PAPIER); cv.rect(0, 0, W, H, stroke=0, fill=1)
    random.seed(42)
    for _ in range(5000):
        cv.setFillColor(Color(0, 0, 0, alpha=random.uniform(0.05, 0.15)))
        cv.circle(random.uniform(0, W), random.uniform(0, H), random.uniform(0.3, 1.5), stroke=0, fill=1)
    logo_grunge_rl(cv, W / 2 - 40, H - 105, 2.0)
    cv.setFillColor(TONER)
    cv.setFont("RubikGlitch", 16)
    cv.drawCentredString(W / 2, H - 160, "rIVERS rOCK")
    cv.setFillColor(MARQ)
    cv.setFont("RubikGlitch", 22)
    cv.drawCentredString(W / 2, H - 190, "SETLIST")
    card_w, card_h = 250, 74
    col_gap = (W - 2 * card_w) / 3
    col_c = [col_gap + card_w / 2, col_gap * 2 + card_w + card_w / 2]
    row_pitch, rows_top = 86, 610
    for idx, (artist, title) in enumerate(SETLIST):
        col, row = idx // 6, idx % 6
        cx = col_c[col]; cy = rows_top - row * row_pitch
        cl, cb = cx - card_w / 2, cy - card_h / 2
        cv.setFillColor(TONER)
        cv.setFont("SpaceMono", 10)
        cv.drawString(cl + 8, cy + 18, f">{idx+1}")
        cv.setFillColor(TONER)
        cv.setFont("SpaceMono", 15)
        cv.drawString(cl + 30, cy + 6, artist)
        if idx % 3 == 0:
            cv.setStrokeColor(MARQ)
            cv.setLineWidth(2)
            cv.line(cl + 30, cy + 20, cl + 30 + pdfmetrics.stringWidth(artist, "SpaceMono", 15), cy + 20)
        if title:
            cv.setFillColor(Color(0, 0, 0, alpha=0.6))
            cv.setFont("SpaceMono", 9)
            cv.drawCentredString(cx, cy - 18, title)
    cv.setFillColor(Color(0, 0, 0, alpha=0.3))
    cv.setFont("SyneMono", 7)
    text, tr = "R O U E N", 3
    x = W / 2 - (sum(pdfmetrics.stringWidth(c, "SyneMono", 7) for c in text) + tr * (len(text) - 1)) / 2
    for c in text: w = pdfmetrics.stringWidth(c, "SyneMono", 7); cv.drawString(x, 14, c); x += w + tr
    save_with_crop_marks(cv, W, H, bleed)
    print(f"[Grunge] Setlist > {path}")

def gen_poster():
    W, H = A4; path = os.path.join(PDF, "poster-grunge.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, W, H)
    cv.setFillColor(PAPIER); cv.rect(0, 0, W, H, stroke=0, fill=1)
    random.seed(42)
    for _ in range(5000):
        cv.setFillColor(Color(0, 0, 0, alpha=random.uniform(0.05, 0.15)))
        cv.circle(random.uniform(0, W), random.uniform(0, H), random.uniform(0.3, 1.5), stroke=0, fill=1)
    logo_grunge_rl(cv, W / 2, H - 190, 2.0)
    cv.setFillColor(TONER)
    cv.setFont("RubikGlitch", 16)
    cv.drawCentredString(W / 2, H - 250, "rIVERS rOCK")
    cv.setFillColor(MARQ)
    cv.setFont("SpaceMono", 12)
    cv.drawCentredString(W / 2, H - 275, ">> concert <<")
    cv.setFillColor(TONER)
    cv.setFont("RubikGlitch", 44)
    cv.drawCentredString(W / 2, H - 340, "VEN 26 JUIN")
    cv.setFillColor(Color(0, 0, 0, alpha=0.6))
    cv.setFont("SpaceMono", 14)
    cv.drawCentredString(W / 2, H - 380, "Montigny / 19h30")
    cv.setStrokeColor(MARQ)
    cv.setLineWidth(3)
    cv.line(W / 2 - 80, H - 410, W / 2 + 80, H - 410)
    cv.setFillColor(Color(0, 0, 0, alpha=0.3))
    cv.setFont("SyneMono", 7)
    text, tr = "R O U E N", 3
    x = W / 2 - (sum(pdfmetrics.stringWidth(c, "SyneMono", 7) for c in text) + tr * (len(text) - 1)) / 2
    for c in text: w = pdfmetrics.stringWidth(c, "SyneMono", 7); cv.drawString(x, 14, c); x += w + tr
    save_with_crop_marks(cv, W, H, bleed)
    print(f"[Grunge] Poster > {path}")

def gen_flyer():
    FW, FH = A6; path = os.path.join(PDF, "flyer-grunge.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, A4[0], A4[1])
    def draw_recto(cv, ox, oy):
        cv.setFillColor(PAPIER); cv.rect(ox, oy, FW, FH, stroke=0, fill=1)
        cx = ox + FW / 2
        logo_grunge_rl(cv, cx, oy + FH - 50, 1.0)
        cv.setFillColor(TONER); cv.setFont("RubikGlitch", 14)
        cv.drawCentredString(cx, oy + FH - 80, "rIVERS rOCK")
        cv.setFillColor(MARQ); cv.setFont("RubikGlitch", 28)
        cv.drawCentredString(cx, oy + FH - 145, "VEN 26 JUIN 2026")
        cv.setFillColor(Color(0, 0, 0, alpha=0.5))
        cv.setFont("SpaceMono", 10)
        cv.drawCentredString(cx, oy + FH - 175, "Montigny 19h30")
    def draw_verso(cv, ox, oy):
        cv.setFillColor(PAPIER); cv.rect(ox, oy, FW, FH, stroke=0, fill=1)
        cx = ox + FW / 2
        cv.setFillColor(TONER); cv.setFont("SpaceMono", 10)
        cv.drawCentredString(cx, oy + FH - 40, "rIVERS rOCK")
        bio = ["Groupe rouennais", "forme en 2024", "", "Rosaria - batterie", "Christophe - basse",
               "Nicolas - guitare", "David - guitare/chant", "Virginie - chant", "", "book us !"]
        cv.setFillColor(Color(0, 0, 0, alpha=0.7))
        cv.setFont("SpaceMono", 7)
        y = oy + FH - 80
        for line in bio: cv.drawCentredString(cx, y, line); y -= 12
        cv.setFillColor(MARQ)
        cv.setFont("SpaceMono", 7)
        cv.drawCentredString(cx, y - 6, "contactez-nous!")
        cv.setFillColor(Color(0, 0, 0, alpha=0.3))
        cv.setFont("SpaceMono", 7)
        cv.drawCentredString(cx, y - 22, "@riversrock_rouen")
    for page in range(2):
        for row in range(2):
            for col in range(2):
                ox, oy = col * FW, (1 - row) * FH
                if page == 0: draw_recto(cv, ox, oy)
                else: draw_verso(cv, ox, oy)
        if page == 0: cv.showPage()
    cv.save()
    print(f"[Grunge] Flyer > {path}")

def gen_social():
    font_glitch = ImageFont.truetype(RUBIK_PATH, 56)
    font_mono = ImageFont.truetype(SPACE_MONO_PATH, 20)
    font_tag = ImageFont.truetype(SPACE_MONO_PATH, 14)
    w, h = 1080, 1080
    img = Image.new("RGB", (w, h), PAPIER_PIL)
    draw = ImageDraw.Draw(img)
    img = pillow_grain_overlay(img, 0.15, seed=10)
    logo_grunge_pil(draw, w / 2, 140, 2.5)
    bbox = draw.textbbox((0,0), "rIVERS rOCK", font=font_glitch); tw=bbox[2]-bbox[0]
    draw.text(((w-tw)/2,155), "rIVERS rOCK", fill=TONER_PIL, font=font_glitch)
    draw.text((200,400), "VEN 26 JUIN", fill=MARQ_PIL, font=font_mono)
    draw.text((200,440), "Montigny 19h30", fill=TONER_PIL, font=font_mono)
    draw.text((200,860), "@riversrock_rouen", fill=(150,150,150), font=font_tag)
    img.save(os.path.join(TMPL, "instagram-post.png"))
    w, h = 1080, 1920
    img = Image.new("RGB", (w, h), PAPIER_PIL)
    draw = ImageDraw.Draw(img)
    img = pillow_grain_overlay(img, 0.15, seed=20)
    logo_grunge_pil(draw, w / 2, 180, 3.0)
    bbox = draw.textbbox((0,0), "rIVERS rOCK", font=font_glitch); tw=bbox[2]-bbox[0]
    draw.text(((w-tw)/2+20,195), "rIVERS rOCK", fill=TONER_PIL, font=font_glitch)
    draw.text((200,650), "VEN 26 JUIN", fill=MARQ_PIL, font=ImageFont.truetype(SPACE_MONO_PATH, 80))
    draw.text((200,750), "Montigny 19h30", fill=TONER_PIL, font=font_mono)
    draw.text((200,1750), "@riversrock_rouen", fill=(150,150,150), font=font_tag)
    img.save(os.path.join(TMPL, "instagram-story.png"))
    print(f"[Grunge] Social > {TMPL}")

def gen_banners():
    for n,w,h,s in [("facebook-banner.png",1640,624,48),("youtube-banner.png",2560,1440,72)]:
        img = Image.new("RGB", (w,h), PAPIER_PIL)
        draw = ImageDraw.Draw(img)
        img = pillow_grain_overlay(img, 0.15, seed=30)
        font_l = ImageFont.truetype(RUBIK_PATH, s)
        tw = draw.textbbox((0,0), "rIVERS rOCK", font=font_l)[2]
        sx = (w - tw) / 2
        draw.text((sx, h/2-tw*0.25), "rIVERS rOCK", fill=TONER_PIL, font=font_l)
        img.save(os.path.join(TMPL, n))
    print(f"[Grunge] Banners > {TMPL}")

def gen_avatar():
    S = 500
    img = Image.new("RGBA", (S, S), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    r = 80
    draw.ellipse([S/2-r, S/2-r, S/2+r, S/2+r], fill=MARQ_PIL)
    font = ImageFont.truetype(RUBIK_PATH, 60)
    bbox = draw.textbbox((0,0), "RR", font=font); tw=bbox[2]-bbox[0]
    draw.text(((S-tw)/2, S/2-30), "RR", fill=CORR_PIL, font=font)
    img.save(os.path.join(TMPL, "avatar.png"))
    print(f"[Grunge] Avatar > {TMPL}")

def gen_stickers():
    from reportlab.lib.units import mm
    W, H = A4; SR = 40*mm; MX=(W-2*SR*2)/3; MY=(H-3*SR*2)/4
    centers = [(MX+SR+c*(MX+SR*2), MY+SR+r*(MY+SR*2)) for c in range(2) for r in range(3)]
    path = os.path.join(PDF, "stickers-grunge.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, A4[0], A4[1])
    for cx, cy in centers:
        cv.setFillColor(PAPIER); cv.circle(cx, cy, SR, stroke=0, fill=1)
        cv.setStrokeColor(TONER); cv.setLineWidth(3); cv.circle(cx, cy, SR, stroke=1, fill=0)
        sr = SR * 0.50
        cv.setFillColor(MARQ); cv.circle(cx, cy, sr*0.5, stroke=0, fill=1)
        cv.setFillColor(TONER); cv.setFont("RubikGlitch", 8)
        cv.drawCentredString(cx, cy+sr+8, "rIVERS rOCK")
    cv.save()
    print(f"[Grunge] Stickers > {path}")

def gen_tshirt():
    from reportlab.lib.units import mm
    w,h=A4; sz=[("S",22*mm,w/4,h-200),("M",28*mm,w*3/4,h-200),("L",34*mm,w/4,h-440),("XL",40*mm,w*3/4,h-440)]
    path=os.path.join(PDF,"tshirt-grunge.pdf")
    cv=canvas.Canvas(path,pagesize=A4)
    cv.setFillColor(Color(0,0,0,alpha=0.04)); cv.rect(0,0,w,h,stroke=0,fill=1)
    for label,sr,cx,cy in sz:
        cv.setFillColor(MARQ); cv.circle(cx,cy,sr*0.5,stroke=0,fill=1)
        cv.setFillColor(TONER); cv.setFont("RubikGlitch",max(8,int(sr*1.2)))
        cv.drawCentredString(cx,cy+sr*0.6+4,"rIVERS rOCK")
        if label:
            cv.setFillColor(Color(0,0,0,alpha=0.3)); cv.setFont("SpaceMono",7)
            cv.drawCentredString(cx,cy+sr+60,label)
    cv.save()
    print(f"[Grunge] T-shirt > {path}")

def gen_animated():
    path = os.path.join(TMPL, "logo-animated-grunge.html")
    with open(path, "w") as f:
        f.write('''<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rivers Rock \u2014 Grunge</title>
<meta name="description" content="Rivers Rock \u2014 Grunge — Rivers Rock, groupe de reprises rock base a Rouen. Rock, pop-rock, inde et alternatif — 5 musiciens, 12 titres.">
<meta property="og:title" content="Rivers Rock \u2014 Grunge">
<meta property="og:description" content="Rivers Rock \u2014 Grunge — Rivers Rock, groupe de reprises rock base a Rouen. Rock, pop-rock, inde et alternatif — 5 musiciens, 12 titres.">
<meta property="og:type" content="music.group">
<meta property="og:url" content="https://clucet.github.io/rivers_rock/propositions/08-grunge/">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="Rivers Rock \u2014 Grunge">
<link rel="icon" type="image/svg+xml" sizes="32x32" href="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzMiAzMiI+PGNpcmNsZSBjeD0iMTYiIGN5PSIxNiIgcj0iMTUiIGZpbGw9IiNGRjMzNjYiLz48dGV4dCB4PSIxNiIgeT0iMjIiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtZmFtaWx5PSJzYW5zLXNlcmlmIiBmb250LXNpemU9IjE2IiBmaWxsPSIjZmZmIiBmb250LXdlaWdodD0iYm9sZCI+ZzwvdGV4dD48L3N2Zz4=">
<style>
*{margin:0;padding:0}
body{width:1080px;height:1920px;overflow:hidden;background:#F5EADD;display:flex;align-items:center;justify-content:center}
canvas{position:absolute;top:0;left:0;width:1080px;height:1920px}
svg{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:400px;height:400px;overflow:visible}
.stamp{fill:#FF3366;opacity:0;animation:stampIn .8s cubic-bezier(0.34,1.56,0.64,1) 2.8s forwards}
@keyframes stampIn{0%{opacity:0;transform:scale(0) rotate(-10deg)}100%{opacity:1;transform:scale(1) rotate(-3deg)}}
.letter{font-family:'Courier New',monospace;font-size:34px;fill:#1A1A1A;opacity:0}
.lR{animation:dropGlitch .4s ease-out .5s forwards}
.lI{animation:dropGlitch .4s ease-out .8s forwards}
.lV{animation:dropGlitch .4s ease-out 1.1s forwards}
.lE{animation:dropGlitch .4s ease-out 1.4s forwards}
.lR2{animation:dropGlitch .4s ease-out 1.9s forwards}
.lS{animation:dropGlitch .4s ease-out 2.2s forwards}
.lROCK_R{animation:dropGlitch .4s ease-out 3.0s forwards}
.lROCK_O{animation:dropGlitch .4s ease-out 3.3s forwards}
.lROCK_C{animation:dropGlitch .4s ease-out 3.6s forwards}
.lROCK_K{animation:dropGlitch .4s ease-out 4.0s forwards}
@keyframes dropGlitch{0%{opacity:0;transform:translateY(-20px) skewX(10deg)}50%{opacity:0.5;transform:translateY(5px) skewX(-5deg)}100%{opacity:1;transform:translateY(0) skewX(0deg)}}

a:focus-visible{outline:2px solid var(--accent,#E85D3A);outline-offset:2px}
button:focus-visible{outline:2px solid var(--accent,#E85D3A);outline-offset:2px}
@media(max-width:640px){
  header h1{font-size:28px}
  .members-grid{grid-template-columns:repeat(2,1fr)}
  .section{padding:30px 12px}
  nav{margin:6px 0}
  nav .nav-links{display:none}
  .hero h2{font-size:22px}
}
@media(max-width:400px){
  header h1{font-size:22px}
  .members-grid{grid-template-columns:1fr}
  .hero{padding:40px 16px 20px}
}
</style></head>
<body>
<canvas id="p"></canvas>
<svg viewBox="-200 -200 400 400">
  <circle class="stamp" cx="60" cy="-20" r="30"/>
  <text x="-60" y="-52.9" text-anchor="middle" class="letter lR">r</text>
  <text x="-36" y="-71.4" text-anchor="middle" class="letter lI">I</text>
  <text x="-12" y="-79.1" text-anchor="middle" class="letter lV">V</text>
  <text x="12" y="-79.1" text-anchor="middle" class="letter lE">E</text>
  <text x="36" y="-71.4" text-anchor="middle" class="letter lR2">R</text>
  <text x="60" y="-52.9" text-anchor="middle" class="letter lS">S</text>
  <text x="-45" y="74.2" text-anchor="middle" class="letter lROCK_R" font-size="28">r</text>
  <text x="-15" y="79.4" text-anchor="middle" class="letter lROCK_O" font-size="28">O</text>
  <text x="15" y="79.4" text-anchor="middle" class="letter lROCK_C" font-size="28">C</text>
  <text x="45" y="74.2" text-anchor="middle" class="letter lROCK_K" font-size="28">K</text>
</svg>
<script>
const c=document.getElementById('p'),ctx=c.getContext('2d');
c.width=1080;c.height=1920;
const ps=[];
for(let i=0;i<40;i++){ps.push({x:Math.random()*1080,y:Math.random()*1920,s:Math.random()*2+0.5,a:Math.random()*0.1+0.02})}
function draw(){ctx.clearRect(0,0,1080,1920);
ctx.fillStyle='#F5EADD';ctx.fillRect(0,0,1080,1920);
for(const p of ps){ctx.beginPath();ctx.rect(p.x,p.y,p.s,p.s);ctx.fillStyle='rgba(0,0,0,'+p.a+')';ctx.fill();p.y+=0.5;if(p.y>1920){p.y=0;p.x=Math.random()*1080}}
requestAnimationFrame(draw)}draw();
</script>
</body></html>''')
    print(f"[Grunge] Animated logo > {path}")

def gen_site():
    path = os.path.join(OUT, "index.html")
    with open(path, "w") as f:
        f.write('''<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rivers Rock \u2014 Grunge</title>
<meta name="description" content="Rivers Rock \u2014 Grunge — Rivers Rock, groupe de reprises rock base a Rouen. Rock, pop-rock, inde et alternatif — 5 musiciens, 12 titres.">
<meta property="og:title" content="Rivers Rock \u2014 Grunge">
<meta property="og:description" content="Rivers Rock \u2014 Grunge — Rivers Rock, groupe de reprises rock base a Rouen. Rock, pop-rock, inde et alternatif — 5 musiciens, 12 titres.">
<meta property="og:type" content="music.group">
<meta property="og:url" content="https://clucet.github.io/rivers_rock/propositions/08-grunge/">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="Rivers Rock \u2014 Grunge">
<link rel="preload" href="assets/logo.svg" as="image" type="image/svg+xml">
<link rel="icon" type="image/svg+xml" sizes="32x32" href="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzMiAzMiI+PGNpcmNsZSBjeD0iMTYiIGN5PSIxNiIgcj0iMTUiIGZpbGw9IiNGRjMzNjYiLz48dGV4dCB4PSIxNiIgeT0iMjIiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtZmFtaWx5PSJzYW5zLXNlcmlmIiBmb250LXNpemU9IjE2IiBmaWxsPSIjZmZmIiBmb250LXdlaWdodD0iYm9sZCI+ZzwvdGV4dD48L3N2Zz4=">
<style>
*{margin:0;padding:0}
body{font-family:'Courier New',monospace;background:#F5EADD;color:#1A1A1A;min-height:100vh}
@media(prefers-color-scheme:dark){body{background:#1A1A1A;color:#E8D8CC}}
.bg{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;background:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256'%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23g)' opacity='0.12'/%3E%3C/svg%3E")}
header{padding:20px 24px 10px;text-align:center;position:relative;z-index:1;border-bottom:3px dashed #1A1A1A}
header h1{font-size:42px;letter-spacing:-2px;text-transform:uppercase;color:#FF3366}
header p{font-size:11px;color:#1A1A1A;margin-top:4px}
nav{margin:10px 0;text-align:center}
nav a{color:#1A1A1A;text-decoration:none;font-size:13px;margin:0 10px;padding:2px 6px;border:1px solid #1A1A1A}
nav a:hover{background:#FF3366;color:#fff}
.hero{padding:60px 24px 40px;text-align:center;position:relative;z-index:1}
.hero h2{font-size:28px;text-transform:uppercase;letter-spacing:-1px;margin-bottom:8px}
.hero .tag{font-size:12px;color:#FF3366;margin-bottom:20px}
.section{padding:30px 24px;max-width:600px;margin:0 auto;position:relative;z-index:1}
.section h3{font-size:18px;margin-bottom:16px;border-left:4px solid #FF3366;padding-left:10px}
.mg{display:flex;flex-wrap:wrap;gap:8px;justify-content:center}
.mg>div{text-align:center;padding:8px}
.mg h4{font-size:14px}
.mg p{font-size:11px;color:#666}
.cl{list-style:none}
.cl li{padding:6px 0;font-size:13px}
.cl .d{color:#FF3366}
footer{padding:30px;text-align:center;font-size:10px;color:#999;position:relative;z-index:1;border-top:1px dashed #1A1A1A}

a:focus-visible{outline:2px solid var(--accent,#E85D3A);outline-offset:2px}
button:focus-visible{outline:2px solid var(--accent,#E85D3A);outline-offset:2px}
@media(max-width:640px){
  header h1{font-size:28px}
  .members-grid{grid-template-columns:repeat(2,1fr)}
  .section{padding:30px 12px}
  nav{margin:6px 0}
  nav .nav-links{display:none}
  .hero h2{font-size:22px}
}
@media(max-width:400px){
  header h1{font-size:22px}
  .members-grid{grid-template-columns:1fr}
  .hero{padding:40px 16px 20px}
}

@media(max-width:640px){
  .hero h1{font-size:28px}
  .members-grid{grid-template-columns:repeat(2,1fr)}
  .section{padding:30px 12px}
  nav{padding:10px 16px}
  nav .nav-links{display:none}
}
@media(max-width:400px){
  .hero h1{font-size:22px}
  .members-grid{grid-template-columns:1fr}
  .hero{padding:80px 16px 40px}
}
</style></head>
<body>
<div class="bg"></div>
<header><h1>rIVERS rOCK</h1><p>Reprises rock \u2014 Rouen</p></header>
<nav><a href="#g">groupe</a><a href="#c">concerts</a><a href="#m">musique</a><a href="#ct">contact</a></nav>
<section class="hero"><h2>rIVERS rOCK</h2><div class="tag">>> Reprises rock - Rouen <<</div>
<p>Groupe rouennais forme en 2024. Rock, pop-rock, inde, alternatif.</p></section>
<section id="g" class="section"><h3>groupe</h3>
<div class="mg">
<div><h4>Rosaria</h4><p>batterie</p></div>
<div><h4>Christophe</h4><p>basse</p></div>
<div><h4>Nicolas</h4><p>guitare</p></div>
<div><h4>David</h4><p>guitare/chant</p></div>
<div><h4>Virginie</h4><p>chant</p></div></div></section>
<section id="c" class="section"><h3>concerts</h3>
<ul class="cl"><li><span class="d">VEN 26 JUIN 2026</span> - Montigny . 19h30</li></ul>
<div style="margin-top:16px;max-width:300px;margin-left:auto;margin-right:auto;border:2px dashed #1A1A1A;padding:4px"><img src="../../../images/IMG-20260620-WA0001.jpg" style="width:100%;height:auto;display:block" alt="Affiche"></div></section>
<section id="m" class="section"><h3>musique</h3>
<p>Decouvrez Rivers Rock en action</p>
<div style="padding:20px;text-align:center;border:2px dashed #1A1A1A;margin-top:10px"><div style="text-align:center;padding:30px 20px;background:rgba(128,128,128,0.04);border-radius:8px"><p style="color:rgba(128,128,128,0.5);font-size:14px;margin-bottom:12px;font-family:sans-serif">Playlist musicale a venir</p><a href="https://www.youtube.com/@RiversRockRouen" target="_blank" style="display:inline-block;padding:10px 24px;border-radius:6px;background:var(--accent,#E85D3A);color:#fff;text-decoration:none;font-size:13px">Suivre sur YouTube</a></div></div></section>
<section id="ct" class="section"><h3>contact</h3>
<p>riversrock_rouen@gmail.com</p>
<p><a href="https://www.instagram.com/riversrock_rouen" style="color:#1A1A1A">Instagram</a>
| <a href="https://www.facebook.com/RiversRockRouen" style="color:#1A1A1A">Facebook</a>
| <a href="https://www.youtube.com/@RiversRockRouen" style="color:#1A1A1A">YouTube</a></p>
<form action="https://formsubmit.co/riversrock_rouen@gmail.com" method="POST" enctype="text/plain" style="max-width:360px;margin:16px auto;font-family:Courier New,monospace">
  <input type="text" name="nom" placeholder="nom" required style="width:100%;padding:6px;margin-bottom:6px;border:1px solid #1A1A1A;background:transparent;font-family:inherit;font-size:12px">
  <input type="email" name="email" placeholder="email" required style="width:100%;padding:6px;margin-bottom:6px;border:1px solid #1A1A1A;background:transparent;font-family:inherit;font-size:12px">
  <textarea name="message" placeholder="message" required rows="2" style="width:100%;padding:6px;margin-bottom:6px;border:1px solid #1A1A1A;background:transparent;font-family:inherit;font-size:12px;resize:vertical"></textarea>
  <button type="submit" style="width:100%;padding:6px;border:1px solid #1A1A1A;background:#FF3366;color:#fff;font-family:inherit;font-size:12px;cursor:pointer">envoyer</button>
</form>
</section>
<footer>R O U E N</footer>
</body></html>''')
    print(f"[Grunge] Site > {path}")

if __name__ == "__main__":
    gen_setlist(); gen_poster(); gen_flyer()
    gen_social(); gen_banners(); gen_avatar()
    gen_stickers(); gen_tshirt(); gen_animated(); gen_site()
