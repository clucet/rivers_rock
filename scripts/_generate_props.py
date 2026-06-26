#!/usr/bin/env python3
"""Generate the 5 new proposition generate.py files from templates."""

import os, sys

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT, "scripts"))

from palette import BITUME, CORDES_VOIX, HERITAGE, RUBICON, MINUIT

PROPS = [
    ("10-bitume",     BITUME,   "B", "#2C2C2C", "#F4D03F", "Stencil, spray, bitume"),
    ("11-cordes-voix",CORDES_VOIX,"C","#FFF8F0","#FFB74D", "Acoustique, intimiste, bois et cordes"),
    ("12-heritage",   HERITAGE, "H", "#1A237E", "#D4AF37", "Patrimoine normand, vitrail, colombages"),
    ("13-rubicon",    RUBICON,  "R", "#FFF8E1", "#E65100", "Road trip, americana, horizon"),
    ("14-minuit",     MINUIT,   "M", "#0D0D0D", "#C9A87C", "Soiree chic, french touch, velours"),
]

for slug, cfg, letter, bg, accent, tagline in PROPS:
    prop_dir = os.path.join(PROJECT, "propositions", slug)
    gen_path = os.path.join(prop_dir, "generate.py")
    cn = cfg.__class__.__name__ if hasattr(cfg, '__class__') else cfg.name.lower().replace(' & ','-')
    config_name = slug.split('-')[1].replace('-','_').upper()
    # Map slug to config constant name
    config_map = {"10-bitume": "BITUME", "11-cordes-voix": "CORDES_VOIX",
                  "12-heritage": "HERITAGE", "13-rubicon": "RUBICON", "14-minuit": "MINUIT"}
    config_name = config_map[slug]
    
    c1 = cfg.colors["bleu_seine"][0]
    c2 = cfg.colors["vert_eau"][0]
    a = cfg.colors["accent"][0]
    o = cfg.colors["or_vieilli"][0]
    b = cfg.colors["blanc"][0]
    bc = cfg.colors["blanc_casse"][0]
    
    site_html = (
        '<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Rivers Rock -- ' + cfg.name + '</title>'
        '<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@300;400;600&display=swap" rel="stylesheet"><style>'
        '*{margin:0;padding:0;box-sizing:border-box}'
        ':root{--c1:' + c1 + ';--c2:' + c2 + ';--accent:' + a + ';--or:' + o + ';--blanc:' + b + '}'
        'body{font-family:Montserrat,sans-serif;background:var(--c1);color:var(--blanc);min-height:100vh}'
        '.hero{min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:100px 24px 60px}'
        '.hero h1{font-family:Bebas Neue,sans-serif;font-size:64px;letter-spacing:3px;color:var(--accent)}'
        '.hero .tag{font-size:14px;color:var(--or);margin-top:8px}'
        '.section{padding:60px 24px;max-width:800px;margin:0 auto}'
        '.section h2{font-family:Bebas Neue,sans-serif;font-size:32px;letter-spacing:2px;margin-bottom:20px;color:var(--accent)}'
        '.members-grid{display:flex;flex-wrap:wrap;gap:16px;justify-content:center}'
        '.member-card{text-align:center;padding:20px;background:rgba(255,255,255,0.04);border-radius:8px;flex:0 0 140px}'
        '.avatar-circle{width:56px;height:56px;border-radius:50%;background:var(--accent);margin:0 auto 8px;display:flex;align-items:center;justify-content:center;font-family:Bebas Neue,sans-serif;font-size:24px;color:var(--c1)}'
        '.member-card h3{font-size:14px;margin-bottom:2px}'
        '.member-card p{font-size:11px;color:rgba(255,255,255,0.5)}'
        '.links-social a{display:inline-block;padding:8px 16px;margin:4px;border-radius:6px;background:rgba(255,255,255,0.06);color:var(--or);text-decoration:none;font-size:12px;transition:.2s}'
        '.links-social a:hover{background:var(--accent);color:var(--c1)}'
        'form{max-width:400px;margin:20px auto}'
        'input,textarea{width:100%;padding:10px;margin-bottom:8px;border:1px solid rgba(255,255,255,0.15);border-radius:6px;background:rgba(255,255,255,0.05);color:#fff;font-family:inherit;font-size:14px}'
        'button{width:100%;padding:10px;border:none;border-radius:6px;background:var(--accent);color:#fff;font-family:inherit;font-size:14px;cursor:pointer}'
        '@media(max-width:640px){.hero h1{font-size:36px}.members-grid{grid-template-columns:repeat(2,1fr)}}'
        '@media(prefers-color-scheme:light){:root{--c1:' + bc + ';--blanc:#1A1A1A}}'
        '@media(prefers-reduced-motion){*{animation:none!important;transition:none!important}}'
        'a:focus-visible,button:focus-visible{outline:2px solid var(--accent);outline-offset:2px}'
        '</style></head><body>'
        '<section class="hero"><h1>RIVERS ROCK</h1><div class="tag">' + tagline + '</div></section>'
        '<section class="section" id="groupe"><h2>Le groupe</h2><p>Groupe rouennais forme en 2024. Rock, pop-rock, inde et alternatif.</p>'
        '<div class="members-grid">'
        '<div class="member-card"><div class="avatar-circle">R</div><h3>Rosaria</h3><p>Batterie</p></div>'
        '<div class="member-card"><div class="avatar-circle">C</div><h3>Christophe</h3><p>Basse</p></div>'
        '<div class="member-card"><div class="avatar-circle">N</div><h3>Nicolas</h3><p>Guitare</p></div>'
        '<div class="member-card"><div class="avatar-circle">D</div><h3>David</h3><p>Guitare / Chant</p></div>'
        '<div class="member-card"><div class="avatar-circle">V</div><h3>Virginie</h3><p>Chant</p></div>'
        '</div></section>'
        '<section class="section" id="concerts"><h2>Concerts</h2><p>Contactez-nous pour programmer un concert.</p></section>'
        '<section class="section" id="musique"><h2>Musique</h2><p>Playlist a venir -- suivez-nous sur YouTube.</p></section>'
        '<section class="section" id="contact"><h2>Contact</h2>'
        '<form action="https://formsubmit.co/riversrock_rouen@gmail.com" method="POST">'
        '<input type="text" name="nom" placeholder="Votre nom" required>'
        '<input type="email" name="email" placeholder="Votre email" required>'
        '<textarea name="message" placeholder="Votre message" required rows="3"></textarea>'
        '<button type="submit">Envoyer</button></form>'
        '<div class="links-social">'
        '<a href="https://www.instagram.com/riversrock_rouen">Instagram</a>'
        '<a href="https://www.facebook.com/RiversRockRouen">Facebook</a>'
        '<a href="https://www.youtube.com/@RiversRockRouen">YouTube</a>'
        '<a href="mailto:riversrock_rouen@gmail.com">Email</a>'
        '</div></section></body></html>'
    )
    
    # Build the generate.py content
    code = '#!/usr/bin/env python3\n'
    code += '# Auto-generated -- do not edit directly\n'
    code += 'import os, sys, math, random\n'
    code += "sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))\n"
    code += 'from logoutils import (\n'
    code += '    create_bleed_canvas, save_with_crop_marks, draw_qr_pillow, draw_qr_reportlab,\n'
    code += '    pillow_grain_overlay, draw_gradient_pdf, draw_waves_pdf, draw_grain_pdf,\n'
    code += '    BEBAS_PATH, SPACE_MONO_PATH, JETBRAINS_PATH, DMMONO_PATH,\n'
    code += ')\n'
    code += 'from palette import ' + config_name + ' as CFG\n'
    code += 'from reportlab.lib.pagesizes import A4, A6\n'
    code += 'from reportlab.lib.colors import Color\n'
    code += 'from reportlab.pdfgen import canvas\n'
    code += 'from reportlab.pdfbase import pdfmetrics\n'
    code += 'from reportlab.pdfbase.ttfonts import TTFont\n'
    code += 'from PIL import Image, ImageDraw, ImageFont\n\n'
    code += "OUT = os.path.join(os.path.dirname(__file__), 'assets')\n"
    code += "PDF = os.path.join(OUT, 'pdf')\n"
    code += "TMPL = os.path.join(OUT, 'templates')\n"
    code += 'for d in (OUT, PDF, TMPL): os.makedirs(d, exist_ok=True)\n\n'
    code += '# Font registrations\n'
    code += "for role in ['hero', 'logo', 'body', 'badge', 'song', 'data', 'quote']:\n"
    code += '    fname = CFG.fonts.get(role)\n'
    code += '    if fname:\n'
    code += '        try:\n'
    code += '            from logoutils import _resolve_font\n'
    code += '            fpath = _resolve_font(fname)\n'
    code += '            if fpath:\n'
    code += '                pdfmetrics.registerFont(TTFont(fname, fpath))\n'
    code += '        except: pass\n\n'
    code += 'from setlist_data import SETLIST, GREEN_INDICES\n\n'
    code += 'C1 = CFG.rl(\"bleu_seine\")\n'
    code += 'C2 = CFG.rl(\"vert_eau\")\n'
    code += 'ACCENT = CFG.rl(\"accent\")\n'
    code += 'OR = CFG.rl(\"or_vieilli\")\n'
    code += 'BLANC = CFG.rl(\"blanc\")\n'
    code += 'C1_PIL = CFG.pil(\"bleu_seine\")\n'
    code += 'C2_PIL = CFG.pil(\"vert_eau\")\n'
    code += 'ACCENT_PIL = CFG.pil(\"accent\")\n\n'
    code += 'sl = \"' + slug.split('-')[1] + '\"\n\n'
    
    # Generate function stubs
    funcs = '''
def gen_setlist():
    W, H = A4
    path = os.path.join(PDF, "setlist-" + sl + ".pdf")
    cv, _, _, bleed = create_bleed_canvas(path, W, H)
    draw_gradient_pdf(cv, W, H, C1, C2)
    draw_grain_pdf(cv, W, H, seed=42)
    draw_waves_pdf(cv, W, H, count=CFG.token("wave_rows", 3), opacity=CFG.token("wave_opacity", 0.04))
    cv.setFillColor(BLANC)
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
'''
    code += funcs
    
    anim_svg = {
        "10-bitume": '<circle cx="0" cy="0" r="120" fill="none" stroke="' + a + '" stroke-width="3" stroke-dasharray="4 6" opacity="0"/><text x="0" y="-5" text-anchor="middle" font-family="sans-serif" font-size="40" fill="' + a + '" font-weight="bold" opacity="0">' + letter + '</text><text x="0" y="40" text-anchor="middle" font-family="sans-serif" font-size="18" fill="' + o + '" letter-spacing="4" opacity="0">RIVERS ROCK</text>',
        "11-cordes-voix": '<circle cx="0" cy="0" r="100" fill="none" stroke="' + c2 + '" stroke-width="1" opacity="0.3"/><path d="M-80,0 Q-40,-15 0,0 Q40,15 80,0" fill="none" stroke="' + a + '" stroke-width="2" stroke-linecap="round"><animate attributeName="d" dur="1.5s" repeatCount="indefinite" values="M-80,0 Q-40,-15 0,0 Q40,15 80,0;M-80,0 Q-40,-10 0,0 Q40,10 80,0;M-80,0 Q-40,-15 0,0 Q40,15 80,0"/></path><text x="0" y="40" text-anchor="middle" font-family="serif" font-size="20" fill="' + c2 + '" letter-spacing="3">RIVERS ROCK</text>',
        "12-heritage": '<circle cx="0" cy="0" r="140" fill="none" stroke="' + a + '" stroke-width="2" opacity="0.5"><animate attributeName="r" dur="4s" repeatCount="indefinite" values="140;145;140"/></circle><path d="M0,-100 L20,-80 L40,-60 L20,-40 L0,-20 L-20,-40 L-40,-60 L-20,-80 Z" fill="' + a + '" opacity="0.15"><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="20s" repeatCount="indefinite"/></path><text x="0" y="10" text-anchor="middle" font-family="serif" font-size="22" fill="' + o + '" letter-spacing="4">RIVERS ROCK</text>',
        "13-rubicon": '<circle cx="0" cy="0" r="100" fill="none" stroke="' + a + '" stroke-width="3" stroke-dasharray="10 8"><animate attributeName="stroke-dashoffset" dur="1s" repeatCount="indefinite" values="0;-36"/></circle><text x="0" y="5" text-anchor="middle" font-family="sans-serif" font-size="24" fill="' + c2 + '" letter-spacing="3" font-weight="bold">RIVERS ROCK</text>',
        "14-minuit": '<circle cx="0" cy="0" r="140" fill="none" stroke="' + a + '" stroke-width="1" opacity="0.15"/><path d="M-40,-60 A50,50 0 1,1 40,-60" fill="none" stroke="' + a + '" stroke-width="2"><animate attributeName="d" dur="6s" repeatCount="indefinite" values="M-40,-60 A50,50 0 1,1 40,-60;M-30,-70 A40,40 0 1,1 30,-70;M-40,-60 A50,50 0 1,1 40,-60"/></path><text x="0" y="50" text-anchor="middle" font-family="serif" font-size="20" fill="' + o + '" letter-spacing="5" opacity="0"><animate attributeName="opacity" dur="2s" fill="freeze" values="0;1"/></text>',
    }[slug]
    
    code += '\ndef gen_animated():\n'
    code += '    path = os.path.join(TMPL, "logo-animated-" + sl + ".html")\n'
    code += '    with open(path, "w") as f:\n'
    code += '        f.write("""<!DOCTYPE html><html lang=\\"fr\\"><head><meta charset=\\"UTF-8\\"><meta name=\\"viewport\\" content=\\"width=device-width,initial-scale=1\\">\n'
    code += '<title>Rivers Rock -- ' + cfg.name + '</title>\n'
    code += '<style>*{margin:0;padding:0}\n'
    code += 'body{width:1080px;height:1920px;overflow:hidden;background:' + bg + ';display:flex;align-items:center;justify-content:center}\n'
    code += 'svg{width:400px;height:400px;overflow:visible}\n'
    code += '</style></head><body>\n'
    code += '<svg viewBox="-200 -200 400 400">\n'
    code += anim_svg + '\n'
    code += '</svg></body></html>""")\n'
    code += '    print("' + '[' + cfg.name + ']' + ' Animated logo > " + path)\n'
    
    code += '\ndef gen_site():\n'
    code += '    path = os.path.join(OUT, "index.html")\n'
    code += '    with open(path, "w") as f:\n'
    code += '        f.write("""' + site_html.replace('"', '\\"') + '""")\n'
    code += '    print("' + '[' + cfg.name + ']' + ' Site > " + path)\n'
    
    code += '\nif __name__ == "__main__":\n'
    code += '    gen_setlist()\n'
    code += '    gen_poster()\n'
    code += '    gen_flyer()\n'
    code += '    from generate_social import generate_post, generate_story\n'
    code += '    from generate_banners import gen_banners\n'
    code += '    from generate_avatar import gen_avatar\n'
    code += '    from generate_stickers import gen_stickers\n'
    code += '    from generate_tshirts import generate_print, generate_mockup\n'
    code += '    gen_setlist()\n'
    code += '    gen_poster()\n'
    code += '    gen_flyer()\n'
    code += '    gen_animated()\n'
    code += '    gen_site()\n'
    
    with open(gen_path, "w") as f:
        f.write(code)
    print(f"  {slug}: generate.py written ({len(code)} bytes)")

print("Done")
