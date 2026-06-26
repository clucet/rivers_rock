#!/usr/bin/env python3
"""Generate preview.html per proposition with logo variants, palette, typography,
animated logo iframe, PDF thumbnails, and charte download link.
Also updates propositions/index.html with Apercu links.

Usage: python3 scripts/generate_preview.py [--skip-thumbs]
"""

import os, sys, io, re, base64, subprocess, zipfile, glob as globmod

sys.path.insert(0, os.path.dirname(__file__))
from palette import FLUID_WAVE, ROCK_BRUT, SCENE_VINTAGE, PONTS_LUMIERE, NEON_NIGHTS, SABLE_BRONZE, NORDIK, GRUNGE, JAZZ_CLUB
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

COLOR_NAMES = {
    "vert_profond": "Vert profond", "vert_eau": "Vert d'eau", "ambre": "Ambre",
    "accent": "Accent", "vert_repere": "Vert repère", "gris_acier": "Gris acier",
    "blanc_casse": "Blanc cassé", "blanc": "Blanc",
    "noir": "Noir", "vert_accent": "Vert accent",
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

FLAG_LABELS = {
    "use_grain": "Grain overlay",
    "use_halftone": "Halftone dots",
    "use_flare": "Lens flares",
    "use_or_wave": "Sinusoidal wave",
    "use_duotone": "Duotone filter",
    "use_glow": "Neon glow",
    "use_timbre": "Timbre stamp",
}

FONT_LABELS = {
    "BebasNeue": "Bebas Neue",
    "Anton": "Anton",
    "Montserrat": "Montserrat",
    "SpaceMono": "Space Mono",
    "PlayfairDisplay": "Playfair Display",
    "Nunito": "Nunito",
    "InterTight": "Inter Tight",
    "JetBrainsMono": "JetBrains Mono",
    "Teko": "Teko",
    "Raleway": "Raleway",
    "DMMono": "DM Mono",
    "Orbitron": "Orbitron",
    "Rajdhani": "Rajdhani",
    "Cinzel": "Cinzel",
    "Lato": "Lato",
    "Cormorant": "Cormorant",
    "Inter": "Inter",
    "RubikGlitch": "Rubik Glitch",
    "SyneMono": "Syne Mono",
    "Karla": "Karla",
}


def slug(name):
    return name.lower().replace(" &", "").replace(" ", "-")


def read_file(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return ""


def svg_to_data_uri(svg_content):
    b64 = base64.b64encode(svg_content.encode("utf-8")).decode()
    return f"data:image/svg+xml;base64,{b64}"


def generate_pdf_thumbnail(pdf_path):
    thumb_path = pdf_path.replace(".pdf", "-preview.png")
    if os.path.exists(thumb_path):
        return thumb_path
    try:
        stem = pdf_path.replace(".pdf", "-preview")
        subprocess.run(
            ["pdftoppm", "-png", "-f", "1", "-l", "1", "-scale-to", "240",
             pdf_path, stem],
            capture_output=True, timeout=30
        )
        # pdftoppm appends -1.png for first page
        paged = stem + "-1.png"
        if os.path.exists(paged):
            os.rename(paged, thumb_path)
        if os.path.exists(thumb_path):
            return thumb_path
    except Exception:
        pass
    return None


def generate_preview(cfg, dirname):
    prop_dir = os.path.join(OUT_DIR, dirname)
    assets_dir = os.path.join(prop_dir, "assets")
    pdf_dir = os.path.join(assets_dir, "pdf")
    tmpl_dir = os.path.join(assets_dir, "templates")

    logo_variants = []
    for fname in ["logo.svg", "logo-mono.svg", "logo-icon.svg", "logo-compact.svg", "logo-watermark.svg"]:
        svg_path = os.path.join(assets_dir, fname)
        content = read_file(svg_path)
        label = {
            "logo.svg": "Standard",
            "logo-mono.svg": "Monochrome",
            "logo-icon.svg": "Icône",
            "logo-compact.svg": "Compact",
            "logo-watermark.svg": "Watermark",
        }.get(fname, fname)
        logo_variants.append((label, fname, content))

    # Animated logo
    animated_path = os.path.join(tmpl_dir, f"logo-animated-{slug(cfg.name)}.html")
    if not os.path.exists(animated_path):
        animated_path = os.path.join(tmpl_dir, f"logo-animated-{dirname.split('-',1)[1]}.html")
    has_animated = os.path.exists(animated_path)

    # Colors
    color_items = []
    for name, (hex_val, _) in cfg.colors.items():
        if name.startswith("_"):
            continue
        display = COLOR_NAMES.get(name, name)
        color_items.append((display, hex_val))

    # Fonts
    font_items = []
    for role in ["hero", "logo", "body", "badge", "song", "data", "accent", "quote"]:
        fname = cfg.fonts.get(role)
        if fname:
            label = FONT_LABELS.get(fname, fname)
            font_items.append((role.upper(), label))

    # Flags
    active_flags = [FLAG_LABELS.get(k, k) for k, v in cfg.flags.items() if v]

    # PDFs
    pdf_files = []
    if os.path.exists(pdf_dir):
        for f in sorted(os.listdir(pdf_dir)):
            if f.endswith(".pdf"):
                fpath = os.path.join(pdf_dir, f)
                pdf_files.append((f, fpath))

    # PNG templates for thumbnails
    template_thumbs = []
    if os.path.exists(tmpl_dir):
        for f in sorted(os.listdir(tmpl_dir)):
            if f.endswith(".png") and not f.startswith("watermark"):
                tp = os.path.join(tmpl_dir, f)
                template_thumbs.append((f, tp))

    # Charte PDF
    charte_pdf = os.path.join(prop_dir, f"charte-graphique-{dirname}.pdf")
    has_charte = os.path.exists(charte_pdf)

    # First color for accent
    first_hex = list(cfg.colors.values())[0][0] if cfg.colors else "#333333"
    first_rgb = tuple(int(first_hex.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))

    logo_section = ""
    for label, fname, content in logo_variants:
        if content:
            uri = svg_to_data_uri(content)
            logo_section += f'''
        <div class="logo-card">
          <div class="logo-frame"><img src="{uri}" alt="{label}"></div>
          <div class="logo-label">{label}</div>
          <div class="logo-fname">{fname}</div>
        </div>'''
        else:
            logo_section += f'''
        <div class="logo-card missing">
          <div class="logo-frame"><span class="missing-icon">—</span></div>
          <div class="logo-label">{label}</div>
          <div class="logo-fname">{fname}</div>
        </div>'''

    palette_section = ""
    for display, hex_val in color_items:
        try:
            h = hex_val.lstrip("#")
            r, g, b = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
            lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            text_color = "#1a1a1a" if lum > 0.5 else "#f0f0f0"
        except:
            text_color = "#fff"
        palette_section += f'''
        <div class="swatch" style="background:{hex_val}">
          <div class="swatch-info" style="color:{text_color}">
            <span class="swatch-name">{display}</span>
            <span class="swatch-hex">{hex_val}</span>
          </div>
        </div>'''

    font_section = ""
    for role, label in font_items:
        font_section += f'''
        <div class="font-row">
          <div class="font-role">{role}</div>
          <div class="font-name">{label}</div>
          <div class="font-specimen" style="font-family:'{label}',sans-serif">Aa Bb 0123</div>
        </div>'''

    flags_section = ""
    for flag in active_flags:
        flags_section += f'<span class="flag-badge">{flag}</span>'

    pdf_section = ""
    for fname, fpath in pdf_files:
        thumb = generate_pdf_thumbnail(fpath)
        thumb_html = f'<img src="pdf/{os.path.basename(thumb)}" alt="{fname}" loading="lazy" class="pdf-thumb">' if thumb else '<div class="pdf-icon">📄</div>'
        fsize = os.path.getsize(fpath) // 1024
        pdf_section += f'''
        <a class="pdf-card" href="pdf/{fname}" target="_blank">
          {thumb_html}
          <div class="pdf-info">
            <span class="pdf-name">{fname}</span>
            <span class="pdf-size">{fsize} Ko</span>
          </div>
        </a>'''

    tmpl_section = ""
    for fname, fpath in template_thumbs:
        b64img = ""
        try:
            from PIL import Image
            img = Image.open(fpath)
            img.thumbnail((160, 160))
            buf = io.BytesIO()
            img.save(buf, "PNG")
            b64img = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
        except:
            b64img = ""
        tmpl_section += f'''
        <div class="tmpl-card">
          {"<img src='" + b64img + "' alt='" + fname + "' loading='lazy'>" if b64img else '<div class="tmpl-placeholder">—</div>'}
          <div class="tmpl-name">{fname}</div>
        </div>'''

    charte_section = ""
    if has_charte:
        csize = os.path.getsize(charte_pdf) // 1024
        charte_section = f'''
        <div class="charte-card">
          <div class="charte-icon">📘</div>
          <div class="charte-info">
            <div class="charte-title">Charte Graphique</div>
            <div class="charte-desc">{csize} Ko — PDF complet avec logos, palette et règles d'usage</div>
          </div>
          <a href="../charte-graphique-{dirname}.pdf" class="charte-btn" target="_blank">Télécharger</a>
        </div>'''

    # Compute proposition number
    prop_num = dirname[:2]

    html = f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{cfg.name} — Aperçu · Rivers Rock</title>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Space+Mono&family=Montserrat:wght@300;400;600&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:#0D1117;--bg2:#161B22;--bg3:#1C2333;--text:#E6EDF3;--text2:#8B949E;--border:rgba(255,255,255,0.06);--accent:{first_hex};--radius:10px}}
body{{font-family:'Montserrat',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;line-height:1.5}}
.bg-grain{{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;
  background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23g)' opacity='0.03'/%3E%3C/svg%3E")}}
.container{{max-width:1100px;margin:0 auto;padding:24px;position:relative;z-index:1}}

/* Header */
.header{{text-align:center;padding:60px 0 20px;position:relative}}
.header .num{{font-family:'Anton',sans-serif;font-size:14px;color:rgba(255,255,255,0.15);letter-spacing:4px;text-transform:uppercase}}
.header h1{{font-family:'Anton',sans-serif;font-size:42px;letter-spacing:2px;margin:8px 0;background:linear-gradient(135deg,var(--text) 30%,{first_hex});-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.header .tagline{{font-size:13px;color:var(--text2);font-family:'Space Mono',monospace}}
.header-actions{{display:flex;gap:12px;justify-content:center;margin-top:20px;flex-wrap:wrap}}
.header-actions a{{padding:10px 24px;border-radius:8px;text-decoration:none;font-family:'Space Mono',monospace;font-size:12px;transition:.2s;letter-spacing:.5px}}
.btn-site{{background:{first_hex};color:#fff}}
.btn-site:hover{{filter:brightness(1.15)}}
.btn-back{{background:rgba(255,255,255,0.06);color:var(--text2)}}
.btn-back:hover{{background:rgba(255,255,255,0.1);color:var(--text)}}

/* Sections */
.section{{margin:48px 0}}
.section-title{{font-family:'Anton',sans-serif;font-size:20px;letter-spacing:1px;margin-bottom:16px;padding-bottom:8px;border-bottom:1px solid var(--border)}}

/* Logos */
.logo-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:16px}}
.logo-card{{background:var(--bg2);border-radius:var(--radius);border:1px solid var(--border);padding:20px;text-align:center;transition:.2s}}
.logo-card:hover{{background:var(--bg3)}}
.logo-card.missing{{opacity:0.3}}
.logo-frame{{height:100px;display:flex;align-items:center;justify-content:center;margin-bottom:10px}}
.logo-frame img{{max-width:100%;max-height:100%;object-fit:contain}}
.logo-label{{font-size:12px;font-weight:600}}
.logo-fname{{font-size:10px;color:var(--text2);margin-top:2px}}
.missing-icon{{color:var(--text2);font-size:24px}}

/* Animated logo iframe */
.anim-wrapper{{max-width:300px;margin:0 auto;border-radius:var(--radius);overflow:hidden;border:1px solid var(--border)}}
.anim-wrapper iframe{{width:100%;aspect-ratio:9/16;display:block;border:none}}

/* Palette */
.palette-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px}}
.swatch{{border-radius:var(--radius);height:80px;position:relative;overflow:hidden}}
.swatch-info{{position:absolute;bottom:0;left:0;right:0;padding:8px 10px;background:rgba(0,0,0,0.2);backdrop-filter:blur(4px);display:flex;justify-content:space-between;align-items:center}}
.swatch-name{{font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.5px}}
.swatch-hex{{font-family:'Space Mono',monospace;font-size:9px;opacity:0.7}}

/* Typography */
.font-row{{display:flex;align-items:center;gap:16px;padding:12px 16px;background:var(--bg2);border-radius:var(--radius);border:1px solid var(--border);margin-bottom:8px}}
.font-role{{font-size:10px;font-weight:600;color:var(--text2);text-transform:uppercase;letter-spacing:1px;min-width:60px}}
.font-name{{font-size:14px;min-width:130px}}
.font-specimen{{font-size:18px;color:var(--text);flex:1;text-align:right}}

/* Flags */
.flags-wrap{{display:flex;flex-wrap:wrap;gap:8px}}
.flag-badge{{padding:5px 14px;border-radius:20px;font-size:11px;background:{first_hex}22;color:{first_hex};border:1px solid {first_hex}44;font-family:'Space Mono',monospace}}

/* PDFs */
.pdf-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px}}
.pdf-card{{background:var(--bg2);border-radius:var(--radius);border:1px solid var(--border);overflow:hidden;text-decoration:none;color:var(--text);transition:.2s}}
.pdf-card:hover{{background:var(--bg3);transform:translateY(-2px)}}
.pdf-card .pdf-thumb{{width:100%;height:150px;object-fit:cover;display:block;background:var(--bg3)}}
.pdf-icon{{height:150px;display:flex;align-items:center;justify-content:center;font-size:36px;background:var(--bg3)}}
.pdf-info{{padding:10px 12px;display:flex;justify-content:space-between;align-items:center}}
.pdf-name{{font-size:12px;font-weight:600}}
.pdf-size{{font-size:10px;color:var(--text2);font-family:'Space Mono',monospace}}

/* Template thumbnails */
.tmpl-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:12px}}
.tmpl-card{{background:var(--bg2);border-radius:var(--radius);border:1px solid var(--border);padding:8px;text-align:center;transition:.2s}}
.tmpl-card:hover{{background:var(--bg3)}}
.tmpl-card img{{width:100%;height:80px;object-fit:contain;display:block;border-radius:4px}}
.tmpl-placeholder{{width:100%;height:80px;display:flex;align-items:center;justify-content:center;color:var(--text2);font-size:20px;background:var(--bg3);border-radius:4px}}
.tmpl-name{{font-size:10px;margin-top:6px;color:var(--text2);word-break:break-all}}

