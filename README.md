# Rivers Rock — Identité Visuelle

9 propositions identitaires complètes pour **Rivers Rock**, groupe de reprises rock basé à Rouen.

Chaque proposition inclut : site web responsive, setlist PDF, poster, flyer, stickers, t-shirt, templates réseaux (Instagram/Facebook/YouTube), logo animé HTML, charte graphique PDF, 5 variantes SVG, overlays vidéo, business card, stage plot, tech sheet, lyrics, et signature email.

## Propositions

| # | Nom | Ambiance |
|---|-----|----------|
| 01 | Fluid Wave | Organique, aquatique |
| 02 | Rock Brut | Industriel, percutant |
| 03 | Scène & Vintage | Rétro, scène, vinyle |
| 04 | Ponts & Lumière | Architectural, nocturne |
| 05 | Neon Nights | Cyberpunk, électrique |
| 06 | Sable & Bronze | Voyage, chaleur, nature |
| 07 | Nordik | Minimaliste, scandinave |
| 08 | Grunge | Punk, photocopie, chaos |
| 09 | Jazz Club | Cuivres, velours, jazz |

## Structure

```
propositions/NN-xxx/          ← Proposition isolée
  generate.py                 ← Générateur Python
  charte-graphique.md         ← Charte Markdown
  charte-graphique-NN-xxx.pdf ← Charte PDF
  assets/
    logo*.svg                 ← 5 variantes de logo
    index.html                ← Site de la proposition
    pdf/                      ← PDF générés
    templates/                ← Templates PNG/HTML
scripts/
  palette.py                  ← Config couleurs/fonts/tokens
  logoutils.py                ← Utilitaires partagés
  generate_all.py             ← Point d'entrée --config
  generate_preview.py         ← Pages d'aperçu
  convert_to_cmyk.py          ← Post-process CMYK
  render_animation.py         ← Rendu MP4
  setlist_data.py             ← Setlist centralisée
```

## Commandes

```bash
# Générer les assets d'une proposition
python3 scripts/generate_all.py --config scene-vintage

# Générer le site seulement
python3 scripts/generate_all.py --config nordik --site-only

# Générer les pages d'aperçu
python3 scripts/generate_preview.py

# Convertir les PDF en CMYK
python3 scripts/convert_to_cmyk.py --all

# Rendu MP4 du logo animé
python3 scripts/render_animation.py --config scene-vintage --render-scale 0.5
```

## Déploiement

GitHub Pages : [clucet.github.io/rivers_rock](https://clucet.github.io/rivers_rock/)

- Page comparaison : `propositions/index.html`
- Setlist interactive : `site/setlist/`
- EPK / Press Kit : `site/epk/`

## Réseaux

- **Gmail** : riversrockrouen@gmail.com
- **YouTube** : [@RiversRockRouen](https://www.youtube.com/@RiversRockRouen)
- **Facebook** : [Rivers Rock Rouen](https://www.facebook.com/RiversRockRouen)
- **Instagram** : @riversrockrouen (appel en cours) / @riversrock_rouen (secours)
