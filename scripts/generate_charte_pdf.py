#!/usr/bin/env python3
"""Generate professional PDF chartes graphiques for all 9 propositions.
Each PDF includes: logo, palette, typography, logo variants, graphic elements, and asset previews."""

import os, sys, math, io, re, tempfile
import cairosvg
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib.colors import Color, HexColor
from reportlab.pdfgen import canvas as rlcanvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from logoutils import (
    BEBAS_PATH, MONTSERRAT_PATH, ANTON_PATH, SPACE_MONO_PATH,
    NUNITO_PATH, INTERTIGHT_PATH, JETBRAINS_PATH,
    ORBITRON_PATH, RAJDHANI_PATH, CINZEL_PATH, LATO_PATH,
    TEKO_PATH, RALEWAY_PATH, DMMONO_PATH,
    KARLA_PATH, RUBIK_PATH, SYNEMONO_PATH, INTER_PATH, CORMORANT_PATH,
)
from palette import BASE, FLUID_WAVE, ROCK_BRUT, SCENE_VINTAGE, PONTS_LUMIERE, NEON_NIGHTS, SABLE_BRONZE, NORDIK, GRUNGE, JAZZ_CLUB
from palette import BITUME, CORDES_VOIX, HERITAGE, RUBICON, MINUIT

PROPS = [
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

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "propositions")

# Colors name mapping for display
COLOR_NAMES = {
    "vert_profond": "Vert profond", "vert_eau": "Vert d'eau", "ambre": "Ambre",
    "accent": "Accent", "vert_repere": "Vert repère", "gris_acier": "Gris acier",
    "blanc_casse": "Blanc cassé", "blanc": "Blanc",
    "noir": "Noir", "noir_profond": "Noir", "vert_accent": "Vert accent",
    "gris_fonce": "Gris foncé", "bleu_seine": "Bleu Seine",
    "teal_profond": "Teal profond", "terracotta": "Terracotta",
    "or_vieilli": "Or vieilli", "nuit": "Nuit", "acier": "Acier",
    "lumiere": "Lumière", "seine": "Seine", "brouillard": "Brouillard",
    "nuit_profonde": "Nuit profonde", "rose_neon": "Rose néon",
    "cyan": "Cyan", "violet_fonce": "Violet foncé", "blanc_bleute": "Blanc bleuté",
    "sable": "Sable", "terre_cuite": "Terre cuite", "bronze": "Bronze",
    "vert_palmier": "Vert palmier", "creme": "Crème",
    "blanc_pur": "Blanc pur", "gris_nuage": "Gris nuage",
    "gris_ardoise": "Gris ardoise", "noir_doux": "Noir doux", "accent_lin": "Accent lin",
    "papier": "Papier", "toner": "Toner", "marqueur": "Marqueur",
    "correcteur": "Correcteur", "agrafes": "Agrafes",
    "or_bruni": "Or bruni", "cuivre": "Cuivre", "rouge_velours": "Rouge velours",
    "blanc_ivoire": "Blanc ivoire",
}


def get_font_for_role(cfg):
    """Return a TTF path for a font role."""
    from logoutils import _find_font
    from palette import font_filename
    role_map = {"hero": cfg.fonts.get("hero", "Montserrat"),
                "logo": cfg.fonts.get("logo", "BebasNeue"),
                "body": cfg.fonts.get("body", "Montserrat"),
                "data": cfg.fonts.get("data", "Montserrat")}
    paths = {}
    for role, name in role_map.items():
        fname = font_filename(role, cfg)
        path = _find_font(fname)
        if not path:
            path = BEBAS_PATH  # fallback
        paths[role] = path
    return paths


