#!/usr/bin/env python3
"""Shared Rivers Rock crest drawing functions for ReportLab and Pillow."""

import math, os, urllib.request, random
from reportlab.lib.colors import HexColor, Color
from PIL import Image, ImageFont, ImageDraw

from palette import BASE, SCENE_VINTAGE, FLUID_WAVE, ROCK_BRUT, font_filename
from palette import PONTS_LUMIERE, NEON_NIGHTS, SABLE_BRONZE, NORDIK, GRUNGE, JAZZ_CLUB


def _find_font(filename, alt_names=None):
    """Search for a font file in common locations across OSes."""
    search_paths = [
        os.path.expanduser(f"~/Library/Fonts/{filename}"),
        os.path.expanduser(f"~/.fonts/{filename}"),
        os.path.expanduser(f"~/.local/share/fonts/{filename}"),
        f"/usr/share/fonts/{filename}",
        f"/usr/share/fonts/truetype/{filename}",
        os.path.join(os.path.dirname(__file__), filename),
    ]
    for p in search_paths:
        if os.path.exists(p):
            return p
    if alt_names:
        for alt in alt_names:
            for p in search_paths:
                if os.path.exists(p):
                    return p
    return None


def _ensure_font(filename, url):
    """Download font if missing."""
    dest = os.path.expanduser(f"~/.fonts/{filename}")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if not os.path.exists(dest):
        try:
            urllib.request.urlretrieve(url, dest)
            print(f"Téléchargement : {dest}")
        except Exception:
            raise RuntimeError(
                f"Police {filename} introuvable. Placez-la dans ~/.fonts/ "
                f"ou téléchargez-la depuis : {url}"
            )
    return dest


