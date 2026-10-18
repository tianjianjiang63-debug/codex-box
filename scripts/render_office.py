"""Render an Office file with an isolated LibreOffice profile and inspect its PDF."""
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile


def render(source: Path, output_dir: Path, png: bool = False) -> Path:
    from pypdf import PdfReader

    source = source.resolve(strict=True)
    if source.suffix.lower() not in {".docx", ".pptx", ".xlsx", ".odt", ".ods", ".odp"}:
        raise ValueError("Unsupported Office file extension.")
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    binary = shutil.which("libreoffice") or shutil.which("soffice")
    if not binary:
        raise RuntimeError("LibreOffice is required; run the cloud setup first.")
    pdf_path = output_dir / (source.stem + ".pdf")
    if pdf_path.exists():
        raise FileExistsError(f"Use a fresh output directory; existing PDF is preserved: {pdf_path}")
    with tempfile.TemporaryDirectory(prefix="codex-box-lo-") as temp:
        profile = Path(temp) / "profile"
        result = subprocess.run([binary, f"-env:UserInstallation={profile.as_uri()}", "--headless", "--convert-to", "pdf", "--outdir", str(output_dir), str(source)], capture_output=True, text=True, timeout=180)
        if result.returncode or not pdf_path.is_file() or pdf_path.stat().st_size == 0:
            raise RuntimeError(f"Office rendering failed: {result.stdout}\n{result.stderr}")
    pages = len(PdfReader(str(pdf_path)).pages)
    if pages < 1:
        raise RuntimeError("Rendered PDF has no pages.")
    if png:
        import fitz
        with fitz.open(pdf_path) as document:
            for index, page in enumerate(document, 1):
                page.get_pixmap(matrix=fitz.Matrix(1.3, 1.3)).save(output_dir / f"page-{index:03d}.png")
    print(f"Rendered {source.name}: {pages} pages -> {pdf_path}")
    return pdf_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--png", action="store_true")
    args = parser.parse_args()
    render(args.source, args.output_dir, args.png)
