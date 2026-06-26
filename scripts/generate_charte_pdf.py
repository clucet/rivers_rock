#!/usr/bin/env python3
"""Generate professional PDF chartes graphiques for all 14 propositions.
Each PDF (landscape A4, ~6 pages) includes: identity, palette, typography,
logo variants, generated assets, usage rules."""
import os, sys, math, io, re, tempfile
import cairosvg
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image
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
    BANGERS_PATH, CINZELDECO_PATH, OSWALD_PATH, SOURCESANS_PATH, DMSANS_PATH,
)
from palette import BASE, FLUID_WAVE, ROCK_BRUT, SCENE_VINTAGE, PONTS_LUMIERE
from palette import NEON_NIGHTS, SABLE_BRONZE, NORDIK, GRUNGE, JAZZ_CLUB
from palette import BITUME, CORDES_VOIX, HERITAGE, RUBICON, MINUIT

PROPS = [
    (BASE, "00-originale"),
    (FLUID_WAVE, "01-fluid-wave"),
    (ROCK_BRUT, "02-rock-brut"),
    (SCENE_VINTAGE, "03-scene-vintage"),
    (PONTS_LUMIERE, "04-ponts-lumiere"),
    (NEON_NIGHTS, "05-neon-nights"),
    (SABLE_BRONZE, "06-sable-bronze"),
    (NORDIK, "07-nordik"),
    (GRUNGE, "08-grunge"),
    (JAZZ_CLUB, "09-jazz-club"),
    (BITUME, "10-bitume"),
    (CORDES_VOIX, "11-cordes-voix"),
    (HERITAGE, "12-heritage"),
    (RUBICON, "13-rubicon"),
    (MINUIT, "14-minuit"),
]

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "propositions")

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
    "blanc_ivoire": "Blanc ivoire", "bitume": "Bitume", "beton": "Béton",
    "fluo": "Jaune fluo", "brique": "Brique", "craie": "Craie",
    "creme": "Crème", "acajou": "Acajou", "ambre_doux": "Ambre doux",
    "foret": "Forêt", "noir_doux": "Noir doux",
    "vitrail": "Bleu vitrail", "or_feuille": "Or feuille", "colombage": "Colombage",
    "pierre": "Pierre", "parchemin": "Parchemin",
    "route": "Orange route", "ciel": "Bleu ciel", "poussiere": "Poussière",
    "pin": "Vert pin",
    "velours": "Noir velours", "bordeaux": "Bordeaux", "or_bruni": "Or bruni",
    "ivoire": "Ivoire", "perle": "Gris perle",
}


def get_font_for_role(cfg):
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
            path = BEBAS_PATH
        paths[role] = path
    return paths


def draw_page_bg(cv, W, H, cfg):
    """Draw background and header/footer for each page."""
    bg_hex = cfg.get("blanc_casse", "#F5F5F0")
    accent_hex = cfg.get("accent", "#E85D3A")
    try:
        bg = HexColor(bg_hex)
    except:
        bg = Color(0.95, 0.95, 0.95)
    cv.setFillColor(bg)
    cv.rect(0, 0, W, H, stroke=0, fill=1)
    # Accent top bar
    try:
        a = HexColor(accent_hex)
        cv.setFillColor(a)
        cv.rect(0, H - 4, W, 4, stroke=0, fill=1)
    except:
        pass


def draw_footer(cv, W, H, page_num, total_pages, cfg):
    """Draw page number and document reference in footer."""
    cv.setFillColor(Color(0, 0, 0, alpha=0.15))
    cv.setFont("Helvetica", 7)
    cv.drawString(40, 18, f"CHARTE GRAPHIQUE — {cfg.name} — Rivers Rock")
    cv.drawRightString(W - 40, 18, f"{page_num}/{total_pages}")
    cv.setStrokeColor(Color(0, 0, 0, alpha=0.06))
    cv.setLineWidth(0.5)
    cv.line(40, 28, W - 40, 28)


