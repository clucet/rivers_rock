<!-- AUTO-UPDATE: Dernière mise à jour automatique par opencode (24/06/2026) -->
<!-- Sections gérées automatiquement : Propositions design, Tâches, Journal. Toute modification manuelle de ces sections sera écrasée. -->

# Rivers Rock — Suivi de projet

## Identité
**Groupe :** Rivers Rock (Rouen)
**Genre :** Reprises rock, pop-rock, rock indé, alternatif
**Répétition :** Le 106 (studios), Rouen
**Charte graphique :** `charte-graphique-rivers-rock.md`

---

## Tâches

### ✅ Accomplies
| Tâche | Fichier(s) | Date |
|-------|-----------|------|
| Charte graphique initiale | `charte-graphique-rivers-rock.md` | 18/06 |
| Setlist PDF v1 (paysage, 3 colonnes) | `setlist-rivers-rock.pdf`, `generate_setlist.py` | 18/06 |
| Ajout bandes vertes/rouges (titres ton adapté) | `generate_setlist.py` | 18/06 |
| Passage A4 portrait, 2 colonnes × 6 lignes | `generate_setlist.py` | 18/06 |
| Noms uniformes taille max (31pt) | `generate_setlist.py` | 18/06 |
| Centrage contenu + marges de sécurité | `generate_setlist.py` | 18/06 |
| Ombre portée + bordure cartes | `generate_setlist.py` | 18/06 |
| Numéros 16pt + vague décorative | `generate_setlist.py` | 18/06 |
| Refonte logo (symbole cercle+vague, horizontal) | `generate_setlist.py` | 18/06 |
| Badge circulaire + fond dégradé cartes | `generate_setlist.py` | 18/06 |
| Templates Instagram (post + story) | `generate_social.py`, `templates/instagram-*.png` | 18/06 |
| Alignement badge, SETLIST BebasNeue, titres Regular | `generate_setlist.py` | 18/06 |
| Suivi de projet | `suivi-projet-rivers-rock.md` | 18/06 |
| Vérification disponibilité noms réseaux | — | 18/06 |
| Installation qrcode | — | 18/06 |
| Avatar (symbole seul, 500×500) | `generate_avatar.py`, `templates/avatar.png` | 18/06 |
| Affiche A4 concert | `generate_poster.py`, `poster-a4.pdf` | 18/06 |
| Flyer A6 recto/verso | `generate_flyer.py`, `flyer-a6.pdf` | 18/06 |
| Carte de visite 85×55 mm QR | `generate_businesscard.py`, `business-card.pdf` | 18/06 |
| Bannière Facebook (1640×624) | `generate_banners.py`, `pdf/templates/facebook-banner.png` | 18/06 |
| Bannière YouTube (2560×1440) | `generate_banners.py`, `pdf/templates/youtube-banner.png` | 18/06 |
| Signature email (600×200) | `generate_signature.py`, `pdf/templates/email-signature.png` | 18/06 |
| Stickers ∅80mm (planche de 6 / A4) | `generate_stickers.py`, `pdf/stickers.pdf` | 18/06 |
| T-shirt design B (print + mockup) | `generate_tshirts.py`, `pdf/t-shirt-print.pdf`, `pdf/templates/tshirt-mockup.png` | 18/06 |
| Flyer A6 — 4/A4 duplex, bio verso | `generate_flyer.py`, `pdf/flyer-a6.pdf` | 18/06 |
| Fiche technique sérigraphe | `generate_techsheet.py`, `pdf/t-shirt-techsheet.pdf` | 18/06 |
| Site one-page | `site/index.html` | 18/06 |
| Carte visite — retrait QR | `generate_businesscard.py`, `pdf/business-card.pdf` | 18/06 |
| Nouveau logo écusson (RIVERS/ROCK intégré) + animation HTML | `logoutils.py`, tous les scripts generate_*, `generate_animated_logo.html` | 18/06 |
| Stage plot / fiche technique son | `generate_stageplot.py`, `pdf/stage-plot.pdf` | 18/06 |
| Songsheets (paroles) — 12 PDF | `generate_lyrics.py`, `pdf/lyrics/*.pdf` | 18/06 |
| Polices — résolution automatique cross-platform | `logoutils.py` | 20/06 |
| `requirements.txt` | `requirements.txt` | 20/06 |
| Logo animé — ROCK slide depuis la droite | `generate_animated_logo.html`, `render_animation.py` | 20/06 |
| Logo animé — RIVERS/ROCK sur arcs du cercle | `generate_animated_logo.html`, `render_animation.py` | 20/06 |
| Développement proposition Fluid Wave (setlist, poster, flyer, social, banners, avatar, stickers, t-shirt, logo, site) | `propositions/01-fluid-wave/generate.py`, `propositions/01-fluid-wave/assets/` | 24/06 |
| Développement proposition Rock Brut (setlist, poster, flyer, social, banners, avatar, stickers, t-shirt, logo, site) | `propositions/02-rock-brut/generate.py`, `propositions/02-rock-brut/assets/` | 24/06 |
| Propositions 05 « Neon Nights » et 06 « Sable & Bronze » (palette, fonts, assets, overlays) | `propositions/05-neon-nights/`, `propositions/06-sable-bronze/` | 24/06 |
| QR codes réels (draw_qr_pillow + draw_qr_reportlab) dans les 6 propositions | Tous les `generate.py` | 24/06 |
| Bleed + crop marks (business card, stage plot, t-shirt) | `scripts/generate_businesscard.py`, `stageplot.py`, `tshirts.py` | 24/06 |
| Section Musique YouTube (propositions 01 et 04) | `propositions/01-fluid-wave/generate.py`, `04-ponts-lumiere/generate.py` | 24/06 |
| Setlist interactive web (minuteur, BPM, chronomètre) | `scripts/generate_setlist_web.py`, `site/setlist/index.html` | 24/06 |
| GitHub Pages activé + page comparaison 6 propositions | `propositions/index.html` | 24/06 |
| Facebook Page « Rivers Rock Rouen » créée | — | 24/06 |

