# Plan de vote — Rivers Rock

_Objectif : faire choisir une identité visuelle parmi les 15 propositions par les 5 membres du groupe._

---

## 1. Les propositions

Les 15 propositions sont visibles ici :
👉 **https://clucet.github.io/rivers_rock/propositions/**

| # | Proposition | Concept | Ambiance |
|---|-------------|---------|----------|
| 00 | Ombre & Lumière | Clair-obscur, argentique | Noir & blanc, photo, l'essentiel |
| 01 | Fluid Wave | Vague, eau, organique | Vert profond, ambre, fluide |
| 02 | Rock Brut | Industriel, percutant | Noir, orange, hexagone |
| 03 | Scène & Vintage | Rétro, vinyle, projecteurs | Teal, terracotta, or, timbre |
| 04 | Ponts & Lumière | Architectural, nocturne | Nuit, acier, lumière, ponts |
| 05 | Neon Nights | Cyberpunk, électrique | Violet, rose, cyan, éclairs |
| 06 | Sable & Bronze | Voyage, nature, chaleur | Sable, terre cuite, soleil |
| 07 | Nordik | Minimaliste, scandinave | Blanc, gris, trait horizontal |
| 08 | Grunge | Punk, anti-design | Papier, toner, marqueur rose |
| 09 | Jazz Club | Cuivres, velours, jazz | Noir, or, rouge, projecteur |
| 10 | Bitume | Street art, urbain | Gris, jaune fluo, brique, stencil |
| 11 | Cordes & Voix | Acoustique, intimiste | Crème, acajou, ambre, cordes |
| 12 | Héritage | Patrimoine normand | Vitrail, or, colombage, rosace |
| 13 | Rubicon | Americana, road trip | Orange, bleu ciel, vert pin, route |
| 14 | Minuit | French touch, élégance | Noir velours, bordeaux, lune |

---

## 2. Page de vote

Une page de vote interactive est disponible :
👉 **https://clucet.github.io/rivers_rock/propositions/vote/**

**Fonctionnement :**
1. Parcourir les 15 propositions
2. Cliquer sur 3 propositions favorites (⭐ apparaît)
3. Remplir son nom (optionnel)
4. Cliquer sur "Envoyer mon vote"
5. L'email s'ouvre automatiquement avec le vote pré-rempli
6. Envoyer

---

## 3. Procédure pour les 5 membres

| Étape | Action | Responsable | Date butoir |
|-------|--------|-------------|-------------|
| **1** | Envoyer l'URL de vote aux 5 membres par email/SMS | Toi | J1 |
| **2** | Chaque membre vote individuellement (sans se concerter) | Membres | J1 → J3 |
| **3** | Relance des non-votants à J+2 | Toi | J3 |
| **4** | Clôture des votes | Toi | J5 |
| **5** | Dépouillement et annonce des résultats | Toi | J5 |

---

## 4. Message type à envoyer au groupe

```
Objet : 🎸 Rivers Rock — Choisissez notre identité visuelle !

Salut à tous,

J'ai préparé 15 propositions d'identité visuelle pour le groupe.
Chacune a son propre site, ses logos, ses couleurs, sa charte graphique
et même des templates Instagram/Facebook/YouTube.

Pour nous aider à choisir, voici la page de vote :
👉 https://clucet.github.io/rivers_rock/propositions/vote/

Le principe est simple :
1. Parcourez les 15 propositions (cliquez dessus pour voir le détail)
2. Sélectionnez vos 3 préférées
3. Envoyez votre vote par email (le lien s'ouvre tout seul)

⚠️ Ne vous concertez pas — chacun vote individuellement.
Il n'y a pas de "bonne" réponse, juste vos préférences personnelles.

Si vous voulez explorer les propositions plus en détail avant de voter :
👉 https://clucet.github.io/rivers_rock/propositions/

Merci ! 🤘
```

---

## 5. Dépouillement

| Résultat | Action |
|----------|--------|
| **Unanimité** (même prop #1 pour tous) | ✅ Proposition retenue, on finalise |
| **Top 2-3** (2-3 props se détachent) | 🔄 Second tour avec les finalistes |
| **Éparpillement** (aucune tendance) | 📅 Réunion pour départager |

**Système de points :**
- 1er choix = 3 points
- 2e choix = 2 points
- 3e choix = 1 point

La proposition avec le plus de points gagne.

---

## 6. Après le choix

| Priorité | Action |
|----------|--------|
| 🔴 | Définir la proposition retenue comme ACTIVE dans `palette.py` |
| 🔴 | Régénérer le site racine avec `generate_all.py --config NOM --site-only` |
| 🟠 | Nettoyer les propositions non retenues (archivage) |
| 🟠 | Lancer le rendu MP4 final haute qualité |
| 🟡 | Optimiser les assets pour la prop retenue (couleurs, typos définitives) |
| 🟡 | Lancer les réseaux sociaux (Instagram, Facebook, YouTube) |
| 🟢 | Publier les drafts Facebook |
| 🟢 | Créer la playlist Spotify/YouTube |
