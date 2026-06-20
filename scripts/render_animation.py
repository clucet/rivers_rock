#!/usr/bin/env python3
"""Render Rivers Rock animated logo as MP4 via Pillow + FFmpeg."""

import os, math, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "pdf", "templates")
OUTPUT = os.path.join(OUT_DIR, "logo-animated.mp4")
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 540, 960
FPS = 30
DURATION = 6
FRAMES = FPS * DURATION

BLEU = (26, 58, 92)
VERT = (74, 155, 142)
ACCENT = (232, 93, 58)
BLANC = (255, 255, 255)

BEBAS = os.path.expanduser("~/Library/Fonts/BebasNeue-Regular.ttf")


def lerp(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def frame(t):
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)

    for i in range(100):
        ty = i / 99
        color = lerp(BLEU, VERT, ty)
        draw.rectangle([0, i * H / 100, W, (i + 1) * H / 100], fill=color)

    cx, cy = W / 2, 280
    r = 130
    scale = 1 + 0.015 * math.sin(t * 2 * math.pi / 4)
    cr = r * scale
    draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], outline=BLANC, width=6)

    margin = r * 0.08
    amp = 12 * math.sin(t * 2 * math.pi / 3)
    segs = 30
    for i in range(segs):
        ti = i / segs
        x1 = cx - r + margin + ti * (r * 2 - margin * 2)
        y1 = cy + amp * math.sin(ti * 2 * math.pi * 2.5)
        x2 = cx - r + margin + (ti + 1 / segs) * (r * 2 - margin * 2)
        y2 = cy + amp * math.sin((ti + 1 / segs) * 2 * math.pi * 2.5)
        draw.line([(x1, y1), (x2, y2)], fill=ACCENT, width=5)

    fade = min(1, max(0, (t - 1) / 1.5))
    if fade > 0:
        img = img.convert("RGBA")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(BEBAS, 72)
        bbox = draw.textbbox((0, 0), "RIVERS ROCK", font=font)
        tw = bbox[2] - bbox[0]
        alpha = int(255 * fade)
        draw.text(((W - tw) / 2, 380), "RIVERS ROCK", fill=(255, 255, 255, alpha), font=font)
        img = img.convert("RGB")

    return img


tmpdir = tempfile.mkdtemp()
for i in range(FRAMES):
    t = i / FPS
    f = frame(t)
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
