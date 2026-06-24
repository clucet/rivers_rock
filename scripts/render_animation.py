#!/usr/bin/env python3
"""Render Rivers Rock animated logo as MP4 — Scene & Vintage design.
Usage: python3 scripts/render_animation.py [--render-scale 0.5] [--output path]"""

import os, math, subprocess, tempfile, sys, random, argparse
sys.path.insert(0, os.path.dirname(__file__))
from logoutils import BEBAS_PATH, ANTON_PATH
from palette import SCENE_VINTAGE as CFG_BASE
from palette import set_active
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "pdf", "templates")
OUTPUT = os.path.join(OUT_DIR, "logo-animated.mp4")
os.makedirs(OUT_DIR, exist_ok=True)

parser = argparse.ArgumentParser()
parser.add_argument("--render-scale", type=float, default=1.0, help="Render scale (0.5=540x960, 1.0=1080x1920)")
parser.add_argument("--output", default=OUTPUT)
parser.add_argument("--config", default="scene-vintage",
                    choices=["scene-vintage", "fluid-wave", "rock-brut", "originale", "ponts-lumiere", "neon-nights", "sable-bronze"])
args = parser.parse_args()

CFG = set_active(args.config) if args.config else CFG_BASE

SCALE = args.render_scale
OUTPUT = args.output

W, H = int(1080 * SCALE), int(1920 * SCALE)
FPS = 30
DURATION = 7
FRAMES = FPS * DURATION
CX, CY = W // 2, H // 2

BLEU = CFG.pil("bleu_seine")
TEAL = CFG.pil("teal_profond")
ACCENT = CFG.pil("accent")
OR = CFG.pil("or_vieilli")
BLANC = (255, 255, 255)

FONT_RIVERS = ImageFont.truetype(ANTON_PATH, max(8, int(34 * SCALE)))
FONT_ROCK = ImageFont.truetype(BEBAS_PATH, max(8, int(26 * SCALE)))

PARTICLES = []
for _ in range(int(35 * SCALE)):
    PARTICLES.append({
        'x': random.random() * W, 'y': random.random() * H,
        's': random.random() * 2 + 0.5, 'a': random.random() * 0.06 + 0.01,
    })

RIVERS_INFO = [("R", -60, 1.0), ("I", -36, 1.1), ("V", -12, 1.2),
               ("E", 12, 1.3), ("R", 36, 1.4), ("S", 60, 1.5)]
ROCK_INFO = [("R", -30, 1.9), ("O", -10, 2.0), ("C", 10, 2.1), ("K", 30, 2.2)]


def arc_y(x, r=80):
    return math.sqrt(max(0, r * r - x * x))