def _resolve_font(role, cfg=None):
    c = cfg or SCENE_VINTAGE
    fname = font_filename(role, c)

    fnames = [fname]
    if fname == "Montserrat-VariableFont_wght.ttf":
        fnames.append("Montserrat-VF.ttf")
    elif fname == "Anton-Regular.ttf":
        fnames.append("Anton.ttf")
    elif fname == "SpaceMono-Regular.ttf":
        fnames.append("SpaceMono.ttf")
    elif fname == "PlayfairDisplay[wght].ttf":
        fnames.append("PlayfairDisplay.ttf")
    elif fname == "Nunito[wght].ttf":
        fnames.append("Nunito.ttf")
    elif fname == "InterTight[wght].ttf":
        fnames.append("InterTight.ttf")
    elif fname == "JetBrainsMono[wght].ttf":
        fnames.append("JetBrainsMono.ttf")
    elif fname == "Teko[wght].ttf":
        fnames.append("Teko.ttf")
    elif fname == "Raleway[wght].ttf":
        fnames.append("Raleway.ttf")
    elif fname == "DMMono-Regular.ttf":
        fnames.append("DMMono.ttf")
    elif fname == "Orbitron[wght].ttf":
        fnames.append("Orbitron.ttf")
    elif fname == "Rajdhani-Regular.ttf":
        fnames.append("Rajdhani.ttf")
    elif fname == "Inter[opsz,wght].ttf":
        fnames.append("Inter.ttf")
    elif fname == "Karla[wght].ttf":
        fnames.append("Karla.ttf")
    elif fname == "RubikGlitch-Regular.ttf":
        fnames.append("RubikGlitch.ttf")
    elif fname == "SyneMono-Regular.ttf":
        fnames.append("SyneMono.ttf")
        fnames.append("Rajdhani.ttf")
    elif fname == "Cinzel[wght].ttf":
        fnames.append("Cinzel.ttf")
    elif fname == "Lato-Regular.ttf":
        fnames.append("Lato.ttf")
    elif fname == "Cormorant-VariableFont_wght.ttf":
        fnames.append("Cormorant-VF.ttf")

    path = None
    for fn in fnames:
        path = _find_font(fn)
        if path:
            break

    if not path:
        urls = {
            "BebasNeue-Regular.ttf": "https://github.com/google/fonts/raw/main/ofl/bebasneue/BebasNeue-Regular.ttf",
            "Anton-Regular.ttf": "https://github.com/google/fonts/raw/main/ofl/anton/Anton-Regular.ttf",
            "Montserrat-VariableFont_wght.ttf": "https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat-VariableFont_wght.ttf",
            "SpaceMono-Regular.ttf": "https://github.com/google/fonts/raw/main/ofl/spacemono/SpaceMono-Regular.ttf",
            "PlayfairDisplay[wght].ttf": "https://github.com/google/fonts/raw/main/ofl/playfairdisplay/PlayfairDisplay%5Bwght%5D.ttf",
            "Nunito[wght].ttf": "https://github.com/google/fonts/raw/main/ofl/nunito/Nunito%5Bwght%5D.ttf",
            "InterTight[wght].ttf": "https://github.com/google/fonts/raw/main/ofl/intertight/InterTight%5Bwght%5D.ttf",
            "JetBrainsMono[wght].ttf": "https://github.com/google/fonts/raw/main/ofl/jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf",
            "Teko[wght].ttf": "https://github.com/google/fonts/raw/main/ofl/teko/Teko%5Bwght%5D.ttf",
            "Raleway[wght].ttf": "https://github.com/google/fonts/raw/main/ofl/raleway/Raleway%5Bwght%5D.ttf",
            "DMMono-Regular.ttf": "https://github.com/google/fonts/raw/main/ofl/dmmono/DMMono-Regular.ttf",
            "Inter[opsz,wght].ttf": "https://github.com/google/fonts/raw/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf",
            "Karla[wght].ttf": "https://github.com/google/fonts/raw/main/ofl/karla/Karla%5Bwght%5D.ttf",
            "RubikGlitch-Regular.ttf": "https://github.com/google/fonts/raw/main/ofl/rubikglitch/RubikGlitch-Regular.ttf",
            "SyneMono-Regular.ttf": "https://github.com/google/fonts/raw/main/ofl/synemono/SyneMono-Regular.ttf",
            "Orbitron[wght].ttf": "https://github.com/google/fonts/raw/main/ofl/orbitron/Orbitron%5Bwght%5D.ttf",
            "Rajdhani-Regular.ttf": "https://github.com/google/fonts/raw/main/ofl/rajdhani/Rajdhani-Regular.ttf",
            "Cinzel[wght].ttf": "https://github.com/google/fonts/raw/main/ofl/cinzel/Cinzel%5Bwght%5D.ttf",
            "Lato-Regular.ttf": "https://github.com/google/fonts/raw/main/ofl/lato/Lato-Regular.ttf",
            "Cormorant-VariableFont_wght.ttf": "https://github.com/google/fonts/raw/main/ofl/cormorant/Cormorant%5Bwght%5D.ttf",
        }
        url = urls.get(fname, urls.get("Montserrat-VariableFont_wght.ttf"))
        path = _ensure_font(fname, url)
    return path


BEBAS_PATH = _resolve_font("logo", BASE)
MONTSERRAT_PATH = _resolve_font("body", BASE)
ANTON_PATH = _resolve_font("hero", SCENE_VINTAGE)
SPACE_MONO_PATH = _resolve_font("accent", SCENE_VINTAGE)
PLAYFAIR_PATH = _resolve_font("hero", FLUID_WAVE)
NUNITO_PATH = _resolve_font("body", FLUID_WAVE)
INTERTIGHT_PATH = _resolve_font("body", ROCK_BRUT)
JETBRAINS_PATH = _resolve_font("data", ROCK_BRUT)
TEKO_PATH = _resolve_font("hero", PONTS_LUMIERE)
RALEWAY_PATH = _resolve_font("body", PONTS_LUMIERE)
DMMONO_PATH = _resolve_font("data", PONTS_LUMIERE)
ORBITRON_PATH = _resolve_font("hero", NEON_NIGHTS)
RAJDHANI_PATH = _resolve_font("body", NEON_NIGHTS)
INTER_PATH = _resolve_font("hero", NORDIK)
KARLA_PATH = _resolve_font("body", JAZZ_CLUB)
RUBIK_PATH = _resolve_font("hero", GRUNGE)
SYNEMONO_PATH = _resolve_font("data", GRUNGE)
CINZEL_PATH = _resolve_font("hero", SABLE_BRONZE)
LATO_PATH = _resolve_font("body", SABLE_BRONZE)
CORMORANT_PATH = _resolve_font("quote", SABLE_BRONZE)
LATO_PATH = _resolve_font("body", SABLE_BRONZE)
CORMORANT_PATH = _resolve_font("quote", SABLE_BRONZE)

