# Proposition n°3 — « Scène & Vintage » (Nostalgique & Lumineux) — ✅ Retenue

**Date :** 24 juin 2026
**Inspiration :** Affiches Milton Glaser / Push Pin Studio, pochettes vinyles 70-80, couchers de soleil sur la Seine, chaleur des projecteurs de scène
**Références musicales :** Queen, AC/DC, Rolling Stones, Radiohead (groupes repris par Rivers Rock)

## Palette augmentée

| Rôle | Actuel | Nouveau | Apport |
|------|--------|---------|--------|
| Primaire | `#1A3A5C` | Conservé | Profondeur, identité, nuit |
| Secondaire | `#4A9B8E` | Conservé + `#1A5C5C` (Teal profond) | Double vert, plus de richesse |
| Accent 1 | `#E85D3A` | Conservé | Feu de la scène, énergie |
| **Accent 2** | — | **`#C96D4D` Terracotta** | Chaleur, vintage, rouille, vieux cuivre |
| **Accent 3** | — | **`#C9A84C` Or vieilli** | Soleil, lumière, premium, coucher de soleil |
| Neutre | `#8C9196` | Conservé | Sobriété |
| Fond clair | `#F5F5F0` | Conservé | Supports imprimés |

> **Référence programmatique :** `palette.SCENE_VINTAGE`

### Déclinaisons

- **Fond sombre :** Titres blanc, accent `#E85D3A` / `#C9A84C`, secondaire `#4A9B8E`
- **Fond clair :** Titres `#1A3A5C`, accent `#C96D4D`
- **Noir & blanc :** Gris acier `#8C9196`, remplacer les couleurs par des niveaux de gris

## Typographie étendue

| Usage | Police | Poids | Taille repère |
|-------|--------|-------|---------------|
| Logo / Écusson | Bebas Neue | Regular | Idem charte actuelle |
| **Titres héro** | **Anton** | Regular | 80–140 pt (affiche, story, site) |
| Sous-titres fonctionnels | Bebas Neue | Regular | 28 pt |
| Noms de groupe (setlist) | Bebas Neue | Regular | 29–31 pt |
| Titres chansons | Montserrat | Regular | 14 pt |
| Corps de texte | Montserrat | Light, Regular | 11–16 pt |
| **Citations / Lyrics / Dates** | **Space Mono** | Regular | 10–18 pt |
| **Décoratif (biographie)** | Abril Fatface *ou* Bebas Neue | — | À définir |

### Substitutions

- **Titres →** Anton → Oswald ou Impact
- **Corps →** Inter ou Open Sans
- **Monospace →** JetBrains Mono ou Fira Code

## Logo / Marque

### Variante standard
- Écusson actuel inchangé (cercle + vague + RIVERS/ROCK)
- Règles d'usage identiques à la charte originale

### Variante néon digital (Nouveau)
- Cercle + vague avec **box-shadow glow** `#E85D3A`
- Vibration lumineuse au hover (CSS `filter: drop-shadow`)
- Usage : site web, vidéos, stories Instagram, logo animé

