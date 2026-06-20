#!/usr/bin/env python3
"""Generate Rivers Rock lyrics — 12 individual song PDFs, full A4, maximized layout."""

import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from logoutils import reportlab_crest, BEBAS_PATH, MONTSERRAT_PATH
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "pdf", "lyrics")
os.makedirs(OUT_DIR, exist_ok=True)

ACCENT = HexColor("#E85D3A")
BLEU = HexColor("#1A3A5C")
NOIR = HexColor("#222222")

pdfmetrics.registerFont(TTFont("BebasNeue", BEBAS_PATH))
pdfmetrics.registerFont(TTFont("Montserrat", MONTSERRAT_PATH))

W, H = A4
M = 45
TITLE_SIZE = 28
ARTIST_SIZE = 13
FONT_SIZE = 13
LINE_H = 19
SECTION_H = 12
HEADER_Y = H - 65
TOP_MARGIN = 95

SONGS = [
    {
        "title": "J'ai vu",
        "artist": "Niagara",
        "lyrics": [
            ("Couplet 1", [
                "J'ai vu Berlin, Bucarest et Pékin comme si j'y étais",
                "Matin et soir le nez dans la télé, c'est encore plus vrai",
                "J'étais de tous les combats, collée devant l'écran",
                "À la fois à Soweto, en Chine et au Liban",
                "Lancer des pierres au bord de Gaza, je ne regrette pas",
                "Des religieux, au nom de leur foi, m'ont lancé une fatwa",
            ]),
            ("Refrain", [
                "J'ai vu la guerre, la victoire était au bout de leurs fusils",
                "J'ai vu le sang sur ma peau, j'ai vu la fureur et les cris",
                "Et j'ai prié, j'ai prié pour ceux qui se sont sacrifiés",
                "J'ai vu la mort se marrer et ramasser ceux qui restaient...",
            ]),
            ("Couplet 2", [
                "Que cent mille fleurs s'ouvrent à jamais, et j'ai déjà donné",
                "Les drapeaux rouges ont cessé de flotter, je les ai brûlés",
                "Un homme ce matin s'est jeté sous un train",
                "Abandonné comme un chien, la misère et la faim",
                "La pire est à craindre pour demain, ça ne me fait rien",
                "Accrochée à ma fenêtre bleutée, j'ai cherché la vérité",
            ]),
            ("Refrain", [
                "J'ai vu la guerre, la victoire était au bout de leurs fusils",
                "J'ai vu le sang sur ma peau, j'ai vu la fureur et les cris",
                "Et j'ai prié, j'ai prié pour ceux qui se sont sacrifiés",
                "J'ai vu la mort se marrer et ramasser ceux qui restaient...",
            ]),
        ],
    },
    {
        
        "title": "You Shook Me All Night Long",
        "artist": "AC/DC",
        "lyrics": [
            ("Verse 1", [
                "She was a fast machine, she kept her motor clean",
                "She was the best damn woman that I ever seen",
                "She had the sightless eyes, tellin' me no lies",
                "Knockin' me out with those American thighs",
                "Takin' more than her share, had me fightin' for air",
                "She told me to come, but I was already there",
                "'Cause the walls start shakin', the Earth was quakin'",
                "My mind was achin', and we were makin' it",
            ]),
            ("Chorus", [
                "And you shook me all night long",
                "Yeah, you shook me all night long",
            ]),
            ("Verse 2", [
                "Workin' double-time on the seduction line",
                "She's one of a kind, she's just a-mine, all mine",
                "Wanted no applause, just another course",
                "Made a meal outta me, and come back for more",
                "Had to cool me down to take another round",
                "Now I'm back in the ring to take another swing",
                "That the walls were shakin', the Earth was quakin'",
                "My mind was achin', and we were makin' it",
            ]),
            ("Chorus", [
                "And you shook me all night long",
                "Yeah, you shook me all night long",
                "It knocked me out that you shook me all night long",
                "It had me shakin' and you shook me all night long",
            ]),
            ("Outro", [
                "Yeah, you shook me",
                "Well, you took me",
                "You really took me and you shook me all night long",
                "Yeah, you shook me all night long",
            ]),
        ],
    },
    {
        "title": "Je n'veux pas rester sage",
        "artist": "Dolly",
        "lyrics": [
            ("Couplet 1", [
                "Le mal est entré",
                "Meilleur ennemi",
                "Il sait m'abandonner",
                "Me ramener près de lui",
            ]),
            ("Refrain", [
                "Je n'veux pas rester sage",
                "J'aime le souffre et l'envie",
                "Abuser de mon âge",
                "Je n'veux pas rester sage",
            ]),
            ("Pont", [
                "Le mal est ma lueur",
                "Son ombre est ma couleur",
                "Le mal est ma lueur",
                "Mon parfum, son odeur",
                "Prends ton mal en douceur",
            ]),
            ("Couplet 2", [
                "Le mal est entré",
                "Et je sais qu'il détruit",
                "Qu'il pourrait m'faire crever",
                "Que reste-t-il ici",
            ]),
            ("Refrain", [
                "Je n'veux pas rester sage",
                "J'aime le souffre et l'envie",
                "Abuser de mon âge",
                "Je n'veux pas rester sage",
            ]),
            ("Pont", [
                "Le mal est ma lueur",
                "Son ombre est ma couleur",
                "Le mal est ma lueur",
                "Mon parfum, son odeur",
                "Prends ton mal en douceur",
            ]),
        ],
    },
    {
        "title": "Where Is My Mind?",
        "artist": "Pixies",
        "lyrics": [
            ("Verse 1", [
                "With your feet in the air and your head on the ground",
                "Try this trick and spin it, yeah",
                "Your head will collapse, if there's nothing in it",
                "And you'll ask yourself",
            ]),
            ("Chorus", [
                "Where is my mind?",
                "Where is my mind?",
                "Where is my mind?",
                "Way out in the water, see it swimmin'",
            ]),
            ("Verse 2", [
                "I was swimmin' in the Caribbean",
                "Animals were hidin' behind the rock",
                "Except the little fish",
                "Bump into me, swear he's tryin' to talk to me,",
                "Say wait, wait",
            ]),
            ("Chorus", [
                "Where is my mind?",
                "Where is my mind?",
                "Where is my mind?",
                "Way out in the water, see it swimmin'",
            ]),
            ("Outro", [
                "With your feet in the air and your head on the ground",
                "Try this trick and spin it, yeah",
            ]),
        ],
    },
    {
        "title": "Good Fortune",
        "artist": "PJ Harvey",
        "lyrics": [
            ("Verse 1", [
                "Threw my bad fortune off the top of a tall building",
                "I'd rather done it with you",
                "Your boy's smile, five in the morning",
                "Looked into your eyes and I was really in love",
                "In Chinatown, hungover",
                "You showed me just what I could do",
                "Talking about time travel and the meaning",
                "And just what it was worth",
            ]),
            ("Chorus", [
                "And I feel like some bird of paradise",
                "My bad fortune slipping away",
                "And I feel the innocence of a child",
                "Everybody's got something good to say",
            ]),
            ("Verse 2", [
                "Things I once thought unbelievable in my life",
                "Have all taken place",
                "When we walked through Little Italy",
                "I saw my reflection come right off your face",
                "I paint pictures to remember",
                "You're too beautiful to put into words",
                "Like a gypsy, you dance in circles all around me",
                "And all over the world",
            ]),
            ("Chorus", [
                "And I feel like some bird of paradise",
                "My bad fortune slipping away",
                "And I feel the innocence of a child",
                "Everybody's got something good to say",
            ]),
            ("Outro", [
                "So I take my good fortune",
                "And I fantasize of our leaving",
                "Like some modern day gypsy landslide",
                "Like some modern day Bonnie and Clyde",
                "On the run again",
            ]),
        ],
    },
    {
        "title": "Bella ciao",
        "artist": "Traditionnel italien",
        "lyrics": [
            ("Strofa 1", [
                "Una mattina mi son svegliato",
                "o bella ciao, bella ciao, bella ciao, ciao, ciao",
                "una mattina mi son svegliato",
                "e ho trovato l'invasor.",
            ]),
            ("Strofa 2", [
                "O partigiano, portami via",
                "o bella ciao, bella ciao, bella ciao, ciao, ciao",
                "o partigiano, portami via",
                "che mi sento di morir.",
            ]),
            ("Strofa 3", [
                "E se io muoio da partigiano",
                "o bella ciao, bella ciao, bella ciao, ciao, ciao",
                "e se io muoio da partigiano",
                "tu mi devi seppellir.",
            ]),
            ("Strofa 4", [
                "E seppellire lassù in montagna",
                "o bella ciao, bella ciao, bella ciao, ciao, ciao",
                "e seppellire lassù in montagna",
                "sotto l'ombra di un bel fior.",
            ]),
            ("Strofa 5", [
                "Tutte le genti che passeranno",
                "o bella ciao, bella ciao, bella ciao, ciao, ciao",
                "tutte le genti che passeranno",
                "mi diranno: «Che bel fior!»",
            ]),
            ("Strofa 6", [
                "E questo è il fiore del partigiano",
                "o bella ciao, bella ciao, bella ciao, ciao, ciao",
                "e questo è il fiore del partigiano",
                "morto per la libertà.",
            ]),
            ("Strofa 7", [
                "E questo è il fiore del partigiano",
                "o bella ciao, bella ciao, bella ciao, ciao, ciao",
                "e questo è il fiore del partigiano",
                "morto per la libertà.",
            ]),
        ],
    },
    {
        "title": "Today",
        "artist": "The Smashing Pumpkins",
        "lyrics": [
            ("Chorus", [
                "Today is the greatest",
                "Day I've ever known",
                "Can't live for tomorrow",
                "Tomorrow's much too long",
                "I'll burn my eyes out",
                "Before I get out",
            ]),
            ("Verse 1", [
                "I wanted more",
                "Than life could ever grant me",
                "Bored by the chore",
                "Of saving face",
            ]),
            ("Chorus", [
                "Today is the greatest",
                "Day I've ever known",
                "Can't wait for tomorrow",
                "I might not have that long",
                "I'll tear my heart out",
                "Before I get out",
            ]),
            ("Verse 2", [
                "Pink ribbon scars",
                "That never forget",
                "I tried so hard",
                "To cleanse these regrets",
                "My angel wings",
                "Were bruised and restrained",
                "My belly stings",
            ]),
            ("Bridge", [
                "I want to turn you on",
                "I want to turn you on",
                "I want to turn you on",
                "I want to turn you",
            ]),
            ("Outro", [
                "Today is the greatest",
                "Today is the greatest day",
                "Today is the greatest day",
                "That I have ever really known",
            ]),
        ],
    },
    {
        "title": "Creep",
        "artist": "Radiohead",
        "lyrics": [
            ("Verse 1", [
                "When you were here before",
                "Couldn't look you in the eye",
                "You're just like an angel",
                "Your skin makes me cry",
                "You float like a feather",
                "In a beautiful world",
                "I wish I was special",
                "You're so fuckin' special",
            ]),
            ("Chorus", [
                "But I'm a creep",
                "I'm a weirdo",
                "What the hell am I doin' here?",
                "I don't belong here",
            ]),
            ("Verse 2", [
                "I don't care if it hurts",
                "I wanna have control",
                "I want a perfect body",
                "I want a perfect soul",
                "I want you to notice",
                "When I'm not around",
                "You're so fuckin' special",
                "I wish I was special",
            ]),
            ("Chorus", [
                "But I'm a creep",
                "I'm a weirdo",
                "What the hell am I doin' here?",
                "I don't belong here",
                "Oh-oh, oh-oh",
            ]),
            ("Bridge", [
                "She's runnin' out the door",
                "She's runnin' out",
                "She run, run, run, run",
                "Run",
            ]),
            ("Chorus", [
                "But I'm a creep",
                "I'm a weirdo",
                "What the hell am I doin' here?",
                "I don't belong here",
                "I don't belong here",
            ]),
        ],
    },
    {
        "title": "Voyage, voyage",
        "artist": "Desireless",
        "lyrics": [
            ("Couplet 1", [
                "Au-dessus des vieux volcans",
                "Glisse tes ailes sous le tapis du vent",
                "Voyage, voyage",
                "Éternellement",
                "De nuages en marécages",
                "De vent d'Espagne en pluie d'équateur",
                "Voyage, voyage",
                "Vole dans les hauteurs",
            ]),
            ("Pré-refrain", [
                "Au-dessus des capitales",
                "Des idées fatales",
                "Regarde l'océan",
            ]),
            ("Refrain", [
                "Voyage, voyage",
                "Plus loin que la nuit et le jour",
                "Voyage",
                "Dans l'espace inouï de l'amour",
                "Voyage, voyage",
                "Sur l'eau sacrée d'un fleuve indien",
                "Voyage",
                "Et jamais ne reviens",
            ]),
            ("Couplet 2", [
                "Sur le Gange ou l'Amazone",
                "Chez les Blacks, chez les Sikhs, chez les Jaunes",
                "Voyage, voyage",
                "Dans tout le royaume",
                "Sur les dunes du Sahara",
                "Des îles Fidji au Fuji-yama",
                "Voyage, voyage",
                "Ne t'arrête pas",
            ]),
            ("Pré-refrain", [
                "Au-dessus des barbelés",
                "Des cœurs bombardés",
                "Regarde l'océan",
            ]),
            ("Refrain", [
                "Voyage, voyage",
                "Plus loin que la nuit et le jour",
                "Voyage",
                "Dans l'espace inouï de l'amour",
                "Voyage, voyage",
                "Sur l'eau sacrée d'un fleuve indien",
                "Voyage",
                "Et jamais ne reviens",
            ]),
        ],
    },
    {
        "title": "We Will Rock You",
        "artist": "Queen",
        "lyrics": [
            ("Verse 1", [
                "Buddy, you're a boy, make a big noise",
                "Playing in the street, gonna be a big man someday",
                "You got mud on your face, you big disgrace",
                "Kickin' your can all over the place, singin'",
            ]),
            ("Chorus", [
                "We will, we will rock you",
                "We will, we will rock you",
            ]),
            ("Verse 2", [
                "Buddy, you're a young man, hard man",
                "Shouting in the street, gonna take on the world someday",
                "You got blood on your face, you big disgrace",
                "Wavin' your banner all over the place",
            ]),
            ("Chorus", [
                "We will, we will rock you",
                "We will, we will rock you",
            ]),
            ("Verse 3", [
                "Buddy, you're an old man, poor man",
                "Pleading with your eyes, gonna make you some peace someday",
                "You got mud on your face, big disgrace",
                "Somebody better put you back into your place",
            ]),
            ("Chorus", [
                "We will, we will rock you, sing it",
                "We will, we will rock you",
                "Everybody, we will, we will rock you",
                "We will, we will rock you",
            ]),
        ],
    },
    {
        "title": "Jumpin' Jack Flash",
        "artist": "The Rolling Stones",
        "lyrics": [
            ("Verse 1", [
                "I was born in a crossfire hurricane",
                "And I howled at my ma in the drivin' rain",
            ]),
            ("Chorus", [
                "But it's all right now",
                "In fact, it's a gas!",
                "But it's all right",
                "I'm Jumpin' Jack Flash, it's a gas, gas, gas!",
            ]),
            ("Verse 2", [
                "I was raised by a tooth-less, bearded hag",
                "I was schooled with a strap right 'cross my back",
            ]),
            ("Chorus", [
                "But it's all right now",
                "In fact, it's a gas!",
                "But it's all right",
                "I'm Jumpin' Jack Flash, it's a gas, gas, gas!",
            ]),
            ("Verse 3", [
                "I was drowned, I was washed up 'n left for dead",
                "I fell down to my feet and I saw they bled, yeah, yeah",
                "I frowned at the crumbs of a crust of bread, yeah, yeah, yeah",
                "I was crowned with a spike right through my head, my, my, yeah",
            ]),
            ("Chorus", [
                "But it's all right now",
                "In fact, it's a gas!",
                "But it's all right",
                "I'm Jumpin' Jack Flash, it's a gas, gas, gas",
            ]),
        ],
    },
    {
        "title": "Seven Nation Army",
        "artist": "The White Stripes",
        "lyrics": [
            ("Verse 1", [
                "I'm gonna fight 'em off",
                "A seven-nation army couldn't hold me back",
                "They're gonna rip it off",
                "Takin' their time right behind my back",
                "And I'm talkin' to myself at night because I can't forget",
                "Back and forth through my mind, behind a cigarette",
                "And the message comin' from my eyes says, \"Leave it alone\"",
            ]),
            ("Verse 2", [
                "Don't wanna hear about it",
                "Every single one's got a story to tell",
                "Everyone knows about it",
                "From the Queen of England to the Hounds of Hell",
                "And if I catch it comin' back my way, I'm gonna serve it to you",
                "And that ain't what you want to hear, but that's what I'll do",
                "And the feelin' comin' from my bones says, \"Find a home\"",
            ]),
            ("Verse 3", [
                "I'm goin' to Wichita",
                "Far from this opera forevermore",
                "I'm gonna work the straw",
                "Make the sweat drip out of every pore",
                "And I'm bleedin' and I'm bleedin' and I'm bleedin' right before the Lord",
                "All the words are gonna bleed from me and I will think no more",
                "And the stains comin' from my blood tell me, \"Go back home\"",
            ]),
        ],
    },
]


