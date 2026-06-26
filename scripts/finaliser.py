#!/usr/bin/env python3
"""Finalize the chosen Rivers Rock proposition.

Usage:
    python3 scripts/finaliser.py --config rock-brut
    python3 scripts/finaliser.py --config neon-nights

Actions:
1. Switch palette.ACTIVE to the chosen config
2. Regenerate the root site
3. Archive non-chosen propositions
4. Update README.md and liens-projet.md
5. Commit and push
"""

import os, sys, shutil, subprocess, datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.join(SCRIPT_DIR, "..")

# ── Config mapping ──
CONFIG_DIRS = {
    "ombre-lumiere": "00-originale",
    "fluid-wave":    "01-fluid-wave",
    "rock-brut":     "02-rock-brut",
    "scene-vintage": "03-scene-vintage",
    "ponts-lumiere": "04-ponts-lumiere",
    "neon-nights":   "05-neon-nights",
    "sable-bronze":  "06-sable-bronze",
    "nordik":        "07-nordik",
    "grunge":        "08-grunge",
    "jazz-club":     "09-jazz-club",
    "bitume":        "10-bitume",
    "cordes-voix":   "11-cordes-voix",
    "heritage":      "12-heritage",
    "rubicon":       "13-rubicon",
    "minuit":        "14-minuit",
}

ARCHIVE = os.path.join(PROJECT, "archive")
PROPOSITIONS = os.path.join(PROJECT, "propositions")

def main():
    if len(sys.argv) < 2 or "--config" not in sys.argv:
        print("Usage: python3 scripts/finaliser.py --config <name>")
        print("Configs: " + ", ".join(sorted(CONFIG_DIRS.keys())))
        sys.exit(1)
    
    idx = sys.argv.index("--config")
    config_name = sys.argv[idx + 1]
    
    if config_name not in CONFIG_DIRS:
        print(f"Unknown config: {config_name}")
        print(f"Available: {', '.join(sorted(CONFIG_DIRS.keys()))}")
        sys.exit(1)
    
    chosen_dir = CONFIG_DIRS[config_name]
    chosen_path = os.path.join(PROPOSITIONS, chosen_dir)
    
    if not os.path.exists(chosen_path):
        print(f"Proposition directory not found: {chosen_path}")
        sys.exit(1)
    
    print(f"\n🎯 Finalisation: {config_name} ({chosen_dir})")
    
    # ── Step 1: Update palette.py ACTIVE ──
    palette_path = os.path.join(SCRIPT_DIR, "palette.py")
    with open(palette_path, "r") as f:
        palette = f.read()
    
    # Find ACTIVE line and replace it
    import re
    palette = re.sub(
        r'^ACTIVE = \w+',
        f'ACTIVE = {config_name.upper().replace("-", "_")}',
        palette,
        flags=re.MULTILINE
    )
    
    with open(palette_path, "w") as f:
        f.write(palette)
    print(f"  ✅ palette.py ACTIVE = {config_name}")
    
    # ── Step 2: Regenerate root site ──
    print("  🔄 Regenerating root site...")
    subprocess.run([sys.executable, os.path.join(SCRIPT_DIR, "generate_all.py"),
                    "--config", config_name, "--site-only"],
                   cwd=PROJECT, capture_output=True)
    print(f"  ✅ Root site regenerated")
    
    # ── Step 3: Archive non-chosen propositions ──
    os.makedirs(ARCHIVE, exist_ok=True)
    archived = 0
    for name, dirname in CONFIG_DIRS.items():
        if dirname == chosen_dir:
            continue
        src = os.path.join(PROPOSITIONS, dirname)
        dst = os.path.join(ARCHIVE, dirname)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.move(src, dst)
            archived += 1
            print(f"  📦 Archived: {dirname}")
    print(f"  ✅ {archived} propositions archived to {ARCHIVE}")
    
    # ── Step 4: Update README.md ──
    readme_path = os.path.join(PROJECT, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r") as f:
            readme = f.read()
        readme = readme.replace(
            "15 propositions identitaires complètes",
            f"Proposition retenue : {config_name}"
        )
        readme = readme.replace(
            "| 00 | Ombre & Lumière",
            f"| ✅ | **{config_name}** (retenue)",
        )
        with open(readme_path, "w") as f:
            f.write(readme)
        print(f"  ✅ README.md updated")
    
    # ── Step 5: Update liens-projet.md ──
    liens_path = os.path.join(PROJECT, "liens-projet.md")
    if os.path.exists(liens_path):
        with open(liens_path, "r") as f:
            liens = f.read()
        liens = liens.replace(
            "15 propositions",
            f"1 proposition retenue : {config_name}"
        )
        with open(liens_path, "w") as f:
            f.write(liens)
        print(f"  ✅ liens-projet.md updated")
    
    # ── Step 6: Commit ──
    today = datetime.date.today().strftime("%d/%m/%Y")
    msg = f"Finalisation: proposition {config_name} retenue ({today})"
    try:
        subprocess.run(["git", "add", "-A"], cwd=PROJECT, capture_output=True)
        subprocess.run(["git", "commit", "-m", msg], cwd=PROJECT, capture_output=True)
        subprocess.run(["git", "push"], cwd=PROJECT, capture_output=True)
        print(f"  ✅ Commit + push: {msg}")
    except Exception as e:
        print(f"  ⚠️ Git error: {e}")
    
    print(f"\n🎉 Proposition {config_name} finalisée et déployée !")


if __name__ == "__main__":
    main()