# Default config for logoutils functions
DEFAULT_CFG = SCENE_VINTAGE

# Backward-compatible color constants (from default config)
ACCENT    = DEFAULT_CFG.rl("accent")
BLANC     = DEFAULT_CFG.rl("blanc")
TERRACOTTA = DEFAULT_CFG.rl("terracotta")
OR_VIEILLI = DEFAULT_CFG.rl("or_vieilli")
TEAL_PROFOND = DEFAULT_CFG.rl("teal_profond")

ACCENT_PIL    = DEFAULT_CFG.pil("accent")
BLANC_PIL     = DEFAULT_CFG.pil("blanc")
TERRACOTTA_PIL = DEFAULT_CFG.pil("terracotta")
OR_VIEILLI_PIL = DEFAULT_CFG.pil("or_vieilli")
TEAL_PROFOND_PIL = DEFAULT_CFG.pil("teal_profond")


def reportlab_crest(cv, cx, cy, scale=1.0):
    ir = 25 * scale
    cv.setStrokeColor(BLANC)
    cv.setLineWidth(2.5 * scale)
    cv.circle(cx, cy, ir, stroke=1, fill=0)
    cv.setStrokeColor(ACCENT)
    cv.setLineWidth(2 * scale)
    margin = ir * 0.1
    segs = 30
    p = cv.beginPath()
    p.moveTo(cx - ir + margin, cy)
    for i in range(segs + 1):
        t = i / segs
        px = cx - ir + margin + t * (ir * 2 - margin * 2)
        py = cy + 3 * scale * math.sin(t * 2 * math.pi * 2.5)
        p.lineTo(px, py)
    cv.drawPath(p, stroke=1, fill=0)
    cv.setFillColor(BLANC)
    cv.setFont("BebasNeue", 11 * scale)
    cv.drawCentredString(cx, cy - ir - 14 * scale, "RIVERS")
    cv.setFont("BebasNeue", 14 * scale)
    cv.drawCentredString(cx, cy + ir + 6 * scale, "ROCK")


def pillow_crest(draw, cx, cy, scale=1.0, wave_color=None):
    ir = 25 * scale
    draw.ellipse([cx - ir, cy - ir, cx + ir, cy + ir], outline=BLANC_PIL, width=max(2, int(2.5 * scale)))
    margin = ir * 0.1
    segs = 30
    wc = wave_color or ACCENT_PIL
    for i in range(segs):
        t = i / segs
        x1 = cx - ir + margin + t * (ir * 2 - margin * 2)
        y1 = cy + 3 * scale * math.sin(t * 2 * math.pi * 2.5)
        x2 = cx - ir + margin + (t + 1 / segs) * (ir * 2 - margin * 2)
        y2 = cy + 3 * scale * math.sin((t + 1 / segs) * 2 * math.pi * 2.5)
        draw.line([(x1, y1), (x2, y2)], fill=wc, width=max(1, int(2 * scale)))
    font = ImageFont.truetype(BEBAS_PATH, max(1, int(11 * scale)))
    bbox = draw.textbbox((0, 0), "RIVERS", font=font)
    tw = bbox[2] - bbox[0]
    draw.text((cx - tw / 2, cy - ir - 14 * scale - bbox[1]), "RIVERS", fill=BLANC_PIL, font=font)
    font2 = ImageFont.truetype(BEBAS_PATH, max(1, int(14 * scale)))
    bbox2 = draw.textbbox((0, 0), "ROCK", font=font2)
    tw2 = bbox2[2] - bbox2[0]
    draw.text((cx - tw2 / 2, cy + ir + 6 * scale - bbox2[1]), "ROCK", fill=BLANC_PIL, font=font2)


