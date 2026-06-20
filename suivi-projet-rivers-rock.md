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

### 📋 À faire
- [ ] Création comptes réseaux (Instagram, Facebook, YouTube)
- [ ] Héberger le site sur GitHub Pages (`riversrock.github.io`)
- [ ] Remplacer `[DATE]` `[LIEU]` dans les templates pour un vrai concert
- [ ] Setlist interactive web
- [ ] Merchandising (t-shirts)

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
| `scripts/generate_animated_logo.html` | Animation logo dans navigateur |
| `scripts/logoutils.py` | Fonctions écusson partagées (ReportLab + Pillow) |

---

## Structure du projet

```
setlist/
├── charte-graphique-rivers-rock.md
├── suivi-projet-rivers-rock.md
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
│   └── logoutils.py
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

- **QR code dynamique** : URL courte redirigeant vers la dernière version de la setlist
- **Setlist interactive** : app web accessible depuis le QR, avec minuterie scène
- **Fiche technique son** (stage plot) — ✅ fait
- **Logo animé** pour Reels/Shorts — ✅ fait

---

## Notes techniques

- **Palette** : Bleu Seine `#1A3A5C`, Vert d'eau `#4A9B8E`, Accent `#E85D3A`, Vert repère `#2D8A6E`
- **Logo** : écusson (cercle + vague + RIVERS/ROCK intégré), Bebas Neue 11–14 pt
- **Typo corps** : Montserrat Regular / Italic
- **Taille uniforme** noms de groupe : 29–31 pt Bebas Neue (calée sur "SMASHING PUMPKINS")
- **Badges** : ∅24 pt blanc, numéro en couleur de carte (accent sur vert, vert repère sur rouge)
- **QR code** : généré avec lib `qrcode`, encode URLs à définir

---

## Réseaux sociaux — Disponibilité

| Plateforme | Nom recherché | Disponible | Suggestion |
|------------|--------------|------------|------------|
| Instagram | @riversrock | ✅ Libre | Page générique Instagram |
| Instagram | @riversrock.rouen | ✅ Libre | Page générique Instagram |
| Instagram | @riversrockoff | ✅ Libre | Page générique Instagram |
| Facebook | /riversrockrouen | ✅ Libre | 400 → pas de page |
| YouTube | @riversrock | ❌ Pris | Compte "Mark Powell" |
| YouTube | @riversrockband | ✅ Libre | 404 → disponible |
| YouTube | @riversrockrouen | ✅ Libre | 404 → disponible |
| Gmail | riversrock.rouen | ❓ Non vérifiable en ligne | API Google bloquée |
| Gmail | riversrockrouen | ❓ Non vérifiable en ligne | Alternative sans point |
| Gmail | riversrockband | ❓ Non vérifiable en ligne | Correspond à YouTube dispo |

**Recommandation :** `@riversrock.rouen` (Instagram), `Rivers Rock Rouen` (Facebook), `@riversrockband` (YouTube), `riversrock.rouen@gmail.com` (Gmail).

### Guide création comptes

1. **Gmail** → [accounts.google.com/signup](https://accounts.google.com/signup) → créer `riversrock.rouen@gmail.com`
2. **Instagram** → app Instagram → s'inscrire avec l'email Gmail → pseudo `@riversrock.rouen` → avatar = `pdf/templates/avatar.png`
3. **Facebook** → [facebook.com/pages/create](https://facebook.com/pages/create) → créer une page "Groupe de musique" → nom "Rivers Rock Rouen" → avatar + bannière + `pdf/templates/instagram-post.png` comme première publication
4. **YouTube** → avec le compte Gmail → [youtube.com](https://youtube.com) → créer une chaîne → handle `@riversrockband`

---

*Document mis à jour le 18 juin 2026*