### Variante timbre disque (Nouveau)
- Un **anneau concentrique supplémentaire** autour du cercle (comme les sillons d'un vinyle)
- Le texte "RIVERS ROCK" peut optionnellement suivre l'arc du cercle extérieur
- Usage : merchandising, stickers, pochettes, mockup t-shirt

### Monogramme "RR" (Nouveau)
- Deux lettres R entrelacées
- Une vague sinusoïdale traverse les deux lettres
- Usage : favicon (16–32 px), watermark vidéo, petits formats (< 30 pt)
- Version simplifiée pour l'impression (1 couleur)

## Éléments graphiques

### Vagues
- Vagues sinusoïdales conservées
- **Superposition** de 3 à 5 vagues d'amplitudes et phases différentes en dégradé (opacité cumulée 5–20 %)
- Couleur : `#C9A84C` (or) en variante pour les séparateurs
- Largeur de trait : 1–3 pt selon le support

### Textures
- **Grain overlay** : bruit granuleux à 3–8 % d'opacité sur tous les fonds de setlist, affiches, templates
- **Halftone dots** : motifs de points en filigrane sur les bords (rappel des affiches psychédéliques 70s)
- Génération procédurale (Python) ou texture PNG superposée

### Flares lumineux
- Dégradés radiaux rappelant un **projecteur de scène**
- Centre du flare : `#C9A84C` (or) → bord : `transparent`
- Usage : templates Instagram, bannière YouTube, hero du site

### Badge circulaire
- ∅24 pt, fond blanc, numéro 12 pt **en `#C9A84C` (or)** sur cartes terracotta
- ∅24 pt, fond blanc, numéro 12 pt **en `#E85D3A`** sur cartes teal
- Option : espacement renforcé entre badge et texte

### Formes géométriques
- Cercles concentriques conservés (rappel du 106)
- Ajout de **cercles pointillés** (rappel des sillons vinyles)
- Angles droits : conservés pour l'univers rock

## Applications

### Setlist PDF (A4 portrait)
- Fond : dégradé `#1A3A5C` → `#1A5C5C` (teal profond au lieu de vert d'eau), grain overlay 5 %
- Logotype en haut : écusson + "RIVERS ROCK" Bebas Neue 56 pt (inchangé)
- "SETLIST" : Bebas Neue 28 pt, accent `#E85D3A` (inchangé)
- Vague séparatrice : **or `#C9A84C`** au lieu de blanc, opacité 50 %
- **Cartes terracotta** (`#C96D4D` avec dégradé) : titres en ton normal
- **Cartes teal** (`#1A5C5C` avec dégradé) : titres joués un ton en dessous (remplace le `#2D8A6E`)
- **Bordure** : double trait (blanc 0.5 pt + or `#C9A84C` 1 pt)
- **Ombre portée** : noir 20 %, décalée 4 pt + **petit reflet chaud** (blanc 5 %, décalé -2 pt)
- Badges circulaires : fond blanc, numéro en `#C9A84C` (or) ou `#E85D3A`
- Footer : "R O U E N" Montserrat 7 pt, tracking 3 pt, grain overlay

### Instagram — Post carré (1080 × 1080 px)
- Fond : **dégradé radial** chaud `#C96D4D` → `#C9A84C` (centre), bord `#1A3A5C`
- Logo écusson en haut, **avec glow néon** `#E85D3A`
- "PROCHAIN CONCERT" : Space Mono 22 pt, blanc
- [DATE] : Anton 64 pt, `#C9A84C`
- [LIEU] : Montserrat 24 pt, blanc 80 %
- Zone QR code : carré blanc 120 px, bordure `#C96D4D` 3 px
- "@riversrock.rouen" : Space Mono 14 pt, bas

### Instagram — Story (1080 × 1920 px)
- Fond : photo duo-tone (teal + orange) avec flare projecteur au centre
- Logo timbre disque en haut à gauche
- [DATE] : Anton 120 pt, `#E85D3A`, centré
- [LIEU] : Space Mono 28 pt, blanc
- Grain overlay 5 %

### Affiche A4 (poster)
- Fond : dégradé `#1A3A5C` → `#1A5C5C`, grain overlay 5 %
- Logo horizontal + "PROCHAIN CONCERT" : Space Mono 14 pt, `#C9A84C`
- [DATE] : Anton 56 pt, blanc
- [LIEU] : Montserrat 18 pt, blanc 70 %
- Vague séparatrice en `#C9A84C`
- Halftone dots discrets sur les bords

### Flyer A6 — 4 par planche A4, duplex
- **Recto** : logo + [DATE] Anton 38 pt `#C9A84C` + [LIEU] Space Mono 16 pt
- **Verso** : bio + membres + QR code (nouveau) + @riversrock.rouen
- Fond dégradé avec grain overlay
- Vagues or en filigrane

### Carte de visite (85 × 55 mm)
- Fond : dégradé `#1A3A5C` → `#4A9B8E` (inchangé)
- Symbole réduit (∅11 mm) + "RIVERS ROCK" Bebas Neue 14 pt
- Mention "Reprises rock — Rouen" en Space Mono 8 pt
- Nom, téléphone, email en Montserrat 9–11 pt
- `riversrock.fr` en accent `#C9A84C`

### Bannière Facebook (1640 × 624 px)
- Fond : dégradé `#1A3A5C` → `#1A5C5C`, grain overlay
- Logo écusson + "RIVERS ROCK" Anton 48 pt
- Photo groupe en duo-tone teal/orange
- Vague or filigrane

### Bannière YouTube (2560 × 1440 px)
- Même layout que Facebook, logo Anton 72 pt
- Flare projecteur au centre
- Zone de sécurité respectée

### Signature email (600 × 200 px)
- Fond dégradé (inchangé)
- Symbole ∅18 px + "RIVERS ROCK" Bebas Neue 18 pt
- Noms/Space Mono pour email, téléphone
- Lien `riversrock.fr/setlist` en `#C9A84C`

### Stickers (∅80 mm, planche A4 de 6)
- Fond dégradé dans chaque cercle : `#C96D4D` → `#C9A84C` (variante chaude)
- Symbole seul centré + anneau concentrique (timbre disque)
- Repères de coupe

### T-shirt — Écusson poitrine
- Écusson standard inchangé (blanc + `#E85D3A`)
- **Variante timbre** : ajout d'un anneau extérieur pointillé
- Couleurs : blanc + `#C9A84C` (or) possible pour série limitée

### Site one-page — Structure proposée

```
HEADER
├── Logo écusson + "RIVERS ROCK" en Anton
├── Navigation sticky (Le groupe · Concerts · Contact)
└── Hero : photo groupe (duo-tone teal/orange) + tagline "Reprises rock — Rouen"

SECTIONS
├── Bio — photos en damier, texte large Montserrat, citation du groupe en Space Mono
├── Membres — photos individuelles cercles, rôles, citation Space Mono
├── Concerts — calendrier avec dates + réservation, icônes de lieu
├── Musique — embed YouTube playlist / clips
└── Contact — formulaire + liens réseaux + petite carte

FOOTER
├── Logo timbre variante
└── "R O U E N" tracking + grain texture
```

## Fichiers à modifier

| Fichier | Modifications |
|---------|---------------|
| `charte-graphique-rivers-rock.md` | Palette, typo, logo (variantes néon, timbre, monogramme), textures |
| `logoutils.py` | Nouvelles couleurs, nouveau badge `#C9A84C` |
| `generate_setlist.py` | Fond teal, cartes terracotta/teal, double bordure, ombre + reflet, vague or |
| `generate_social.py` | Dégradé radial chaud, glow logo, Space Mono, flare projecteur |
| `generate_poster.py` | Anton, Space Mono, halftone dots |
| `generate_flyer.py` | QR code verso, Anton, Space Mono |
| `generate_banners.py` | Duo-tone photo, grain overlay, flare |
| `generate_signature.py` | Space Mono, `#C9A84C` pour lien |
| `generate_stickers.py` | Variante timbre disque |
| `generate_tshirts.py` | Variante timbre (anneau pointillé) |
| `generate_animated_logo.html` | Glow néon `#E85D3A` |
| `generate_avatar.py` | Monogramme "RR" en 500×500 |
| `site/index.html` | Restructuration complète (voir ci-dessus) |
