#!/usr/bin/env python3
"""Shared Rivers Rock crest drawing functions for ReportLab and Pillow."""

import math, os, urllib.request, zipfile, tempfile
from reportlab.lib.colors import HexColor, Color
from PIL import ImageFont


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


BEBAS_PATH = _find_font("BebasNeue-Regular.ttf")
if not BEBAS_PATH:
    BEBAS_PATH = _ensure_font(
        "BebasNeue-Regular.ttf",
        "https://github.com/google/fonts/raw/main/ofl/bebasneue/BebasNeue-Regular.ttf",
    )

MONTSERRAT_PATH = (
    _find_font("Montserrat-VariableFont_wght.ttf")
    or _find_font("Montserrat-VF.ttf")
)
if not MONTSERRAT_PATH:
    MONTSERRAT_PATH = _ensure_font(
        "Montserrat-VF.ttf",
        "https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat-VariableFont_wght.ttf",
    )

ACCENT = HexColor("#E85D3A")
BLANC = HexColor("#FFFFFF")
ACCENT_PIL = (232, 93, 58)
BLANC_PIL = (255, 255, 255)


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
    cv.setFont("BebasNeue", 14 * scale)
    cv.drawCentredString(cx, cy + ir + 6 * scale, "RIVERS")
    cv.setFont("BebasNeue", 11 * scale)
    cv.drawCentredString(cx, cy - ir - 14 * scale, "ROCK")


def pillow_crest(draw, cx, cy, scale=1.0):
    ir = 25 * scale
    draw.ellipse([cx - ir, cy - ir, cx + ir, cy + ir], outline=BLANC_PIL, width=max(2, int(2.5 * scale)))
    margin = ir * 0.1
    segs = 30
    for i in range(segs):
        t = i / segs
        x1 = cx - ir + margin + t * (ir * 2 - margin * 2)
        y1 = cy + 3 * scale * math.sin(t * 2 * math.pi * 2.5)
        x2 = cx - ir + margin + (t + 1 / segs) * (ir * 2 - margin * 2)
        y2 = cy + 3 * scale * math.sin((t + 1 / segs) * 2 * math.pi * 2.5)
        draw.line([(x1, y1), (x2, y2)], fill=ACCENT_PIL, width=max(1, int(2 * scale)))
    font = ImageFont.truetype(BEBAS_PATH, max(1, int(14 * scale)))
    bbox = draw.textbbox((0, 0), "RIVERS", font=font)
    tw = bbox[2] - bbox[0]
    draw.text((cx - tw / 2, cy + ir + 6 * scale - bbox[1]), "RIVERS", fill=BLANC_PIL, font=font)
    font2 = ImageFont.truetype(BEBAS_PATH, max(1, int(11 * scale)))
    bbox2 = draw.textbbox((0, 0), "ROCK", font=font2)
    tw2 = bbox2[2] - bbox2[0]
    draw.text((cx - tw2 / 2, cy - ir - 14 * scale - bbox2[1]), "ROCK", fill=BLANC_PIL, font=font2)
