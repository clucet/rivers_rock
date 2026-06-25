#!/usr/bin/env python3
"""Generate video overlays (lower-thirds, bumpers) for all 4 propositions."""

import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image, ImageDraw, ImageFont
from logoutils import BEBAS_PATH, MONTSERRAT_PATH, ANTON_PATH, SPACE_MONO_PATH, NUNITO_PATH, INTERTIGHT_PATH, JETBRAINS_PATH, BLANC_PIL, ACCENT_PIL, OR_VIEILLI_PIL, TERRACOTTA_PIL, TEAL_PROFOND_PIL
from palette import BASE, FLUID_WAVE, ROCK_BRUT, SCENE_VINTAGE, PONTS_LUMIERE, NEON_NIGHTS, SABLE_BRONZE, NORDIK, GRUNGE, JAZZ_CLUB, Config

OUT = os.path.join(os.path.dirname(__file__), "..", "propositions")


def gen_lowerthird(cfg, dirname):
    """Generate a 1080x180 lower-third overlay for a proposition."""
    w, h = 1080, 180
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Gradient background bar (left to right fade)
    for i in range(w):
        t = i / w
        alpha = int(180 * (1 - t * 0.7))
        if cfg.name == "Fluid Wave":
            c = (26, 74, 58, alpha)
        elif cfg.name == "Rock Brut":
            c = (10, 10, 10, alpha)
        elif cfg.name == "Scène & Vintage":
            c = (26, 58, 92, alpha)
        else:
            c = (26, 58, 92, alpha)
        draw.line([(i, 0), (i, h)], fill=c)

    # Accent bar (left edge)
    if cfg.name == "Rock Brut":
        draw.rectangle([0, 0, 6, h], fill=(255, 59, 0, 200))
    elif cfg.name == "Fluid Wave":
        draw.rectangle([0, 0, 6, h], fill=(212, 168, 67, 200))
    elif cfg.name == "Scène & Vintage":
        draw.rectangle([0, 0, 6, h], fill=(232, 93, 58, 200))
    else:
        draw.rectangle([0, 0, 6, h], fill=(232, 93, 58, 200))

    # Brand name
    font_name = None
    font_tag = None
    if cfg.name == "Fluid Wave":
        font_name = ImageFont.truetype(NUNITO_PATH, 40) if NUNITO_PATH else ImageFont.truetype(BEBAS_PATH, 40)
        font_tag = ImageFont.truetype(NUNITO_PATH, 20) if NUNITO_PATH else ImageFont.truetype(MONTSERRAT_PATH, 20)
    elif cfg.name == "Rock Brut":
        font_name = ImageFont.truetype(ANTON_PATH, 44) if ANTON_PATH else ImageFont.truetype(BEBAS_PATH, 44)
        font_tag = ImageFont.truetype(JETBRAINS_PATH, 18) if JETBRAINS_PATH else ImageFont.truetype(MONTSERRAT_PATH, 18)
    elif cfg.name == "Scène & Vintage":
        font_name = ImageFont.truetype(ANTON_PATH, 42) if ANTON_PATH else ImageFont.truetype(BEBAS_PATH, 42)
        font_tag = ImageFont.truetype(SPACE_MONO_PATH, 18) if SPACE_MONO_PATH else ImageFont.truetype(MONTSERRAT_PATH, 18)
    else:
        font_name = ImageFont.truetype(BEBAS_PATH, 44)
        font_tag = ImageFont.truetype(MONTSERRAT_PATH, 20)

    draw.text((32, 32), "RIVERS ROCK", fill=BLANC_PIL, font=font_name)
    draw.text((32, 90), "@riversrockrouen  ·  Reprises rock — Rouen",
              fill=(255, 255, 255, 180), font=font_tag)

    # Small logo in right area
    logo_x, logo_y = w - 90, h // 2
    logo_r = 30
    if cfg.name == "Rock Brut":
        pts = []
        for i in range(6):
            a = math.radians(60 * i - 30)
            pts.append((logo_x + logo_r * math.cos(a), logo_y + logo_r * math.sin(a)))
        for i in range(6):
            draw.line([pts[i], pts[(i + 1) % 6]], fill=(255, 255, 255, 100), width=2)
    elif cfg.name == "Fluid Wave":
        for i in range(15):
            t = i / 14
            x1 = logo_x - logo_r + t * logo_r * 2
            y1 = logo_y + 4 * math.sin(t * 2 * math.pi * 2)
            x2 = logo_x - logo_r + ((i + 1) / 14) * logo_r * 2
            y2 = logo_y + 4 * math.sin(((i + 1) / 14) * 2 * math.pi * 2)
            draw.line([(x1, y1), (x2, y2)], fill=(255, 255, 255, 80), width=2)
    else:
        draw.ellipse([logo_x - logo_r, logo_y - logo_r, logo_x + logo_r, logo_y + logo_r],
                     outline=(255, 255, 255, 80), width=2)
        draw.line([(logo_x - logo_r * 0.7, logo_y), (logo_x + logo_r * 0.7, logo_y)],
                  fill=(232, 93, 58, 80), width=2)

    base_path = os.path.join(OUT, dirname, "assets", "templates")
    os.makedirs(base_path, exist_ok=True)
    path = os.path.join(base_path, "lowerthird.png")
    img.save(path)
    print(f"  {path} ({cfg.name})")


