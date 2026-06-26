#!/usr/bin/env python3
# Auto-generated -- do not edit directly
import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from logoutils import (
    create_bleed_canvas, save_with_crop_marks, draw_qr_pillow, draw_qr_reportlab,
    pillow_grain_overlay, draw_gradient_pdf, draw_waves_pdf, draw_grain_pdf,
    BEBAS_PATH, SPACE_MONO_PATH, JETBRAINS_PATH, DMMONO_PATH, MONTSERRAT_PATH,
)
from palette import HERITAGE as CFG
from reportlab.lib.pagesizes import A4, A6
from reportlab.lib.colors import Color
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(__file__), 'assets')
PDF = os.path.join(OUT, 'pdf')
TMPL = os.path.join(OUT, 'templates')
for d in (OUT, PDF, TMPL): os.makedirs(d, exist_ok=True)

# Font registrations
pdfmetrics.registerFont(TTFont("BebasNeue", BEBAS_PATH))
pdfmetrics.registerFont(TTFont("Montserrat", MONTSERRAT_PATH))
for role in ['hero', 'logo', 'body', 'badge', 'song', 'data', 'quote']:
    fname = CFG.fonts.get(role)
    if fname:
        try:
            from logoutils import _resolve_font
            fpath = _resolve_font(fname)
            if fpath:
                pdfmetrics.registerFont(TTFont(fname, fpath))
        except: pass

from setlist_data import SETLIST, GREEN_INDICES

C1 = CFG.rl("bleu_seine")
C2 = CFG.rl("vert_eau")
ACCENT = CFG.rl("accent")
OR = CFG.rl("or_vieilli")
BLANC = CFG.rl("blanc")
C1_PIL = CFG.pil("bleu_seine")
C2_PIL = CFG.pil("vert_eau")
ACCENT_PIL = CFG.pil("accent")

sl = "heritage"


def gen_setlist():
    W, H = A4
    path = os.path.join(PDF, "setlist-" + sl + ".pdf")
    cv, _, _, bleed = create_bleed_canvas(path, W, H)
    cv.setFillColor(Color(1, 1, 1))
    cv.rect(0, 0, W, H, stroke=0, fill=1)
    cv.setFillColor(Color(0, 0, 0, alpha=0.90))
    cv.setFont("BebasNeue", 28)
    cv.drawCentredString(W / 2, H - 115, "RIVERS ROCK")
    cv.setFillColor(ACCENT)
    cv.setFont("BebasNeue", 28)
    cv.drawCentredString(W / 2, H - 165, "SETLIST")
    for idx, (artist, title) in enumerate(SETLIST):
        col = idx // 6
        row = idx % 6
        cx = 150 + col * 270
        cy = 610 - row * 86
        bg = C2 if idx in GREEN_INDICES else ACCENT
        cv.setFillColor(Color(bg.red + 0.12, bg.green + 0.12, bg.blue + 0.12))
        cv.roundRect(cx - 125, cy - 37, 250, 74, 6, stroke=0, fill=1)
        cv.setFillColor(BLANC)
        cv.setFont("BebasNeue", 16)
        cv.drawCentredString(cx, cy + 5, artist)
        if title:
            cv.setFont("Montserrat", 9)
            cv.drawCentredString(cx, cy - 17, title)
    cv.setFillColor(Color(1, 1, 1, alpha=0.18))
    cv.setFont("Montserrat", 7)
    text, tr = "R O U E N", 3
    x = W / 2 - (sum(pdfmetrics.stringWidth(c, "Montserrat", 7) for c in text) + tr * (len(text) - 1)) / 2
    for c in text:
        w = pdfmetrics.stringWidth(c, "Montserrat", 7)
        cv.drawString(x, 14, c)
        x += w + tr
    save_with_crop_marks(cv, W, H, bleed)
    print("[" + CFG.name + "] Setlist > " + path)

