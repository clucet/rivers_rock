# Plan de migration — OVH VPS Value

_Préparé avant réservation — Document de référence pour la migration_
_Dernière mise à jour : 30 juin 2026_

---

## 1. Offre retenue

| Élément | Valeur |
|---------|--------|
| **Offre** | OVH VPS Value |
| **Prix** | ~4,50 €/mois |
| **RAM** | 2 Go |
| **Stockage** | 20 Go NVMe |
| **CPU** | 1 vCore |
| **Docker** | ✅ Pris en charge |
| **OS** | Debian 12 |
| **Domaines** | `riversrock.fr` (à réserver) + `phaenna-formation.fr` (Gandi, DNS à pointer) |

---

## 2. Sites à héberger

### 2.1 Rivers Rock (riversrock.fr)

| Caractéristique | Valeur |
|-----------------|--------|
| **Type** | Site statique (HTML/CSS/JS) |
| **Taille** | ~10 Mo (hors archive) |
| **Base de données** | Non nécessaire |
| **PHP** | Non nécessaire |
| **Génération** | Python (local → push FTP/rsync) |

### 2.2 Moodle Phaenna (moodle.phaenna-formation.fr)

| Caractéristique | Valeur |
|-----------------|--------|
| **Type** | Application PHP + MariaDB (Docker) |
| **Port** | `localhost:8090` (conteneur) |
| **Domaine** | `phaenna-formation.fr` (Gandi) |
| **Sous-domaine** | `moodle.phaenna-formation.fr` |
| **Docker** | `docker-compose.yml` existant |

---

## 3. Structure finale du serveur

```
VPS OVH (Debian 12)
├── /var/www/
│   └── riversrock/         ← Site statique riversrock.fr
│       ├── index.html
│       ├── 404.html
│       ├── templates/
│       ├── setlist/
│       ├── epk/
│       ├── planning/
│       ├── propositions/
│       │   ├── 02-rock-brut/
│       │   └── vote/
│       └── md/
│
├── /home/dev/moodle-phaenna/ ← Moodle (Docker)
│   └── docker-compose.yml
│
├── /etc/nginx/sites-available/
│   ├── riversrock.fr       ← Sert les fichiers statiques
│   └── moodle.phaenna-formation.fr ← Reverse proxy → localhost:8090
│
└── /etc/letsencrypt/       ← SSL (Certbot)
```

---

## 4. Étapes de migration

### 4.1 Réservation et accès

| # | Action | Détail |
|---|--------|--------|
| 1 | Commander VPS Value | `ovh.com` → VPS Value → Debian 12 |
| 2 | Réserver `riversrock.fr` | Chez OVH (ou transfert) |
| 3 | DNS `phaenna-formation.fr` | Gandi → pointer vers IP du VPS (entrée A) |
| 4 | Noter IP du VPS | `ssh root@IP_VPS` |

### 4.2 Configuration du serveur

| # | Action | Commande |
|---|--------|----------|
| 5 | Connexion SSH | `ssh root@IP_VPS` |
| 6 | Mise à jour | `apt update && apt upgrade -y` |
| 7 | Installer Nginx | `apt install nginx -y` |
| 8 | Installer Certbot | `apt install certbot python3-certbot-nginx -y` |
| 9 | Installer Docker | `curl -fsSL https://get.docker.com | sh` |
| 10 | Vérifier Docker | `docker --version && docker compose version` |

### 4.3 Déploiement Rivers Rock

| # | Action | Commande |
|---|--------|----------|
| 11 | Créer dossier | `mkdir -p /var/www/riversrock` |
| 12 | Transférer fichiers | `rsync -avz --exclude=.git --exclude=archive /home/voidmaster/dev/rivers_rock/ root@IP_VPS:/var/www/riversrock/` |
| 13 | Config Nginx | Créer `/etc/nginx/sites-available/riversrock.fr` (voir section 5) |
| 14 | Activer site | `ln -s /etc/nginx/sites-available/riversrock.fr /etc/nginx/sites-enabled/` |
| 15 | SSL Let's Encrypt | `certbot --nginx -d riversrock.fr -d www.riversrock.fr` |
| 16 | Redémarrer Nginx | `systemctl restart nginx` |

### 4.4 Déploiement Moodle

