# Rivers Rock — Aide-mémoire des commandes

_Version 1.1 — 27 juin 2026_

## Génération

| Commande | Action |
|----------|--------|
| `python3 scripts/generate_all.py --config rock-brut` | Site + PDF complets |
| `python3 scripts/generate_all.py --config rock-brut --site-only` | Site uniquement |
| `python3 scripts/generate_all.py --config rock-brut --pdf-only` | PDF uniquement |
| `python3 scripts/generate_preview.py` | Pages d'aperçu (complet) |
| `python3 scripts/generate_preview.py --skip-thumbs` | Pages d'aperçu (rapide) |
| `python3 scripts/generate_charte_pdf.py` | Chartes graphiques PDF |
| `python3 scripts/generate_missing.py` | Assets manquants (lyrics, stage…) |
| `python3 scripts/generate_setlist_web.py` | Setlist interactive PWA |

## Templates réseaux

```bash
python3 scripts/generate_avatar.py     # avatar.png + monogramme-rr.png
python3 scripts/generate_signature.py  # email-signature.png
python3 -c "from generate_social import generate_post, generate_story; generate_post(); generate_story()"
python3 -c "from generate_banners import gen_banners; gen_banners()"
python3 -c "from generate_tshirts import generate_mockup; generate_mockup()"
```

## Rendu MP4

```bash
python3 scripts/render_animation.py --config rock-brut --render-scale 0.5
python3 scripts/render_animation.py --config rock-brut --render-scale 1.0
```

## Conversion CMYK

```bash
python3 scripts/convert_to_cmyk.py --all
python3 scripts/convert_to_cmyk.py --input setlist/setlist.pdf --output setlist/setlist-cmyk.pdf
```

## Divers

```bash
python3 scripts/migrer_instagram.py              # Migration handle IG
python3 scripts/migrer_instagram.py --rollback   # Restauration
python3 scripts/finaliser.py --config rock-brut  # Finalisation (déjà fait)
```

## Git

```bash
git status                # État des modifications
git add -A                # Ajouter tout
git commit -m "message"   # Commiter
git push                  # Pousser (déclenche déploiement)
git pull --rebase         # Synchroniser
```

## Vérifications

```bash
python3 -c "import reportlab, PIL, qrcode, cairosvg; print('✅ Dépendances OK')"
python3 -c "from palette import ACTIVE; print(f'Config: {ACTIVE.name}')"
pdftoppm -v | head -1
gs --version
```
