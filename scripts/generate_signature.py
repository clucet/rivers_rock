#!/usr/bin/env python3
"""Generate Rivers Rock email signatures — Rock Brut.
Generates a generic version + personalized for each member."""

import os
from PIL import Image, ImageDraw, ImageFont
import sys
sys.path.insert(0, os.path.dirname(__file__))
from logoutils import hexagon_logo_pillow, ANTON_PATH

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")
os.makedirs(OUT_DIR, exist_ok=True)

ORANGE = (255, 59, 0)
BLANC = (255, 255, 255)
GRIS = (150, 150, 150)
GRIS_F = (100, 100, 100)
NOIR = (10, 10, 10)

W, H = 600, 200
GROUP_EMAIL = "riversrock_rouen@gmail.com"

MEMBRES = [
    {"nom": "David DIAS",         "email": "dias.david77@gmail.com",         "fichier": "email-signature-david.png"},
    {"nom": "Virginie JACQUIER-DIAS", "email": "virginie.jacquierdias@gmail.com", "fichier": "email-signature-virginie.png"},
    {"nom": "Nicolas RENNES",     "email": "labochariz@gmail.com",          "fichier": "email-signature-nicolas.png"},
    {"nom": "Rosaria NUCIFORA",   "email": "rosaria.nucifora@yahoo.fr",     "fichier": "email-signature-rosaria.png"},
    {"nom": "Christophe LUCET",   "email": "c.lucet@gmail.com",             "fichier": "email-signature-christophe.png"},
]


def make_signature(path, nom=None, email_perso=None):
    img = Image.new("RGB", (W, H), NOIR)
    draw = ImageDraw.Draw(img)

    font_logo = ImageFont.truetype(ANTON_PATH, 20)
    font_nom = ImageFont.truetype(ANTON_PATH, 12)
    font_infos = ImageFont.truetype(ANTON_PATH, 9)

    hexagon_logo_pillow(draw, 40, 80, 28)

    y = 62
    if nom:
        draw.text((68, y), nom, fill=BLANC, font=font_nom)
        y += 18
    if email_perso:
        draw.text((68, y), email_perso, fill=GRIS, font=font_infos)
        y += 14
    draw.text((68, y), GROUP_EMAIL, fill=GRIS_F, font=font_infos)

    draw.text((20, 168), "RIVERS ROCK", fill=ORANGE, font=font_infos)

    img.save(path)
    print(f"  {os.path.basename(path)}")


def gen_signature():
    # Generique
    make_signature(os.path.join(OUT_DIR, "email-signature.png"),
                   nom=None, email_perso=None)
    make_signature(os.path.join(OUT_DIR, "email-signature-generic.png"),
                   nom=None, email_perso=None)

    # Personnalisees
    for m in MEMBRES:
        make_signature(os.path.join(OUT_DIR, m["fichier"]),
                       nom=m["nom"], email_perso=m["email"])


if __name__ == "__main__":
    gen_signature()