### 📋 À faire
- [x] Création comptes réseaux — Gmail + YouTube + Instagram + Facebook faits
  - Gmail : `riversrockrouen@gmail.com`
  - YouTube : `@RiversRockRouen`
  - Instagram : `@riversrockrouen`
  - Facebook : `Rivers Rock Rouen`
- [ ] Publier les 5 posts de lancement sur Facebook — brouillons prêts dans `propositions/drafts/publications-facebook.md`
- [ ] Remplacer `[DATE]` `[LIEU]` dans les templates pour un vrai concert
- [ ] Merchandising (t-shirts)
- [ ] Session photo promo du groupe
- [ ] Choisir la proposition définitive parmi les 9
- [ ] Nettoyer les propositions non retenues
- [ ] Lancer le rendu MP4 final (`python3 scripts/render_animation.py`)

---

## Fichiers générés

| Fichier | Description |
|---------|-------------|
| `charte-graphique-rivers-rock.md` | Charte graphique complète (palette, typo, logo, supports) |
| `suivi-projet-rivers-rock.md` | Suivi de projet (ce fichier) |
| `scripts/generate_setlist.py` | Script → `pdf/setlist-rivers-rock.pdf` |
| `scripts/generate_social.py` | Script → `pdf/templates/instagram-*.png` |
| `scripts/generate_avatar.py` | Script → `pdf/templates/avatar.png` |
| `scripts/generate_poster.py` | Script → `pdf/poster-a4.pdf` |
| `scripts/generate_flyer.py` | Script → `pdf/flyer-a6.pdf` |
| `scripts/generate_businesscard.py` | Script → `pdf/business-card.pdf` |
| `pdf/setlist-rivers-rock.pdf` | Setlist A4 — 2 col., cartes vertes/rouges, badges, logo |
| `pdf/poster-a4.pdf` | Affiche concert A4 — logo + date/lieu |
| `pdf/flyer-a6.pdf` | Flyer A6 (2 p.) — recto promo, verso noms |
| `pdf/business-card.pdf` | Carte 85×55 mm — logo + contact + QR code |
| `pdf/templates/avatar.png` | Avatar 500×500, symbole seul, fond transparent |
| `pdf/templates/instagram-post.png` | Post carré 1080×1080 |
| `pdf/templates/instagram-story.png` | Story 1080×1920 |
| `pdf/templates/facebook-banner.png` | Bannière Facebook 1640×624 |
| `pdf/templates/youtube-banner.png` | Bannière YouTube 2560×1440 |
| `pdf/templates/email-signature.png` | Signature email 600×200 |
| `pdf/stickers.pdf` | Planche de 6 stickers ∅80mm sur A4 |
| `pdf/t-shirt-print.pdf` | Planche print t-shirt (S/M/L/XL) design B |
| `pdf/templates/tshirt-mockup.png` | Mockup t-shirt noir 1200×1600 |
| `pdf/t-shirt-techsheet.pdf` | Fiche technique sérigraphe |
| `site/index.html` | Site one-page (GitHub Pages) |
| `pdf/stage-plot.pdf` | Fiche technique son (stage plot + input list) |
| `pdf/templates/logo-animated.mp4` | Logo animé (6s, 1080×1920) |
| `scripts/generate_animated_logo.html` | Animation logo dans navigateur (arcs cercle) |
| `scripts/render_animation.py` | Rendu MP6 du logo animé |
| `scripts/logoutils.py` | Fonctions écusson + résolution polices cross-platform |
| `requirements.txt` | Dépendances Python |

---

## Structure du projet