def pillow_crest_timbre(draw, cx, cy, scale=1.0, wave_color=None):
    """Timbre disque variant with concentric ring."""
    ir = 25 * scale
    ring_r = ir + 6 * scale
    draw.ellipse([cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r],
                 outline=BLANC_PIL, width=max(1, int(1 * scale)))
    draw.ellipse([cx - ir, cy - ir, cx + ir, cy + ir], outline=BLANC_PIL,
                 width=max(2, int(2.5 * scale)))
    margin = ir * 0.1
    segs = 30
    wc = wave_color or ACCENT_PIL
    for i in range(segs):
        t = i / segs
        x1 = cx - ir + margin + t * (ir * 2 - margin * 2)
        y1 = cy + 3 * scale * math.sin(t * 2 * math.pi * 2.5)
        x2 = cx - ir + margin + (t + 1 / segs) * (ir * 2 - margin * 2)
        y2 = cy + 3 * scale * math.sin((t + 1 / segs) * 2 * math.pi * 2.5)
        draw.line([(x1, y1), (x2, y2)], fill=wc, width=max(1, int(2 * scale)))
    font = ImageFont.truetype(BEBAS_PATH, max(1, int(11 * scale)))
    bbox = draw.textbbox((0, 0), "RIVERS", font=font)
    tw = bbox[2] - bbox[0]
    draw.text((cx - tw / 2, cy - ir - 14 * scale - bbox[1]), "RIVERS", fill=BLANC_PIL, font=font)
    font2 = ImageFont.truetype(BEBAS_PATH, max(1, int(14 * scale)))
    bbox2 = draw.textbbox((0, 0), "ROCK", font=font2)
    tw2 = bbox2[2] - bbox2[0]
    draw.text((cx - tw2 / 2, cy + ir + 6 * scale - bbox2[1]), "ROCK", fill=BLANC_PIL, font=font2)


def pillow_monogramme_rr(draw, cx, cy, scale=1.0, color=None):
    """Draw monogramme RR (two R's intertwined + wave)."""
    c = color or BLANC_PIL
    ir = 20 * scale
    font_size = max(1, int(32 * scale))
    font_path = ANTON_PATH or BEBAS_PATH
    font = ImageFont.truetype(font_path, font_size)
    bbox = draw.textbbox((0, 0), "R", font=font)
    rw = bbox[2] - bbox[0]
    rh = bbox[3] - bbox[1]
    r_offset = rw * 0.4
    draw.text((cx - r_offset - rw / 2, cy - rh / 2 - bbox[1]), "R", fill=c, font=font)
    draw.text((cx + r_offset - rw / 2, cy - rh / 2 - bbox[1]), "R", fill=c, font=font)
    wave_color = OR_VIEILLI_PIL if color is None else (c[0] ^ 255, c[1] ^ 255, c[2] ^ 255)
    segs = 20
    for i in range(segs):
        t = i / segs
        x1 = cx - ir + t * ir * 2
        y1 = cy + 2 * scale * math.sin(t * 2 * math.pi * 2)
        x2 = cx - ir + (t + 1 / segs) * ir * 2
        y2 = cy + 2 * scale * math.sin((t + 1 / segs) * 2 * math.pi * 2)
        draw.line([(x1, y1), (x2, y2)], fill=OR_VIEILLI_PIL, width=max(1, int(2 * scale)))


def pillow_grain_overlay(img, intensity=0.05, seed=None):
    """Add film grain texture to a PIL image."""
    if seed is not None:
        random.seed(seed)
    w, h = img.size
    grain = Image.new("L", (w, h))
    pixels = grain.load()
    for y in range(h):
        for x in range(w):
            pixels[x, y] = int(random.gauss(128, 128 * intensity))
    return Image.composite(img, Image.new("RGB", (w, h), (128, 128, 128)), grain)