def gen_intro_bumper_html(cfg, dirname):
    """Generate a 3s intro bumper HTML with logo reveal + RIVERS ROCK."""
    accent = cfg.pil("accent")
    bg_colors = {
        "Fluid Wave": ("#1A4A3A", "#4A9B8E"),
        "Rock Brut": ("#0A0A0A", "#0A0A0A"),
        "Scène & Vintage": ("#1A3A5C", "#1A5C5C"),
        "Originale": ("#1A3A5C", "#4A9B8E"),
    }
    c1, c2 = bg_colors.get(cfg.name, ("#1A3A5C", "#4A9B8E"))
    font_fam = "'Anton', sans-serif" if cfg.name in ("Rock Brut", "Scène & Vintage") else "'Bebas Neue', sans-serif"

    html = f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rivers Rock — Intro Bumper</title>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Bebas+Neue&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0}}
body{{width:1080px;height:1920px;overflow:hidden;background:linear-gradient(135deg,{c1},{c2});display:flex;align-items:center;justify-content:center}}
.logo{{opacity:0;animation:fadeIn .3s ease-out .2s forwards}}
.logo svg{{width:160px;height:160px}}
.logo svg circle{{fill:none;stroke:#fff;stroke-width:4}}
.logo svg path{{fill:none;stroke:#{accent[0]:02x}{accent[1]:02x}{accent[2]:02x};stroke-width:3.5}}
h1{{font-family:{font_fam};font-size:72px;letter-spacing:4px;color:#fff;opacity:0;animation:slideUp .5s ease-out .8s forwards}}
.tagline{{font-family:'Montserrat',sans-serif;font-size:16px;color:rgba(255,255,255,0.6);letter-spacing:3px;text-transform:uppercase;opacity:0;animation:slideUp .4s ease-out 1.4s forwards}}
@keyframes fadeIn{{to{{opacity:1}}}}
@keyframes slideUp{{0%{{opacity:0;transform:translateY(40px)}}100%{{opacity:1;transform:translateY(0)}}}}
</style>
</head>
<body>
<div style="text-align:center">
  <div class="logo">
    <svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="42"/><path d="M18,50 Q30,42 42,50 Q54,58 66,50 Q78,42 90,50"/></svg>
  </div>
  <h1>RIVERS ROCK</h1>
  <div class="tagline">Reprises rock — Rouen</div>
</div>
</body>
</html>'''
    base_path = os.path.join(OUT, dirname, "assets", "templates")
    os.makedirs(base_path, exist_ok=True)
    path = os.path.join(base_path, "intro-bumper.html")
    with open(path, "w") as f:
        f.write(html)
    print(f"  {path}")


def gen_outro_bumper_html(cfg, dirname):
    """Generate a 5s outro bumper with subscribe CTA."""
    accent = cfg.pil("accent")
    bg_colors = {
        "Fluid Wave": ("#1A4A3A", "#4A9B8E"),
        "Rock Brut": ("#0A0A0A", "#0A0A0A"),
        "Scène & Vintage": ("#1A3A5C", "#1A5C5C"),
        "Originale": ("#1A3A5C", "#4A9B8E"),
    }
    c1, c2 = bg_colors.get(cfg.name, ("#1A3A5C", "#4A9B8E"))

    html = f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rivers Rock — Outro Bumper</title>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Space+Mono&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0}}
body{{width:1080px;height:1920px;overflow:hidden;background:linear-gradient(135deg,{c1},{c2});display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}}
h2{{font-family:'Anton',sans-serif;font-size:48px;letter-spacing:3px;color:#fff;opacity:0;animation:slideUp .5s ease-out .3s forwards}}
p{{font-family:'Space Mono',monospace;font-size:18px;color:rgba(255,255,255,0.5);margin:12px 0 40px;opacity:0;animation:slideUp .4s ease-out .9s forwards}}
.ytb{{display:inline-block;padding:14px 40px;background:rgba(255,255,255,0.1);border:2px solid rgba(255,255,255,0.2);border-radius:8px;color:#fff;text-decoration:none;font-family:'Anton',sans-serif;font-size:22px;letter-spacing:2px;opacity:0;animation:slideUp .4s ease-out 1.5s forwards}}
@keyframes slideUp{{0%{{opacity:0;transform:translateY(30px)}}100%{{opacity:1;transform:translateY(0)}}}}
</style>
</head>
<body>
<h2>RIVERS ROCK</h2>
<p>Abonnez-vous pour ne rien manquer</p>
<a class="ytb" href="https://www.youtube.com/@RiversRockRouen" target="_blank">▶  S'ABONNER</a>
</body>
</html>'''
    base_path = os.path.join(OUT, dirname, "assets", "templates")
    os.makedirs(base_path, exist_ok=True)
    path = os.path.join(base_path, "outro-bumper.html")
    with open(path, "w") as f:
        f.write(html)
    print(f"  {path}")


if __name__ == "__main__":
    configs = [
        (BASE, "00-originale"),
        (FLUID_WAVE, "01-fluid-wave"),
        (ROCK_BRUT, "02-rock-brut"),
        (SCENE_VINTAGE, "03-scene-vintage"),
        (PONTS_LUMIERE, "04-ponts-lumiere"),
        (NEON_NIGHTS, "05-neon-nights"),
    (NORDIK, "07-nordik"),
    (GRUNGE, "08-grunge"),
    (JAZZ_CLUB, "09-jazz-club"),
        (SABLE_BRONZE, "06-sable-bronze"),
    ]
    for cfg, dirname in configs:
        print(f"Overlays pour {cfg.name}...")
        gen_lowerthird(cfg, dirname)
        gen_intro_bumper_html(cfg, dirname)
        gen_outro_bumper_html(cfg, dirname)
    print("✅ Overlays + bumpers générés")
