#!/usr/bin/env python3
"""Generate missing assets for all 5 propositions: business cards, signatures, mockups, stage plots, tech sheets, lyrics."""

import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib.colors import Color, HexColor
from reportlab.pdfgen import canvas as rlcanvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from logoutils import (
    reportlab_crest, pillow_crest, pillow_crest_timbre, pillow_monogramme_rr,
    pillow_bridge_silhouette, pillow_monogramme_wave, pillow_hexagon_monogramme,
    pillow_neon_logo, pillar_neon_logo, pillow_sun_logo, pillar_sun_logo,
    pillow_grain_overlay,
    create_bleed_canvas, save_with_crop_marks,
    BEBAS_PATH, MONTSERRAT_PATH, ANTON_PATH, SPACE_MONO_PATH,
    NUNITO_PATH, INTERTIGHT_PATH, JETBRAINS_PATH,
    TEKO_PATH, RALEWAY_PATH, DMMONO_PATH,
    BANGERS_PATH, CINZELDECO_PATH, OSWALD_PATH, SOURCESANS_PATH, DMSANS_PATH,
)
from palette import BASE, FLUID_WAVE, ROCK_BRUT, SCENE_VINTAGE, PONTS_LUMIERE, NEON_NIGHTS, SABLE_BRONZE, NORDIK, GRUNGE, JAZZ_CLUB
from palette import BITUME, CORDES_VOIX, HERITAGE, RUBICON, MINUIT

PROPS = [
    (BASE,          "00-originale"),
    (FLUID_WAVE,    "01-fluid-wave"),
    (ROCK_BRUT,     "02-rock-brut"),
    (SCENE_VINTAGE, "03-scene-vintage"),
    (PONTS_LUMIERE, "04-ponts-lumiere"),
    (NEON_NIGHTS,   "05-neon-nights"),
    (SABLE_BRONZE,  "06-sable-bronze"),
    (NORDIK,        "07-nordik"),
    (GRUNGE,        "08-grunge"),
    (JAZZ_CLUB,     "09-jazz-club"),
    (BITUME,        "10-bitume"),
    (CORDES_VOIX,   "11-cordes-voix"),
    (HERITAGE,      "12-heritage"),
    (RUBICON,       "13-rubicon"),
    (MINUIT,        "14-minuit"),
]

from setlist_data import SETLIST, GREEN_INDICES


# ── Logo dispatch ──

def _hexagon_logo_rl(cv, cx, cy, r):
    r_size = r
    from math import radians, cos, sin
    pts = [(cx + r_size * cos(radians(60 * i - 30)), cy + r_size * sin(radians(60 * i - 30))) for i in range(6)]
    cv.setStrokeColor(Color(1, 231/255, 0))
    cv.setLineWidth(3)
    for i in range(6):
        cv.line(pts[i][0], pts[i][1], pts[(i+1) % 6][0], pts[(i+1) % 6][1])
    inner = [(cx + (p[0]-cx) * 0.85, cy + (p[1]-cy) * 0.85) for p in pts]
    cv.setStrokeColor(Color(1, 1, 1))
    cv.setLineWidth(1.5)
    for i in range(6):
        cv.line(inner[i][0], inner[i][1], inner[(i+1) % 6][0], inner[(i+1) % 6][1])


def _bridge_logo_rl(cv, cx, cy, scale=1.0):
    w = 60 * scale
    segs = 30
    for arc_offset, (rc, gc, bc), lw in [(0, (224, 225, 221), 1.5), (-10, (255, 183, 3), 1.0)]:
        cv.setStrokeColor(Color(rc/255, gc/255, bc/255))
        cv.setLineWidth(lw * scale)
        p = cv.beginPath()
        p.moveTo(cx - w, cy + arc_offset)
        for i in range(segs + 1):
            t = i / segs
            px = cx - w + t * w * 2
            py = cy + arc_offset - 30 * scale * ((t - 0.5) ** 2 - 0.25)
            p.lineTo(px, py)
        cv.drawPath(p, stroke=1, fill=0)
    cv.setFillColor(Color(1, 183/255, 3/255))
    cv.circle(cx, cy - 7 * scale, 4 * scale, stroke=0, fill=1)


