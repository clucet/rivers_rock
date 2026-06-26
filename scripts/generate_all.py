#!/usr/bin/env python3
"""Generate all assets for the active config. Usage: python3 scripts/generate_all.py [--config <name>]"""

import os, sys, argparse, glob

sys.path.insert(0, os.path.dirname(__file__))
from palette import set_active, proposition_dir

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
    from generate_setlist import create_pdf
    from generate_poster import gen_poster
    from generate_flyer import gen_flyer
    from generate_social import generate_post, generate_story
    from generate_banners import gen_banners
    from generate_signature import gen_signature
    from generate_stickers import gen_stickers
    from generate_tshirts import generate_print, generate_mockup
    from generate_avatar import gen_avatar

    create_pdf()
    gen_poster()
    gen_flyer()
    generate_post()
    generate_story()
    gen_banners()
    gen_signature()
    gen_stickers()
    generate_print()
    generate_mockup()
    gen_avatar()

    print(f"\n✅ Tous les assets générés dans pdf/ pour : {cfg.name}")

    if args.cmyk:
        print("\nConversion CMYK...")
        from convert_to_cmyk import convert_pdf_to_cmyk
        pdf_dir = proposition_dir(args.config)
        pdf_glob = os.path.join(os.path.dirname(pdf_dir), "pdf", "*.pdf")
        for pdf_path in glob.glob(pdf_glob):
            cmyk_path = pdf_path.replace(".pdf", "-cmyk.pdf")
            if not os.path.exists(cmyk_path):
                convert_pdf_to_cmyk(pdf_path, cmyk_path)