```
setlist/
├── charte-graphique-rivers-rock.md
├── suivi-projet-rivers-rock.md
├── requirements.txt
├── propositions/
│   ├── 00-originale/
│   │   ├── spec.md
│   │   ├── generate.py
│   │   └── assets/
│   │       ├── index.html
│   │       ├── pdf/
│   │       │   ├── setlist-original.pdf
│   │       │   ├── poster-original.pdf
│   │       │   ├── flyer-original.pdf
│   │       │   ├── stickers-original.pdf
│   │       │   └── tshirt-original.pdf
│   │       └── templates/
│   │           ├── avatar.png
│   │           ├── facebook-banner.png
│   │           ├── youtube-banner.png
│   │           ├── instagram-post.png
│   │           ├── instagram-story.png
│   │           └── logo-animated-original.html
│   ├── 01-fluid-wave/
│   │   ├── spec.md
│   │   ├── generate.py
│   │   └── assets/
│   │       ├── index.html
│   │       ├── pdf/
│   │       │   ├── setlist-fluid-wave.pdf
│   │       │   ├── poster-fluid-wave.pdf
│   │       │   ├── flyer-fluid-wave.pdf
│   │       │   ├── stickers-fluid-wave.pdf
│   │       │   └── tshirt-fluid-wave.pdf
│   │       └── templates/
│   │           ├── avatar.png
│   │           ├── facebook-banner.png
│   │           ├── youtube-banner.png
│   │           ├── instagram-post.png
│   │           ├── instagram-story.png
│   │           └── logo-animated-fluid-wave.html
│   ├── 02-rock-brut/
│   │   ├── spec.md
│   │   ├── generate.py
│   │   └── assets/
│   │       ├── index.html
│   │       ├── pdf/
│   │       │   ├── setlist-rock-brut.pdf
│   │       │   ├── poster-rock-brut.pdf
│   │       │   ├── flyer-rock-brut.pdf
│   │       │   ├── stickers-rock-brut.pdf
│   │       │   └── tshirt-rock-brut.pdf
│   │       └── templates/
│   │           ├── avatar.png
│   │           ├── facebook-banner.png
│   │           ├── youtube-banner.png
│   │           ├── instagram-post.png
│   │           ├── instagram-story.png
│   │           └── logo-animated-rock-brut.html
│   └── 03-scene-vintage/
│       ├── spec.md
│       ├── generate.py
│       └── assets/
│           ├── index.html
│           ├── pdf/
│           │   ├── setlist-scene-vintage.pdf
│           │   ├── poster-scene-vintage.pdf
│           │   ├── flyer-scene-vintage.pdf
│           │   ├── stickers-scene-vintage.pdf
│           │   └── tshirt-scene-vintage.pdf
│           └── templates/
│               ├── avatar.png
│               ├── monogramme-rr.png
│               ├── facebook-banner.png
│               ├── youtube-banner.png
│               ├── instagram-post.png
│               └── instagram-story.png
├── scripts/
│   ├── logoutils.py
│   ├── generate_setlist.py
│   ├── generate_social.py
│   ├── generate_avatar.py
│   ├── generate_poster.py
│   ├── generate_flyer.py
│   ├── generate_businesscard.py
│   ├── generate_banners.py
│   ├── generate_signature.py
│   ├── generate_stickers.py
│   ├── generate_tshirts.py
│   ├── generate_techsheet.py
│   ├── generate_stageplot.py
│   ├── generate_lyrics.py
│   ├── generate_animated_logo.html
│   ├── render_animation.py
├── site/
│   └── index.html
└── pdf/
    ├── setlist-rivers-rock.pdf
    ├── poster-a4.pdf
    ├── flyer-a6.pdf
    ├── business-card.pdf
    ├── stickers.pdf
    ├── t-shirt-print.pdf
    ├── t-shirt-techsheet.pdf
    ├── stage-plot.pdf
    ├── lyrics/
    │   ├── 01-niagara-jai-vu.pdf
    │   ├── 02-acdc-you-shook-me.pdf
    │   ├── 03-dolly-je-ne-veux-pas-rester-sage.pdf
    │   ├── 04-pixies-where-is-my-mind.pdf
    │   ├── 05-pj-harvey-good-fortune.pdf
    │   ├── 06-bella-ciao.pdf
    │   ├── 07-smashing-pumpkins-today.pdf
    │   ├── 08-radiohead-creep.pdf
    │   ├── 09-desireless-voyage-voyage.pdf
    │   ├── 10-queen-we-will-rock-you.pdf
    │   ├── 11-rolling-stones-jumpin-jack-flash.pdf
    │   └── 12-white-stripes-seven-nation-army.pdf
    └── templates/
        ├── avatar.png
        ├── instagram-post.png
        ├── instagram-story.png
        ├── facebook-banner.png
        ├── youtube-banner.png
        ├── email-signature.png
        ├── tshirt-mockup.png
        └── logo-animated.mp4
```

---

## Améliorations possibles

- **QR code dynamique** : URL courte redirigeant vers la dernière version de la setlist
- **Setlist interactive** : app web accessible depuis le QR, avec minuterie scène
- **Fiche technique son** (stage plot) — ✅ fait
- **Logo animé** pour Reels/Shorts — ⚠️ en cours (rendu à retravailler)

---

## Propositions design (24 juin 2026)

### Proposition n°1 — « Fluid Wave » (Organique & Contemporain)

**Concept :** La Seine comme fluidité, mouvements d'eau, transitions douces.

| Élément | Actuel | Proposé |
|---------|--------|---------|
| **Palette** | Bleu + Vert + Orange sec | Ajout d'un ambre doux `#D4A843` (chaleur, vieux cuivre) |
| **Dégradés** | Linéaires verticaux | Dégradés radiaux et diagonaux, fondus plus longs |
| **Vagues** | 1 sinusoïde répétée | Vagues multiples, courbes de Bézier organiques, superposition floutée en filigrane |
| **Logo** | Écusson unique | Ajout d'un symbole vague seule (sans cercle) pour usage réduit |
| **Setlist** | Cartes rectangulaires | Cartes aux coins arrondis + bords irréguliers (galets), placement plus aéré |
| **Photos** | Aucune | Cercles flous en overlay sur les photos, cadre vague |
| **Site** | Texte seul | Bandeau hero avec animation vague CSS, photos en damier, embed YouTube |
| **Typo** | Bebas Neue + Montserrat | On conserve, ajout de Playfair Display pour les citations/lyrics |

**Ambiance :** Vibrations douces, eau qui coule, énergie fluide.