def gen_poster():
    W, H = A4
    path = os.path.join(PDF, "poster-" + sl + ".pdf")
    cv, _, _, bleed = create_bleed_canvas(path, W, H)
    draw_gradient_pdf(cv, W, H, C1, C2)
    draw_grain_pdf(cv, W, H, seed=42)
    cv.setFillColor(BLANC)
    cv.setFont("BebasNeue", 28)
    cv.drawCentredString(W / 2, H - 190, "RIVERS ROCK")
    cv.setFillColor(ACCENT)
    cv.setFont("BebasNeue", 56)
    cv.drawCentredString(W / 2, H - 340, "VEN 26 JUIN 2026")
    cv.setFillColor(Color(1, 1, 1, alpha=0.7))
    cv.setFont("Montserrat", 18)
    cv.drawCentredString(W / 2, H - 385, "Montigny . 19h30")
    save_with_crop_marks(cv, W, H, bleed)
    print("[" + CFG.name + "] Poster > " + path)

def gen_flyer():
    FW, FH = A6
    path = os.path.join(PDF, "flyer-" + sl + ".pdf")
    cv, trim_w, trim_h, bleed = create_bleed_canvas(path, A4[0], A4[1])
    for page in range(2):
        for row in range(2):
            for col in range(2):
                ox, oy = col * FW, (1 - row) * FH
                draw_gradient_pdf(cv, FW, FH, C1, C2, steps=60, x=ox, y=oy)
                cx = ox + FW / 2
                cv.setFillColor(BLANC)
                cv.setFont("BebasNeue", 22)
                cv.drawCentredString(cx, oy + FH - 40, "RIVERS ROCK")
                cv.setFillColor(ACCENT)
                cv.setFont("BebasNeue", 34)
                cv.drawCentredString(cx, oy + FH - 110, "VEN 26 JUIN 2026")
                cv.setFillColor(Color(1, 1, 1, alpha=0.7))
                cv.setFont("Montserrat", 10)
                cv.drawCentredString(cx, oy + FH - 140, "Montigny . 19h30")
        if page == 0: cv.showPage()
    save_with_crop_marks(cv, trim_w, trim_h, bleed)
    print("[" + CFG.name + "] Flyer > " + path)

def gen_animated():
    path = os.path.join(TMPL, "logo-animated-" + sl + ".html")
    with open(path, "w") as f:
        f.write("""<!DOCTYPE html><html lang=\"fr\"><head><meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
<title>Rivers Rock -- Héritage</title>
<style>*{margin:0;padding:0}
body{width:1080px;height:1920px;overflow:hidden;background:#1A237E;display:flex;align-items:center;justify-content:center}
svg{width:400px;height:400px;overflow:visible}
</style></head><body>
<svg viewBox="-200 -200 400 400">
<circle cx="0" cy="0" r="140" fill="none" stroke="#D4AF37" stroke-width="2" opacity="0.5"><animate attributeName="r" dur="4s" repeatCount="indefinite" values="140;145;140"/></circle><path d="M0,-100 L20,-80 L40,-60 L20,-40 L0,-20 L-20,-40 L-40,-60 L-20,-80 Z" fill="#D4AF37" opacity="0.15"><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="20s" repeatCount="indefinite"/></path><text x="0" y="10" text-anchor="middle" font-family="serif" font-size="22" fill="#D4AF37" letter-spacing="4">RIVERS ROCK</text>
</svg></body></html>""")
    print("[Héritage] Animated logo > " + path)

