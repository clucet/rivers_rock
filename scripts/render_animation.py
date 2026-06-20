#!/usr/bin/env python3
"""Render Rivers Rock animated logo as MP4 — matching generate_animated_logo.html exactly."""

import os, math, subprocess, tempfile, sys, random
sys.path.insert(0, os.path.dirname(__file__))
from logoutils import BEBAS_PATH
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "pdf", "templates")
OUTPUT = os.path.join(OUT_DIR, "logo-animated.mp4")
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 540, 960
FPS = 30
DURATION = 7
FRAMES = FPS * DURATION

BLEU = (26, 58, 92)
VERT = (74, 155, 142)
ACCENT = (232, 93, 58)
BLANC = (255, 255, 255)

S = 0.5
CX, CY = W // 2, H // 2

FONT_32 = ImageFont.truetype(BEBAS_PATH, max(1, int(32 * S + 0.5)))
FONT_26 = ImageFont.truetype(BEBAS_PATH, max(1, int(26 * S + 0.5)))

PARTICLES = []
for _ in range(25):
    PARTICLES.append({
        'x': random.random() * W, 'y': random.random() * H,
        's': random.random() * 1 + 0.5, 'a': random.random() * 0.08 + 0.02,
    })

RIVERS_X = [-60, -36, -12, 12, 36, 60]
RIVERS_STARTS = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5]
ROCK_X = [-30, -10, 10, 30]
ROCK_STARTS = [1.9, 2.0, 2.1, 2.2]


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


def draw_wave(draw, t, alpha):
    wave_t = t % 3
    angle = wave_t / 3 * 2 * math.pi
    offset = math.sin(angle) * 20
    pts = []
    segs = 15
    for i in range(segs):
        x, y = qbezier((-72, 0), (-40, -offset), (0, 0), i / segs)
        pts.append((CX + x * S, CY - y * S))
    for i in range(1, segs + 1):
        x, y = qbezier((0, 0), (40, offset), (72, 0), i / segs)
        pts.append((CX + x * S, CY - y * S))
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i + 1]], fill=(ACCENT[0], ACCENT[1], ACCENT[2], alpha), width=max(1, int(4 * S + 0.5)))


def make_frame(t):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    for i in range(100):
        ty = i / 99
        color = lerp(BLEU, VERT, ty)
        draw.rectangle([0, i * H / 100, W, (i + 1) * H / 100], fill=color + (255,))

    for p in PARTICLES:
        py = (p['y'] - t * FPS * 0.15) % H
        draw.ellipse([p['x'] - p['s'], py - p['s'], p['x'] + p['s'], py + p['s']],
                     fill=(255, 255, 255, int(255 * p['a'])))

    outer_r = 165 * S
    draw.ellipse([CX - outer_r, CY - outer_r, CX + outer_r, CY + outer_r],
                 outline=(255, 255, 255, 64), width=max(1, int(2 * S + 0.5)))

    inner_prog = min(1, max(0, (t - 0.3) / 0.8))
    if inner_prog > 0:
        inner_r = 80 * S
        end_a = -90 + 360 * inner_prog
        draw.arc([CX - inner_r, CY - inner_r, CX + inner_r, CY + inner_r],
                 -90, end_a, fill=(255, 255, 255, 255), width=max(1, int(5 * S + 0.5)))

    wave_prog = min(1, max(0, (t - 1.5) / 0.5))
    if wave_prog > 0:
        draw_wave(draw, t, int(255 * wave_prog))

    for ch, sx, start in zip("RIVERS", RIVERS_X, RIVERS_STARTS):
        prog = min(1, max(0, (t - start) / 0.4))
        if prog > 0:
            ep = ease_out(prog)
            ay = arc_y(sx)
            tx = CX + sx * S
            ty = CY + ay * S
            sy = ty - 40 * S * (1 - ep)
            draw.text((tx, sy), ch, fill=(255, 255, 255, int(255 * ep)), font=FONT_32, anchor="mm")

    for ch, sx, start in zip("ROCK", ROCK_X, ROCK_STARTS):
        prog = min(1, max(0, (t - start) / 0.4))
        if prog > 0:
            ep = ease_out(prog)
            ay = arc_y(sx)
            tx = CX + sx * S + 200 * S * (1 - ep)
            ty = CY - ay * S
            draw.text((tx, ty), ch, fill=(255, 255, 255, int(255 * ep)), font=FONT_26, anchor="mm")

    return img.convert("RGB")


if __name__ == "__main__":
    tmpdir = tempfile.mkdtemp()
    for i in range(FRAMES):
        t = i / FPS
        f = make_frame(t)
        f.save(os.path.join(tmpdir, f"frame_{i:04d}.png"), "PNG")

    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(FPS),
        "-i", os.path.join(tmpdir, "frame_%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-vf", "scale=1080:1920:flags=lanczos",
        OUTPUT
    ], capture_output=True)

    for f in os.listdir(tmpdir):
        os.remove(os.path.join(tmpdir, f))
    os.rmdir(tmpdir)

    print(f"MP4 généré : {OUTPUT}")