def generate_charte(cfg, dirname):
    """Generate a multi-page PDF charte for one proposition."""
    prop_dir = os.path.join(OUT_DIR, dirname)
    out_path = os.path.join(prop_dir, f"charte-graphique-{dirname}.pdf")
    pdf_dir = os.path.join(prop_dir, "pdf")
    os.makedirs(pdf_dir, exist_ok=True)

    W, H = landscape(A4)
    cv = rlcanvas.Canvas(out_path, pagesize=(W, H))

    # Colors for this proposition
    colors = cfg.colors
    font_paths = get_font_for_role(cfg)

    # ── Page 1: Identity + Palette ──
    # Background
    cv.setFillColor(Color(0.95, 0.95, 0.95))
    cv.rect(0, 0, W, H, stroke=0, fill=1)

    # Title
    cv.setFillColor(HexColor("#2B2B2B"))
    cv.setFont("Helvetica", 28)
    cv.drawString(40, H - 50, f"CHARTE GRAPHIQUE")
    cv.setFont("Helvetica", 16)
    cv.drawString(40, H - 75, f"{cfg.name} — Rivers Rock")

    # Palette swatches
    y_start = H - 130
    x_start = 40
    swatch_size = 30
    row = 0
    col = 0

    cv.setFont("Helvetica", 9)
    for name, (hex_val, pil_val) in colors.items():
        if name.startswith("_"):
            continue
        x = x_start + col * (swatch_size + 50 + 80)
        y = y_start - row * (swatch_size + 30)

        # Color swatch
        try:
            c = HexColor(hex_val)
            cv.setFillColor(c)
        except:
            cv.setFillColor(Color(0.5, 0.5, 0.5))
        cv.rect(x, y - swatch_size, swatch_size, swatch_size, stroke=0, fill=1)
        cv.setStrokeColor(Color(0, 0, 0, alpha=0.1))
        cv.setLineWidth(0.5)
        cv.rect(x, y - swatch_size, swatch_size, swatch_size, stroke=1, fill=0)

        # Color name + hex
        display_name = COLOR_NAMES.get(name, name)
        cv.setFillColor(HexColor("#2B2B2B"))
        cv.setFont("Helvetica", 7)
        cv.drawString(x + swatch_size + 5, y - 8, display_name)
        cv.drawString(x + swatch_size + 5, y - 18, hex_val)

        col += 1
        if col > 2:
            col = 0
            row += 1

    # ── Page 2: Typography ──
    cv.showPage()
    cv.setFillColor(Color(0.95, 0.95, 0.95))
    cv.rect(0, 0, W, H, stroke=0, fill=1)

    cv.setFillColor(HexColor("#2B2B2B"))
    cv.setFont("Helvetica", 22)
    cv.drawString(40, H - 50, "TYPOGRAPHIE")

    y = H - 100
    for role, fpath in font_paths.items():
        try:
            sz = 9 if role in ("body", "data") else 14
            pdfmetrics.registerFont(TTFont(f"Charte_{role}", fpath))
            cv.setFont(f"Charte_{role}", sz)
        except:
            cv.setFont("Helvetica", sz)

        font_name = cfg.fonts.get(role, "?")
        cv.setFillColor(HexColor("#2B2B2B"))
        cv.setFont("Helvetica", 9)
        cv.drawString(40, y, f"{role.upper()}: {font_name}")
        try:
            cv.setFont(f"Charte_{role}", sz)
            cv.drawString(40, y - 22, f"ABCDEFGHIJKLM abcdefghijklm 0123456789")
        except:
            cv.setFont("Helvetica", sz)
            cv.drawString(40, y - 22, f"ABCDEFGHIJKLM abcdefghijklm 0123456789")
        y -= 60

    # ── Page 3: Logo variants ──
    cv.showPage()
    cv.setFillColor(Color(0.95, 0.95, 0.95))
    cv.rect(0, 0, W, H, stroke=0, fill=1)

    cv.setFillColor(HexColor("#2B2B2B"))
    cv.setFont("Helvetica", 22)
    cv.drawString(40, H - 50, "LOGOS & VARIANTES")

    # Render SVG logos using cairosvg
    svg_dir = os.path.join(prop_dir, "assets")
    logo_variants = [
        ("logo.svg", "Standard couleur"),
        ("logo-mono.svg", "Monochrome"),
        ("logo-icon.svg", "Icône seule"),
        ("logo-compact.svg", "Compact"),
        ("logo-watermark.svg", "Watermark"),
    ]

    x, y = 40, H - 120
    for fname, label in logo_variants:
        svg_path = os.path.join(svg_dir, fname)
        if os.path.exists(svg_path):
            # Get SVG viewBox for aspect ratio
            with open(svg_path, "r") as f:
                svg_content = f.read()
            vb_match = re.search(r'viewBox="([^"]+)"', svg_content)
            vb = vb_match.group(1) if vb_match else "0 0 100 100"
            vb_parts = list(map(float, vb.split()))
            svg_w, svg_h = vb_parts[2], vb_parts[3]
            aspect = svg_h / svg_w if svg_w > 0 else 1

            display_w = min(140, (W - 80) / 3)
            display_h = display_w * aspect

            # Convert SVG to PNG via cairosvg
            try:
                png_data = cairosvg.svg2png(url=svg_path, output_width=int(display_w * 3))
                img = Image.open(io.BytesIO(png_data))
                tmp_path = f"/tmp/charte_{dirname}_{fname.replace('.svg','')}.png"
                img.save(tmp_path)

                cv.drawImage(tmp_path, x, y - display_h, display_w, display_h)
                os.remove(tmp_path)
            except Exception as e:
                # Fallback: draw placeholder
                cv.setStrokeColor(Color(0, 0, 0, alpha=0.08))
                cv.setLineWidth(0.5)
                cv.rect(x, y - display_h, display_w, display_h, stroke=1, fill=0)

            cv.setFillColor(HexColor("#2B2B2B"))
            cv.setFont("Helvetica", 7)
            cv.drawString(x, y - display_h - 12, label)
            cv.drawString(x, y - display_h - 21, fname)

            x += display_w + 25
            if x > W - 100:
                x = 40
                y -= max(display_h + 30, 90)

    # ── Page 4: Éléments graphiques + Assets aperçu ──
    cv.showPage()
    cv.setFillColor(Color(0.95, 0.95, 0.95))
    cv.rect(0, 0, W, H, stroke=0, fill=1)

    cv.setFillColor(HexColor("#2B2B2B"))
    cv.setFont("Helvetica", 22)
    cv.drawString(40, H - 50, "ASSETS GÉNÉRÉS")

    # List the generated PDFs in pdf/
    pdf_files = []
    if os.path.exists(pdf_dir):
        for f in sorted(os.listdir(pdf_dir)):
            if f.endswith(".pdf"):
                pdf_files.append(f)

    cv.setFont("Helvetica", 9)
    y = H - 100
    for f in pdf_files[:20]:
        fpath = os.path.join(pdf_dir, f)
        size = os.path.getsize(fpath) if os.path.exists(fpath) else 0
        cv.drawString(40, y, f"  {f}  ({size // 1024} Ko)")
        y -= 16

    # Template thumbnails
    tmpl_dir = os.path.join(prop_dir, "assets", "templates")
    if os.path.exists(tmpl_dir):
        cv.drawString(40, y - 10, "Templates :")
        y -= 26
        # Show key templates as small thumbnails
        preview_files = []
        for key in ["avatar.png", "instagram-post.png", "instagram-story.png", "facebook-banner.png", "youtube-banner.png", "lowerthird.png"]:
            tp = os.path.join(tmpl_dir, key)
            if os.path.exists(tp):
                preview_files.append(tp)

        tx, ty = 40, y
        for pf in preview_files[:3]:
            try:
                img = Image.open(pf)
                iw, ih = img.size
                # Scale to fit ~80px height
                ratio = 80 / ih
                dw, dh = int(iw * ratio), 80
                if dw > 150:
                    ratio = 150 / iw
                    dw, dh = 150, int(ih * ratio)
                cv.drawImage(pf, tx, ty - dh, dw, dh)
                tx += dw + 15
            except:
                pass
        
        y2 = ty - 95
        cv.setFont("Helvetica", 7)
        for f in sorted(os.listdir(tmpl_dir))[:8]:
            cv.drawString(40, y2, f"  {f}")
            y2 -= 12

    cv.save()
    print(f"  Charte PDF : {out_path}")


if __name__ == "__main__":
    print("Génération des chartes graphiques PDF...")
    for cfg, dirname in PROPS:
        generate_charte(cfg, dirname)
    print("\n✅ {len(PROPS)} chartes PDF générées")
