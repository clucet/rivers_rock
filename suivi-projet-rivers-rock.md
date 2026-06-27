<!-- AUTO-UPDATE: Dernière mise à jour automatique par opencode (28/06/2026) -->
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
| Setlist interactive web (minuteur, BPM, chronomètre) | `scripts/generate_setlist_web.py`, `setlist/index.html` | 24/06 |
| GitHub Pages activé + page comparaison 6 propositions | `propositions/index.html` | 24/06 |
| Facebook Page « Rivers Rock Rouen » créée | — | 24/06 |

### 📋 À faire
- [x] Création comptes réseaux — Gmail + YouTube + Instagram + Facebook faits
  - Gmail : `riversrock_rouen@gmail.com`
  - YouTube : `@RiversRockRouen`
  - Instagram : `@riversrock_rouen` — 🔴 désactivé (appel en cours, secours `@riversrock_rouen`)
  - Facebook : `Rivers Rock Rouen`
- [ ] Publier les 5 posts de lancement sur Facebook — brouillons prêts dans `propositions/drafts/publications-facebook.md`
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
| `scripts/palette.py` | Palette centralisée — 9 configurations (Config dataclass) |
| `scripts/logoutils.py` | Fonctions partagées (création logo, QR, bleed, crop marks) |
| `scripts/generate_all.py` | Générateur multi-config (`--config`) |
| `scripts/generate_site.py` | Génération du site live |
| `scripts/generate_missing.py` | Assets manquants (business card, lyrics, stage plot, tech sheet) |
| `scripts/generate_overlays.py` | Overlays vidéo (lower-third, bumper intro/outro) |
| `scripts/generate_watermarks.py` | Filigranes vidéo semi-transparents (200/100/50px) |
| `scripts/generate_setlist_web.py` | Setlist interactive web (minuteur, BPM) |
| `scripts/generate_charte_pdf.py` | PDF chartes graphiques (logos + assets) |
| `propositions/index.html` | Page comparaison des 9 propositions |
| `propositions/drafts/publications-facebook.md` | Brouillons Facebook (5 posts) |
| `propositions/infos-comptes-reseaux.md` | Accès réseaux sociaux du groupe |
| `setlist/index.html` | Setlist interactive (minuteur concert) |
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
│   ├── 04-ponts-lumiere/
│   │   ├── spec.md
│   │   ├── generate.py
│   │   └── assets/
│   │       ├── index.html
│   │       ├── pdf/ (5 fichiers)
│   │       └── templates/ (15 fichiers)
│   ├── 05-neon-nights/
│   │   ├── spec.md
│   │   ├── generate.py
│   │   └── assets/ (35 fichiers)
│   ├── 06-sable-bronze/
│   │   ├── spec.md
│   │   ├── generate.py
│   │   └── assets/ (35 fichiers)
│   ├── 07-nordik/
│   │   ├── spec.md, charte-graphique.md, generate.py
│   │   └── assets/ (35 fichiers)
│   ├── 08-grunge/
│   │   ├── spec.md, charte-graphique.md, generate.py
│   │   └── assets/ (35 fichiers)
│   ├── 09-jazz-club/
│   │   ├── spec.md, charte-graphique.md, generate.py
│   │   └── assets/ (35 fichiers)
│   ├── drafts/
│   │   └── publications-facebook.md
│   └── 03-scene-vintage/
│   ├── 03-scene-vintage/
│   │   ├── spec.md
│   │   ├── generate.py
│   │   └── assets/
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

- **QR code dynamique** : URL courte redirigeant vers la dernière version de la setlist — ✅ fait, QR réels branchés
- **Setlist interactive** : app web accessible depuis le QR, avec minuterie scène — ✅ fait, `setlist/index.html`
- **Fiche technique son** (stage plot) — ✅ fait
- **Logo animé** pour Reels/Shorts — ✅ fait, `render_animation.py` paramétrable
- **PDF chartes graphiques** — ✅ fait, `scripts/generate_charte_pdf.py` + cairosvg
- **Pages d'aperçu** — ✅ fait, `scripts/generate_preview.py` — 9 preview.html avec logos, palette, iframe animé
- **PWA Setlist offline** — ✅ fait, `setlist/manifest.json` + `sw.js`
- **EPK / Press Kit** — ✅ fait, `epk/index.html`
- **CI/CD GitHub Actions** — ✅ fait, `.github/workflows/generate.yml`
- **CMYK print** — ✅ fait, `scripts/convert_to_cmyk.py` + flag `--cmyk`
- **Setlist centralisée** — ✅ fait, `scripts/setlist_data.py` (13 fichiers)
- **WCAG auto-checker** — ✅ fait, `scripts/palette.py` — `contrast_ratio()`, `check_wcag_aa()`
- **Spotify embeds** — ✅ fait, iframes dans les 9 sites (placeholder à remplacer)