def _draw_logo_rl(cv, cfg, cx, cy, scale=1.0):
    name = cfg.name
    if name == "Rock Brut":
        _hexagon_logo_rl(cv, cx, cy, 25 * scale)
    elif name == "Ponts & Lumiere":
        _bridge_logo_rl(cv, cx, cy, scale)
    elif name == "Neon Nights":
        pillar_neon_logo(cv, cx, cy, scale)
    elif name == "Sable & Bronze":
        pillar_sun_logo(cv, cx, cy, scale)
    else:
        reportlab_crest(cv, cx, cy, scale)


def _draw_logo_pil(draw, cfg, cx, cy, scale=1.0):
    name = cfg.name
    if name == "Fluid Wave":
        pillow_monogramme_wave(draw, cx, cy, scale)
    elif name == "Rock Brut":
        pillow_hexagon_monogramme(draw, cx, cy, scale)
    elif name == "Ponts & Lumiere":
        pillow_bridge_silhouette(draw, cx, cy, scale)
    elif name == "Neon Nights":
        pillow_neon_logo(draw, cx, cy, scale)
    elif name == "Sable & Bronze":
        pillow_sun_logo(draw, cx, cy, scale)
    else:
        pillow_crest(draw, cx, cy, scale)


# ── 1. Business card ──

def gen_businesscard(cfg, out_dir):
    from reportlab.lib.units import mm
    from reportlab.lib.colors import Color as _Color
    W, H = 85 * mm, 55 * mm
    pdf_dir = os.path.join(out_dir, "pdf")
    os.makedirs(pdf_dir, exist_ok=True)
    path = os.path.join(pdf_dir, "business-card.pdf")
    cv, trim_w, trim_h, bleed = create_bleed_canvas(path, W, H)

    if cfg.name == "Rock Brut":
        pdfmetrics.registerFont(TTFont("Anton", ANTON_PATH))
        cv.setFillColor(HexColor("#0A0A0A"))
        cv.rect(0, 0, W, H, stroke=0, fill=1)
        _draw_logo_rl(cv, cfg, 20 * mm, H / 2, 0.7)
        cv.setFillColor(Color(1, 1, 1))
        cv.setFont("Anton", 12)
        cv.drawString(32 * mm, H / 2 + 6, "RIVERS ROCK")
        cv.setFillColor(Color(1, 1, 1, alpha=0.4))
        cv.setFont("Anton", 6)
        cv.drawString(32 * mm, H / 2 - 6, "Reprises rock — Rouen")
        cv.drawString(32 * mm, H / 2 - 13, "riversrock_rouen@gmail.com")
    elif cfg.name in ("Ponts & Lumiere", "Fluid Wave"):
        c1 = HexColor("#0D1B2A" if cfg.name == "Ponts & Lumiere" else "#1A4A3A")
        c2 = HexColor("#1B263B" if cfg.name == "Ponts & Lumiere" else "#4A9B8E")
        for i in range(60):
            t = i / 59
            r = c1.red + (c2.red - c1.red) * t
            g = c1.green + (c2.green - c1.green) * t
            b = c1.blue + (c2.blue - c1.blue) * t
            cv.setFillColor(Color(r, g, b))
            cv.rect(0, i * H / 60, W, H / 60 + 0.5, stroke=0, fill=1)
        _draw_logo_rl(cv, cfg, 20 * mm, H / 2, 0.7)
        cv.setFillColor(Color(1, 1, 1))
        cv.setFont("BebasNeue", 14)
        cv.drawString(38 * mm, H / 2 + 8, "RIVERS ROCK")
        cv.setFont("Montserrat", 7)
        cv.drawString(38 * mm, H / 2 - 8, "Reprises rock — Rouen")
        cv.drawString(38 * mm, H / 2 - 18, "riversrock_rouen@gmail.com")
    else:
        c1, c2 = cfg.rl("bleu_seine"), cfg.rl("vert_eau")
        for i in range(60):
            t = i / 59
            r = c1.red + (c2.red - c1.red) * t
            g = c1.green + (c2.green - c1.green) * t
            b = c1.blue + (c2.blue - c1.blue) * t
            cv.setFillColor(Color(r, g, b))
            cv.rect(0, i * H / 60, W, H / 60 + 0.5, stroke=0, fill=1)
        _draw_logo_rl(cv, cfg, 20 * mm, H / 2, 0.7)
        cv.setFillColor(Color(1, 1, 1))
        cv.setFont("BebasNeue", 14)
        cv.drawString(38 * mm, H / 2 + 8, "RIVERS ROCK")
        cv.setFont("Montserrat", 7)
        cv.drawString(38 * mm, H / 2 - 8, "Reprises rock — Rouen")
        cv.drawString(38 * mm, H / 2 - 18, "riversrock_rouen@gmail.com")

    save_with_crop_marks(cv, trim_w, trim_h, bleed)
    print(f"  Business card → {path}")


