#!/usr/bin/env python3
"""Build and compile LaTeX .tex files into PDFs and store them.

Usage:
  python3 tools/build_pdf.py <file.tex>
  python3 tools/build_pdf.py --all
"""

from __future__ import annotations
import argparse
import glob
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TECTONIC = ROOT / "tools" / "bin" / "tectonic"


def check_compiler() -> str:
    """Find tectonic or system xelatex/lualatex."""
    if TECTONIC.is_file() and os.access(TECTONIC, os.X_OK):
        return str(TECTONIC)
    if shutil.which("xelatex"):
        return "xelatex"
    if shutil.which("lualatex"):
        return "lualatex"
    sys.exit("Error: No LaTeX compiler found. Neither tools/bin/tectonic nor xelatex are available.")


def compile_tex(tex_path: Path, compiler: str) -> Path | None:
    """Compile a single .tex file to PDF."""
    tex_path = tex_path.resolve()
    if not tex_path.is_file():
        print(f"Error: {tex_path} does not exist.", file=sys.stderr)
        return None

    work_dir = tex_path.parent
    rel_path = tex_path.relative_to(ROOT)
    print(f"--> Compiling {rel_path}...")

    cmd = [compiler, tex_path.name]
    proc = subprocess.run(cmd, cwd=work_dir, capture_output=True, text=True)

    pdf_name = tex_path.stem + ".pdf"
    pdf_path = work_dir / pdf_name

    if proc.returncode != 0 or not pdf_path.is_file():
        print(f"FAILED: Could not compile {rel_path}", file=sys.stderr)
        # print error preview
        err_lines = [l for l in proc.stdout.splitlines() if l.startswith("!") or "error:" in l.lower()]
        if err_lines:
            for l in err_lines[:5]:
                print(f"   {l}", file=sys.stderr)
        return None

    # Check page count
    pages_info = ""
    try:
        import pypdf
        reader = pypdf.PdfReader(str(pdf_path))
        pages_info = f" ({len(reader.pages)} pages)"
    except Exception:
        pass

    size_kb = pdf_path.stat().st_size / 1024
    print(f"✓ Generated: {pdf_path.relative_to(ROOT)}{pages_info} [{size_kb:.1f} KB]")

    # Check if this matches an application folder and copy it there
    match_company = tex_path.stem.replace("main_", "").replace("cover_", "")
    app_dir = ROOT / "documents" / "applications" / match_company
    if app_dir.is_dir():
        dest = app_dir / pdf_name
        shutil.copy2(pdf_path, dest)
        print(f"  └─ Copied to application dossier: {dest.relative_to(ROOT)}")

    return pdf_path


def main():
    parser = argparse.ArgumentParser(description="Compile TeX documents into PDFs")
    parser.add_argument("file", nargs="?", help="Specific .tex file to compile")
    parser.add_argument("--all", action="store_true", help="Compile all CVs and cover letters")
    args = parser.parse_args()

    compiler = check_compiler()

    if args.all:
        cv_files = sorted(Path(ROOT / "cv").glob("*.tex"))
        cover_files = sorted(Path(ROOT / "cover_letters").glob("*.tex"))
        all_targets = [f for f in cv_files + cover_files if not f.name.endswith("_example.tex")]

        print(f"Compiling {len(all_targets)} documents using {compiler}...")
        success = 0
        for f in all_targets:
            if compile_tex(f, compiler):
                success += 1
        print(f"\nCompleted: {success}/{len(all_targets)} documents compiled successfully.")
    elif args.file:
        compile_tex(Path(args.file), compiler)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