---

## Prochaines évolutions possibles (28 juin 2026)

| # | Suggestion | Effort | Impact | Description |
|---|-----------|--------|--------|-------------|
| # | Suggestion | Effort | Impact | Statut | Description |
|---|-----------|--------|--------|--------|-------------|
| # | Suggestion | Effort | Impact | Statut | Description |
|---|-----------|--------|--------|--------|-------------|
| 1 | **PWA Setlist** | 🟢 Faible | 🟠 Moyen | ✅ Fait | Service worker + manifest — utilisable hors-ligne sur scène |
| 2 | **Cartes NFC** | 🟡 Moyen | 🟠 Moyen | 🔜 | Générer des cartes de visite NFC compatibles Apple Wallet / Google Wallet avec les designs existants |
| 3 | **Spotify / Apple Music** | 🟢 Faible | 🔴 Élevé | 🔶 Partiel | Iframes Spotify ajoutés aux 15 sites (placeholder à remplacer) |
| 4 | **Vote setlist public** | 🟡 Moyen | 🔴 Élevé | 🔜 | Page publique où les fans votent pour les chansons du prochain concert |
| 5 | **Merch store** | 🟡 Moyen | 🟠 Moyen | 🔜 | Page merch liée à Printful/Spreadshirt avec les designs existants |
| 6 | **Mailing list** | 🟢 Faible | 🟡 Moyen | 🔜 | Formulaire newsletter + envoi d'emails automatiques |
| 7 | **EPK / Press Kit** | 🟢 Faible | 🔴 Élevé | ✅ Fait | `epk/index.html` — bio, membres, répertoire, downloads |
| 8 | **Planning répétitions** | 🟢 Faible | 🟡 Moyen | ✅ Fait | `planning/index.html` — tableau 5×7×3, localStorage, copie WhatsApp |
| 9 | **CI/CD GitHub Actions** | 🟡 Moyen | 🔴 Élevé | ✅ Fait | `.github/workflows/generate.yml` |
| 10 | **Dashboard analytics** | 🟡 Moyen | 🟢 Faible | 🔜 | Tableau de bord privé avec stats visites, QR scans, vues setlist |
| 11 | **Vote groupe** | 🟢 Faible | 🔴 Élevé | ✅ Fait | `propositions/vote/index.html` — top 3 par email |
| 12 | **Plan vote** | 🟢 Faible | 🔴 Élevé | ✅ Fait | `plan-vote-groupe.md` — procédure pour les 5 membres |
| 13 | **MP4 toutes les props** | 🟡 Moyen | 🟠 Moyen | ✅ Fait | 14 frame handlers + dispatch dans render_animation.py |
| 14 | **Sessions photos** | 🟡 Moyen | 🔴 Élevé | 🔜 | 5 portraits + 1 photo groupe + photos scène — prérequis lancement réseaux |
| 15 | **Instagram** | 🟡 Moyen | 🔴 Élevé | 🔜 | Résoudre blocage `@riversrockrouen` ou activer `@riversrock_rouen` |

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
| **Adresse** | `riversrock_rouen@gmail.com` |
| **Mot de passe** | `!LeGroupe76140@` |

### ✅ YouTube — Créé
| Champ | Valeur |
|-------|--------|
| **Chaîne** | Rivers Rock Rouen |
| **Handle** | `@RiversRockRouen` |
| **Email lié** | `riversrock_rouen@gmail.com` |

