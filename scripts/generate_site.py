#!/usr/bin/env python3
"""Generate site/index.html from the active config by copying from propositions/."""

import os, sys, shutil

sys.path.insert(0, os.path.dirname(__file__))
from palette import ACTIVE, CONFIG_NAMES, proposition_dir, set_active

SITE_DIR = os.path.join(os.path.dirname(__file__), "..", "site")


def get_source_path():
    """Get the path to the proposition's index.html based on active config."""
    for name, dirname in CONFIG_NAMES.items():
        if ACTIVE.name.lower() in name.lower().replace("-", " "):
            props_dir = os.path.join(os.path.dirname(__file__), "..", "propositions", dirname, "assets", "index.html")
            if os.path.exists(props_dir):
                return props_dir
    # Fallback: try matching by checking all propositions
    for dirname in CONFIG_NAMES.values():
        props_dir = os.path.join(os.path.dirname(__file__), "..", "propositions", dirname, "assets", "index.html")
        if os.path.exists(props_dir):
            return props_dir
    return None


def generate_site():
    os.makedirs(SITE_DIR, exist_ok=True)
    dst = os.path.join(SITE_DIR, "index.html")

    # Find the correct proposition site using CONFIG_NAMES mapping
    src = None
    for cfg_name, dirname in CONFIG_NAMES.items():
        candidate = os.path.join(os.path.dirname(__file__), "..", "propositions", dirname, "assets", "index.html")
        if os.path.exists(candidate):
            src = candidate
            # Check if this config matches the active one
            if cfg_name == ACTIVE.name.lower().replace("è", "e").replace(" ", "-").replace("&", "vintage"):
                break

    if src and os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"Site généré : {dst} ({ACTIVE.name})")
    else:
        print(f"⚠️  Aucun site trouvé pour {ACTIVE.name}, création d'un site minimal...")
        html = f"""<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rivers Rock — {ACTIVE.name}</title></head>
<body style="background:#1A3A5C;color:#fff;font-family:sans-serif;padding:60px;text-align:center">
<h1>Rivers Rock</h1><p>Config active : {ACTIVE.name}</p></body></html>"""
        with open(dst, "w") as f:
            f.write(html)
        print(f"Site minimal créé : {dst}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=None)
    args = parser.parse_args()
    if args.config:
        set_active(args.config)
    generate_site()