def reportlab_crest_vintage(cv, cx, cy, scale=1.0):
    """Timbre variant for ReportLab."""
    ir = 25 * scale
    ring_r = ir + 6 * scale
    cv.setStrokeColor(BLANC)
    cv.setLineWidth(1 * scale)
    cv.circle(cx, cy, ring_r, stroke=1, fill=0)
    cv.setLineWidth(2.5 * scale)
    cv.circle(cx, cy, ir, stroke=1, fill=0)
    cv.setStrokeColor(ACCENT)
    cv.setLineWidth(2 * scale)
    margin = ir * 0.1
    segs = 30
    p = cv.beginPath()
    p.moveTo(cx - ir + margin, cy)
    for i in range(segs + 1):
        t = i / segs
        px = cx - ir + margin + t * (ir * 2 - margin * 2)
        py = cy + 3 * scale * math.sin(t * 2 * math.pi * 2.5)
        p.lineTo(px, py)
    cv.drawPath(p, stroke=1, fill=0)
    cv.setFillColor(BLANC)
    cv.setFont("BebasNeue", 11 * scale)
    cv.drawCentredString(cx, cy - ir - 14 * scale, "RIVERS")
    cv.setFont("BebasNeue", 14 * scale)
    cv.drawCentredString(cx, cy + ir + 6 * scale, "ROCK")


# ── Print production utilities ──

BLEED_MM = 3

def create_bleed_canvas(output_path, trim_w, trim_h):
    """Create a canvas with 3mm bleed. Returns (canvas, trim_w, trim_h, bleed)."""
    from reportlab.pdfgen import canvas as rlcanvas
    from reportlab.lib.units import mm
    bleed = BLEED_MM * mm
    total_w = trim_w + 2 * bleed
    total_h = trim_h + 2 * bleed
    cv = rlcanvas.Canvas(output_path, pagesize=(total_w, total_h))
    cv.translate(bleed, bleed)
    cv.setPageSize((trim_w, trim_h))
    return cv, trim_w, trim_h, bleed


def save_with_crop_marks(cv, trim_w, trim_h, bleed):
    """Draw crop marks and save the canvas."""
    from reportlab.lib.colors import Color
    mark_len = 5
    cv.saveState()
    cv.setStrokeColor(Color(0, 0, 0, alpha=0.5))
    cv.setLineWidth(0.5)

    for cx, cy, dx, dy in [(0, 0, 1, 1), (trim_w, 0, -1, 1),
                            (0, trim_h, 1, -1), (trim_w, trim_h, -1, -1)]:
        cv.line(cx - bleed, cy, cx - bleed + dx * mark_len, cy)
        cv.line(cx, cy - bleed, cx, cy - bleed + dy * mark_len)

    cv.restoreState()
    cv.showPage()
    cv.save()


def draw_qr_reportlab(cv, cx, cy, size, url="https://clucet.github.io/rivers_rock/setlist/", fill_color=None):
    """Draw a QR code at position using ReportLab."""
    try:
        import qrcode
        from reportlab.lib.colors import HexColor
        qr = qrcode.QRCode(box_size=3, border=1)
        qr.add_data(url)
        qr.make(fit=True)
        matrix = qr.get_matrix()
        n = len(matrix)
        cell = size / n
        fc = fill_color or HexColor("#1A3A5C")
        cv.setFillColor(fc)
        for y in range(n):
            for x in range(n):
                if matrix[y][x]:
                    cv.rect(cx - size / 2 + x * cell,
                            cy + size / 2 - y * cell - cell,
                            cell, cell, stroke=0, fill=1)
    except ImportError:
        cv.setFillColor(HexColor("#CCCCCC"))
        cv.rect(cx - size / 2, cy - size / 2, size, size, stroke=0, fill=1)
        cv.setFillColor(HexColor("#333333"))
        cv.setFont("Helvetica", size * 0.12)
        cv.drawCentredString(cx, cy - size * 0.06, "QR")


