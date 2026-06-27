#!/usr/bin/env python3
"""Generate all assets for the active config. Usage: python3 scripts/generate_all.py [--config <name>]"""

import os, sys, argparse, glob

sys.path.insert(0, os.path.dirname(__file__))
from palette import set_active, proposition_dir, CONFIG_NAMES

parser = argparse.ArgumentParser(description="Generate Rivers Rock assets for a given config")
parser.add_argument("--config", default="scene-vintage",
                     choices=["originale", "fluid-wave", "rock-brut", "scene-vintage", "ponts-lumiere",
                              "neon-nights", "sable-bronze", "nordik", "grunge", "jazz-club",
                              "bitume", "cordes-voix", "heritage", "rubicon", "minuit"],
                    help="Design config to generate (default: scene-vintage)")
parser.add_argument("--site-only", action="store_true", help="Only generate the site")
parser.add_argument("--pdf-only", action="store_true", help="Only generate PDFs/PNGs")
parser.add_argument("--cmyk", action="store_true", help="Post-process PDFs to CMYK via Ghostscript")
args = parser.parse_args()

cfg = set_active(args.config)
print(f"🎨 Config active : {cfg.name}")

if not args.pdf_only:
    from generate_site import generate_site
    generate_site()

if not args.site_only:
    print("  Generation des assets via le generateur de la proposition...")
    prop_gen = os.path.join(os.path.dirname(__file__), "..", "propositions",
                            CONFIG_NAMES.get(args.config, "02-rock-brut"), "generate.py")
    if os.path.exists(prop_gen):
        import importlib.util as _util
        _spec = _util.spec_from_file_location("prop_gen", prop_gen)
        _mod = _util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        _mod.gen_setlist()
        _mod.gen_poster()
        _mod.gen_flyer()
        _mod.gen_social()
        _mod.gen_banners()
        _mod.gen_avatar()
        _mod.gen_stickers()
        _mod.gen_tshirt()
        _mod.gen_animated()
        _mod.gen_site()
        print(f"\n✅ Tous les assets générés pour : {cfg.name}")
    else:
        print(f"⚠️  Proposition non trouvee : {prop_gen}")

    if args.cmyk:
        print("\nConversion CMYK...")
        from convert_to_cmyk import convert_pdf_to_cmyk
        pdf_dir = proposition_dir(args.config)
        pdf_glob = os.path.join(pdf_dir, "pdf", "*.pdf")
        for pdf_path in glob.glob(pdf_glob):
            cmyk_path = pdf_path.replace(".pdf", "-cmyk.pdf")
            if not os.path.exists(cmyk_path):
                convert_pdf_to_cmyk(pdf_path, cmyk_path)