def draw_song_full(cv, song, idx):
    lines_total = sum(len(lines) for _, lines in song["lyrics"])
    sections = len(song["lyrics"])
    needed = lines_total * LINE_H + sections * (SECTION_H + 8) + HEADER_Y - 60
    available = H - HEADER_Y + 60 - 35

    scale = 1.0
    if needed > available:
        scale = available / needed

    fs = max(10, int(FONT_SIZE * scale))
    lh = max(14, int(LINE_H * scale))
    sh = max(9, int(SECTION_H * scale))

    cv.setFillColor(Color(1, 1, 1))
    cv.rect(0, 0, W, H, stroke=0, fill=1)

    reportlab_crest(cv, M + 10, HEADER_Y, 0.9)

    cv.setFillColor(ACCENT)
    cv.setFont("BebasNeue", TITLE_SIZE)
    cv.drawString(M + 60, HEADER_Y - 4, song["title"])

    cv.setFillColor(BLEU)
    cv.setFont("Montserrat", ARTIST_SIZE)
    cv.drawString(M + 60, HEADER_Y - 24, song["artist"])

    cv.setStrokeColor(Color(0, 0, 0, alpha=0.1))
    cv.setLineWidth(0.5)
    cv.line(M, HEADER_Y - 38, W - M, HEADER_Y - 38)

    y = HEADER_Y - 60
    for section_name, lines in song["lyrics"]:
        if y < 35:
            break
        cv.setFillColor(ACCENT)
        cv.setFont("Montserrat", 8)
        cv.drawString(M, y, section_name.upper())
        y -= sh

        cv.setFont("Montserrat", fs)
        cv.setFillColor(NOIR)
        for line in lines:
            if y < 35:
                break
            cv.drawString(M, y, line)
            y -= lh

        y -= 6

    cv.setFillColor(Color(0, 0, 0, alpha=0.3))
    cv.setFont("Montserrat", 7)
    cv.drawString(M, 16, f"RIVERS ROCK — Rouen — {idx + 1} / {len(SONGS)}")


filenames = [
    "01-niagara-jai-vu", "02-acdc-you-shook-me", "03-dolly-je-ne-veux-pas-rester-sage",
    "04-pixies-where-is-my-mind", "05-pj-harvey-good-fortune", "06-bella-ciao",
    "07-smashing-pumpkins-today", "08-radiohead-creep", "09-desireless-voyage-voyage",
    "10-queen-we-will-rock-you", "11-rolling-stones-jumpin-jack-flash",
    "12-white-stripes-seven-nation-army",
]

for idx, song in enumerate(SONGS):
    path = os.path.join(OUT_DIR, f"{filenames[idx]}.pdf")
    cv = canvas.Canvas(path, pagesize=A4)
    draw_song_full(cv, song, idx)
    cv.save()
    print(f"  {path}")

print(f"12 chansons générées dans {OUT_DIR}/")

