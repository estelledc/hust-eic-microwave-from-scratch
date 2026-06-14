#!/usr/bin/env python3
"""Build offline PDF volumes from the static site (Playwright print-to-PDF + PyMuPDF merge).

Requires: pip install -r requirements-pdf.txt && playwright install chromium
"""

from __future__ import annotations

import argparse
import html
import json
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import build as site_build  # noqa: E402

try:
    import fitz  # PyMuPDF
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: pymupdf. Run `python -m pip install -r requirements-pdf.txt` first."
    ) from exc

try:
    from playwright.sync_api import sync_playwright
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: playwright. Run:\n"
        "  python -m pip install -r requirements-pdf.txt\n"
        "  playwright install chromium"
    ) from exc


SITE_DIR = site_build.SITE_DIR
PDF_CSS = ROOT / "assets" / "pdf.css"
DIST_DIR = ROOT / "dist" / "pdf"
MANIFEST_NAME = "manifest.json"

VOLUMES: dict[str, dict[str, object]] = {
    "guide": {
        "title": "学习指南",
        "filename": "microwave-guide",
        "groups": ["首页", "学习指南", "附录"],
    },
    "knowledge": {
        "title": "知识点讲义",
        "filename": "microwave-knowledge",
        "groups": ["知识点讲义"],
    },
    "solutions": {
        "title": "作业解答",
        "filename": "microwave-solutions",
        "groups": ["作业解答"],
    },
    "experiments": {
        "title": "实验环节",
        "filename": "microwave-experiments",
        "groups": ["实验环节"],
    },
    "complete": {
        "title": "全书合集",
        "filename": "microwave-complete",
        "groups": ["首页", "学习指南", "知识点讲义", "作业解答", "实验环节", "附录"],
    },
}

PDF_OPTIONS = {
    "format": "A4",
    "print_background": True,
    "margin": {"top": "18mm", "right": "14mm", "bottom": "20mm", "left": "14mm"},
    "display_header_footer": True,
    "header_template": (
        '<div style="font-size:8px;width:100%;text-align:center;color:#666;'
        'font-family:system-ui,sans-serif;">微波技术基础 · 离线版</div>'
    ),
    "footer_template": (
        '<div style="font-size:8px;width:100%;text-align:center;color:#666;'
        'font-family:system-ui,sans-serif;">'
        '<span class="pageNumber"></span> / <span class="totalPages"></span></div>'
    ),
}


def ensure_site(*, rebuild: bool) -> list[site_build.Page]:
    if rebuild:
        print("Building static site …")
        site_build.main()
    elif not (SITE_DIR / "index.html").exists():
        raise SystemExit(
            f"Missing built site at {SITE_DIR}. Run `python build.py` first, or pass --rebuild."
        )
    pages = site_build.collect_pages()
    if not pages:
        raise SystemExit("No pages collected from content/.")
    return pages


def pages_for_volume(pages: list[site_build.Page], volume_key: str) -> list[site_build.Page]:
    spec = VOLUMES[volume_key]
    groups = set(spec["groups"])  # type: ignore[arg-type]
    return [page for page in pages if page.group in groups]