---

### Proposition n°2 — « Rock Brut » (Industriel & Performatif)

**Concept :** L'énergie rock, l'industrie rouennaise, le contraste fort.

| Élément | Actuel | Proposé |
|---------|--------|---------|
| **Palette** | Bleu + Vert + Orange | Noir `#0A0A0A` remplace le bleu en fond, vert `#4A9B8E` en accents lumineux, `#E85D3A` secondaire. Ajout blanc pur |
| **Dégradés** | Doux, large | Tranchés nets, demi-teintes, split-tones |
| **Vagues** | Sinusoïde douce | Lignes brisées, vagues carrées, formes géométriques angulaires |
| **Logo** | Écusson cercle+vague | Version monochrome (blanc sur noir), version découpée — hexagone ou carré aux coins coupés |
| **Setlist** | Cartes ombrées arrondies | Cartes sans ombre, bord vif, séparateurs traits épais, numéros dans des carrés |
| **Photos** | Aucune | Noir & blanc, grain argentique, fort contraste |
| **Site** | Claire, centrée | Dark mode uniquement, typo large, sections séparées par bandes de couleur |
| **Typo** | Bebas Neue + Montserrat | Ajout d'Unica77 ou Inter Tight pour le corps |

**Ambiance :** Noir profond, flashs orange, typo massive. Style fiche technique roadie.

---

### Proposition n°3 — « Scène & Vintage » (Nostalgique & Lumineux) — ✅ Retenue

**Concept :** L'énergie du live, les années 70-80 revisitées, la chaleur des projecteurs de scène. Inspirations : affiches Milton Glaser, pochettes vinyles, couchers de soleil sur la Seine.

#### Palette augmentée

| Rôle | Actuel | Nouveau | Apport |
|------|--------|---------|--------|
| Primaire | `#1A3A5C` | Conservé | Profondeur, identité |
| Secondaire | `#4A9B8E` | Conservé + `#1A5C5C` (Teal profond) | Double vert plus riche |
| Accent 1 | `#E85D3A` | Conservé | Feu de la scène |
| Accent 2 (nouveau) | — | `#C96D4D` Terracotta | Chaleur, vintage, rouille |
| Accent 3 (nouveau) | — | `#C9A84C` Or vieilli | Soleil, lumière, premium |
| Neutre | `#8C9196` | Conservé | — |
| Fond clair | `#F5F5F0` | Conservé | — |

#### Déclinaisons du logo

| Variante | Description | Usage |
|----------|-------------|-------|
| **Standard** | Écusson actuel (cercle + vague + RIVERS/ROCK) | Tous supports |
| **Néon digital** | Cercle + vague avec box-shadow glow `#E85D3A` | Site web, vidéos, stories Instagram |
| **Timbre disque** | Anneau concentrique supplémentaire autour du cercle | Merchandising, stickers, pochettes |
| **Monogramme "RR"** (nouveau) | Deux R entrelacés avec vague intégrée | Favicon, watermark, petits formats |

#### Typographie étendue

| Usage | Police | Notes |
|-------|--------|-------|
| Titres héro | **Anton** | 80–140pt, tracking serré, plus percutant que Bebas Neue |
| Logo / Setlist art | Bebas Neue (conservé) | Remplacer par Anton sur les supports XXL |
| Corps | Montserrat (conservé) | — |
| Citations / Lyrics / Dates | **Space Mono** | 10–18pt, vibe machine à écrire / ticket de concert |
| Décoratif grandes citations | Abril Fatface (envisagé) | Biographie du groupe |

#### Motifs & textures

- **Vagues superposées** en dégradé (opacité 5–20 %) en fond de tous les supports
- **Texture granuleuse** (grain overlay 3–8 %) sur fonds de setlist et affiches
- **Halftone dots** en filigrane sur les bords (rappel affiches psychédéliques)
- **Flares lumineux** — dégradés radiaux projecteur (templates Instagram, bannière YouTube)

#### Setlist revisitée

| Élément | Actuel | Proposé |
|---------|--------|---------|
| Fond | Bleu → Vert | `#1A3A5C` → `#1A5C5C` (teal profond), grain overlay 5 % |
| Cartes normales | `#E85D3A` avec dégradé | `#C96D4D` Terracotta |
| Cartes ton adapté | `#2D8A6E` | `#1A5C5C` Teal profond |
| Bordure cartes | Blanche 35 % | Double bordure (blanc fin + or `#C9A84C`) |
| Badges | Cercles blancs, numéro en vert/rouge | Cercles blancs, numéro en `#C9A84C` (or) |
| Vague séparatrice | Blanche 20 % | Or `#C9A84C`, opacité 50 % |
| Ombre portée | Noir 15 %, 3 pt | Noir 20 %, 4 pt + reflet chaud |

#### Site web — Nouvelle structure

```
site/index.html :

HEADER
├── Logo écusson + "RIVERS ROCK" en Anton
├── Navigation sticky (Le groupe · Concerts · Contact)
└── Hero photo groupe (fond duo-tone teal+orange)

SECTIONS
├── Bio — photos en damier, texte large Montserrat
├── Concerts — calendrier dates/réservations
├── Musique — embed YouTube playlist
├── Membres — photos individuelles cercles, rôles, citation Space Mono
└── Contact — formulaire + liens réseaux + carte

FOOTER
├── Logo timbre variante
└── "R O U E N" tracking + grain texture
```

