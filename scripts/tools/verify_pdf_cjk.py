#!/usr/bin/env python3
"""Verify PDF text layers contain readable Chinese (not tofu / replacement chars)."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

try:
    import fitz  # PyMuPDF
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: pymupdf. Run `python -m pip install -r requirements-pdf.txt` first."
    ) from exc

CJK_RE = re.compile(r"[\u4e00-\u9fff]")
REPLACEMENT_RE = re.compile(r"[\ufffd\u25a1\u25a0]")
# Common microwave-course terms that should appear in any volume TOC or body
EXPECTED_SNIPPETS = ("微波", "学习", "讲义", "实验", "解答", "指南", "技术", "基础", "目录")

DEFAULT_GLOBS = (
    "microwave-guide-*.pdf",
    "microwave-knowledge-*.pdf",
    "microwave-solutions-*.pdf",
    "microwave-experiments-*.pdf",
    "microwave-complete-*.pdf",
)


def extract_sample_text(pdf_path: Path, *, max_pages: int = 5) -> str:
    doc = fitz.open(pdf_path)
    try:
        chunks: list[str] = []
        for index in range(min(max_pages, doc.page_count)):
            chunks.append(doc[index].get_text())
        return "\n".join(chunks)
    finally:
        doc.close()


def verify_pdf(pdf_path: Path, *, min_cjk: int = 20, max_pages: int = 5) -> list[str]:
    errors: list[str] = []
    text = extract_sample_text(pdf_path, max_pages=max_pages)
    if not text.strip():
        errors.append("text layer empty on sampled pages")
        return errors

    cjk_chars = CJK_RE.findall(text)
    if len(cjk_chars) < min_cjk:
        errors.append(f"too few CJK chars ({len(cjk_chars)} < {min_cjk})")

    replacements = REPLACEMENT_RE.findall(text)
    if replacements:
        errors.append(f"found {len(replacements)} replacement/box glyphs")

    if not any(word in text for word in EXPECTED_SNIPPETS):
        errors.append("no expected course vocabulary in sample text")

    return errors


def collect_pdfs(pdf_dir: Path, include_complete: bool) -> list[Path]:
    paths: list[Path] = []
    for pattern in DEFAULT_GLOBS:
        if not include_complete and pattern.startswith("microwave-complete"):
            continue
        paths.extend(sorted(pdf_dir.glob(pattern)))
    # Prefer non-sample builds
    paths = [p for p in paths if "-sample" not in p.name]
    return paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify Chinese text in exported PDF volumes.")
    parser.add_argument(
        "--dir",
        type=Path,
        default=ROOT / "dist" / "pdf",
        help="Directory containing PDF files (default: dist/pdf).",
    )
    parser.add_argument(
        "--include-complete",
        action="store_true",
        help="Also verify microwave-complete-*.pdf if present.",
    )
    parser.add_argument(
        "--min-cjk",
        type=int,
        default=20,
        help="Minimum CJK characters required in sampled pages.",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=5,
        help="Number of pages to sample from the start of each PDF.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    pdf_dir = args.dir.resolve()
    if not pdf_dir.is_dir():
        raise SystemExit(f"PDF directory not found: {pdf_dir}")

    pdfs = collect_pdfs(pdf_dir, args.include_complete)
    if not pdfs:
        raise SystemExit(f"No PDF files found in {pdf_dir}")

    failed = False
    for pdf_path in pdfs:
        errors = verify_pdf(pdf_path, min_cjk=args.min_cjk, max_pages=args.max_pages)
        if errors:
            failed = True
            print(f"FAIL {pdf_path.name}: {'; '.join(errors)}")
        else:
            sample = extract_sample_text(pdf_path, max_pages=1)
            preview = CJK_RE.findall(sample)
            print(f"OK   {pdf_path.name} ({len(preview)}+ CJK on page 1)")

    if failed:
        raise SystemExit(1)
    print(f"\nAll {len(pdfs)} PDF(s) passed CJK verification.")


if __name__ == "__main__":
    main()