def lerp(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def ease_out(t):
    return 1 - (1 - t) * (1 - t)


def qbezier(p0, p1, p2, t):
    return (
        (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0],
        (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1],
    )


def make_frame(t):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    # Radial gradient background with flare
    for i in range(200):
        rt = i / 199
        r = math.sqrt(CX**2 + CY**2) * rt
        if rt < 0.15:
            c = lerp(OR, ACCENT, rt / 0.15)
        elif rt < 0.4:
            c = lerp(ACCENT, BLEU, (rt - 0.15) / 0.25)
        else:
            c = lerp(BLEU, TEAL, (rt - 0.4) / 0.6)
        draw.ellipse([CX - r, CY - r, CX + r, CY + r], fill=c + (255,))

    # Particle overlay
    for p in PARTICLES:
        py = (p['y'] - t * FPS * 0.35) % H
        draw.ellipse([p['x'] - p['s'], py - p['s'], p['x'] + p['s'], py + p['s']],
                     fill=ACCENT + (int(255 * p['a']),))

    # Outer circle (timbre ring) — dashed simulated
    outer_r = 165 * SCALE
    timbre_prog = min(1, max(0, (t - 0.6) / 0.6))
    if timbre_prog > 0:
        for ang in range(0, 360 * timbre_prog, 8):
            a1 = math.radians(ang)
            a2 = math.radians(min(ang + 4, 360 * timbre_prog))
            draw.arc([CX - outer_r, CY - outer_r, CX + outer_r, CY + outer_r],
                     ang, ang + 4, fill=(255, 255, 255, 38), width=max(1, int(1.5 * SCALE)))

    # Inner circle with neon glow (draw multiple offsets for glow)
    inner_prog = min(1, max(0, (t - 0.3) / 0.8))
    if inner_prog > 0:
        inner_r = 80 * SCALE
        # Glow layers
        for glow_r in range(5, 0, -1):
            glow_a = int(60 * (1 - glow_r / 5))
            draw.arc([CX - inner_r - glow_r * 2, CY - inner_r - glow_r * 2,
                      CX + inner_r + glow_r * 2, CY + inner_r + glow_r * 2],
                     -90, -90 + 360 * inner_prog,
                     fill=ACCENT + (glow_a,), width=3)
        # Main white circle
        draw.arc([CX - inner_r, CY - inner_r, CX + inner_r, CY + inner_r],
                 -90, -90 + 360 * inner_prog,
                 fill=BLANC + (255,), width=max(2, int(5 * SCALE)))

    # Wave with neon glow
    wave_prog = min(1, max(0, (t - 1.5) / 0.5))
    if wave_prog > 0:
        wave_t = t % 3
        angle = wave_t / 3 * 2 * math.pi
        offset = math.sin(angle) * 20
        pts = []
        segs = 15
        for i in range(segs):
            x, y = qbezier((-72, 0), (-40, -offset), (0, 0), i / segs)
            pts.append((CX + x * SCALE, CY - y * SCALE))
        for i in range(1, segs + 1):
            x, y = qbezier((0, 0), (40, offset), (72, 0), i / segs)
            pts.append((CX + x * SCALE, CY - y * SCALE))
        alpha = int(255 * wave_prog)
        # Glow
        for gl in range(3, 0, -1):
            for i in range(len(pts) - 1):
                draw.line([pts[i], pts[i + 1]], fill=ACCENT + (alpha // 3,),
                          width=max(1, int((4 + gl * 3) * SCALE)))
        for i in range(len(pts) - 1):
            draw.line([pts[i], pts[i + 1]], fill=ACCENT + (alpha,),
                      width=max(1, int(4 * SCALE)))

    # RIVERS (above circle, Anton font)
    for ch, sx, start in RIVERS_INFO:
        prog = min(1, max(0, (t - start) / 0.4))
        if prog > 0:
            ep = ease_out(prog)
            ay = arc_y(sx)
            tx = CX + sx * SCALE
            ty = CY + ay * SCALE
            sy = ty - 40 * SCALE * (1 - ep)
            # Glow
            for gl in range(3, 0, -1):
                draw.text((tx + gl, sy), ch, fill=ACCENT + (40,), font=FONT_RIVERS, anchor="mm")
                draw.text((tx - gl, sy), ch, fill=ACCENT + (40,), font=FONT_RIVERS, anchor="mm")
            draw.text((tx, sy), ch, fill=BLANC + (int(255 * ep),), font=FONT_RIVERS, anchor="mm")

    # ROCK (below circle, Bebas Neue, slide from right)
    for ch, sx, start in ROCK_INFO:
        prog = min(1, max(0, (t - start) / 0.4))
        if prog > 0:
            ep = ease_out(prog)
            ay = arc_y(sx)
            tx = CX + sx * SCALE + 200 * SCALE * (1 - ep)
            ty = CY - ay * SCALE
            draw.text((tx, ty), ch, fill=BLANC + (int(255 * ep),), font=FONT_ROCK, anchor="mm")

    return img.convert("RGB")


def add_grain(img, intensity=0.04):
    """Add film grain to the final frame."""
    w, h = img.size
    grain = Image.new("L", (w, h))
    pixels = grain.load()
    for y in range(h):
        for x in range(w):
            pixels[x, y] = int(random.gauss(128, 128 * intensity))
    return Image.composite(img, Image.new("RGB", (w, h), (128, 128, 128)), grain)


if __name__ == "__main__":
    tmpdir = tempfile.mkdtemp()
    print(f"Rendu de {FRAMES} frames à {W}x{H}...")
    for i in range(FRAMES):
        t = i / FPS
        f = make_frame(t)
        if SCALE < 1.0:
            f = f.resize((1080, 1920), Image.LANCZOS)
        f = add_grain(f, 0.03)
        f.save(os.path.join(tmpdir, f"frame_{i:04d}.png"), "PNG")
        if i % 30 == 0:
            print(f"  Frame {i}/{FRAMES}")

    print("Assemblage MP4...")
    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(FPS),
        "-i", os.path.join(tmpdir, "frame_%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-preset", "medium", "-crf", "18",
        OUTPUT
    ], capture_output=True)

    for f in os.listdir(tmpdir):
        os.remove(os.path.join(tmpdir, f))
    os.rmdir(tmpdir)

    print(f"MP4 généré : {OUTPUT}")

    # Also generate a high-quality still frame
    still = make_frame(3.0)
    still = add_grain(still, 0.03)
    still_path = OUTPUT.replace(".mp4", ".png")
    still.save(still_path, "PNG")
    print(f"Still frame : {still_path}")
