# Rivers Rock — Administration du projet

_Version 1.0 — 28 juin 2026_

---

## 1. Présentation

**Rivers Rock** est un groupe de reprises rock basé à Rouen (5 musiciens).
Ce projet génère **15 propositions d'identité visuelle** complètes (sites, PDF, templates réseaux, chartes graphiques, logos animés, vidéos).

- **Dépôt :** [github.com/clucet/rivers_rock](https://github.com/clucet/rivers_rock)
- **Site :** [clucet.github.io/rivers_rock](https://clucet.github.io/rivers_rock)
- **Technologies :** Python (ReportLab, Pillow, cairosvg) + HTML/CSS + GitHub Pages

---

## 2. Structure du projet

```
rivers_rock/
├── ADMIN.md                   ← Ce fichier
├── COMMANDS.md                ← Aide-mémoire des commandes
├── README.md                  ← Documentation du projet
├── suivi-projet-rivers-rock.md ← Journal de bord complet
├── liens-projet.md            ← Tous les URLs du projet
├── plan-vote-groupe.md        ← Procédure de vote du groupe
├── impression-production.md  ← Analyse impression et production
├── .gitignore
├── .github/workflows/generate.yml  ← CI/CD (GitHub Actions)
│
├── scripts/                   ← Générateurs Python (31 fichiers)
│   ├── palette.py             ← ★ CENTRAL : 15 Configs couleurs/fonts/tokens/flags
│   ├── logoutils.py           ← Utilitaires partagés (dessin, polices, QR)
│   ├── setlist_data.py        ← Données setlist centralisées (12 titres)
│   ├── generate_all.py        ← Point d'entrée principal CLI
│   ├── generate_preview.py    ← Pages d'aperçu par proposition
│   ├── generate_charte_pdf.py ← Chartes graphiques PDF (5 pages)
│   ├── generate_missing.py    ← Assets manquants (business card, lyrics, stage…)
│   ├── generate_setlist.py    ← Setlist PDF (config active)
│   ├── generate_poster.py     ← Poster A4
│   ├── generate_flyer.py      ← Flyer A6
│   ├── generate_social.py     ← Templates Instagram
│   ├── generate_banners.py    ← Bannières Facebook/YouTube
│   ├── generate_avatar.py     ← Avatar PNG
│   ├── generate_stickers.py   ← Planche de stickers A4
│   ├── generate_tshirts.py    ← T-shirt print + mockup
│   ├── generate_businesscard.py ← Carte de visite
│   ├── generate_signature.py  ← Signature email
│   ├── generate_stageplot.py  ← Stage plot technique
│   ├── generate_techsheet.py  ← Fiche technique sérigraphe
│   ├── generate_lyrics.py     ← 12 fiches paroles
│   ├── generate_setlist_web.py← Setlist interactive (PWA)
│   ├── generate_site.py       ← Copie le site actif vers site/
│   ├── generate_watermarks.py ← Watermarks vidéo
│   ├── generate_overlays.py   ← Overlays vidéo (bumpers, lower-third)
│   ├── render_animation.py    ← Rendu MP4 logo animé (14 configs)
│   ├── convert_to_cmyk.py     ← Post-process CMYK via Ghostscript
│   ├── migrer_instagram.py    ← Migration handle Instagram
│   ├── finaliser.py           ← Bascule proposition gagnante
│   └── _generate_props.py    ← Générateur des props 10-14
│
├── propositions/              ← 15 propositions identitaires
│   ├── index.html             ← Page de comparaison des 15 props
│   ├── chartes-graphiques.zip ← ZIP des 15 chartes PDF
│   ├── vote/index.html        ← Page de vote du groupe
│   ├── drafts/publications-facebook.md ← 7 posts Facebook prêts
│   ├── infos-comptes-reseaux.md ← Identifiants réseaux sociaux
│   ├── 00-originale/          ← Ombre & Lumière (N&B, argentique)
│   ├── 01-fluid-wave/         ← Fluid Wave (organique, aquatique)
│   ├── 02-rock-brut/          ← Rock Brut (industriel, rock)
│   ├── … (03 à 14)            ← Chaque proposition a la même structure :
│   │   ├── generate.py        ← Générateur (site + PDF + templates)
│   │   ├── charte-graphique-XX.pdf ← Charte graphique PDF (5 pages)
│   │   └── assets/
│   │       ├── index.html     ← Site de la proposition
│   │       ├── preview.html   ← Page d'aperçu
│   │       ├── logo*.svg      ← 5 variantes de logo
│   │       ├── pdf/           ← PDF générés
│   │       └── templates/     ← Templates PNG + HTML
│   └── …
│
└── site/                      ← Site déployé sur GitHub Pages
    ├── index.html             ← Root site (copie de la config active)
    ├── epk/index.html         ← Press Kit
    ├── setlist/               ← Setlist interactive (PWA offline)
    │   ├── index.html
    │   ├── manifest.json
    │   └── sw.js              ← Service Worker
    └── planning/index.html    ← Planning répétitions
```

---

## 3. Commandes essentielles

Toutes les commandes s'exécutent depuis la racine du projet (`/home/voidmaster/dev/rivers_rock`).

| Commande | Action |
|----------|--------|
| `python3 scripts/generate_all.py --config scene-vintage` | Génère site + PDF pour une proposition |
| `python3 scripts/generate_all.py --config scene-vintage --site-only` | Site uniquement |
| `python3 scripts/generate_preview.py` | Regénère toutes les pages d'aperçu |
| `python3 scripts/generate_charte_pdf.py` | Regénère les 15 chartes PDF |
| `python3 scripts/generate_missing.py` | Regénère les assets manquants (lyrics, stage…) |
| `python3 scripts/convert_to_cmyk.py --all` | Convertit tous les PDF en CMYK |
| `python3 scripts/render_animation.py --config scene-vintage` | Rendu MP4 logo animé |
| `python3 scripts/finaliser.py --config rock-brut` | Bascule définitive vers une proposition |
| `python3 scripts/migrer_instagram.py` | Migre le handle Instagram (secours) |

Voir `COMMANDS.md` pour la liste complète avec tous les arguments.

---

## 4. Les 15 propositions

| # | Nom | Dossier | Config | Ambiance |
|---|-----|---------|--------|----------|
| 00 | Ombre & Lumière | `00-originale` | `BASE` | N&B, argentique, diaphragme |
| 01 | Fluid Wave | `01-fluid-wave` | `FLUID_WAVE` | Organique, vert/ambre |
| 02 | Rock Brut | `02-rock-brut` | `ROCK_BRUT` | Industriel, noir/orange |
| 03 | Scène & Vintage | `03-scene-vintage` | `SCENE_VINTAGE` | Rétro, teal/terracotta/or |
| 04 | Ponts & Lumière | `04-ponts-lumiere` | `PONTS_LUMIERE` | Architectural, nuit/acier |
| 05 | Neon Nights | `05-neon-nights` | `NEON_NIGHTS` | Cyberpunk, violet/rose/cyan |
| 06 | Sable & Bronze | `06-sable-bronze` | `SABLE_BRONZE` | Voyage, sable/terre cuite |
| 07 | Nordik | `07-nordik` | `NORDIK` | Minimal, blanc/gris |
| 08 | Grunge | `08-grunge` | `GRUNGE` | Anti-design, papier/toner |
| 09 | Jazz Club | `09-jazz-club` | `JAZZ_CLUB` | Cuivres, noir/or/rouge |
| 10 | Bitume | `10-bitume` | `BITUME` | Street art, gris/fluo |
| 11 | Cordes & Voix | `11-cordes-voix` | `CORDES_VOIX` | Acoustique, crème/acajou |
| 12 | Héritage | `12-heritage` | `HERITAGE` | Patrimoine, vitrail/or |
| 13 | Rubicon | `13-rubicon` | `RUBICON` | Americana, orange/bleu |
| 14 | Minuit | `14-minuit` | `MINUIT` | French touch, velours/or |

---

## 5. Config active

La config active est définie dans `scripts/palette.py` ligne ~490 :

```python
ACTIVE = NEON_NIGHTS   ← Par défaut. Change selon la proposition affichée sur le root site.
```

Le root site (`site/index.html`) affiche toujours la proposition définie par `ACTIVE`.
Pour changer :
```bash
python3 scripts/generate_all.py --config rock-brut --site-only
```
→ Modifie `ACTIVE` dans palette.py via `set_active()`.

---

## 6. Déploiement (GitHub Pages)

**Automatique :** `.github/workflows/generate.yml` — à chaque `git push` sur `main` :
1. Installe les dépendances Python
2. Regénère les previews (`generate_preview.py --skip-thumbs`)
3. Convertit les PDF en CMYK (`convert_to_cmyk.py --all`)
4. Déploie sur GitHub Pages

**Manuel :**
```bash
git add -A && git commit -m "message" && git push
```

---

## 7. Dépendances

### Python
```bash
pip install reportlab Pillow qrcode cairosvg numpy
```

### Système
```bash
sudo apt-get install poppler-utils ghostscript
```

### Polices Google Fonts (téléchargement automatique)
Les 20 polices sont résolues automatiquement dans `~/.fonts/` via `logoutils._resolve_font()`.
Si une police manque, elle est téléchargée depuis le dépôt Google Fonts GitHub.
Liste complète dans `scripts/palette.py` — `FONT_MAP` (lignes 442-462).

---

## 8. Impression

- **Imprimante :** Brother DCP-L3560CDW (laser couleur, A4 max, 2400×600 dpi)
- **Papier :** 80g pour setlists, 120-160g pour flyers, adhésif pour stickers
- **CMYK :** `python3 scripts/convert_to_cmyk.py --all` avant impression
- **Bleed/crop marks :** Inclus dans tous les PDF (3mm)
- **Voir :** `impression-production.md` pour les détails complets

---

## 9. Réseaux sociaux

| Plateforme | Identifiant | Mot de passe | Statut |
|------------|-------------|-------------|--------|
| **Gmail** | riversrock_rouen@gmail.com | `!LeGroupe76140@` | ✅ |
| **YouTube** | @RiversRockRouen | via Gmail | ✅ |
| **Facebook** | Rivers Rock Rouen | Compte personnel | ✅ |
| **Instagram** | @riversrockrouen | via Gmail | 🔴 Désactivé (appel en cours) |
| **Instagram secours** | @riversrock_rouen | via Gmail | ✅ Prêt |

### Publications Facebook
7 posts draftés dans `propositions/drafts/publications-facebook.md`.
Prêts à publier (copier/coller + ajouter le visuel).

---

## 10. Dépannage

| Problème | Solution |
|----------|----------|
| **Police manquante** | `python3 -c "from logoutils import _resolve_font; print(_resolve_font('Bangers-Regular.ttf'))"` |
| **MP4 trop lent** | Ajouter `--no-grain` ou réduire le scale (`--render-scale 0.25`) |
| **Preview sans logo animé** | `python3 scripts/generate_preview.py --skip-thumbs` |
| **Site pas à jour** | `python3 scripts/generate_all.py --config <nom> --site-only` |
| **Formulaires contact** | Les formulaires utilisent `formsubmit.co` (gratuit, sans inscription) |
| **Votes bloqués** | Vérifier `propositions/vote/index.html` — envoi par `mailto:` |
| **Instagram désactivé** | Appel en cours via help.instagram.com. Secours : `python3 scripts/migrer_instagram.py` |

---

## 11. URLs utiles

| Page | URL |
|------|-----|
| **Site racine** | [clucet.github.io/rivers_rock](https://clucet.github.io/rivers_rock) |
| **Propositions** | [clucet.github.io/rivers_rock/propositions/](https://clucet.github.io/rivers_rock/propositions/) |
| **Vote** | [clucet.github.io/rivers_rock/propositions/vote/](https://clucet.github.io/rivers_rock/propositions/vote/) |
| **Setlist** | [clucet.github.io/rivers_rock/setlist/](https://clucet.github.io/rivers_rock/setlist/) |
| **EPK** | [clucet.github.io/rivers_rock/epk/](https://clucet.github.io/rivers_rock/epk/) |
| **Planning** | [clucet.github.io/rivers_rock/planning/](https://clucet.github.io/rivers_rock/planning/) |
| **Dépôt** | [github.com/clucet/rivers_rock](https://github.com/clucet/rivers_rock) |

---

_Document généré le 28 juin 2026. Pour toute question, ouvrir une issue sur le dépôt GitHub._