### 📋 À créer
| Plateforme | Nom prévu | Avatar |
|------------|-----------|--------|
| Instagram | `@riversrock_rouen` | `propositions/03-scene-vintage/assets/templates/avatar.png` |
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
| 24/06/2026 | Mise à jour comptes réels : Gmail `riversrock_rouen@gmail.com`, YouTube `@RiversRockRouen` — mise à jour site + toutes propositions + suivi | opencode |
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
| 24/06/2026 | **Enrichissement 5 propositions** : sticky nav, member cards grid, scroll indicator, footer logo SVG, dark mode CSS, responsive 640+400px pour 01, 02, 04, 05, 06 | opencode |
| 24/06/2026 | **Proposition 07 « Nordik »** : minimaliste scandinave — blanc/gris/lin, Inter seul (tous usages), logo trait horizontal, setlist fond blanc pur | opencode |
| 24/06/2026 | **Proposition 08 « Grunge »** : anti-design — papier/toner/marqueur rose, fonts Rubik Glitch + Space Mono + Syne Mono, logo tampon rouge, grain 15% | opencode |
| 24/06/2026 | **Proposition 09 « Jazz Club »** : cuivres/velours — nuit/or/cuivre/rouge, fonts Playfair + Karla + DM Mono, logo cercle projecteur + ligne dorée | opencode |
| 24/06/2026 | **Correctifs 10/10** : favicons ajoutés aux propositions 07/08/09, suivi-projet mis à jour (journal + todo 9 propositions) | opencode |
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
| 24/06/2026 | **Enrichissement 5 propositions** : sticky nav, member cards, scroll indicator, footer logo, responsive, dark mode pour 01, 02, 04, 05, 06 | opencode |
| 24/06/2026 | **Correctifs 10/10** : favicons, formulaires de contact, animations, contrastes, halftone dots, double bordures | opencode |
| 25/06/2026 | **Formulaires de contact** ajoutés dans les 9 propositions (nom/email/message) | opencode |
| 25/06/2026 | **Favicons inline** ajoutés aux propositions 01, 02, 04, 05, 06 | opencode |
| 25/06/2026 | **Photos placeholders** intégrés dans les cartes membres des 9 propositions | opencode |
| 25/06/2026 | **Audit évolutions futures** : 10 suggestions identifiées (PWA, NFC, Spotify, vote setlist, merch, newsletter, EPK, planning, CI/CD, analytics) | opencode |
| 25/06/2026 | **Lot 1 — 9 logos SVG vectoriels** : grilles précises, proportions professionnelles, coordonnées mathématiques | opencode |
| 25/06/2026 | **Lot 2 — 36 déclinaisons SVG** : mono, icône, compact, watermark × 9 propositions | opencode |
| 25/06/2026 | **Lot 3-5 — Chartes enrichies** : grilles de construction, règles d'usage pro, preload SVG dans générateurs | opencode |
| 25/06/2026 | **Instagram `@riversrock_rouen` désactivé** — appel en cours. Handle de secours : `@riversrock_rouen` | opencode |
| 25/06/2026 | **Chartes PDF avec logos + assets** : cairosvg installé, rendu SVG, miniatures templates | opencode |
| 25/06/2026 | **Pages d'aperçu par proposition** : `scripts/generate_preview.py` — 9 preview.html avec logos, palette, iframe animé, miniatures PDF, charte ZIP | opencode |
| 25/06/2026 | **Lien Aperçu + Charte PDF** dans propositions/index.html pour chaque carte | opencode |
| 26/06/2026 | **Lot 1 — Print** : bleed/crop sur flyer, police 5-6pt→7pt (07/08/09), script CMYK Ghostscript + flag `--cmyk` | opencode |
| 26/06/2026 | **Lot 3 — Technique** : factorisation 4 fonctions dans logoutils.py (gradient, waves, grain, footer) + setlist centralisée setlist_data.py (13 fichiers mis à jour) | opencode |
| 26/06/2026 | **Lot 5 — Accessibilité** : dark mode préfères-color-scheme sur sites 07/08/09 + WCAG auto-checker dans palette.py | opencode |
| 26/06/2026 | **PWA Setlist** : manifest.json + sw.js + enregistrement service worker — utilisable hors-ligne sur scène | opencode |
| 26/06/2026 | **EPK / Press Kit** : `epk/index.html` — bio, membres, répertoire, downloads chartes/PDF, liens réseaux | opencode |
| 26/06/2026 | **CI/CD GitHub Actions** : `.github/workflows/generate.yml` — validation → génération → déploiement automatique | opencode |
| 26/06/2026 | **README.md** : documentation complète du projet (structure, commandes, liens) | opencode |
| 26/06/2026 | **.gitignore** : patterns pour previews PNG, chartes ZIP, /tmp/ | opencode |
| 26/06/2026 | **Spotify embeds** : iframes Spotify playlist ajoutés aux 9 propositions (placeholder `REMPLACER_PAR_ID`) + section Musique créée pour 00-originale | opencode |
| 26/06/2026 | **Rendu MP4** : tentative à l'échelle 0.5 — trop lent (add_grain pixel loop). MP4 existant conservé. Optimisation nécessaire (numpy) pour le rendu final | opencode |
| 26/06/2026 | **Audit complet 3 métiers** : webdesigner, infographiste, community manager — 10 faiblesses critiques identifiées, matrice P1→P4 | opencode |
| 26/06/2026 | **Correctifs P1/P2** : Instagram handle migré (30 fichiers), responsive 07/08/09, formulaire FormSubmit, SEO meta tags, focus-visible, font-display:swap, favicons distincts, bleed/crop dans generate_missing.py | opencode |
| 26/06/2026 | **5 nouvelles propositions** : 10-Bitume (street), 11-Cordes&Voix (acoustique), 12-Héritage (patrimoine), 13-Rubicon (americana), 14-Minuit (french touch) — palette.py, 25 SVG logos, 5 generate.py, 5 animated logo HTML, previews, chartes PDF | opencode |
| 26/06/2026 | **Assets complets pour 10-14** : setlist, poster, flyer, social, banners, avatar, stickers, t-shirt générés pour les 5 nouvelles propositions | opencode |
| 26/06/2026 | **propositions/index.html mis à jour** : 14 cartes (ajout 10-14), badges CSS, tableau legend complété, bandeau coloré par proposition | opencode |
| 26/06/2026 | **Chartes graphiques enrichies** : page 5 "Règles d'usage du logo" ajoutée aux 14 chartes PDF | opencode |
| 26/06/2026 | **liens-projet.md** : fichier de référence avec tous les URLs du projet | opencode |
| 26/06/2026 | **Webdesign cards** : barre colorée (border-top), flex layout, ombre portée, footer ancré — les 14 propositions visuellement groupées | opencode |
| 27/06/2026 | **Layout cards v2** : cartes restructurées en 2 blocs (card-link + card-actions séparée), bouton "Site" devient un vrai lien, barre d'actions visuellement distincte | opencode |
| 27/06/2026 | **Chartes PDF enrichies** : pagination + footer (nom prop + page X/5) + fond depuis config + contrastes WCAG calculés + proposition 00-originale ajoutée (15 chartes) | opencode |
| 27/06/2026 | **Refonte 00-originale → Ombre & Lumière** : concept N&B (noir/gris/blanc), palette monochrome, logo diaphragme photo, fonts Playfair/Inter/SpaceMono, grain 12%, site argentique | opencode |
| 27/06/2026 | **MP4 toutes les 14 propositions** : 8 nouveaux frame handlers (nordik, grunge, jazz-club, bitume, cordes-voix, heritage, rubicon, minuit), dispatch via dict | opencode |
| 27/06/2026 | **PNG optimisation** : pngquant sur tous les templates réseaux (146 fichiers) | opencode |
| 27/06/2026 | **Page vote** : `propositions/vote/index.html` — sélection top 3, envoi par email | opencode |
| 27/06/2026 | **README.md** : mis à jour avec 15 propositions, table complète | opencode |
| 27/06/2026 | **Plan vote groupe** : `plan-vote-groupe.md` — procédure pour recueillir les votes des 5 membres | opencode |
| 28/06/2026 | **Setlists/posters fonds blancs** : économie d'encre ~80%, lisibilité améliorée — 15 propositions corrigées + scripts/generate_setlist.py refactoré | opencode |
| 28/06/2026 | **Templates Reels/Shorts** : 1080×1920 HTML animé pour Rock Brut et Neon Nights (logo, nom, date, particules) | opencode |
| 28/06/2026 | **Script finaliser.py** : bascule automatique de la proposition gagnante (archive, palette, site, README, commit, push) | opencode |
| 28/06/2026 | **Analyse impression** : `impression-production.md` — Brother DCP-L3560CDW, production famille, prestataires, budget | opencode |
| 28/06/2026 | **Premiers votes** : 3/5 reçus — Neon Nights et Rock Brut en tête, Grunge 3e. 2 votes restants demain | opencode |
| 28/06/2026 | **Planning répétitions** : `planning/index.html` — tableau interactif 5×7×3 créneaux, sauvegarde localStorage, copie WhatsApp, stats disponibilités | opencode |
| 28/06/2026 | **GIF logo animé** : `pdf/templates/logo-animated.gif` — 240px, 10fps, 855 Ko (signature email, WhatsApp) | opencode |
| 28/06/2026 | **Signature email HTML** : `pdf/templates/email-signature.html` — GIF intégré, prêt à copier dans Gmail | opencode |
| 28/06/2026 | **Barre progression votes** : `propositions/vote/index.html` — suivi 0→5 votes, grille cliquable, localStorage | opencode |
| 28/06/2026 | **Nettoyage `site/`** : dossier supprimé, contenu déplacé à la racine (index.html, setlist/, epk/, planning/) | opencode |
| 28/06/2026 | **Admin docs** : `ADMIN.md` + `COMMANDS.md` — documentation administration et aide-mémoire commandes | opencode |
| 28/06/2026 | **🏆 Rock Brut élu** : 4 votes sur 5 — Rock Brut remporte largement devant Neon Nights. Proposition finalisée, 14 autres archivées. Root site, README, liens mis à jour. Vote page marquée | opencode |