#### Templates réseaux sociaux

| Support | Évolution |
|---------|-----------|
| Post Instagram | Dégradé radial chaud `#C96D4D` → `#C9A84C`, logo glow `#E85D3A`, texte Space Mono |
| Story Instagram | Duo-tone photo + dégradé chaud/froid, logo timbre, date Anton 120pt |
| Bannière Facebook | Grain overlay, vague or filigrane, photo groupe duo-tone |

---

## Notes techniques

- **Palette** : Bleu Seine `#1A3A5C`, Vert d'eau `#4A9B8E`, Accent `#E85D3A`, Vert repère `#2D8A6E`
- **Logo** : écusson (cercle + vague + RIVERS/ROCK intégré), Bebas Neue 11–14 pt
- **Typo corps** : Montserrat Regular / Italic
- **Taille uniforme** noms de groupe : 29–31 pt Bebas Neue (calée sur "SMASHING PUMPKINS")
- **Badges** : ∅24 pt blanc, numéro en couleur de carte (accent sur vert, vert repère sur rouge)
- **QR code** : généré avec lib `qrcode`, encode URLs à définir

### Polices — résolution cross-platform

Les chemins de polices sont centralisés dans `scripts/logoutils.py`. La fonction `_find_font()` et `_ensure_font()` cherchent automatiquement dans :

| OS | Chemins |
|----|---------|
| **macOS** | `~/Library/Fonts/` |
| **Linux** | `~/.fonts/`, `~/.local/share/fonts/`, `/usr/share/fonts/` |
| **Projet** | `scripts/` (dossier courant) |

Si BebasNeue-Regular.ttf est introuvable, elle est **téléchargée automatiquement** depuis le dépôt Google Fonts GitHub vers `~/.fonts/`.

**⚠️ Montserrat VF** — La police variable nécessite de préciser l'axe de poids en ReportLab :
```python
pdfmetrics.registerFont(TTFont("Montserrat", MONTSERRAT_PATH))
```
Le poids par défaut correspond à Thin. Pour Regular, utiliser `wght=400`.

### Logo animé

- **HTML** : `scripts/generate_animated_logo.html` — animation SVG+CSS (cercles, vague, particules, texte sur arcs)
- **MP4** : `scripts/render_animation.py` — rendu via Pillow + FFmpeg, synchronisé avec l'HTML
  - Résolution de rendu : 540×960, upscalé à 1080×1920 par ffmpeg
  - 30 FPS, 7 secondes
  - ROCK slide depuis la droite, lettres individuelles (1.9s → 2.2s)

### Dépendances

```
reportlab>=4.0
Pillow>=10.0
qrcode>=8.0
```

---

## Réseaux sociaux — Comptes créés

### ✅ Gmail — Créé
| Champ | Valeur |
|-------|--------|
| **Adresse** | `riversrockrouen@gmail.com` |
| **Mot de passe** | `!LeGroupe76140@` |

### ✅ YouTube — Créé
| Champ | Valeur |
|-------|--------|
| **Chaîne** | Rivers Rock Rouen |
| **Handle** | `@RiversRockRouen` |
| **Email lié** | `riversrockrouen@gmail.com` |

### 📋 À créer
| Plateforme | Nom prévu | Avatar |
|------------|-----------|--------|
| Instagram | `@riversrockrouen` | `propositions/03-scene-vintage/assets/templates/avatar.png` |
| Facebook | `Rivers Rock Rouen` | `propositions/03-scene-vintage/assets/templates/avatar.png` |

### Guide (étape restante)

