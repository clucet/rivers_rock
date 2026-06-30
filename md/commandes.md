# Rivers Rock — Aide-mémoire des commandes

_Version 1.2 — Rock Brut (proposition élue)_

## Génération des templates réseaux

```bash
python3 scripts/generate_avatar.py        # avatar.png + avatar-transparent.png + monogramme-rr.png
python3 scripts/generate_signature.py     # 7 signatures email (générique + 5 membres)
python3 -c "from generate_social import generate_post, generate_story; generate_post(); generate_story()"
python3 -c "from generate_banners import gen_banners; gen_banners()"
python3 -c "from generate_tshirts import generate_mockup; generate_mockup()"
```

## Génération des PDFs

```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
sys.path.insert(0, 'propositions/02-rock-brut')
from generate import gen_setlist, gen_poster, gen_flyer, gen_stickers, gen_tshirt
gen_setlist(); gen_poster(); gen_flyer(); gen_stickers(); gen_tshirt()
"
```

## Rendu MP4

```bash
python3 scripts/render_animation.py --config rock-brut --render-scale 0.5
python3 scripts/render_animation.py --config rock-brut --render-scale 1.0
```

## Conversion CMYK

```bash
python3 scripts/convert_to_cmyk.py --input propositions/02-rock-brut/assets/pdf/setlist-rock-brut.pdf --output propositions/02-rock-brut/assets/pdf/setlist-rock-brut-cmyk.pdf
```

## Site racine

```bash
python3 scripts/generate_all.py --config rock-brut --site-only
```

## Pages d'aperçu

```bash
python3 scripts/generate_preview.py --skip-thumbs
python3 scripts/generate_preview.py           # avec miniatures PDF
```

## Chartes PDF

```bash
python3 scripts/generate_charte_pdf.py
```

## Divers

```bash
python3 scripts/migrer_instagram.py              # Migration handle IG
python3 scripts/convert_to_cmyk.py --all          # Tous les PDFs en CMYK
python3 scripts/finaliser.py --config rock-brut   # Finalisation (déjà fait)
```

## Git

```bash
git status                # État des modifications
git add -A                # Ajouter tout
git commit -m "message"   # Commiter
git push                  # Pousser (déclenche déploiement GitHub Pages)
git pull --rebase         # Synchroniser
```

## Vérifications

```bash
python3 -c "import reportlab, PIL, qrcode, cairosvg; print('OK')"
python3 -c "from palette import ACTIVE; print(ACTIVE.name)"
pdftoppm -v | head -1
gs --version
```