# ── 2. Email signature ──

def gen_signature(cfg, out_dir):
    W, H = 600, 200
    tmp_dir = os.path.join(out_dir, "templates")
    os.makedirs(tmp_dir, exist_ok=True)
    path = os.path.join(tmp_dir, "email-signature.png")
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)

    c1_pil = cfg.pil("bleu_seine") if cfg.name not in ("Rock Brut", "Ponts & Lumiere") else (10, 10, 10)
    c2_pil = cfg.pil("vert_eau") if cfg.name not in ("Rock Brut", "Ponts & Lumiere") else (27, 38, 59)
    if cfg.name == "Rock Brut":
        c1_pil, c2_pil = (10, 10, 10), (30, 30, 35)
    elif cfg.name == "Ponts & Lumiere":
        c1_pil, c2_pil = (13, 27, 42), (27, 38, 59)
    elif cfg.name == "Fluid Wave":
        c1_pil, c2_pil = cfg.pil("vert_profond"), cfg.pil("vert_eau")

    for i in range(80):
        t = i / 79
        color = tuple(int(a + (b - a) * t) for a, b in zip(c1_pil, c2_pil))
        draw.rectangle([0, i * H / 80, W, (i + 1) * H / 80], fill=color)

    _draw_logo_pil(draw, cfg, 35, 75, 0.7)

    font_name = ImageFont.truetype(MONTSERRAT_PATH, 11)
    font_info = ImageFont.truetype(MONTSERRAT_PATH, 9)
    draw.text((62, 78), "[Nom]", fill=(255, 255, 255), font=font_name)
    draw.text((62, 95), "[Téléphone]", fill=(200, 200, 200), font=font_info)
    draw.text((62, 110), "[Email]", fill=(200, 200, 200), font=font_info)

    accent_pil = cfg.pil("accent") if cfg.name == "Scène & Vintage" else cfg.pil("accent")
    link = "riversrock.fr/setlist"
    font_link = ImageFont.truetype(MONTSERRAT_PATH, 8)
    bbox = draw.textbbox((0, 0), link, font=font_link)
    draw.text(((W - (bbox[2] - bbox[0])) / 2, 168), link, fill=accent_pil, font=font_link)
    draw.line([(0, 150), (W, 150)], fill=(255, 255, 255, 60), width=1)

    img.save(path)
    print(f"  Signature → {path}")


# ── 3. T-shirt mockup ──