| # | Action | Commande |
|---|--------|----------|
| 17 | Copier docker-compose | `rsync -avz /home/voidmaster/dev/moodle-phaenna/ root@IP_VPS:/home/dev/moodle-phaenna/` |
| 18 | Lancer Moodle | `cd /home/dev/moodle-phaenna && docker compose up -d` |
| 19 | Vérifier Moodle | `curl http://localhost:8090` |
| 20 | Config Nginx Moodle | Créer `/etc/nginx/sites-available/moodle.phaenna-formation.fr` (voir section 5) |
| 21 | Activer site | `ln -s /etc/nginx/sites-available/moodle.phaenna-formation.fr /etc/nginx/sites-enabled/` |
| 22 | SSL Let's Encrypt | `certbot --nginx -d moodle.phaenna-formation.fr` |
| 23 | Redémarrer Nginx | `systemctl restart nginx` |

### 4.5 Validation

| # | Action | URL |
|---|--------|-----|
| 24 | Tester Rivers Rock | `curl https://riversrock.fr` |
| 25 | Tester pages | `curl https://riversrock.fr/setlist/` |
| 26 | Tester Moodle | `curl https://moodle.phaenna-formation.fr` |
| 27 | Tester flux RSS | Vérifier les logs : `tail -f /var/log/nginx/access.log` |

---

## 5. Configuration Nginx

### 5.1 riversrock.fr

Créer `/etc/nginx/sites-available/riversrock.fr` :

```nginx
server {
    listen 80;
    server_name riversrock.fr www.riversrock.fr;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name riversrock.fr www.riversrock.fr;

    root /var/www/riversrock;
    index index.html;

    ssl_certificate /etc/letsencrypt/live/riversrock.fr/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/riversrock.fr/privkey.pem;

    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-Content-Type-Options "nosniff";

    location / {
        try_files $uri $uri/ =404;
    }

    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|webp)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

### 5.2 Moodle

Créer `/etc/nginx/sites-available/moodle.phaenna-formation.fr` :

```nginx
server {
    listen 80;
    server_name moodle.phaenna-formation.fr;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name moodle.phaenna-formation.fr;

    ssl_certificate /etc/letsencrypt/live/moodle.phaenna-formation.fr/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/moodle.phaenna-formation.fr/privkey.pem;

    location / {
        proxy_pass http://localhost:8090;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    client_max_body_size 100M;
}
```

---

## 6. Après migration — Mise à jour des fichiers

### URLs à changer

| Fichier | Ancienne URL | Nouvelle URL |
|---------|-------------|-------------|
| `index.html` (root site) | GitHub Pages | `riversrock.fr` |
| `md/liens-projet.md` | Toutes les URLs | Mise à jour |
| `templates/email-signature.html` | `clucet.github.io/...` | `riversrock.fr/...` |
| `setlist/manifest.json` | `start_url` | `/` |
| `setlist/sw.js` | URLs de cache | `riversrock.fr` |
| `propositions/02-rock-brut/assets/index.html` | Liens GitHub | Liens directs |

### Script de remplacement automatique

```bash
# Remplacer les URLs GitHub Pages par riversrock.fr
find . -type f \( -name "*.html" -o -name "*.md" -o -name "*.json" -o -name "*.js" \) \
  -not -path "./.git/*" -not -path "./archive/*" \
  -exec sed -i 's|clucet.github.io/rivers_rock|riversrock.fr|g' {} \;
```

---

## 7. Budget

| Poste | Coût mensuel |
|-------|-------------|
| VPS OVH Value | 4,50 € |
| Domaine riversrock.fr | ~0,70 € |
| Domaine phaenna-formation.fr | Déjà possédé (Gandi) |
| **Total** | **~5,20 €/mois** |

---

## 8. Alternatives si VPS indisponible

| Alternative | Prix | Docker | Notes |
|-------------|------|--------|-------|
| OVH VPS Starter | ~3,50 € | ✅ | 1 Go RAM, suffisant pour les deux |
| Hetzner VPS | ~3,50 € | ✅ | Rapport qualité/prix excellent |
| OVH Public Cloud | ~5 € | ✅ | À l'usage, plus flexible |

---

_Document à conserver pour la migration. Les étapes 1 à 4.1 sont à faire avant de pouvoir exécuter le reste._
