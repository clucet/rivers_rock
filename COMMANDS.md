# Rivers Rock — Aide-mémoire des commandes

_Version 1.0 — 28 juin 2026_

---

## 1. Génération des assets

### Générer le site + PDF d'une proposition
```bash
python3 scripts/generate_all.py --config rock-brut
```

### Site uniquement (plus rapide)
```bash
python3 scripts/generate_all.py --config neon-nights --site-only
```

### PDF uniquement
```bash
python3 scripts/generate_all.py --config scene-vintage --pdf-only
```

### Toutes les propositions disponibles
```bash
python3 scripts/generate_all.py --config <nom>
```
Configs : `originale`, `fluid-wave`, `rock-brut`, `scene-vintage`, `ponts-lumiere`, `neon-nights`, `sable-bronze`, `nordik`, `grunge`, `jazz-club`, `bitume`, `cordes-voix`, `heritage`, `rubicon`, `minuit`

---

## 2. Aperçus et chartes

### Pages d'aperçu (preview.html pour chaque proposition)
```bash
python3 scripts/generate_preview.py             # Complet (miniatures PDF)
python3 scripts/generate_preview.py --skip-thumbs  # Rapide (sans miniatures)
```

### Chartes graphiques PDF (5 pages par proposition)
```bash
python3 scripts/generate_charte_pdf.py
```

### Assets manquants (business cards, lyrics, stage plot, tech sheets)
```bash
python3 scripts/generate_missing.py
```

---

## 3. Rendu MP4

### Logo animé (proposition spécifique)
```bash
python3 scripts/render_animation.py --config scene-vintage
python3 scripts/render_animation.py --config neon-nights --render-scale 0.5
python3 scripts/render_animation.py --config rock-brut --render-scale 0.25
```

### Arguments
| Argument | Valeurs | Défaut |
|----------|---------|--------|
| `--config` | `scene-vintage`, `fluid-wave`, `rock-brut`, `originale`, `ponts-lumiere`, `neon-nights`, `sable-bronze` + 7 autres | `scene-vintage` |
| `--render-scale` | `0.25` (270×480), `0.5` (540×960), `1.0` (1080×1920) | `1.0` |
| `--output` | Chemin du fichier MP4 | `templates/logo-animated.mp4` |

### 14 animations disponibles
✅ `scene-vintage`, `fluid-wave`, `rock-brut`, `originale`, `ponts-lumiere`, `neon-nights`, `sable-bronze`, `nordik`, `grunge`, `jazz-club`, `bitume`, `cordes-voix`, `heritage`, `rubicon`, `minuit`

---

## 4. Conversion CMYK (impression professionnelle)

```bash
# Convertir tous les PDF du projet
python3 scripts/convert_to_cmyk.py --all

# Convertir un seul fichier
python3 scripts/convert_to_cmyk.py --input pdf/setlist.pdf --output pdf/setlist-cmyk.pdf
```

---

## 5. Migration Instagram (secours)

```bash
# Migrer du handle désactivé vers le secours
python3 scripts/migrer_instagram.py
# → remplace riversrockrouen → riversrock_rouen dans tous les fichiers

# Restauration (rollback)
python3 scripts/migrer_instagram.py --rollback
# → remplace riversrock_rouen → riversrockrouen
```

---

## 6. Finalisation (quand le groupe a choisi)

```bash
# Une fois la proposition gagnante connue :
python3 scripts/finaliser.py --config rock-brut
python3 scripts/finaliser.py --config neon-nights
# → Archive les 14 autres propositions
# → Met à jour palette.py ACTIVE
# → Regénère le site racine
# → Met à jour README et liens
# → Commit + push
```

---

## 7. Configuration palette (centralisée)

Fichier : `scripts/palette.py`

### Config active
```python
ACTIVE = NEON_NIGHTS   # ← Change ici ou via finaliser.py
```

### Ajouter une nouvelle proposition
1. Copier une Config existante dans `palette.py`
2. Ajouter dans `set_active()` (ligne ~492)
3. Ajouter dans `CONFIG_NAMES` (ligne ~506)
4. Créer le dossier `propositions/NN-nom/`
5. Copier le `generate.py` d'une autre proposition
6. Adapter les imports et couleurs

---

## 8. Git et déploiement

```bash
# Voir l'état des modifications
git status

# Ajouter tout
git add -A

# Commiter
git commit -m "Description du changement"

# Pousser (déclenche GitHub Actions + déploiement)
git push
```

---

## 9. Dépendances

### Installation initiale
```bash
# Packages Python
pip install reportlab Pillow qrcode cairosvg numpy

# Outils système
sudo apt-get install poppler-utils ghostscript

# Polices (téléchargement automatique dans ~/.fonts/)
# Lancer un generate.py pour déclencher le téléchargement
python3 -c "from logoutils import _resolve_font; _resolve_font('Bangers-Regular.ttf')"
```

### Vérification
```bash
python3 -c "import reportlab, PIL, qrcode, cairosvg; print('OK')"
pdftoppm --version
gs --version
fc-list | grep -i bangers  # Vérifier police installée
```

---

## 10. URLs de test

```bash
# Site principal
open https://clucet.github.io/rivers_rock/

# Propositions
open https://clucet.github.io/rivers_rock/propositions/

# Vote
open https://clucet.github.io/rivers_rock/propositions/vote/

# Setlist interactive
open https://clucet.github.io/rivers_rock/setlist/

# Planning répétitions
open https://clucet.github.io/rivers_rock/planning/

# EPK
open https://clucet.github.io/rivers_rock/epk/
```

---

## 11. Raccourcis courants

```bash
# Générer + push en une ligne
python3 scripts/generate_preview.py --skip-thumbs && git add -A && git commit -m "Update" && git push

# Vérifier que tout est OK
python3 scripts/generate_charte_pdf.py 2>&1 | grep -c "OK"
python3 scripts/generate_preview.py --skip-thumbs 2>&1 | tail -1

# Debug une police
python3 -c "from logoutils import _resolve_font; print(_resolve_font('Anton-Regular.ttf'))"
```

---

## 12. Résolution des problèmes courants

| Problème | Commande |
|----------|----------|
| **Preview "Logo animé non disponible"** | `python3 scripts/generate_preview.py --skip-thumbs` |
| **PDF backgrounds foncés** | Les setlists ont été corrigées (fonds blancs). Voir commit `9290238` |
| **Erreur "Police XXX introuvable"** | `python3 scripts/logoutils.py` → l'import déclenche le téléchargement auto |
| **Site pas à jour sur GitHub Pages** | Attendre 1-2 min après le push (le temps que GitHub Actions s'exécute) |
| **render_animation.py trop lent** | Ajouter `--render-scale 0.25` ou modifier `add_grain()` dans le script |

---

_Dernière mise à jour : 28 juin 2026_
