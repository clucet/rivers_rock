# Rivers Rock — Administration

_Version 1.1 — Rock Brut (proposition élue)_

## Stack

| Technologie | Usage |
|-------------|-------|
| Python 3.12 | Génération des assets (ReportLab, Pillow, cairosvg) |
| HTML/CSS | Sites web statiques (GitHub Pages) |
| GitHub Actions | CI/CD : déploiement automatique à chaque push |
| GitHub Pages | Hébergement : `clucet.github.io/rivers_rock` |

## Structure

```
rivers_rock/
├── index.html              ← Site racine (Rock Brut)
├── templates/              ← PNG/HTML/GIF/MP4 réseaux
├── setlist/                ← Setlist interactive (PWA)
├── epk/                    ← Press Kit
├── planning/               ← Planning répétitions
├── md/                     ← Documentation
├── propositions/
│   └── 02-rock-brut/       ← Proposition élue
├── archive/                ← 14 propositions non retenues
└── scripts/                ← 29 générateurs Python
```

## Proposition élue : Rock Brut

| Élément | Valeur |
|---------|--------|
| Palette | Noir `#0A0A0A`, Orange `#FF3B00`, Blanc `#FFFFFF` |
| Logo | Hexagone extérieur orange + intérieur blanc + RR |
| Police | Anton (titres), Inter Tight (corps), JetBrains Mono (data) |
| Règles | Pas d'arrondis, pas de dégradés, pas d'ombres, grain 10% |

## Commandes essentielles

```bash
python3 scripts/generate_all.py --config rock-brut          # Tout regénérer
python3 scripts/generate_all.py --config rock-brut --site-only  # Site uniquement
python3 scripts/generate_preview.py --skip-thumbs           # Pages d'aperçu
python3 scripts/convert_to_cmyk.py --all                    # CMYK pour impression
python3 scripts/render_animation.py --config rock-brut      # MP4 logo animé
```

Voir `md/commandes.md` pour la liste complète.

## Déploiement

Automatique via `.github/workflows/generate.yml` à chaque `git push`.
Manuel : `git add -A && git commit -m "message" && git push`

## URLs

| Page | URL |
|------|-----|
| Site | `clucet.github.io/rivers_rock` |
| Propositions | `clucet.github.io/rivers_rock/propositions/` |
| Setlist | `clucet.github.io/rivers_rock/setlist/` |
| EPK | `clucet.github.io/rivers_rock/epk/` |
| Planning | `clucet.github.io/rivers_rock/planning/` |
| Dépôt | `github.com/clucet/rivers_rock` |

## Réseaux

| Plateforme | Identifiant | Statut |
|------------|-------------|--------|
| Gmail | riversrock_rouen@gmail.com / `!LeGroupe76140@` | ✅ |
| YouTube | @RiversRockRouen | ✅ |
| Facebook | Rivers Rock Rouen | ✅ |
| Instagram | @riversrockrouen | 🔴 Désactivé (appel en cours) |

## Dépannage rapide

| Problème | Solution |
|----------|----------|
| Police manquante | `python3 -c "from logoutils import _resolve_font; _resolve_font('Anton-Regular.ttf')"` |
| Templates pas à jour | `python3 scripts/generate_avatar.py && python3 scripts/generate_signature.py` |
| Site pas à jour | `python3 scripts/generate_all.py --config rock-brut --site-only` |
| Push reject | `git pull --rebase && git push` |