def draw_qr_pillow(draw, cx, cy, size, url="https://clucet.github.io/rivers_rock/setlist/", fill_color=None):
    """Draw a QR code at position using Pillow."""
    try:
        import qrcode
        from PIL import Image
        qr = qrcode.QRCode(box_size=2, border=1)
        qr.add_data(url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color=fill_color or (0, 0, 0), back_color=(255, 255, 255))
        qr_img = qr_img.resize((int(size), int(size)), Image.NEAREST)
        return qr_img
    except ImportError:
        return None


def _resolve_font_ponts():
    """Resolve Ponts & Lumière font paths."""
    return {
        "TEKO": _resolve_font("hero", PONTS_LUMIERE),
        "RALEWAY": _resolve_font("body", PONTS_LUMIERE),
        "DMMONO": _resolve_font("data", PONTS_LUMIERE),
    }


# ── Proposition-specific monogramme functions ──

def pillow_bridge_silhouette(draw, cx, cy, scale=1.0):
    """Ponts & Lumière bridge silhouette (no text) for avatar/watermark."""
    w = 60 * scale
    for arc_offset, c in [(0, (224, 225, 221)), (-10, (255, 183, 3))]:
        for i in range(30):
            t0, t1 = i / 30, (i + 1) / 30
            x1 = cx - w + t0 * w * 2
            y1 = cy + arc_offset - 30 * scale * ((t0 - 0.5) ** 2 - 0.25)
            x2 = cx - w + t1 * w * 2
            y2 = cy + arc_offset - 30 * scale * ((t1 - 0.5) ** 2 - 0.25)
            draw.line([(x1, y1), (x2, y2)], fill=c, width=max(1, int(2 * scale)))
    draw.ellipse([cx - 4 * scale, cy - 7 * scale - 4 * scale,
                  cx + 4 * scale, cy - 7 * scale + 4 * scale],
                 fill=(255, 183, 3))


def pillow_monogramme_wave(draw, cx, cy, scale=1.0):
    """Fluid Wave monogramme: RR + bezier wave in ambre."""
    font = ImageFont.truetype(NUNITO_PATH or BEBAS_PATH, max(8, int(28 * scale)))
    bbox = draw.textbbox((0, 0), "RR", font=font)
    tw = bbox[2] - bbox[0]
    draw.text((cx - tw / 2, cy - bbox[1]), "RR", fill=BLANC_PIL, font=font)
    import math
    for i in range(15):
        t0, t1 = i / 14, (i + 1) / 14
        draw.line([(cx - 15 * scale + t0 * 30 * scale, cy + 8 * scale + 4 * scale * math.sin(t0 * 6)),
                   (cx - 15 * scale + t1 * 30 * scale, cy + 8 * scale + 4 * scale * math.sin(t1 * 6))],
                  fill=(212, 168, 67), width=max(1, int(2 * scale)))


def pillow_hexagon_monogramme(draw, cx, cy, scale=1.0):
    """Rock Brut hexagon monogramme: hexagon + RR + chevron."""
    import math
    r = 20 * scale
    pts = [(cx + r * math.cos(math.radians(60 * i - 30)),
            cy + r * math.sin(math.radians(60 * i - 30))) for i in range(6)]
    for i in range(6):
        draw.line([pts[i], pts[(i + 1) % 6]], fill=(255, 59, 0), width=max(2, int(3 * scale)))
    inner = [(cx + (p[0] - cx) * 0.8, cy + (p[1] - cy) * 0.8) for p in pts]
    for i in range(6):
        draw.line([inner[i], inner[(i + 1) % 6]], fill=BLANC_PIL, width=max(1, int(1.5 * scale)))
    font = ImageFont.truetype(ANTON_PATH or BEBAS_PATH, max(8, int(16 * scale)))
    bbox = draw.textbbox((0, 0), "RR", font=font)
    tw = bbox[2] - bbox[0]
    draw.text((cx - tw / 2, cy - bbox[1] * 0.5), "RR", fill=BLANC_PIL, font=font)
    draw.line([(cx - r * 0.6, cy + r * 0.5), (cx, cy + r * 0.2), (cx + r * 0.6, cy + r * 0.5)],
              fill=BLANC_PIL, width=max(1, int(2 * scale)))