/* Charte */
.charte-card{{display:flex;align-items:center;gap:16px;background:var(--bg2);border-radius:var(--radius);border:1px solid {first_hex}44;padding:16px 20px}}
.charte-icon{{font-size:32px;flex-shrink:0}}
.charte-info{{flex:1}}
.charte-title{{font-weight:600;font-size:14px}}
.charte-desc{{font-size:11px;color:var(--text2);margin-top:2px}}
.charte-btn{{padding:8px 20px;border-radius:6px;background:{first_hex};color:#fff;text-decoration:none;font-family:'Space Mono',monospace;font-size:11px;transition:.2s;flex-shrink:0}}
.charte-btn:hover{{filter:brightness(1.15)}}

/* Page de comparaison link */
.back-link{{text-align:center;padding:40px 0 20px}}
.back-link a{{color:var(--text2);text-decoration:none;font-size:12px;font-family:'Space Mono',monospace;transition:.2s}}
.back-link a:hover{{color:var(--text)}}

/* Responsive */
@media(max-width:600px){{
  .header h1{{font-size:28px}}
  .logo-grid{{grid-template-columns:repeat(2,1fr)}}
  .palette-grid{{grid-template-columns:repeat(2,1fr)}}
  .font-row{{flex-wrap:wrap}}
  .font-specimen{{text-align:left;width:100%;margin-top:4px}}
  .charte-card{{flex-wrap:wrap}}
}}

@media(prefers-color-scheme:light){{
  :root{{--bg:#F5F5F0;--bg2:#FFFFFF;--bg3:#F0F0EB;--text:#1A1A1A;--text2:#666;--border:rgba(0,0,0,0.08)}}
}}

@media(prefers-reduced-motion){{
  *{{animation:none!important;transition:none!important}}
}}
</style>
</head>
<body>
<div class="bg-grain"></div>
<div class="container">

  <div class="header">
    <div class="num">{dirname} · Proposition {prop_num}</div>
    <h1>{cfg.name}</h1>
    <p class="tagline">{cfg.tokens.get("gradient_style","").capitalize()} · {cfg.tokens.get("badge_shape","").capitalize()} badges · {cfg.tokens.get("wave_style","").capitalize()} wave</p>
    <div class="header-actions">
      <a class="btn-site" href="index.html" target="_blank">Voir le site →</a>
      <a class="btn-back" href="../../propositions/">← Toutes les propositions</a>
    </div>
  </div>

  <div class="section">
    <div class="section-title">Logo · 5 variantes</div>
    <div class="logo-grid">{logo_section}</div>
  </div>

  <div class="section">
    <div class="section-title">Logo animé</div>
    <div class="anim-wrapper">
      {"<iframe src='templates/" + os.path.basename(animated_path) + "' title='Logo animé " + cfg.name + "' loading='lazy'></iframe>" if has_animated else '<div style="padding:40px;text-align:center;color:var(--text2)">Logo animé non disponible</div>'}
    </div>
  </div>

  <div class="section">
    <div class="section-title">Palette couleurs <span style="font-family:'Space Mono',monospace;font-size:11px;color:var(--text2);font-weight:400">({len(color_items)} couleurs)</span></div>
    <div class="palette-grid">{palette_section}</div>
  </div>

  <div class="section">
    <div class="section-title">Typographie</div>
    {font_section}
  </div>

  <div class="section">
    <div class="section-title">Éléments graphiques</div>
    <div class="flags-wrap">{flags_section if flags_section else '<span style="color:var(--text2);font-size:13px">Aucun effet spécial</span>'}</div>
  </div>

  <div class="section">
    <div class="section-title">PDF générés <span style="font-family:'Space Mono',monospace;font-size:11px;color:var(--text2);font-weight:400">({len(pdf_files)} fichiers)</span></div>
    <div class="pdf-grid">{pdf_section if pdf_section else '<p style="color:var(--text2)">Aucun PDF généré</p>'}</div>
  </div>

  <div class="section">
    <div class="section-title">Templates réseaux <span style="font-family:'Space Mono',monospace;font-size:11px;color:var(--text2);font-weight:400">({len(template_thumbs)} fichiers)</span></div>
    <div class="tmpl-grid">{tmpl_section if tmpl_section else '<p style="color:var(--text2)">Aucun template</p>'}</div>
  </div>

  <div class="section">
    <div class="section-title">Charte Graphique</div>
    {charte_section if charte_section else '<p style="color:var(--text2)">Charte PDF non disponible</p>'}
  </div>

  <div class="back-link">
    <a href="../../propositions/">← Retour à la page de comparaison</a>
  </div>

</div>
</body>
</html>'''

    out_path = os.path.join(assets_dir, "preview.html")
    with open(out_path, "w") as f:
        f.write(html)
    print(f"  Preview : {out_path}")
    return True


def update_index_html():
    """Add Apercu and Charte links to propositions/index.html."""
    index_path = os.path.join(OUT_DIR, "index.html")
    if not os.path.exists(index_path):
        print(f"  WARNING: {index_path} not found")
        return

    content = read_file(index_path)

    for cfg, dirname in PROPS:
        prop_dir = os.path.join(OUT_DIR, dirname)
        assets_dir = os.path.join(prop_dir, "assets")
        preview_path = os.path.join(assets_dir, "preview.html")
        charte_pdf = os.path.join(prop_dir, f"charte-graphique-{dirname}.pdf")

        if not os.path.exists(preview_path):
            continue

        # Find the card-footer for this proposition
        # Pattern: href="{dirname}/assets/index.html"
        # We need to find the .card-footer div after this link
        search = f'href="{dirname}/assets/index.html"'
        idx = content.find(search)
        if idx == -1:
            continue

        # Find the .card-footer div for this card
        footer_start = content.find('<div class="card-footer">', idx)
        if footer_start == -1:
            continue
        footer_end = content.find('</div>', footer_start)
        if footer_end == -1:
            continue

        # Check if Apercu link already exists
        existing = content[footer_start:footer_end]
        if f'href="{dirname}/assets/preview.html"' in existing:
            continue

        # Build the links to insert
        apercu_link = f'      <a class="btn-pdf" href="{dirname}/assets/preview.html">Aperçu</a>\n'
        charte_link = ""
        if os.path.exists(charte_pdf):
            charte_link = f'      <a class="btn-pdf" href="{dirname}/charte-graphique-{dirname}.pdf">Charte PDF</a>\n'

        # Insert before the closing of card-footer
        insert_pos = footer_end
        new_content = content[:insert_pos] + "\n" + apercu_link + charte_link + content[insert_pos:]
        content = new_content

    with open(index_path, "w") as f:
        f.write(content)
    print(f"  Updated: {index_path}")


def create_chartes_zip():
    """Create a ZIP archive of all charte graphique PDFs."""
    zip_path = os.path.join(OUT_DIR, "chartes-graphiques.zip")
    if os.path.exists(zip_path):
        os.remove(zip_path)
    count = 0
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for cfg, dirname in PROPS:
            charte_pdf = os.path.join(OUT_DIR, dirname, f"charte-graphique-{dirname}.pdf")
            if os.path.exists(charte_pdf):
                arcname = f"{dirname}/charte-graphique-{dirname}.pdf"
                zf.write(charte_pdf, arcname)
                count += 1
    if count:
        size = os.path.getsize(zip_path) // 1024
        print(f"  ZIP créé : {zip_path} ({count} fichiers, {size} Ko)")
    return count > 0


if __name__ == "__main__":
    skip_thumbs = "--skip-thumbs" in sys.argv

    print("Génération des pages d'aperçu...")
    for cfg, dirname in PROPS:
        print(f"  {dirname} : {cfg.name}")
        generate_preview(cfg, dirname)

    if not skip_thumbs:
        print("\nGénération des miniatures PDF...")
        for cfg, dirname in PROPS:
            pdf_dir = os.path.join(OUT_DIR, dirname, "assets", "pdf")
            if os.path.exists(pdf_dir):
                for f in sorted(os.listdir(pdf_dir)):
                    if f.endswith(".pdf") and not f.startswith("."):
                        thumb_path = os.path.join(pdf_dir, f.replace(".pdf", "-preview.png"))
                        if not os.path.exists(thumb_path):
                            pdf_path = os.path.join(pdf_dir, f)
                            result = generate_pdf_thumbnail(pdf_path)
                            if result:
                                print(f"    Thumb: {f}")
    else:
        print("\n  (miniatures ignorées --skip-thumbs)")

    print("\nMise à jour de propositions/index.html...")
    update_index_html()

    print("\nCréation du ZIP des chartes graphiques...")
    create_chartes_zip()

    print("\n✅ Fait")
