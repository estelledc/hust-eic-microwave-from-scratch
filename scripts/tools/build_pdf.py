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

TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from ensure_pdf_fonts import ensure_fonts  # noqa: E402


SITE_DIR = site_build.SITE_DIR
PDF_CSS = ROOT / "assets" / "pdf.css"
DIST_DIR = ROOT / "dist" / "pdf"
MANIFEST_NAME = "manifest.json"

# Must match assets/pdf.css — used in Playwright header/footer templates (outside page CSS).
CJK_FONT_FAMILY = (
    '"PDF Noto Sans SC", "Noto Sans CJK SC", "Noto Sans SC", '
    '"Source Han Sans SC", "Microsoft YaHei", sans-serif'
)

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

# Complete edition merges the four release volumes in this order (with divider pages).
COMPLETE_SECTION_KEYS = ["guide", "knowledge", "solutions", "experiments"]

PDF_OPTIONS = {
    "format": "A4",
    "print_background": True,
    "prefer_css_page_size": True,
    "margin": {"top": "18mm", "right": "14mm", "bottom": "20mm", "left": "14mm"},
    "display_header_footer": True,
    "header_template": (
        f'<div style="font-size:8px;width:100%;text-align:center;color:#666;'
        f"font-family:{CJK_FONT_FAMILY};"
        f'">微波技术基础 · 离线版</div>'
    ),
    "footer_template": (
        f'<div style="font-size:8px;width:100%;text-align:center;color:#666;'
        f"font-family:{CJK_FONT_FAMILY};"
        f'">'
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


def stylesheet_links() -> str:
    return f"""
  <link rel="stylesheet" href="{ROOT.as_uri()}/site/assets/jx/tokens.css">
  <link rel="stylesheet" href="{ROOT.as_uri()}/site/assets/jx/base.css">
  <link rel="stylesheet" href="{ROOT.as_uri()}/site/assets/style.css">
  <link rel="stylesheet" href="{PDF_CSS.as_uri()}">
"""


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
  <title>{title} · 目录</title>{stylesheet_links()}
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


def render_complete_toc_html(
    edition: str,
    sections: list[tuple[str, list[site_build.Page]]],
) -> str:
    edition_text = html.escape(edition)
    total_articles = sum(len(pages) for _, pages in sections)
    blocks: list[str] = []
    for index, (section_key, section_pages) in enumerate(sections, start=1):
        section_title = html.escape(str(VOLUMES[section_key]["title"]))
        items = "\n".join(
            f"<li>{html.escape(page.title)} "
            f'<span style="color:#666;">({html.escape(page.group)})</span></li>'
            for page in section_pages
        )
        blocks.append(
            f'<section class="pdf-toc-section">'
            f"<h2>{index}. {section_title}</h2>"
            f"<p>{len(section_pages)} 篇</p>"
            f"<ol>{items}</ol>"
            f"</section>"
        )
    body = "\n".join(blocks)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>全书合集 · 总目录</title>{stylesheet_links()}
</head>
<body>
  <article class="article pdf-toc pdf-toc-complete">
    <h1>全书合集</h1>
    <p>华中科技大学《微波技术基础》离线 PDF · {edition_text}</p>
    <p>共 {total_articles} 篇，按<strong>学习指南 → 知识点讲义 → 作业解答 → 实验环节</strong>顺序编排；各卷之间插入分节页，并保留分卷目录。</p>
    {body}
  </article>
</body>
</html>
"""


def render_section_divider_html(section_title: str, edition: str, section_index: int) -> str:
    title = html.escape(section_title)
    edition_text = html.escape(edition)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>{title}</title>{stylesheet_links()}
</head>
<body>
  <article class="article pdf-section-divider">
    <p class="pdf-section-divider__edition">{edition_text}</p>
    <h1>{title}</h1>
    <p>全书合集 · 分卷 {section_index} / {len(COMPLETE_SECTION_KEYS)}</p>
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


def inject_pdf_styles(page) -> None:
    if PDF_CSS.exists():
        page.add_style_tag(path=str(PDF_CSS))
    # Belt-and-suspenders: force CJK stack even if site CSS loads late.
    page.add_style_tag(
        content=(
            "html, body, .article, .content, p, li, td, th { "
            f"font-family: {CJK_FONT_FAMILY} !important; "
            "}"
        )
    )


def html_to_pdf(context, html_path: Path, output_path: Path) -> None:
    page = context.new_page()
    try:
        page.goto(html_path.as_uri(), wait_until="domcontentloaded", timeout=120_000)
        inject_pdf_styles(page)
        wait_for_render(page)
        page.emulate_media(media="print")
        page.pdf(path=str(output_path), **PDF_OPTIONS)
    finally:
        page.close()


def html_string_to_pdf(context, html_content: str, tmp_dir: Path, output_path: Path) -> None:
    html_path = tmp_dir / f"{output_path.stem}.html"
    html_path.write_text(html_content, encoding="utf-8")
    html_to_pdf(context, html_path, output_path)


def merge_pdfs(parts: list[Path], output_path: Path) -> int:
    merged = fitz.open()
    page_count = 0
    for part in parts:
        doc = fitz.open(part)
        merged.insert_pdf(doc)
        page_count += doc.page_count
        doc.close()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    # Avoid aggressive garbage collection — preserves embedded font subsets.
    merged.save(output_path, garbage=0, deflate=True)
    merged.close()
    return page_count


def volume_output_path(volume_key: str, edition: str, *, sample: int | None) -> Path:
    spec = VOLUMES[volume_key]
    filename = f"{spec['filename']}-{edition}.pdf"
    if sample:
        filename = f"{spec['filename']}-{edition}-sample.pdf"
    return DIST_DIR / filename


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

        output_path = volume_output_path(volume_key, edition, sample=sample)
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


def build_complete_volume(
    context,
    all_pages: list[site_build.Page],
    *,
    edition: str,
    sample: int | None,
    section_pdfs: dict[str, Path],
) -> dict[str, object]:
    spec = VOLUMES["complete"]
    sections: list[tuple[str, list[site_build.Page]]] = []
    for key in COMPLETE_SECTION_KEYS:
        section_pages = pages_for_volume(all_pages, key)
        if sample:
            section_pages = section_pages[:sample]
        sections.append((key, section_pages))

    with tempfile.TemporaryDirectory(prefix="mw-pdf-complete-") as tmp_dir:
        tmp = Path(tmp_dir)
        part_paths: list[Path] = []

        master_toc_pdf = tmp / "00-master-toc.pdf"
        html_string_to_pdf(
            context,
            render_complete_toc_html(edition, sections),
            tmp,
            master_toc_pdf,
        )
        part_paths.append(master_toc_pdf)

        for index, key in enumerate(COMPLETE_SECTION_KEYS):
            section_pdf = section_pdfs.get(key)
            if section_pdf is None or not section_pdf.exists():
                raise SystemExit(f"Missing section PDF for complete volume: {key!r}")
            if index > 0:
                divider_pdf = tmp / f"divider-{key}.pdf"
                html_string_to_pdf(
                    context,
                    render_section_divider_html(
                        str(VOLUMES[key]["title"]), edition, index + 1
                    ),
                    tmp,
                    divider_pdf,
                )
                part_paths.append(divider_pdf)
            part_paths.append(section_pdf)

        output_path = volume_output_path("complete", edition, sample=sample)
        page_count = merge_pdfs(part_paths, output_path)
        size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"  → {output_path.relative_to(ROOT)} ({page_count} pages, {size_mb:.1f} MiB)")
        return {
            "volume": "complete",
            "title": spec["title"],
            "file": output_path.name,
            "pages": page_count,
            "articles": sum(len(pages) for _, pages in sections),
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
        help="Which volume to build (default: all four volumes plus complete edition).",
    )
    parser.add_argument(
        "--include-complete",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--skip-complete",
        action="store_true",
        help="Skip the complete volume when building all volumes.",
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
    parser.add_argument(
        "--skip-font-download",
        action="store_true",
        help="Do not download bundled Noto Sans SC woff2 (use system CJK fonts only).",
    )
    return parser.parse_args()


def volume_keys_to_build(args: argparse.Namespace) -> list[str]:
    if args.volume != "all":
        return [args.volume]
    keys = [key for key in VOLUMES if key != "complete"]
    include_complete = args.include_complete or not args.skip_complete
    if include_complete:
        keys.append("complete")
    return keys


def main() -> None:
    args = parse_args()
    if not args.skip_font_download:
        print("Ensuring bundled CJK fonts …")
        ensure_fonts()

    pages = ensure_site(rebuild=args.rebuild)
    print(f"Site has {len(pages)} HTML pages.")

    keys = volume_keys_to_build(args)
    want_complete = "complete" in keys
    section_keys = [key for key in keys if key != "complete"]
    if want_complete and not section_keys:
        section_keys = list(COMPLETE_SECTION_KEYS)

    entries: list[dict[str, object]] = []
    section_pdf_paths: dict[str, Path] = {}

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context()
        try:
            for key in section_keys:
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
                section_pdf_paths[key] = volume_output_path(key, args.edition, sample=args.sample)

            if want_complete:
                print(f"\n=== {VOLUMES['complete']['title']} (merge) ===")
                entries.append(
                    build_complete_volume(
                        context,
                        pages,
                        edition=args.edition,
                        sample=args.sample,
                        section_pdfs=section_pdf_paths,
                    )
                )
        finally:
            context.close()
            browser.close()

    write_manifest(entries, args.edition)
    print(f"\nDone. PDFs in {DIST_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
