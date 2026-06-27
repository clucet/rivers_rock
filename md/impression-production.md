# Rivers Rock — Impression & Production

_Analyse des options d'impression et de production des supports physiques._

## Imprimante disponible : Brother DCP-L3560CDW

| Spécification | Valeur |
|--------------|--------|
| Type | Laser couleur |
| Résolution max | 2400 × 600 dpi |
| Format max | A4 |
| Grammage max | 163 g/m² |
| Recto-verso | ✅ Oui |
| Toner | TN-247 (Cyan, Magenta, Jaune, Noir) |
| Bord perdu (bleed) | ❌ Non |

## Supports réalisables sur Brother

| Produit | Possible ? | Recommandation papier | Toner |
|---------|-----------|----------------------|-------|
| Setlists (A4) | ✅ | 80 g/m² (standard) | ~5% |
| Flyers (A6, 4 par page A4) | ✅ | 120-160 g/m² | ~10% |
| Stickers (découpe) | ✅ (papier adhésif A4 ~15€) | Papier adhésif laser | ~8% |
| T-shirt tech sheet (A4) | ✅ | 80 g/m² | ~3% |
| Stage plot (A4 paysage) | ✅ | 80 g/m² | ~3% |
| Poster (A3) | ❌ Format trop grand | — | — |
| Cartes de visite | ❌ Grammage insuffisant | — | — |
| T-shirts / Mugs / Goodies | ❌ | Non textile | — |

## Production via famille (flocage textile, goodies)

| Produit | Procédé | Recommandation |
|---------|---------|---------------|
| **T-shirts** | Flocage vinyl ou sérigraphie | Logo de la proposition retenue, centré poitrine |
| **Mugs** | Transfert ou sérigraphie | Logo + nom du groupe |
| **Goodies** | Selon matériel disponible | Stickers, pins, tote bags |

**Fichiers à fournir :** le fichier `logo.svg` de la proposition retenue (dans `propositions/NN-xxx/assets/logo.svg`)
→ Vectoriel, prêt pour flocage et sérigraphie.

## Prestataires recommandés

| Produit | Prestataire | Budget estimé | Délai |
|---------|------------|--------------|-------|
| **Posters A3 / A2** | Reprographie locale (Rouen) | 5-10€ / unité | 2-3 jours |
| **Cartes de visite (×100)** | Helloprint | 15-25€ | 3 jours |
| **Flyers A6 (×500)** | Vistaprint | ~40€ | 5 jours |
| **T-shirts sérigraphie** | La Fabrique à T-shirt ou équivalent local | 15-20€ / pièce | 7 jours |
| **Stickers pro (découpe)** | Stickermule | 30€ / 50 | 5 jours |
| **Mugs** | Helloprint ou famille | 10-15€ / pièce | 5 jours |

## Réglages d'impression recommandés (Brother)

| Réglage | Valeur | Pourquoi |
|---------|--------|----------|
| Mode couleur | ✅ Couleur | Identification des propositions |
| Qualité | Haute (2400 dpi) | Meilleur rendu des logos |
| Papier | Selon grammage (80-160 g/m²) | Adapter au support |
| Économie toner | Désactivé pour les finalistes | Qualité > économie |
| Recto-verso | Oui pour setlists (2 ex.) | Gain de papier |

## Workflow complet

```
1. Choisir la proposition gagnante
2. python3 scripts/finaliser.py --config <nom>
3. (Optionnel) python3 scripts/convert_to_cmyk.py --all
4. Ouvrir les PDF depuis propositions/<gagnant>/assets/pdf/
5. Imprimer sur Brother :
   - Setlist → A4 80g, recto
   - Flyer → A4 120g, 4-up
   - Stickers → A4 adhésif
6. Commander à l'externe :
   - Poster A3 → reprographie
   - Cartes de visite → Helloprint
   - T-shirts → famille ou prestataire
```

## Budget estimé (kit de démarrage)

| Poste | Coût |
|-------|------|
| Papier 80g (500 feuilles) | ~8€ |
| Papier 120-160g (100 feuilles) | ~6€ |
| Papier adhésif A4 (10 feuilles) | ~15€ |
| Posters A3 (×5) | ~25-50€ |
| Cartes de visite (×100) | ~15-25€ |
| T-shirts (×5-10) | ~75-200€ |
| **Total estimation** | **~150-300€** |