def gen_site():
    path = os.path.join(OUT, "index.html")
    with open(path, "w") as f:
        f.write("""<!DOCTYPE html><html lang=\"fr\"><head><meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>Rivers Rock -- Héritage</title><link href=\"https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@300;400;600&display=swap\" rel=\"stylesheet\"><style>*{margin:0;padding:0;box-sizing:border-box}:root{--c1:#1A237E;--c2:#BDBDBD;--accent:#D4AF37;--or:#D4AF37;--blanc:#FFFFFF}body{font-family:Montserrat,sans-serif;background:var(--c1);color:var(--blanc);min-height:100vh}.hero{min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:100px 24px 60px}.hero h1{font-family:Bebas Neue,sans-serif;font-size:64px;letter-spacing:3px;color:var(--accent)}.hero .tag{font-size:14px;color:var(--or);margin-top:8px}.section{padding:60px 24px;max-width:800px;margin:0 auto}.section h2{font-family:Bebas Neue,sans-serif;font-size:32px;letter-spacing:2px;margin-bottom:20px;color:var(--accent)}.members-grid{display:flex;flex-wrap:wrap;gap:16px;justify-content:center}.member-card{text-align:center;padding:20px;background:rgba(255,255,255,0.04);border-radius:8px;flex:0 0 140px}.avatar-circle{width:56px;height:56px;border-radius:50%;background:var(--accent);margin:0 auto 8px;display:flex;align-items:center;justify-content:center;font-family:Bebas Neue,sans-serif;font-size:24px;color:var(--c1)}.member-card h3{font-size:14px;margin-bottom:2px}.member-card p{font-size:11px;color:rgba(255,255,255,0.5)}.links-social a{display:inline-block;padding:8px 16px;margin:4px;border-radius:6px;background:rgba(255,255,255,0.06);color:var(--or);text-decoration:none;font-size:12px;transition:.2s}.links-social a:hover{background:var(--accent);color:var(--c1)}form{max-width:400px;margin:20px auto}input,textarea{width:100%;padding:10px;margin-bottom:8px;border:1px solid rgba(255,255,255,0.15);border-radius:6px;background:rgba(255,255,255,0.05);color:#fff;font-family:inherit;font-size:14px}button{width:100%;padding:10px;border:none;border-radius:6px;background:var(--accent);color:#fff;font-family:inherit;font-size:14px;cursor:pointer}@media(max-width:640px){.hero h1{font-size:36px}.members-grid{grid-template-columns:repeat(2,1fr)}}@media(prefers-color-scheme:light){:root{--c1:#FFF8E1;--blanc:#1A1A1A}}@media(prefers-reduced-motion){*{animation:none!important;transition:none!important}}a:focus-visible,button:focus-visible{outline:2px solid var(--accent);outline-offset:2px}</style></head><body><section class=\"hero\"><h1>RIVERS ROCK</h1><div class=\"tag\">Patrimoine normand, vitrail, colombages</div></section><section class=\"section\" id=\"groupe\"><h2>Le groupe</h2><p>Groupe rouennais forme en 2024. Rock, pop-rock, inde et alternatif.</p><div class=\"members-grid\"><div class=\"member-card\"><div class=\"avatar-circle\">R</div><h3>Rosaria</h3><p>Batterie</p></div><div class=\"member-card\"><div class=\"avatar-circle\">C</div><h3>Christophe</h3><p>Basse</p></div><div class=\"member-card\"><div class=\"avatar-circle\">N</div><h3>Nicolas</h3><p>Guitare</p></div><div class=\"member-card\"><div class=\"avatar-circle\">D</div><h3>David</h3><p>Guitare / Chant</p></div><div class=\"member-card\"><div class=\"avatar-circle\">V</div><h3>Virginie</h3><p>Chant</p></div></div></section><section class=\"section\" id=\"concerts\"><h2>Concerts</h2><p>Contactez-nous pour programmer un concert.</p></section><section class=\"section\" id=\"musique\"><h2>Musique</h2><p>Playlist a venir -- suivez-nous sur YouTube.</p></section><section class=\"section\" id=\"contact\"><h2>Contact</h2><form action=\"https://formsubmit.co/riversrock_rouen@gmail.com\" method=\"POST\"><input type=\"text\" name=\"nom\" placeholder=\"Votre nom\" required><input type=\"email\" name=\"email\" placeholder=\"Votre email\" required><textarea name=\"message\" placeholder=\"Votre message\" required rows=\"3\"></textarea><button type=\"submit\">Envoyer</button></form><div class=\"links-social\"><a href=\"https://www.instagram.com/riversrock_rouen\">Instagram</a><a href=\"https://www.facebook.com/RiversRockRouen\">Facebook</a><a href=\"https://www.youtube.com/@RiversRockRouen\">YouTube</a><a href=\"mailto:riversrock_rouen@gmail.com\">Email</a></div></section></body></html>""")
    print("[Héritage] Site > " + path)