def generate_charte(cfg, dirname):
    prop_dir = os.path.join(OUT_DIR, dirname)
    out_path = os.path.join(prop_dir, f"charte-graphique-{dirname}.pdf")
    pdf_dir = os.path.join(prop_dir, "pdf")
    os.makedirs(pdf_dir, exist_ok=True)

    W, H = landscape(A4)
    cv = rlcanvas.Canvas(out_path, pagesize=(W, H))
    colors = cfg.colors
    font_paths = get_font_for_role(cfg)
    TOTAL = 5

    # ── Page 1: Identity + Palette ──
    draw_page_bg(cv, W, H, cfg)
    accent_hex = cfg.get("accent", "#E85D3A")
    try:
        cv.setFillColor(HexColor(accent_hex))
    except:
        cv.setFillColor(HexColor("#2B2B2B"))
    cv.setFont("Helvetica", 28)
    cv.drawString(40, H - 50, "CHARTE GRAPHIQUE")
    cv.setFillColor(HexColor("#2B2B2B"))
    cv.setFont("Helvetica", 16)
    cv.drawString(40, H - 75, cfg.name + " — Rivers Rock")

    y_start = H - 130
    x_start = 40
    swatch_size = 30
    row, col = 0, 0
    cv.setFont("Helvetica", 9)
    for name, (hex_val, pil_val) in colors.items():
        if name.startswith("_"):
            continue
        x = x_start + col * (swatch_size + 50 + 80)
        y = y_start - row * (swatch_size + 30)
        try:
            cv.setFillColor(HexColor(hex_val))
        except:
            cv.setFillColor(Color(0.5, 0.5, 0.5))
        cv.rect(x, y - swatch_size, swatch_size, swatch_size, stroke=0, fill=1)
        cv.setStrokeColor(Color(0, 0, 0, alpha=0.1))
        cv.setLineWidth(0.5)
        cv.rect(x, y - swatch_size, swatch_size, swatch_size, stroke=1, fill=0)
        display_name = COLOR_NAMES.get(name, name)
        cv.setFillColor(HexColor("#2B2B2B"))
        cv.setFont("Helvetica", 7)
        cv.drawString(x + swatch_size + 5, y - 8, display_name)
        cv.drawString(x + swatch_size + 5, y - 18, hex_val)
        col += 1
        if col > 2:
            col = 0
            row += 1

    # WCAG contrast info on page 1
    from palette import contrast_ratio
    try:
        items = [(n, v[0]) for n, v in colors.items() if not n.startswith("_")]
        worst = 100.0
        best = 0.0
        for i, (n1, h1) in enumerate(items[:10]):
            for n2, h2 in items[i+1:i+4]:
                r = contrast_ratio(h1, h2)
                worst = min(worst, r)
                best = max(best, r)
        cv.setFillColor(HexColor("#2B2B2B"))
        cv.setFont("Helvetica", 7)
        cv.drawString(40, y - 40, f"Contrastes WCAG : min {worst:.1f}:1 / max {best:.1f}:1 (AA small=4.5:1)")
    except:
        pass

    draw_footer(cv, W, H, 1, TOTAL, cfg)

    # ── Page 2: Typography ──
    cv.showPage()
    draw_page_bg(cv, W, H, cfg)
    cv.setFillColor(HexColor("#2B2B2B"))
    cv.setFont("Helvetica", 22)
    cv.drawString(40, H - 50, "TYPOGRAPHIE")
    y = H - 100
    for role, fpath in font_paths.items():
        try:
            sz = 9 if role in ("body", "data") else 14
            pdfmetrics.registerFont(TTFont("Charte_" + role, fpath))
            cv.setFont("Charte_" + role, sz)
        except:
            cv.setFont("Helvetica", sz)
        font_name = cfg.fonts.get(role, "?")
        cv.setFillColor(HexColor("#2B2B2B"))
        cv.setFont("Helvetica", 9)
        cv.drawString(40, y, role.upper() + ": " + font_name)
        try:
            cv.setFont("Charte_" + role, sz)
            cv.drawString(40, y - 22, "ABCDEFGHIJKLM abcdefghijklm 0123456789")
        except:
            cv.setFont("Helvetica", sz)
            cv.drawString(40, y - 22, "ABCDEFGHIJKLM abcdefghijklm 0123456789")
        y -= 60
    draw_footer(cv, W, H, 2, TOTAL, cfg)

    # ── Page 3: Logo variants ──
    cv.showPage()
    draw_page_bg(cv, W, H, cfg)
    cv.setFillColor(HexColor("#2B2B2B"))
    cv.setFont("Helvetica", 22)
    cv.drawString(40, H - 50, "LOGOS & VARIANTES")
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
            with open(svg_path, "r") as f:
                svg_content = f.read()
            vb_match = re.search(r'viewBox="([^"]+)"', svg_content)
            vb = vb_match.group(1) if vb_match else "0 0 100 100"
            vb_parts = list(map(float, vb.split()))
            svg_w, svg_h = vb_parts[2], vb_parts[3]
            aspect = svg_h / svg_w if svg_w > 0 else 1
            display_w = min(140, (W - 80) / 3)
            display_h = display_w * aspect
            try:
                png_data = cairosvg.svg2png(url=svg_path, output_width=int(display_w * 3))
                img = Image.open(io.BytesIO(png_data))
                tmp_path = "/tmp/charte_" + dirname + "_" + fname.replace('.svg', '') + ".png"
                img.save(tmp_path)
                cv.drawImage(tmp_path, x, y - display_h, display_w, display_h)
                os.remove(tmp_path)
            except Exception as e:
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
    draw_footer(cv, W, H, 3, TOTAL, cfg)

    # ── Page 4: Generated assets ──
    cv.showPage()
    draw_page_bg(cv, W, H, cfg)
    cv.setFillColor(HexColor("#2B2B2B"))
    cv.setFont("Helvetica", 22)
    cv.drawString(40, H - 50, "ASSETS GÉNÉRÉS")
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
        cv.drawString(40, y, "  " + f + "  (" + str(size // 1024) + " Ko)")
        y -= 16
    # Template thumbnails in 2-col grid
    tmpl_dir = os.path.join(prop_dir, "assets", "templates")
    if os.path.exists(tmpl_dir):
        cv.drawString(40, y - 10, "Templates :")
        y -= 26
        preview_keys = ["avatar.png", "instagram-post.png", "instagram-story.png",
                        "facebook-banner.png", "youtube-banner.png"]
        preview_files = []
        for key in preview_keys:
            tp = os.path.join(tmpl_dir, key)
            if os.path.exists(tp):
                preview_files.append(tp)
        tx, ty = 40, y
        for idx, pf in enumerate(preview_files):
            try:
                img = Image.open(pf)
                iw, ih = img.size
                ratio = 60 / ih
                dw, dh = int(iw * ratio), 60
                if dw > 110:
                    ratio = 110 / iw
                    dw, dh = 110, int(ih * ratio)
                cv.drawImage(pf, tx, ty - dh, dw, dh)
                cv.setFillColor(HexColor("#2B2B2B"))
                cv.setFont("Helvetica", 6)
                cv.drawString(tx, ty - dh - 10, os.path.basename(pf))
                tx += dw + 15
                if (idx + 1) % 3 == 0:
                    tx = 40
                    ty -= 90
            except:
                pass
    draw_footer(cv, W, H, 4, TOTAL, cfg)

    # ── Page 5: Usage rules ──
    cv.showPage()
    draw_page_bg(cv, W, H, cfg)
    cv.setFillColor(HexColor("#2B2B2B"))
    cv.setFont("Helvetica", 22)
    cv.drawString(40, H - 50, "RÈGLES D'USAGE DU LOGO")
    rules = [
        ("Ne pas déformer", "Le logo ne doit jamais être étiré, compressé ou tordu. Utiliser toujours le fichier SVG source."),
        ("Ne pas recolorier", "Les couleurs du logo sont fixes, sauf pour la version monochrome dédiée."),
        ("Ne pas pivoter", "Le logo ne doit pas être incliné ou retourné."),
        ("Pas d'effets ajoutés", "Pas d'ombres portées, dégradés ou contours non prévus dans la charte."),
        ("Taille minimale", "Icône seule : ∅30px écran / 10mm print. Logo complet : 60px écran / 20mm print."),
        ("Fonds interdits", "Ne pas placer le logo sur des fonds dont le contraste < 3:1 (WCAG AA)."),
    ]
    cv.setFont("Helvetica", 9)
    y = H - 110
    for title, desc in rules:
        cv.setFillColor(HexColor("#2B2B2B"))
        cv.setFont("Helvetica-Bold", 10)
        cv.drawString(40, y, title)
        cv.setFont("Helvetica", 8)
        cv.drawString(40, y - 16, desc)
        y -= 45
    # Proposition accent color
    first_color = list(cfg.colors.values())[0][0]
    try:
        c = HexColor(first_color)
        cv.setFillColor(c)
        cv.setFont("Helvetica", 9)
        cv.drawString(40, y - 10, "Couleur accent : " + first_color)
    except:
        pass
    # WCAG computed ratios
    from palette import contrast_ratio, print_wcag_report
    cv.setFillColor(HexColor("#2B2B2B"))
    cv.setFont("Helvetica-Bold", 9)
    cv.drawString(40, y - 35, "Contrastes WCAG AA :")
    cv.setFont("Helvetica", 7)
    y2 = y - 52
    try:
        items = [(n, v[0]) for n, v in cfg.colors.items() if not n.startswith("_")]
        count = 0
        for i, (n1, h1) in enumerate(items):
            for n2, h2 in items[i+1:]:
                if count > 8:
                    break
                r = contrast_ratio(h1, h2)
                status = "✅" if r >= 4.5 else ("⚠️" if r >= 3.0 else "❌")
                label1 = COLOR_NAMES.get(n1, n1)
                label2 = COLOR_NAMES.get(n2, n2)
                cv.drawString(40, y2, "  " + status + " " + label1 + " / " + label2 + " = " + f"{r:.1f}" + ":1")
                y2 -= 11
                count += 1
    except:
        pass
    draw_footer(cv, W, H, 5, TOTAL, cfg)

    cv.save()
    print(f"  Charte PDF : {out_path}")


if __name__ == "__main__":
    print("Génération des chartes graphiques PDF...")
    for cfg, dirname in PROPS:
        generate_charte(cfg, dirname)
    print(f"\n✅ {len(PROPS)} chartes PDF générées")