def render_toc_html(volume_key: str, pages: list[site_build.Page], edition: str) -> str:
    spec = VOLUMES[volume_key]
    title = html.escape(str(spec["title"]))
    edition_text = html.escape(edition)
    items = "\n".join(
        f"<li>{html.escape(page.title)} "
        f'<span style="color:#666;">({html.escape(page.group)})</span></li>'
        for page in pages
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>{title} · 目录</title>
  <link rel="stylesheet" href="{ROOT.as_uri()}/site/assets/jx/tokens.css">
  <link rel="stylesheet" href="{ROOT.as_uri()}/site/assets/jx/base.css">
  <link rel="stylesheet" href="{ROOT.as_uri()}/site/assets/style.css">
  <link rel="stylesheet" href="{PDF_CSS.as_uri()}">
</head>
<body>
  <article class="article pdf-toc">
    <h1>{title}</h1>
    <p>华中科技大学《微波技术基础》离线 PDF · {edition_text}</p>
    <p>共 {len(pages)} 篇，按站点阅读顺序排列。正文不含原始课件或站外出处引用。</p>
    <ol>{items}</ol>
  </article>
</body>
</html>
"""


def wait_for_render(page) -> None:
    page.wait_for_load_state("networkidle", timeout=120_000)
    uses_mathjax = page.locator('script[src*="mathjax"]').count() > 0
    if uses_mathjax:
        try:
            page.wait_for_function(
                """() => {
                    if (!window.MathJax) return false;
                    if (window.MathJax.startup && window.MathJax.startup.promise) {
                        return window.MathJax.startup.promise.then(() => true);
                    }
                    return typeof window.MathJax.typesetPromise === 'function';
                }""",
                timeout=90_000,
            )
            page.evaluate(
                "() => window.MathJax.typesetPromise && window.MathJax.typesetPromise()"
            )
        except Exception:
            pass
    if page.locator(".mermaid").count() > 0:
        try:
            page.wait_for_selector(".mermaid svg", timeout=15_000)
        except Exception:
            pass
    page.wait_for_timeout(400)


def html_to_pdf(context, html_path: Path, output_path: Path) -> None:
    page = context.new_page()
    try:
        page.goto(html_path.as_uri(), wait_until="domcontentloaded", timeout=120_000)
        if PDF_CSS.exists():
            page.add_style_tag(path=str(PDF_CSS))
        wait_for_render(page)
        page.emulate_media(media="print")
        page.pdf(path=str(output_path), **PDF_OPTIONS)
    finally:
        page.close()


def merge_pdfs(parts: list[Path], output_path: Path) -> int:
    merged = fitz.open()
    page_count = 0
    for part in parts:
        doc = fitz.open(part)
        merged.insert_pdf(doc)
        page_count += doc.page_count
        doc.close()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    merged.save(output_path, garbage=4, deflate=True)
    merged.close()
    return page_count


def build_volume(
    context,
    volume_key: str,
    pages: list[site_build.Page],
    *,
    edition: str,
    sample: int | None,
) -> dict[str, object]:
    spec = VOLUMES[volume_key]
    selected = pages[:sample] if sample else pages
    if not selected:
        raise SystemExit(f"Volume {volume_key!r} has no pages.")

    with tempfile.TemporaryDirectory(prefix="mw-pdf-") as tmp_dir:
        tmp = Path(tmp_dir)
        part_paths: list[Path] = []

        toc_html = tmp / "00-toc.html"
        toc_html.write_text(render_toc_html(volume_key, selected, edition), encoding="utf-8")
        toc_pdf = tmp / "00-toc.pdf"
        html_to_pdf(context, toc_html, toc_pdf)
        part_paths.append(toc_pdf)

        for index, page in enumerate(selected, start=1):
            html_path = page.output.resolve()
            if not html_path.exists():
                raise SystemExit(f"Missing built HTML: {html_path}")
            part_pdf = tmp / f"{index:03d}.pdf"
            print(f"  [{index}/{len(selected)}] {page.title}")
            html_to_pdf(context, html_path, part_pdf)
            part_paths.append(part_pdf)

        filename = f"{spec['filename']}-{edition}.pdf"
        if sample:
            filename = f"{spec['filename']}-{edition}-sample.pdf"
        output_path = DIST_DIR / filename
        page_count = merge_pdfs(part_paths, output_path)
        size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"  → {output_path.relative_to(ROOT)} ({page_count} pages, {size_mb:.1f} MiB)")
        return {
            "volume": volume_key,
            "title": spec["title"],
            "file": output_path.name,
            "pages": page_count,
            "articles": len(selected),
            "size_mb": round(size_mb, 2),
        }


def write_manifest(entries: list[dict[str, object]], edition: str) -> None:
    manifest = {
        "edition": edition,
        "generated": date.today().isoformat(),
        "site_pages": len(site_build.collect_pages()),
        "volumes": entries,
    }
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    (DIST_DIR / MANIFEST_NAME).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build offline PDF volumes from the static site.")
    parser.add_argument(
        "--volume",
        choices=[*VOLUMES.keys(), "all"],
        default="all",
        help="Which volume to build (default: all except skipping complete unless --include-complete).",
    )
    parser.add_argument(
        "--include-complete",
        action="store_true",
        help="Also build the single-file complete volume (large).",
    )
    parser.add_argument(
        "--edition",
        default=date.today().strftime("%Y.%m"),
        help="Edition suffix for filenames, e.g. 2026.06 (default: current YYYY.MM).",
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Run build.py before exporting PDFs.",
    )
    parser.add_argument(
        "--sample",
        type=int,
        metavar="N",
        help="Only export first N articles per volume (for smoke tests).",
    )
    return parser.parse_args()


def volume_keys_to_build(args: argparse.Namespace) -> list[str]:
    if args.volume != "all":
        return [args.volume]
    keys = [key for key in VOLUMES if key != "complete"]
    if args.include_complete:
        keys.append("complete")
    return keys


def main() -> None:
    args = parse_args()
    pages = ensure_site(rebuild=args.rebuild)
    print(f"Site has {len(pages)} HTML pages.")

    keys = volume_keys_to_build(args)
    entries: list[dict[str, object]] = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context()
        try:
            for key in keys:
                volume_pages = pages_for_volume(pages, key)
                print(f"\n=== {VOLUMES[key]['title']} ({len(volume_pages)} articles) ===")
                entries.append(
                    build_volume(
                        context,
                        key,
                        volume_pages,
                        edition=args.edition,
                        sample=args.sample,
                    )
                )
        finally:
            context.close()
            browser.close()

    write_manifest(entries, args.edition)
    print(f"\nDone. PDFs in {DIST_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