# ── Social ──
def gen_social():
    import random as _r
    w, h = 1080, 1080
    img = Image.new("RGB", (w, h), C1_PIL)
    draw = ImageDraw.Draw(img)
    for _ in range(30):
        x = _r.randint(0, w)
        y = _r.randint(0, h)
        r = _r.randint(10, 80)
        draw.ellipse([x-r, y-r, x+r, y+r], fill=ACCENT_PIL + (30,))
    draw.text((w//2, h//2-60), "RIVERS ROCK", fill=(255,255,255), font=ImageFont.truetype(BEBAS_PATH, 56), anchor="mm")
    draw.text((w//2, h//2+40), "VEN 26 JUIN 2026", fill=(255,255,255), font=ImageFont.truetype(BEBAS_PATH, 32), anchor="mm")
    draw.text((w//2, h//2+80), "Montigny . 19h30", fill=(200,200,200), font=ImageFont.truetype(MONTSERRAT_PATH, 18), anchor="mm")
    if CFG.flag("use_grain"):
        img = pillow_grain_overlay(img, CFG.token("grain_intensity", 0.05))
    img.save(os.path.join(TMPL, "instagram-post.png"))
    # Story
    img2 = Image.new("RGB", (1080, 1920), C1_PIL)
    draw2 = ImageDraw.Draw(img2)
    draw2.text((540, 800), "RIVERS ROCK", fill=(255,255,255), font=ImageFont.truetype(BEBAS_PATH, 72), anchor="mm")
    draw2.text((540, 920), "VEN 26 JUIN 2026", fill=(255,255,255), font=ImageFont.truetype(BEBAS_PATH, 48), anchor="mm")
    draw2.text((540, 1000), "Montigny . 19h30", fill=(200,200,200), font=ImageFont.truetype(MONTSERRAT_PATH, 24), anchor="mm")
    img2.save(os.path.join(TMPL, "instagram-story.png"))
    print(f"[{CFG.name}] Social > templates/")

# ── Banners ──
def gen_banners():
    for name, w, h in [("facebook-banner", 1640, 624), ("youtube-banner", 2560, 1440)]:
        img = Image.new("RGB", (w, h), C1_PIL)
        draw = ImageDraw.Draw(img)
        draw.text((w//2, h//2), "RIVERS ROCK", fill=(255,255,255), font=ImageFont.truetype(BEBAS_PATH, int(h/3)), anchor="mm")
        img.save(os.path.join(TMPL, f"{name}.png"))
    print(f"[{CFG.name}] Banners > OK")

# ── Avatar ──
def gen_avatar():
    s = 500
    img = Image.new("RGB", (s, s), C1_PIL)
    draw = ImageDraw.Draw(img)
    draw.ellipse([50, 50, s-50, s-50], fill=ACCENT_PIL)
    draw.text((s//2, s//2), "H", fill=(255,255,255), font=ImageFont.truetype(BEBAS_PATH, 200), anchor="mm")
    img.save(os.path.join(TMPL, "avatar.png"))
    print(f"[{CFG.name}] Avatar > OK")

# ── Stickers ──
def gen_stickers():
    W, H = A4
    path = os.path.join(PDF, f"stickers-{sl}.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, W, H)
    _r = 12
    for i in range(12):
        x = 20 + (i % 4) * 50
        y = 20 + (i // 4) * 50
        cv.setFillColor(ACCENT)
        cv.circle(x + _r, y + _r, _r, stroke=0, fill=1)
        cv.setFillColor(BLANC)
        cv.setFont("BebasNeue", 7)
        cv.drawCentredString(x + _r, y + _r - 2, "H")
    save_with_crop_marks(cv, W, H, bleed)
    print(f"[{CFG.name}] Stickers > {path}")

# ── T-shirt ──
def gen_tshirt():
    W, H = A4
    path = os.path.join(PDF, f"tshirt-{sl}.pdf")
    cv, _, _, bleed = create_bleed_canvas(path, W, H)
    cv.setFillColor(C1)
    cv.rect(0, 0, W, H, stroke=0, fill=1)
    cv.setFillColor(BLANC)
    cv.setFont("BebasNeue", 36)
    cv.drawCentredString(W / 2, H / 2, "RIVERS ROCK")
    save_with_crop_marks(cv, W, H, bleed)
    print(f"[{CFG.name}] T-shirt > {path}")

if __name__ == "__main__":
    gen_setlist()
    gen_poster()
    gen_flyer()
    from generate_social import generate_post, generate_story
    from generate_banners import gen_banners
    from generate_avatar import gen_avatar
    from generate_stickers import gen_stickers
    from generate_tshirts import generate_print, generate_mockup
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