1. **Facebook** → [facebook.com/pages/create](https://facebook.com/pages/create) → créer une page "Groupe de musique" → nom "Rivers Rock Rouen" → avatar + bannière + `propositions/03-scene-vintage/assets/templates/instagram-post.png` comme première publication

---

*Document mis à jour le 24 juin 2026*

---

## Palette centralisée (`scripts/palette.py`)

Depuis le 24 juin 2026, tous les générateurs utilisent `scripts/palette.py` comme source unique de configuration.

### Principe

```python
from palette import SCENE_VINTAGE as CFG
CFG.rl("accent")     # → HexColor("#E85D3A")   pour ReportLab
CFG.pil("accent")    # → (232, 93, 58)          pour Pillow
CFG.token("card_r")  # → 6                      tokens design
CFG.flag("use_grain")# → True                   flags booléens
```

### 4 configurations disponibles

| Config | Usage | Palette |
|--------|-------|---------|
| `palette.BASE` | Design original | bleu, vert, accent, vert_repere, gris, blanc |
| `palette.FLUID_WAVE` | Proposition n°1 | + ambre `#D4A843`, vert_repere |
| `palette.ROCK_BRUT` | Proposition n°2 | noir, vert_accent, accent, gris_fonce, blanc |
| `palette.SCENE_VINTAGE` | Proposition n°3 retenue | + terracotta `#C96D4D`, or `#C9A84C`, teal `#1A5C5C` |

### Fichier de référence

```
scripts/palette.py
├── class Config (dataclass) : rl(), pil(), token(), flag()
├── 4 configurations prédéfinies : BASE, FLUID_WAVE, ROCK_BRUT, SCENE_VINTAGE
├── FONT_MAP : résolution rôle → nom de fichier
└── font_filename() : rôle + config → nom de fichier police
```

---

## Analyse professionnelle (24 juin 2026)

Analyse comparative des 4 propositions (Originale, Fluid Wave, Rock Brut, Scène & Vintage) après génération complète de tous les assets.

### Forces par proposition

| Proposition | Points forts |
|-------------|--------------|
| **Originale** | Simplicité, fichiers légers, charte bien établie, logo écusson efficace, couverture complète des supports |
| **Fluid Wave** | Palette réchauffée (ambre `#D4A843`), dégradés radiaux élégants, grain overlay cohérent, identité organique douce |
| **Rock Brut** | Contrastes AAA, fichiers très légers (flat design vectoriel), identité forte et disruptive, bonne pour print |
| **Scène & Vintage** | Plus complète (grain, halftone, flares, monogramme, timbre), la plus « finie » visuellement, site responsive soigné |

### Faiblesses communes (à corriger)

| Problème | Impact | Gravité |
|----------|--------|---------|
| **Aucun fond perdu (bleed)** sur PDF print — contenu au bord de la page | Inutilisable en imprimerie professionnelle | 🔴 Critique |
| **Palettes RGB uniquement** — pas de CMYK, pas de Pantone | Décalage couleur à l'impression | 🔴 Critique |
| **Aucune photo** — 100 % vectoriel, pas de portraits du groupe, pas de photos de scène | Manque d'incarnation humaine, crucial pour un groupe | 🔴 Critique |
| **Duplication de code massive** (~70 %) — gradients, vagues, cartes setlist copiés dans 10+ fichiers | Maintenance impossible à long terme | 🟠 Élevé |
| **QR codes factices** — texte "QR" au lieu de vrais QR codes | Inutilisable | 🟠 Élevé |
| **Polices non conformes aux specs** — Anton/Space Mono absents de plusieurs générateurs Fluid Wave et Rock Brut | Décalage charte vs rendu | 🟠 Élevé |
| **Tailles de police < 6 pt** (flyer, carte de visite) | Illisible en impression offset | 🟠 Élevé |
| **Absence de repères de coupe** sur la plupart des PDF | Découpage imprécis à l'impression | 🟡 Moyen |
| **Gradients par bandes (120 rectangles)** — fichiers PDF 3-5× plus gros que nécessaire | Poids inutile, lenteur de génération | 🟡 Moyen |
| **Contraste insuffisant** : or `#C9A84C` sur teal `#1A5C5C` (3.7:1) | Échec WCAG AA pour petits textes | 🟡 Moyen |
| **Dossier dupliqué** `02-rock-brute/` vs `02-rock-brut/` (corrigé) | Confusion de navigation | ✅ Corrigé |
| **Aucun test** — pytest, unittest ou doctest | Non maintenable en équipe | 🟡 Moyen |
| **Site pas responsive** pour Fluid Wave et Rock Brut (pas de `@media`) | Mauvaise expérience mobile | 🟡 Moyen |

### Améliorations professionnelles proposées

#### Lot 1 — Print professionnel (priorité haute)
1. Ajouter **3 mm de bleed** sur tous les PDF (setlist, poster, flyer, stickers, business card)
2. Ajouter **repères de coupe** (crop marks) en cyan 100 % sur tous les print PDF
3. Convertir les couleurs en **CMYK** pour les sorties print (conversion au moment de l'export)
4. Ajouter les **références Pantone** dans les PDF techniques (PMS 172 pour `#E85D3A`, PMS 7406 pour `#C9A84C`)
5. Interdire les polices < **6 pt** en print ; repasser à 7 pt minimum

#### Lot 2 — Identité visuelle (priorité haute)
6. **Session photo promo** : portraits des 5 membres + photo de groupe + photos de scène
7. Intégrer les photos dans les templates (duo-tone overlay) — social, banners, site, flyer
8. Générer de **vrais QR codes** avec `qrcode` library au lieu de textes "QR"
9. Créer un **favicon 16×32 px** à partir du monogramme RR
10. Ajouter un **logo alternate monochrome** (blanc pur / noir pur) pour tous les supports

#### Lot 3 — Technique (priorité moyenne)
11. **Factoriser les fonctions communes** dans `logoutils.py` :
    - `draw_gradient_pdf(cv, W, H, c1, c2)` — gradient vertical avec 1 seul rectangle + clip
    - `draw_waves_pdf(cv, W, H, count, color, opacity)` — vagues paramétrées
    - `draw_grain_pdf(cv, W, H, intensity, seed)` — grain paramétré
    - `draw_footer_rouen(cv, W)` — footer "ROUEN" paramétré
12. **Centraliser le setlist data** dans un seul fichier JSON ou YAML
13. **Centraliser la palette** : un seul fichier `palette.py` importé partout
14. Ajouter un **système d'arguments CLI** (`argparse`) pour spécifier output dir, proposition, etc.

#### Lot 4 — Contenu & Marketing (priorité moyenne)
15. Ajouter une **section vidéo** sur le site (embed YouTube/Reels)
16. Créer un **template Reels/Shorts** (1080×1920, 30s) avec le logo animé
17. Ajouter le **calendrier des concerts** dynamique sur le site
18. **Setlist interactive web** avec minuterie de scène (accessible via QR)
19. Créer des **cartes de visite numériques** (NFC compatible)
20. Ajouter **Google Analytics** ou équivalent sur le site

#### Lot 5 — Accessibilité (priorité basse)
21. Vérifier tous les contrastes avec WCAG AA (min 4.5:1 petits textes, 3:1 grands)
22. Corriger le ratio or/teal (3.7:1 → > 4.5:1) en assombrissant le teal ou en éclaircissant l'or
23. Ajouter `alt` textes sur le site
24. Support du **dark mode natif** (CSS `prefers-color-scheme`)

---

## Journal des modifications

| Date | Action | Auteur |
|------|--------|--------|
| 24/06/2026 | Ajout section Propositions design (3 directions) + approfondissement proposition n°3 Scène & Vintage | opencode |
| 24/06/2026 | Création dossiers propositions/ avec specs détaillées (00-originale, 01-fluid-wave, 02-rock-brute, 03-scene-vintage) | opencode |
| 24/06/2026 | Mise à jour charte-graphique-rivers-rock.md (palette + Anton + Space Mono + variantes logo + textures) | opencode |
| 24/06/2026 | Mise à jour logoutils.py (TERRACOTTA, OR_VIEILLI, TEAL_PROFOND, monogramme RR, grain overlay, crest timbre) | opencode |
| 24/06/2026 | Mise à jour generate_setlist.py (fond teal, cartes terracotta/teal, double bordure or, vague or, grain) | opencode |
| 24/06/2026 | Mise à jour generate_social.py (dégradé radial, glow logo, Space Mono) | opencode |
| 24/06/2026 | Mise à jour generate_poster.py (teal fond, vague or, halftone dots, grain) | opencode |
| 24/06/2026 | Mise à jour generate_flyer.py (couleurs Scène & Vintage, QR code verso) | opencode |
| 24/06/2026 | Mise à jour generate_banners.py (duo-tone, flare projecteur, grain, bugfix imports) | opencode |
| 24/06/2026 | Mise à jour generate_signature.py (Space Mono, or accent, bugfix imports) | opencode |
| 24/06/2026 | Mise à jour generate_stickers.py (timbre disque, gradient terracotta→or) | opencode |
| 24/06/2026 | Mise à jour generate_tshirts.py (timbre variant, reportlab_crest_vintage) | opencode |
| 24/06/2026 | Mise à jour generate_avatar.py (option monogramme RR) | opencode |
| 24/06/2026 | Mise à jour generate_animated_logo.html (néon glow, radial gradient, particules orange) | opencode |
| 24/06/2026 | Restructuration site/index.html (Scène & Vintage : Anton, Space Mono, hero, membres, concerts, contact, timbre footer) | opencode |
| 24/06/2026 | Développement complet Proposition n°1 Fluid Wave : generate.py + 12 assets générés (setlist, poster, flyer, social, banners, avatar, stickers, t-shirt, logo animé, site) | opencode |
| 24/06/2026 | Développement complet Proposition n°2 Rock Brut : generate.py + 12 assets générés (setlist, poster, flyer, social, banners, avatar, stickers, t-shirt, logo animé, site) | opencode |
| 24/06/2026 | Analyse professionnelle complète des 4 propositions : 24 problèmes identifiés, 5 lots d'améliorations proposés | opencode |
| 24/06/2026 | Correction dossier dupliqué 02-rock-brute/ → 02-rock-brut/ fusionné | opencode |
| 24/06/2026 | Création de scripts/palette.py : Config dataclass + 4 configurations (BASE, FLUID_WAVE, ROCK_BRUT, SCENE_VINTAGE) avec couleurs, fonts, tokens, flags | opencode |
| 24/06/2026 | Refonte logoutils.py : import palette, _resolve_font générique, constantes rétro-compatibles depuis DEFAULT_CFG | opencode |
| 24/06/2026 | Migration de 9 générateurs + 2 propositions vers palette.py (suppression de toutes les couleurs en dur, HexColor → CFG.rl(), tuples → CFG.pil()) | opencode |
| 24/06/2026 | Création generate.py + 12 assets pour proposition 00-originale (config BASE) et 03-scene-vintage (config SCENE_VINTAGE) — chaque proposition a désormais ses propres assets isolés | opencode |
| 24/06/2026 | Mise à jour comptes réels : Gmail `riversrockrouen@gmail.com`, YouTube `@RiversRockRouen` — mise à jour site + toutes propositions + suivi | opencode |
| 24/06/2026 | **Refonte identitaire FLUID_WAVE** : nouveau logo vague seule, palette vert profond + ambre, fonts Playfair Display + Nunito, badges ronds, vagues Bézier, grain 3% | opencode |
| 24/06/2026 | **Refonte identitaire ROCK_BRUT** : nouveau logo hexagone + RR, palette noir + orange `#FF3B00`, fonts Anton + Inter Tight + JetBrains Mono, badges pictogram, chevrons, grain 10% | opencode |
| 24/06/2026 | Système ACTIVE config : `palette.ACTIVE` + `set_active()` + `scripts/generate_all.py --config <name>` — les générateurs principaux (`scripts/`) et `site/` basculent entre les 4 chartes (scene-vintage, fluid-wave, rock-brut, originale) | opencode |
| 24/06/2026 | Nettoyage : suppression `scripts/__pycache__/` + ligne dupliquée logoutils.py dans le suivi | opencode |
| 24/06/2026 | **Correctifs professionnels** : inversion RIVERS/ROCK avatar (4 fonctions), contrastes or/terracotta/ambre ajustés, carte Virginie alignée (flexbox), Instagram handle uniformisé, polices < 6pt passées à 7pt, logo animé créé pour scene-vintage | opencode |
| 24/06/2026 | **Refonte site Scène & Vintage** : reconstruction complète (header sticky, hero glow, flexbox membres, timbre footer, grain SVG, `:root` CSS vars, responsive `@media`, favicon) — correction du bogue `gen_site()` qui écrasait avec l'Originale | opencode |
| 24/06/2026 | **Google Fonts CDN** ajouté dans les 4 logos animés (Bebas Neue pour Originale/Fluid Wave, Anton pour Rock Brut/Scène & Vintage) | opencode |
| 24/06/2026 | **Filigranes vidéo** : génération de `watermark-{200,100,50}x{200,100,50}.png` (semi-transparent, 30% opacité) pour les 4 propositions via `scripts/generate_watermarks.py` | opencode |
| 24/06/2026 | **Bleed 3mm + crop marks** sur setlist, poster, stickers (utilitaires `create_bleed_canvas` + `save_with_crop_marks`) | opencode |
| 24/06/2026 | **QR codes réels** avec `qrcode` library : social post + flyer verso (remplace les textes "QR") | opencode |
| 24/06/2026 | **Hexagone Rock Brut** corrigé : coordonnées précises SVG + générateurs | opencode |
| 24/06/2026 | **Réécriture de render_animation.py** : rendu Scène & Vintage (1080×1920, Anton, néon glow, timbre ring, flare radial, grain, still frame export) | opencode |
| 24/06/2026 | **Overlays vidéo + bumpers** : lower-third (1080×180), intro bumper (3s), outro bumper (5s) pour les 4 propositions via `scripts/generate_overlays.py` | opencode |
| 24/06/2026 | **Proposition n°5 « Ponts & Lumière »** : création complète (palette, spec, generate.py, 12 assets) — inspiration architecturale ponts de Rouen, palette nuit/acier/lumière, fonts Teko + Raleway + DM Mono, logo pont + cercle, courbes caténaires, flares lumineux | opencode |
| 24/06/2026 | **Correctifs 9/10** : balise `<title>` réparée (03), polices Teko/Raleway réelles chargées (04), WCAG contrastes corrigés (5 propositions), section Musique ajoutée (03), générateurs logoutils étendus (TEKO_PATH, RALEWAY_PATH, DMMONO_PATH) | opencode |
| 24/06/2026 | **Finalisation 9/10** : responsive 400px (03, 04), responsive 640px (01, 02, 00), monogrammes spécifiques (bridge silhouette 04, wave RR 01, hexagon RR 02), animation wave ondulée (01), hiérarchie typographique clamp() (00) — 11 correctifs sur 5 propositions | opencode |
| 24/06/2026 | **Assets manquants générés** : `scripts/generate_missing.py` — business cards, signatures, mockups, stage plots, tech sheets, lyrics (×12) pour les 5 propositions — 85 fichiers créés, total projet 176 assets | opencode |
| 24/06/2026 | **Mise en ligne GitHub Pages** : dépôt clucet/rivers_rock passé en public, Pages activé sur `https://clucet.github.io/rivers_rock/` — retrait proposition 00 Originale de la sélection | opencode |
| 24/06/2026 | **Proposition 05 « Neon Nights »** : cyberpunk — violet/rose/cyan, fonts Orbitron + Rajdhani + JetBrains Mono | opencode |
| 24/06/2026 | **Proposition 06 « Sable & Bronze »** : voyage — sable/terre cuite/bronze, fonts Cinzel + Lato + Cormorant | opencode |
| 24/06/2026 | **QR codes réels** : branchement `draw_qr_pillow`/`draw_qr_reportlab` dans les 6 propositions + flyer 03 | opencode |
| 24/06/2026 | **Bleed + crop marks** : appliqués aux générateurs business card, stage plot, t-shirt | opencode |
| 24/06/2026 | **Section Musique** : embed YouTube ajouté aux propositions 01 et 04 | opencode |
| 24/06/2026 | **Setlist interactive web** : `scripts/generate_setlist_web.py` + page avec minuterie, BPM, chronomètre | opencode |
| 24/06/2026 | **Facebook Page** `Rivers Rock Rouen` créée — tous les réseaux sont maintenant opérationnels | opencode |
| 24/06/2026 | **Correctifs 9/10** : WCAG 05/06, dark mode 03, YouTube placeholders, `prefers-reduced-motion`, multi-favicon, scroll indicator cliquable, bleed + crop marks sur les scripts principaux | opencode |
| 24/06/2026 | **Audit complet web/print/vidéo** : 25 correctifs identifiés, priorités établies | opencode |
| 24/06/2026 | **Correctifs 9/10** : WCAG 05/06, dark mode 03, YouTube placeholders, `prefers-reduced-motion`, multi-favicon, bleed + crop marks | opencode |
| 24/06/2026 | **Enrichissement 5 propositions** : sticky nav, member cards, scroll indicator, footer logo, responsive, dark mode pour 01, 02, 04, 05, 06 | opencode |
| 24/06/2026 | **Propositions 07 Nordik, 08 Grunge, 09 Jazz Club** : 3 nouvelles identités complètes (palette, fonts, generate.py, 35 assets chacune) | opencode |
| 24/06/2026 | **Correctifs 10/10** : favicons, formulaires de contact, animations, contrastes, halftone dots, double bordures | opencode |