def gen_tshirt_mockup(cfg, out_dir):
    mw, mh = 1200, 1600
    tmp_dir = os.path.join(out_dir, "templates")
    os.makedirs(tmp_dir, exist_ok=True)
    path = os.path.join(tmp_dir, "tshirt-mockup.png")
    img = Image.new("RGBA", (mw, mh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    NOIR, GRIS_F = (20, 20, 22), (35, 35, 38)
    cx, cy = mw / 2, 400
    tw, th = 700, 820
    rx, ry = cx - tw / 2, cy - th / 2

    def rounded_rect(d, x, y, w, h, r, fill):
        d.rectangle([x + r, y, x + w - r, y + h], fill=fill)
        d.rectangle([x, y + r, x + w, y + h - r], fill=fill)
        d.pieslice([x, y, x + r * 2, y + r * 2], 180, 270, fill=fill)
        d.pieslice([x + w - r * 2, y, x + w, y + r * 2], 270, 360, fill=fill)
        d.pieslice([x, y + h - r * 2, x + r * 2, y + h], 90, 180, fill=fill)
        d.pieslice([x + w - r * 2, y + h - r * 2, x + w, y + h], 0, 90, fill=fill)

    rounded_rect(draw, rx, ry, tw, th, 60, NOIR)
    for side in [-1, 1]:
        cx_e = cx + side * (tw * 0.36)
        y_e = ry + 30
        e_h = th * 0.65
        draw.rectangle([cx_e - tw * 0.1, y_e, cx_e + tw * 0.1, y_e + e_h], fill=NOIR)
        draw.ellipse([cx_e - tw * 0.1 - 5, y_e - 5, cx_e + tw * 0.1 + 5, y_e + 15], fill=NOIR)
        draw.ellipse([cx_e - tw * 0.1 - 5, y_e + e_h - 15, cx_e + tw * 0.1 + 5, y_e + e_h + 5], fill=NOIR)

    draw.ellipse([cx - 40, ry - 20, cx + 40, ry + 30], fill=GRIS_F)

    _draw_logo_pil(draw, cfg, mw / 2, cy - 20, 2.5)

    font_mont = ImageFont.truetype(MONTSERRAT_PATH, 18)
    draw.text((30, mh - 30), f"RIVERS ROCK — T-shirt ({cfg.name})", fill=(255, 255, 255, 80), font=font_mont)
    img.save(path)
    print(f"  Mockup → {path}")


# ── 4. Stage plot ──

def gen_stageplot(cfg, out_dir):
    W, H = landscape(A4)
    pdf_dir = os.path.join(out_dir, "pdf")
    os.makedirs(pdf_dir, exist_ok=True)
    path = os.path.join(pdf_dir, "stage-plot.pdf")
    cv, trim_w, trim_h, bleed = create_bleed_canvas(path, W, H)

    cv.setFillColor(Color(0, 0, 0, alpha=0.03))
    cv.rect(0, 0, W, H, stroke=0, fill=1)

    _draw_logo_rl(cv, cfg, 40, H - 40, 0.8)
    cv.setFillColor(Color(0, 0, 0, alpha=0.6))
    cv.setFont("BebasNeue", 22)
    cv.drawString(100, H - 50, "RIVERS ROCK — Stage Plot")
    cv.setFont("Montserrat", 10)
    cv.drawString(100, H - 70, "Contact: riversrock_rouen@gmail.com")

    sx, sy = 80, H - 200
    sw, sh = W - 160, 240
    cv.setStrokeColor(Color(0, 0, 0, alpha=0.3))
    cv.setLineWidth(1.5)
    cv.rect(sx, sy, sw, sh, stroke=1, fill=0)
    cv.setFont("Montserrat", 8)
    cv.drawCentredString(W / 2, sy - 15, "SCENE - vue de face (FACE)")

    stage_items = [
        (sx + sw * 0.5, sy + sh * 0.85, "Batterie", 40),    # centre-back
        (sx + sw * 0.2, sy + sh * 0.55, "Guitare", 25),      # left
        (sx + sw * 0.35, sy + sh * 0.65, "Guitare / chant", 25), # center-left
        (sx + sw * 0.65, sy + sh * 0.65, "Basse", 25),       # center-right
        (sx + sw * 0.8, sy + sh * 0.55, "Chant", 25),        # right
    ]
    for ix, iy, label, sz in stage_items:
        cv.setStrokeColor(Color(0, 0, 0, alpha=0.4))
        cv.setLineWidth(1)
        cv.circle(ix, iy, sz, stroke=1, fill=0)
        cv.setFont("Montserrat", 7)
        cv.drawCentredString(ix, iy - sz - 10, label)

    input_list = [
        ("1", "Batterie — Kick", "MIC", "Audix D6"),
        ("2", "Batterie — Snare", "MIC", "SM57"),
        ("3", "Batterie — OH", "MIC x2", "AKG C414"),
        ("4", "Basse", "DI", ""),
        ("5", "Guitare 1", "MIC", "SM57"),
        ("6", "Guitare 2", "MIC", "SM57"),
        ("7", "Chant", "MIC", "SM58"),
        ("8", "Choeurs", "MIC", "SM58"),
    ]
    ix0, iy0 = 80, sy - 100
    cv.setFont("Montserrat", 8)
    cv.drawString(ix0, iy0, "Input List")
    cv.setFont("Montserrat", 7)
    for row, (ch, src, mic, note) in enumerate(input_list):
        y = iy0 - 15 - row * 14
        cv.drawString(ix0, y, f"{ch}.")
        cv.drawString(ix0 + 20, y, src)
        cv.drawString(ix0 + 180, y, mic)
        cv.drawString(ix0 + 270, y, note)

    save_with_crop_marks(cv, trim_w, trim_h, bleed)
    print(f"  Stage plot → {path}")


# ── 5. Tech sheet ──

def gen_techsheet(cfg, out_dir):
    W, H = A4
    pdf_dir = os.path.join(out_dir, "pdf")
    os.makedirs(pdf_dir, exist_ok=True)
    path = os.path.join(pdf_dir, "t-shirt-techsheet.pdf")
    cv, trim_w, trim_h, bleed = create_bleed_canvas(path, W, H)

    cv.setFillColor(Color(0, 0, 0, alpha=0.04))
    cv.rect(0, 0, W, H, stroke=0, fill=1)

    _draw_logo_rl(cv, cfg, W / 2, H - 80, 0.8)
    cv.setFillColor(Color(0, 0, 0, alpha=0.6))
    cv.setFont("BebasNeue", 22)
    cv.drawCentredString(W / 2, H - 130, "RIVERS ROCK — Fiche technique sérigraphe")

    cv.setFont("Montserrat", 9)
    y = H - 170
    details = [
        f"Proposition : {cfg.name}",
        f"Logo : écusson / {cfg.tokens.get('badge_shape', 'circle')}",
        f"Couleur impression : Blanc + {cfg.colors.get('accent', ('#E85D3A',))[0]}",
        "Support : T-shirt noir 100% coton",
        "Placement : Centré poitrine, ~5 cm sous le col",
        "",
        "Tailles :",
    ]
    for line in details:
        cv.drawString(60, y, line)
        y -= 14

    sizes = [("S", 22), ("M", 28), ("L", 34), ("XL", 40)]
    cv.setFont("Montserrat", 8)
    for label, sr in sizes:
        cv.drawString(80, y, f"{label} : ∅{sr} mm")
        y -= 12

    cv.setFont("Montserrat", 7)
    cv.drawString(60, y - 10, f"Réf Pantone : {cfg.colors.get('accent', ('#E85D3A',))[0]} ≈ Pantone 172")

    save_with_crop_marks(cv, trim_w, trim_h, bleed)
    print(f"  Tech sheet → {path}")


# ── 6. Lyrics (12 PDFs) ──

def gen_lyrics(cfg, out_dir):
    W, H = A4
    pdf_dir = os.path.join(out_dir, "pdf", "lyrics")
    os.makedirs(pdf_dir, exist_ok=True)

    for idx, (artist, title) in enumerate(SETLIST):
        song_title = title or "(Instrumental)"
        safe_artist = artist.lower().replace(" ", "-").replace("/", "-")
        safe_title = song_title.lower().replace(" ", "-").replace("/", "-")
        path = os.path.join(pdf_dir, f"{idx+1:02d}-{safe_artist}-{safe_title}.pdf")
        cv, trim_w, trim_h, bleed = create_bleed_canvas(path, W, H)

        cv.setFillColor(Color(0, 0, 0, alpha=0.03))
        cv.rect(0, 0, W, H, stroke=0, fill=1)

        _draw_logo_rl(cv, cfg, W / 2, H - 60, 0.5)

        cv.setFillColor(Color(0, 0, 0, alpha=0.7))
        cv.setFont("BebasNeue", 22)
        cv.drawCentredString(W / 2, H - 120, artist)

        if title:
            cv.setFont("Montserrat", 14)
            cv.drawCentredString(W / 2, H - 150, title)

        lyrics = SAMPLE_LYRICS.get((artist, title), "Paroles à venir")
        cv.setFont("Montserrat", 10)
        lines = lyrics.split("\n")
        y = H - 200
        for line in lines:
            cv.drawCentredString(W / 2, y, line)
            y -= 16

        save_with_crop_marks(cv, trim_w, trim_h, bleed)
    print(f"  Lyrics → {pdf_dir}/ (12 fichiers)")


SAMPLE_LYRICS = {
    ("NIAGARA", "J'ai vu"): (
        "J'ai vu le ciel\n"
        "ouvert devant moi\n"
        "J'ai vu le temps\n"
        "qui passe et qui s'en va\n"
        "\n"
        "J'ai vu la mer\n"
        "qui danse sous la pluie\n"
        "J'ai vu l'enfer\n"
        "mais je n'ai pas compris\n"
        "\n"
        "J'ai vu\nJ'ai vu\n"
        "tout ce qu'il faut voir\n"
        "J'ai su\nJ'ai su\n"
        "garder l'espoir"
    ),
    ("AC/DC", "You shook me all night long"): (
        "She was a fast machine\n"
        "She kept her motor clean\n"
        "She was the best damn woman\n"
        "That I had ever seen\n"
        "\n"
        "She had the sightless eyes\n"
        "Telling me no lies\n"
        "Knockin' me out with those\n"
        "American thighs\n"
        "\n"
        "Taking more than her share\n"
        "Had me fighting for air\n"
        "She told me to come\n"
        "But I was already there\n"
        "\n"
        "'Cause the walls start shaking\n"
        "The earth was quaking\n"
        "My mind was aching\n"
        "And we were making it\n"
        "\n"
        "You shook me all night long\n"
        "You shook me all night long"
    ),
    ("DOLLY", "Je n'veux pas rester sage"): (
        "Je n'veux pas rester sage\n"
        "Je veux brûler les pages\n"
        "Et vivre sans image\n"
        "Sans aucun héritage\n"
        "\n"
        "Je n'veux pas faire comme eux\n"
        "Qui marchent sans orage\n"
        "Je veux briser la cage\n"
        "Et changer de visage\n"
        "\n"
        "Je n'veux pas rester sage\n"
        "Je veux vivre autrement\n"
        "Brûler tous les rivages\n"
        "Et partir dans le vent"
    ),
    ("THE PIXIES", "Where is my mind"): (
        "With your feet on the air and your head on the ground\n"
        "Try this trick and spin it, yeah\n"
        "Your head will collapse\n"
        "But there's nothing in it\n"
        "And you'll ask yourself\n"
        "\n"
        "Where is my mind\n"
        "Where is my mind\n"
        "Where is my mind\n"
        "\n"
        "Way out in the water\n"
        "See it swimmin'\n"
        "\n"
        "I was swimmin' in the Caribbean\n"
        "Animals were hiding behind the rock\n"
        "Except the little fish\n"
        "But they told me, he swears\n"
        "Tryin' to talk to me to me to me"
    ),
    ("PJ HARVEY", "Good fortune"): (
        "I've been trying to get good fortune\n"
        "I've been trying to get some luck\n"
        "But it seems to have deserted me\n"
        "Stuck in the muck\n"
        "\n"
        "I've been trying to get good fortune\n"
        "I've been trying to get a break\n"
        "There's too much static in my attic\n"
        "I'm about to break\n"
        "\n"
        "Good fortune, good fortune\n"
        "Won't you come my way\n"
        "Good fortune, good fortune\n"
        "I need you today\n"
        "\n"
        "I've been waiting in line so long\n"
        "I've been waiting for my turn\n"
        "But the queue keeps getting longer\n"
        "I've got so much to learn"
    ),
    ("BELLA CIAO", ""): (
        "Una mattina mi son svegliata\n"
        "O bella ciao, bella ciao, bella ciao ciao ciao\n"
        "Una mattina mi son svegliata\n"
        "e ho trovato l'invasor\n"
        "\n"
        "O partigiano, portami via\n"
        "O bella ciao, bella ciao, bella ciao ciao ciao\n"
        "O partigiano, portami via\n"
        "che mi sento di morir\n"
        "\n"
        "E se io muoio da partigiano\n"
        "O bella ciao, bella ciao, bella ciao ciao ciao\n"
        "E se io muoio da partigiano\n"
        "tu mi devi seppellir\n"
        "\n"
        "E seppellire lassù in montagna\n"
        "O bella ciao, bella ciao, bella ciao ciao ciao\n"
        "E seppellire lassù in montagna\n"
        "sotto l'ombra di un bel fior"
    ),
    ("SMASHING PUMPKINS", "Today"): (
        "Today is the greatest\n"
        "Day I've ever known\n"
        "Can't live for tomorrow\n"
        "Tomorrow's much too long\n"
        "\n"
        "I'll burn my eyes out\n"
        "Before I get out\n"
        "I wanted more\n"
        "Than life could ever grant me\n"
        "Bored by the chore\n"
        "Of saving face\n"
        "\n"
        "Today is the greatest\n"
        "Day I've ever known\n"
        "Can't wait for tomorrow\n"
        "I might not have that long\n"
        "\n"
        "I'll tear my heart out\n"
        "Before I get out\n"
        "Pink ribbon scars\n"
        "That never forget\n"
        "I tried so hard\n"
        "To cleanse these regrets\n"
        "My angel wings\n"
        "Were bruised and battered"
    ),
    ("RADIOHEAD", "Creep"): (
        "When you were here before\n"
        "Couldn't look you in the eye\n"
        "You're just like an angel\n"
        "Your skin makes me cry\n"
        "You float like a feather\n"
        "In a beautiful world\n"
        "I wish I was special\n"
        "You're so fuckin' special\n"
        "\n"
        "But I'm a creep\n"
        "I'm a weirdo\n"
        "What the hell am I doing here\n"
        "I don't belong here\n"
        "\n"
        "I don't care if it hurts\n"
        "I wanna have control\n"
        "I wanna a perfect body\n"
        "I wanna a perfect soul\n"
        "I wish I was special\n"
        "You're so fuckin' special\n"
        "\n"
        "But I'm a creep\n"
        "I'm a weirdo\n"
        "What the hell am I doing here\n"
        "I don't belong here\n"
        "\n"
        "She's running out again\n"
        "She's running out\n"
        "She's run run run running out\n"
        "\n"
        "Whatever makes you happy\n"
        "Whatever you want\n"
        "You're so fuckin' special\n"
        "I wish I was special\n"
        "But I'm a creep"
    ),
    ("DESIRELESS", "Voyage, voyage"): (
        "Au-dessus des vieux volcans\n"
        "Glisse des ailes sous les tapis du vent\n"
        "Voyage, voyage\n"
        "Plus loin que la nuit et le jour\n"
        "Voyage, voyage\n"
        "Dans l'espace inouï de l'amour\n"
        "\n"
        "Sur les fleuves de l'Amazonie\n"
        "Sur l'Océan Pacifique\n"
        "Voyage, voyage\n"
        "Du côté de la Mandchourie\n"
        "Sur les ailes de l'amour\n"
        "Voyage, voyage\n"
        "\n"
        "Sur les toits de Brooklyn le soir\n"
        "Voyage, voyage\n"
        "Dans les vagues de l'exil\n"
        "Voyage, voyage\n"
        "\n"
        "Au-dessus des capitales\n"
        "Des idées fatales\n"
        "Voyage, voyage\n"
        "Regarde l'océane\n"
        "Voyage, voyage"
    ),
    ("QUEEN", "We will rock you"): (
        "Buddy you're a boy make a big noise\n"
        "Playing in the street gonna be a big man someday\n"
        "You got mud on your face\n"
        "You big disgrace\n"
        "Kicking your can all over the place\n"
        "Singin'\n"
        "\n"
        "We will we will rock you\n"
        "We will we will rock you\n"
        "\n"
        "Buddy you're a young man hard man\n"
        "Shouting in the street gonna take on the world someday\n"
        "You got blood on your face\n"
        "You big disgrace\n"
        "Waving your banner all over the place\n"
        "\n"
        "We will we will rock you\n"
        "We will we will rock you\n"
        "\n"
        "Buddy you're an old man poor man\n"
        "Pleading with your eyes gonna make you some peace someday\n"
        "You got mud on your face\n"
        "You big disgrace\n"
        "Somebody better put you back into your place"
    ),
    ("ROLLING STONES", "Jumping jack flash"): (
        "I was born in a cross-fire hurricane\n"
        "And I howled at the morning driving rain\n"
        "But it's all right now, in fact it's a gas\n"
        "But it's all right, I'm Jumping Jack Flash\n"
        "It's a gas, gas, gas\n"
        "\n"
        "I was raised by a toothless, bearded hag\n"
        "I was schooled with a strap right across my back\n"
        "But it's all right now, in fact it's a gas\n"
        "But it's all right, I'm Jumping Jack Flash\n"
        "It's a gas, gas, gas\n"
        "\n"
        "I was drowned, I was washed up and left for dead\n"
        "I fell down to my feet and I saw they bled\n"
        "I frowned at the crumbs of a crust of bread\n"
        "Yeah, yeah, yeah\n"
        "\n"
        "I was crowned with a spike right through my head\n"
        "But it's all right now, in fact it's a gas\n"
        "But it's all right, I'm Jumping Jack Flash\n"
        "It's a gas, gas, gas"
    ),
    ("WHITE STRIPES", "Seven nation army"): (
        "I'm gonna fight 'em off\n"
        "A seven nation army couldn't hold me back\n"
        "They're gonna rip it off\n"
        "Taking their time right behind my back\n"
        "\n"
        "And I'm talking to myself at night\n"
        "Because I can't forget\n"
        "Back and forth through my mind\n"
        "Behind a cigarette\n"
        "\n"
        "And the message coming from my eyes\n"
        "Says leave it alone\n"
        "\n"
        "Don't want to hear about it\n"
        "Every single one's got a story to tell\n"
        "Everyone knows about it\n"
        "From the Queen of England to the hounds of hell\n"
        "\n"
        "And if I catch it coming back my way\n"
        "I'm gonna serve it to you\n"
        "And that ain't what you want to hear\n"
        "But that's what I'll do\n"
        "\n"
        "And the feeling coming from my bones\n"
        "Says find a home"
    ),
}


if __name__ == "__main__":
    # Register fonts
    pdfmetrics.registerFont(TTFont("BebasNeue", BEBAS_PATH))
    pdfmetrics.registerFont(TTFont("Montserrat", MONTSERRAT_PATH))

    for cfg, dirname in PROPS:
        base = os.path.join(os.path.dirname(__file__), "..", "propositions", dirname, "assets")
        print(f"--- {cfg.name} ---")
        gen_businesscard(cfg, base)
        gen_signature(cfg, base)
        gen_tshirt_mockup(cfg, base)
        gen_stageplot(cfg, base)
        gen_techsheet(cfg, base)
        gen_lyrics(cfg, base)
    print("\n✅ Missing assets générés pour les 5 propositions")
