#!/usr/bin/env python3
"""Generate Rivers Rock stage plot (A4 landscape, tech sheet for sound engineer)."""

import os, math, sys
sys.path.insert(0, os.path.dirname(__file__))
from logoutils import BEBAS_PATH, MONTSERRAT_PATH
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

OUTPUT = os.path.join(os.path.dirname(__file__), "..", "pdf", "stage-plot.pdf")

BLEU_SEINE = HexColor("#1A3A5C")
ACCENT = HexColor("#E85D3A")
NOIR = HexColor("#222222")
GRIS = HexColor("#888888")
BLANC = HexColor("#FFFFFF")

pdfmetrics.registerFont(TTFont("BebasNeue", BEBAS_PATH))
pdfmetrics.registerFont(TTFont("Montserrat", MONTSERRAT_PATH))

W, H = A4[1], A4[0]
CX = W / 2


def draw_stage(cv):
    cv.setFillColor(Color(0.95, 0.93, 0.90))
    cv.rect(0, 0, W, H, stroke=0, fill=1)

    cv.setFillColor(NOIR)
    cv.setFont("BebasNeue", 26)
    cv.drawCentredString(CX, H - 45, "FICHE TECHNIQUE — RIVERS ROCK")
    cv.setFont("Montserrat", 10)
    cv.drawCentredString(CX, H - 68, "Stage Plot / Input List")
    cv.setStrokeColor(Color(0, 0, 0, alpha=0.15))
    cv.setLineWidth(0.5)
    cv.line(CX - 140, H - 78, CX + 140, H - 78)

    sx, sy = 30, 320
    sw, sh = W - 60, 180

    cv.setStrokeColor(NOIR)
    cv.setLineWidth(2)
    cv.rect(sx, sy, sw, sh, stroke=1, fill=0)
    cv.setFont("Montserrat", 7)
    cv.setFillColor(Color(0, 0, 0, alpha=0.3))
    cv.drawCentredString(CX, sy + sh + 4, "SCÈNE (vue de face — cordon rouge face public)")

    mon_w, mon_h = 50, 16
    mon_positions = [
        (sx + 20 + mon_w / 2, sy + 20 + mon_h / 2),
        (sx + sw - 20 - mon_w / 2, sy + 20 + mon_h / 2),
        (sx + 20 + mon_w / 2, sy + sh - 20 - mon_h / 2),
        (sx + sw - 20 - mon_w / 2, sy + sh - 20 - mon_h / 2),
    ]

    for i, (mx, my) in enumerate(mon_positions):
        cv.setFillColor(HexColor("#333333"))
        cv.roundRect(mx - mon_w / 2, my - mon_h / 2, mon_w, mon_h, 3, stroke=0, fill=1)
        cv.setFillColor(BLANC)
        cv.setFont("Montserrat", 7)
        cv.drawCentredString(mx, my - 2.5, f"MON {i+1}")

    positions = [
        ("Rosaria\nBatterie / Chœur", CX, sy + sh * 0.30),
        ("Nicolas\nGuitare", sx + sw * 0.20, sy + sh * 0.58),
        ("Christophe\nBasse / Chœur", sx + sw * 0.50, sy + sh * 0.58),
        ("Virginie\nChant", sx + sw * 0.30, sy + sh * 0.78),
        ("David\nGuitare / Chant", sx + sw * 0.70, sy + sh * 0.78),
    ]

    for name, px, py in positions:
        cv.setFillColor(ACCENT)
        by = py
        for line in name.split("\n"):
            if line.startswith(("Rose", "Nico", "Chri", "Virg", "David")):
                cv.setFont("Montserrat", 8)
            else:
                cv.setFont("Montserrat", 7)
                cv.setFillColor(Color(0, 0, 0, alpha=0.6))
            cv.drawCentredString(px, by, line)
            by -= 10
            cv.setFillColor(ACCENT)

    cv.setStrokeColor(Color(0, 0, 0, alpha=0.2))
    cv.setLineWidth(0.5)
    cv.rect(sx, sy, sw, sh, stroke=1, fill=0)

    input_list = [
        ("1", "Kick"),
        ("2", "Snare"),
        ("3", "HH"),
        ("4", "Tom 1"),
        ("5", "Tom 2"),
        ("6", "OH"),
        ("7", "Gt Nicolas"),
        ("8", "Gt David"),
        ("9", "Voix David"),
        ("10", "Voix Virginie", "Nicolas vient sur ce micro pour chorus"),
        ("11", "DI Basse (Christophe)"),
        ("12", "Voix Christophe", "Chorus"),
        ("13", "Voix Rosaria", "Chorus (batterie)"),
    ]

    lx = 40
    ly = sy - 15
    cv.setFillColor(NOIR)
    cv.setFont("Montserrat", 9)
    cv.drawString(lx, ly, "INPUT LIST")
    cv.setStrokeColor(Color(0, 0, 0, alpha=0.3))
    cv.setLineWidth(0.5)
    cv.line(lx, ly - 3, lx + 250, ly - 3)

    headers = ["Can.", "Source", "Notes"]
    hx = [0, 30, 110]
    for i, h in enumerate(headers):
        cv.setFont("Montserrat", 7)
        cv.setFillColor(GRIS)
        cv.drawString(lx + hx[i], ly - 14, h)

    for idx, entry in enumerate(input_list):
        ry = ly - 28 - idx * 12
        cv.setFont("Montserrat", 7)
        cv.setFillColor(NOIR)
        cv.drawString(lx + hx[0], ry, entry[0])
        cv.drawString(lx + hx[1], ry, entry[1])
        if len(entry) > 2:
            cv.setFillColor(ACCENT)
            cv.setFont("Montserrat", 7)
            cv.drawString(lx + hx[2], ry, entry[2])

    ry_footer = ly - 28 - len(input_list) * 12 - 15
    cv.setFillColor(NOIR)
    cv.setFont("Montserrat", 8)
    cv.drawString(lx, ry_footer, "Monitors : 4 retours")
    cv.setFillColor(GRIS)
    cv.setFont("Montserrat", 7)
    cv.drawString(lx, ry_footer - 11, "MON 1 : Batterie (Rosaria)")
    cv.drawString(lx, ry_footer - 20, "MON 2 : Jardin (Nicolas + Christophe)")
    cv.drawString(lx, ry_footer - 29, "MON 3 : Cour (Virginie + David)")
    cv.drawString(lx, ry_footer - 38, "MON 4 : Central avant (voix)")

    cv.setFillColor(NOIR)
    cv.setFont("Montserrat", 8)
    cv.drawRightString(W - 30, ry_footer, "Contact : c.lucet@gmail.com / 06 75 29 99 37")


cv = canvas.Canvas(OUTPUT, pagesize=(W, H))
draw_stage(cv)
cv.save()
print(f"Stage plot : {OUTPUT}")
