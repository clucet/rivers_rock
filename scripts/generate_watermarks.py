#!/usr/bin/env python3
"""Generate video watermark overlays for all 4 propositions."""

import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image, ImageDraw, ImageFont
from logoutils import BEBAS_PATH, ANTON_PATH, NUNITO_PATH, INTERTIGHT_PATH, pillow_monogramme_rr
from palette import BASE, FLUID_WAVE, ROCK_BRUT, SCENE_VINTAGE, PONTS_LUMIERE, NEON_NIGHTS, SABLE_BRONZE

OUT = os.path.join(os.path.dirname(__file__), "..", "propositions")


def make_watermark(cfg, dirname, sizes=[(200, 200), (100, 100), (50, 50)]):
    """Generate semi-transparent watermark PNGs for a proposition."""
    for w, h in sizes:
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        if cfg.name == "Fluid Wave":
            # Wave symbol
            offset = w // 2
            for i in range(20):
                t = i / 19
                x1 = offset - 20 + t * 40
                y1 = h // 2 + 6 * (t * 2 * 3.14 * 2)
                x2 = offset - 20 + ((i + 1) / 19) * 40
                y2 = h // 2 + 6 * (((i + 1) / 19) * 2 * 3.14 * 2)
                draw.line([(x1, y1), (x2, y2)], fill=(212, 168, 67, 77), width=max(1, w // 40))
        elif cfg.name == "Rock Brut":
            hexagon_logo(draw, w // 2, h // 2, min(w, h) * 0.35, (255, 59, 0, 77), (255, 255, 255, 77))
        elif cfg.name == "Ponts & Lumière":
            c = (255, 183, 3, 77)
            for arc_y in [h * 0.3, h * 0.38]:
                for i in range(w - 1):
                    t0 = i / w
                    t1 = (i + 1) / w
                    y0 = arc_y - h * 0.25 * ((t0 - 0.5) ** 2 - 0.25) * 4
                    y1 = arc_y - h * 0.25 * ((t1 - 0.5) ** 2 - 0.25) * 4
                    draw.line([(i, y0), (i + 1, y1)], fill=c, width=1)
            draw.ellipse([w // 2 - 5, int(h * 0.3) - 5, w // 2 + 5, int(h * 0.3) + 5], fill=(224, 225, 221, 100))
        elif cfg.name == "Neon Nights":
            c = (255, 45, 149, 77)
            draw.ellipse([w//2 - 8, h//2 - 8, w//2 + 8, h//2 + 8], outline=c, width=2)
            draw.line([(w//2 + 8, h//2 - 4), (w//2 + 20, h//2 - 8)], fill=c, width=2)
            draw.line([(w//2 + 8, h//2 + 4), (w//2 + 18, h//2 + 10)], fill=c, width=2)
            draw.line([(w//2 - 8, h//2 - 4), (w//2 - 20, h//2 - 8)], fill=c, width=2)
            draw.line([(w//2 - 8, h//2 + 4), (w//2 - 18, h//2 + 10)], fill=c, width=2)
        elif cfg.name == "Sable & Bronze":
            r = min(w, h) * 0.15
            draw.ellipse([w//2 - r, h//2 - r, w//2 + r, h//2 + r], fill=(181, 131, 90, 100))
            for i in range(8):
                a = math.radians(45 * i)
                pts = [(w//2 + r * 0.6 * math.cos(a), h//2 + r * 0.6 * math.sin(a)),
                       (w//2 + r * 2.0 * math.cos(a - 0.15), h//2 + r * 2.0 * math.sin(a - 0.15)),
                       (w//2 + r * 2.0 * math.cos(a + 0.15), h//2 + r * 2.0 * math.sin(a + 0.15))]
                draw.polygon(pts, fill=(204, 107, 73, 80))
        elif cfg.name == "Scène & Vintage" or cfg.name == "Originale":
            # Monogramme RR
            scale = w / 80
            pillow_monogramme_rr(draw, w // 2, h // 2, scale, color=(255, 255, 255, 77))

        base_path = os.path.join(OUT, dirname, "assets", "templates")
        os.makedirs(base_path, exist_ok=True)
        path = os.path.join(base_path, f"watermark-{w}x{h}.png")
        img.save(path)
        print(f"  {path}")


def hexagon_logo(draw, cx, cy, r, color_outer, color_inner):
    """Simplified hexagon for watermark."""
    pts = []
    for i in range(6):
        a = math.radians(60 * i - 30)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    for i in range(6):
        draw.line([pts[i], pts[(i + 1) % 6]], fill=color_outer, width=max(1, int(r / 10)))
    inner = [(cx + (pt[0] - cx) * 0.85, cy + (pt[1] - cy) * 0.85) for pt in pts]
    for i in range(6):
        draw.line([inner[i], inner[(i + 1) % 6]], fill=color_inner, width=max(1, int(r / 15)))


if __name__ == "__main__":
    configs = [
        (BASE, "00-originale"),
        (FLUID_WAVE, "01-fluid-wave"),
        (ROCK_BRUT, "02-rock-brut"),
        (SCENE_VINTAGE, "03-scene-vintage"),
        (PONTS_LUMIERE, "04-ponts-lumiere"),
        (NEON_NIGHTS, "05-neon-nights"),
        (SABLE_BRONZE, "06-sable-bronze"),
    ]
    for cfg, dirname in configs:
        print(f"Watermarks pour {cfg.name}...")
        make_watermark(cfg, dirname)
    print("✅ Watermarks générés")
