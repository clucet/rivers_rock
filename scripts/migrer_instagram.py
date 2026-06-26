#!/usr/bin/env python3
"""Script de secours : remplace le handle Instagram partout dans le projet.
Usage: python3 scripts/migrer_instagram.py  # remplace riversrock_rouen → riversrock_rouen
       python3 scripts/migrer_instagram.py --rollback  # restaure riversrock_rouen → riversrock_rouen"""

import os, sys, argparse

parser = argparse.ArgumentParser()
parser.add_argument("--rollback", action="store_true", help="Restaure l'ancien handle")
parser.add_argument("--new-handle", default="riversrock_rouen", help="Nouveau handle Instagram")
args = parser.parse_args()

if args.rollback:
    old = "riversrock_rouen"
    new = "riversrock_rouen"
    print("⬅️  Rollback : riversrock_rouen → riversrock_rouen")
else:
    old = "riversrock_rouen"
    new = args.new_handle
    print(f"➡️  Migration : {old} → {new}")

# Fichiers à modifier
extensions = (".py", ".md", ".html")
exclude_dirs = {"__pycache__", ".git"}

count = 0
for root, dirs, files in os.walk(os.path.dirname(os.path.dirname(__file__))):
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    for fname in files:
        if any(fname.endswith(e) for e in extensions):
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, "r") as f:
                    content = f.read()
                if old in content:
                    content = content.replace(old, new)
                    with open(fpath, "w") as f:
                        f.write(content)
                    count += 1
                    print(f"  ✅ {fpath}")
            except:
                pass

print(f"\n✅ {count} fichiers modifiés")
print("N'oubliez pas de regénérer les 9 propositions :")
print("  for p in 01* 02* 03* 04* 05* 06* 07* 08* 09*; do python3 propositions/$p/generate.py; done")
