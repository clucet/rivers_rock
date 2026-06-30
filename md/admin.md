# Rivers Rock — Administration

_Version 1.2 — Rock Brut (proposition élue)_

## Stack technique

| Technologie | Usage |
|-------------|-------|
| Python 3.12 | Génération des assets (ReportLab, Pillow, cairosvg) |
| HTML/CSS/JS | Sites web statiques |
| GitHub Pages | Hébergement initial |
| **OVH VPS-1** | **Hébergement actuel** — [riversrock.fr](https://riversrock.fr) |

## Proposition élue : Rock Brut

| Élément | Valeur |
|---------|--------|
| Palette | Noir `#0A0A0A`, Orange `#FF3B00`, Blanc `#FFFFFF` |
| Logo | Hexagone extérieur orange (ouvert top-left) + intérieur blanc + RR centré |
| Polices | Anton (titres), Inter Tight (corps), JetBrains Mono (data) |

## Structure projet

```
rivers_rock/
├── index.html              ← Site racine
├── templates/              ← Templates réseaux (avatar, signature, social, banners...)
├── setlist/                ← Setlist interactive (PWA avec service worker)
├── epk/                    ← Press Kit
├── planning/               ← Planning répétitions
├── 404.html                ← Page introuvable
├── propositions/
│   ├── 02-rock-brut/       ← Proposition élue (generate.py + assets/)
│   │   ├── generate.py     ← Générateur principal
│   │   ├── charte-graphique.md
│   │   ├── assets/
│   │   │   ├── index.html  ← Site de la proposition
│   │   │   ├── logo*.svg   ← 5 variantes
│   │   │   ├── pdf/        ← 16 PDFs
│   │   │   └── templates/  ← Fichiers spécifiques (bumpers, watermarks)
│   ├── vote/               ← Page de vote (archivée)
│   └── index.html          ← Page comparaison (archivée)
├── archive/                ← 14 propositions non retenues
├── scripts/                ← 29 générateurs Python
│   ├── palette.py          ← Configuration centralisée
│   ├── logoutils.py        ← Utilitaires de dessin
│   ├── generate_all.py     ← Point d'entrée CLI
│   └── ...
└── md/                     ← Documentation
```

## Commandes essentielles

```bash
# Regénérer le site racine
python3 scripts/generate_all.py --config rock-brut --site-only

# Regénérer les templates réseaux
python3 scripts/generate_avatar.py
python3 scripts/generate_signature.py
python3 -c "from generate_social import generate_post, generate_story; generate_post(); generate_story()"
python3 -c "from generate_banners import gen_banners; gen_banners()"

# Regénérer les PDFs
python3 -c "import sys; sys.path.insert(0, 'scripts'); sys.path.insert(0, 'propositions/02-rock-brut'); from generate import *; gen_setlist(); gen_poster(); gen_flyer(); gen_stickers(); gen_tshirt()"

# Conversion CMYK
python3 scripts/convert_to_cmyk.py --input propositions/02-rock-brut/assets/pdf/setlist-rock-brut.pdf --output propositions/02-rock-brut/assets/pdf/setlist-rock-brut-cmyk.pdf

# Rendu MP4
python3 scripts/render_animation.py --config rock-brut --render-scale 0.5
```

## Déploiement

**Actuel :** Transfert rsync vers OVH VPS-1 — [riversrock.fr](https://riversrock.fr)
**Source :** Dépôt GitHub → `rsync -avz --exclude=.git --exclude=archive /home/.../rivers_rock/ root@IP:/var/www/riversrock/`

## Réseaux

| Plateforme | Identifiant | Statut |
|------------|-------------|--------|
| Gmail | riversrock_rouen@gmail.com / `!LeGroupe76140@` | ✅ |
| YouTube | @RiversRockRouen | ✅ |
| Facebook | Rivers Rock Rouen | ✅ |
| Instagram | @riversrockrouen | 🔴 Désactivé (appel en cours) |

## URLs

| Page | URL |
|------|-----|
| Site | [riversrock.fr](https://riversrock.fr) |
| Setlist | [riversrock.fr/setlist/](https://riversrock.fr/setlist/) |
| EPK | [riversrock.fr/epk/](https://riversrock.fr/epk/) |
| Planning | [riversrock.fr/planning/](https://riversrock.fr/planning/) |

## Dépendances

```bash
pip install reportlab Pillow qrcode cairosvg numpy
sudo apt-get install poppler-utils ghostscript
```

## Dépannage

| Problème | Solution |
|----------|----------|
| Police manquante | `python3 -c "from logoutils import _resolve_font; _resolve_font('Anton-Regular.ttf')"` |
| Templates pas à jour | `python3 scripts/generate_avatar.py` |
| Site pas à jour | `python3 scripts/generate_all.py --config rock-brut --site-only` |
| Push rejeté | `git pull --rebase && git push` |
