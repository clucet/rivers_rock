#!/usr/bin/env python3
"""Post-process RGB PDFs to CMYK using Ghostscript.
Usage: python3 scripts/convert_to_cmyk.py [--input <path>] [--output <path>]
       python3 scripts/convert_to_cmyk.py --all
       python3 scripts/convert_to_cmyk.py --input pdf/setlist.pdf --output pdf/setlist-cmyk.pdf
"""

import os, sys, subprocess, argparse, glob

SCRIPT_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.join(SCRIPT_DIR, "..")
GS = "/usr/bin/gs"

CMYK_ICCPROFILE = """\
ICCProfile (sRGB IEC61966-2.1)
[
  /CIEBasedABC <<
    /DecodeABC [ { 256 mul 16 add 256 div } bind ] bind
    /MatrixABC [ 0.4124564 0.3575761 0.1804375
                 0.2126729 0.7151522 0.0721750
                 0.0193339 0.1191920 0.9503041 ]
    /MatrixPQR [ 1 0 0 0 1 0 0 0 1 ]
    /RangePQR [ -0.128 0.128 -0.128 0.128 -0.128 0.128 ]
    /TransformPQR [
      { 16 add 116 div } bind
      { neg 16 add 116 div } bind
      { neg 16 add 116 div } bind
    ]
    /EncodePQR [ 1 1 1 ]
    /RangeABC [ 0 1 0 1 0 1 ]
  >> 
]
"""


def convert_pdf_to_cmyk(input_path, output_path):
    """Convert a single RGB PDF to CMYK using Ghostscript."""
    if not os.path.exists(GS):
        print(f"  ⚠ Ghostscript not found at {GS}. Install with: apt install ghostscript")
        return False

    if not os.path.exists(input_path):
        print(f"  ⚠ Input not found: {input_path}")
        return False

    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    cmd = [
        GS, "-dNOPAUSE", "-dBATCH", "-dSAFER", "-sDEVICE=pdfwrite",
        "-dProcessColorModel=/DeviceCMYK",
        "-sColorConversionStrategy=CMYK",
        "-dColorConversionStrategy=/CMYK",
        "-dOverrideICC",
        f"-sOutputFile={output_path}",
        input_path
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0 and os.path.exists(output_path):
            size = os.path.getsize(output_path) // 1024
            print(f"  ✅ CMYK: {os.path.basename(input_path)} → {os.path.basename(output_path)} ({size} Ko)")
            return True
        else:
            print(f"  ⚠ Ghostscript error for {input_path}: {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"  ⚠ Error: {e}")
        return False


def find_all_pdfs():
    """Find all RGB PDFs that need CMYK conversion."""
    patterns = [
        os.path.join(PROJECT_DIR, "pdf", "*.pdf"),
    ]
    # Proposition PDFs
    for prop_dir in sorted(os.listdir(os.path.join(PROJECT_DIR, "propositions"))):
        prop_pdf = os.path.join(PROJECT_DIR, "propositions", prop_dir, "assets", "pdf", "*.pdf")
        patterns.append(prop_pdf)
    pdfs = []
    for pat in patterns:
        pdfs.extend(glob.glob(pat))
    return sorted(set(pdfs))


def convert_all():
    """Convert all RGB PDFs to CMYK."""
    pdfs = find_all_pdfs()
    print(f"Found {len(pdfs)} PDFs to convert")
    for pdf in pdfs:
        output = pdf.replace(".pdf", "-cmyk.pdf")
        if os.path.exists(output):
            print(f"  ⏭ Skipping (exists): {os.path.basename(output)}")
            continue
        convert_pdf_to_cmyk(pdf, output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert RGB PDFs to CMYK via Ghostscript")
    parser.add_argument("--input", help="Input PDF path")
    parser.add_argument("--output", help="Output PDF path")
    parser.add_argument("--all", action="store_true", help="Convert all PDFs in the project")
    args = parser.parse_args()

    if args.all:
        convert_all()
    elif args.input:
        output = args.output or args.input.replace(".pdf", "-cmyk.pdf")
        convert_pdf_to_cmyk(args.input, output)
    else:
        print("Usage: python3 scripts/convert_to_cmyk.py --all")
        print("       python3 scripts/convert_to_cmyk.py --input pdf/setlist.pdf --output pdf/setlist-cmyk.pdf")