def pillow_neon_logo(draw, cx, cy, scale=1.0):
    """Neon Nights: circle + lightning bolts."""
    r = 20 * scale
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(0, 245, 255), width=max(1, int(2 * scale)))
    for dx, dy, dx2, dy2 in [(r*0.7, -r*0.3, r*1.6, -r*0.8), (r*0.9, r*0.2, r*1.4, r*1.0),
                              (-r*0.7, -r*0.5, -r*1.5, -r*0.2), (-r*0.8, r*0.3, -r*1.3, r*0.9)]:
        draw.line([(cx+dx, cy+dy), (cx+dx2, cy+dy2)], fill=(255, 45, 149), width=max(1, int(2*scale)))
    draw.ellipse([cx - r*0.25, cy - r*0.25, cx + r*0.25, cy + r*0.25], fill=(255, 45, 149))


def pillar_neon_logo(cv, cx, cy, scale=1.0):
    """Neon Nights ReportLab: circle + lightning bolts."""
    from reportlab.lib.colors import Color
    r = 20 * scale
    cv.setStrokeColor(Color(0, 245/255, 1))
    cv.setLineWidth(2 * scale)
    cv.circle(cx, cy, r, stroke=1, fill=0)
    cv.setStrokeColor(Color(1, 45/255, 149/255))
    cv.setLineWidth(2 * scale)
    for dx, dy, dx2, dy2 in [(r*0.7, -r*0.3, r*1.6, -r*0.8), (r*0.9, r*0.2, r*1.4, r*1.0),
                              (-r*0.7, -r*0.5, -r*1.5, -r*0.2), (-r*0.8, r*0.3, -r*1.3, r*0.9)]:
        cv.line(cx+dx, cy+dy, cx+dx2, cy+dy2)
    cv.setFillColor(Color(1, 45/255, 149/255))
    cv.circle(cx, cy, r*0.25, stroke=0, fill=1)


def pillow_sun_logo(draw, cx, cy, scale=1.0):
    """Sable & Bronze: sun circle with rays."""
    r = 20 * scale
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(181, 131, 90))
    draw.ellipse([cx - r - 3*scale, cy - r - 3*scale, cx + r + 3*scale, cy + r + 3*scale],
                 outline=(255, 255, 255, 100), width=max(1, int(scale)))
    for i in range(8):
        a = math.radians(45 * i)
        pts = [(cx + r*0.6*math.cos(a), cy + r*0.6*math.sin(a)),
               (cx + r*2.0*math.cos(a-0.15), cy + r*2.0*math.sin(a-0.15)),
               (cx + r*2.0*math.cos(a+0.15), cy + r*2.0*math.sin(a+0.15))]
        draw.polygon(pts, fill=(181, 131, 90))


def pillar_sun_logo(cv, cx, cy, scale=1.0):
    """Sable & Bronze ReportLab: sun circle with rays."""
    from reportlab.lib.colors import Color
    r = 20 * scale
    cv.setFillColor(Color(181/255, 131/255, 90/255))
    cv.circle(cx, cy, r, stroke=0, fill=1)
    cv.setStrokeColor(Color(1, 1, 1, alpha=0.4))
    cv.setLineWidth(0.5 * scale)
    cv.circle(cx, cy, r + 3*scale, stroke=1, fill=0)
    for i in range(8):
        a = math.radians(45 * i)
        pts = [(cx + r*0.6*math.cos(a), cy + r*0.6*math.sin(a)),
               (cx + r*2.0*math.cos(a-0.2), cy + r*2.0*math.sin(a-0.2)),
               (cx + r*2.0*math.cos(a+0.2), cy + r*2.0*math.sin(a+0.2))]
        cv.setFillColor(Color(181/255, 131/255, 90/255))
        p = cv.beginPath()
        p.moveTo(pts[0][0], pts[0][1])
        p.lineTo(pts[1][0], pts[1][1])
        p.lineTo(pts[2][0], pts[2][1])
        p.close()
        cv.drawPath(p, fill=1, stroke=0)
