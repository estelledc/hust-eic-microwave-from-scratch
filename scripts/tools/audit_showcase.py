#!/usr/bin/env python3
"""Audit the hiring-facing public showcase contract in built site/."""

from __future__ import annotations

import json
import re
import sys
from functools import lru_cache
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
SITE_URL = "https://estelledc.github.io/hust-eic-microwave-from-scratch"
OG_URL = f"{SITE_URL}/assets/images/og-microwave.png"
PORTFOLIO_LINKS = (
    "https://estelledc.github.io/",
    "https://estelledc.github.io/about/",
    "https://estelledc.github.io/resume/",
    "https://github.com/estelledc/hust-eic-microwave-from-scratch",
)
ACTION_REF_RE = re.compile(r"^\s*(?:-\s*)?uses:\s*([^\s#]+)", re.MULTILINE)


class Signals(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.canonical: list[str] = []
        self.metas: dict[str, str] = {}
        self.ids: set[str] = set()
        self.id_counts: dict[str, int] = {}
        self.hrefs: set[str] = set()
        self.classes: set[str] = set()
        self.json_ld: list[str] = []
        self.images: list[dict[str, str]] = []
        self._in_json_ld = False
        self._json_buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        if values.get("id"):
            self.ids.add(values["id"])
            self.id_counts[values["id"]] = self.id_counts.get(values["id"], 0) + 1
        self.classes.update(values.get("class", "").split())
        if values.get("href"):
            self.hrefs.add(values["href"])
        if tag == "link" and "canonical" in values.get("rel", "").split():
            self.canonical.append(values.get("href", ""))
        if tag == "meta":
            key = values.get("name") or values.get("property")
            if key:
                self.metas[key] = values.get("content", "")
        if tag == "script" and values.get("type") == "application/ld+json":
            self._in_json_ld = True
            self._json_buffer = []
        if tag == "img":
            self.images.append(values)

    def handle_data(self, data: str) -> None:
        if self._in_json_ld:
            self._json_buffer.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._in_json_ld:
            self.json_ld.append("".join(self._json_buffer))
            self._in_json_ld = False
            self._json_buffer = []


def expected_canonical(path: Path) -> str:
    rel = path.relative_to(SITE)
    if rel.as_posix() == "index.html":
        return f"{SITE_URL}/"
    if rel.name == "index.html":
        return f"{SITE_URL}/{quote(rel.parent.as_posix(), safe='/')}/"
    return f"{SITE_URL}/{quote(rel.as_posix(), safe='/')}"


def check(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


@lru_cache(maxsize=None)
def actual_image_dimensions(path: Path) -> tuple[int, int] | None:
    if not path.is_file():
        return None
    if path.suffix.lower() == ".svg":
        source = path.read_text(encoding="utf-8", errors="ignore")[:2048]
        width = re.search(r'\bwidth=["\']([0-9.]+)', source)
        height = re.search(r'\bheight=["\']([0-9.]+)', source)
        if width and height:
            return round(float(width.group(1))), round(float(height.group(1)))
        view_box = re.search(r'\bviewBox=["\'][^"\']*?([0-9.]+)\s+([0-9.]+)', source)
        if view_box:
            return round(float(view_box.group(1))), round(float(view_box.group(2)))
        return None
    try:
        with Image.open(path) as image:
            return image.size
    except OSError:
        return None


def main() -> int:
    errors: list[str] = []
    html_files = sorted(SITE.rglob("*.html"))
    check(bool(html_files), "site/ has no generated HTML pages", errors)
    canonicals: set[str] = set()
    indexable_canonicals: set[str] = set()

    for path in html_files:
        rel = path.relative_to(SITE).as_posix()
        source = path.read_text(encoding="utf-8")
        signals = Signals()
        signals.feed(source)
        check(len(signals.canonical) == 1, f"{rel}: expected one canonical", errors)
        if signals.canonical:
            expected = expected_canonical(path)
            check(signals.canonical[0] == expected, f"{rel}: canonical mismatch", errors)
            check(signals.canonical[0] not in canonicals, f"{rel}: duplicate canonical", errors)
            canonicals.add(signals.canonical[0])
            if rel != "404.html":
                indexable_canonicals.add(signals.canonical[0])
        for key in (
            "description",
            "og:type",
            "og:title",
            "og:description",
            "og:url",
            "og:image",
            "twitter:card",
            "twitter:title",
            "twitter:description",
            "twitter:image",
        ):
            check(bool(signals.metas.get(key)), f"{rel}: missing {key}", errors)
        check(signals.metas.get("og:image") == OG_URL, f"{rel}: wrong og:image", errors)
        check(signals.metas.get("twitter:image") == OG_URL, f"{rel}: wrong twitter:image", errors)
        check(signals.metas.get("twitter:card") == "summary_large_image", f"{rel}: wrong twitter card", errors)
        duplicate_ids = [identifier for identifier, count in signals.id_counts.items() if count > 1]
        check(not duplicate_ids, f"{rel}: duplicate ids {duplicate_ids[:5]}", errors)
        check(signals.metas.get("author") == "Jason Xun", f"{rel}: author identity mismatch", errors)
        for image in signals.images:
            src = image.get("src", "<unknown>")
            for attribute in ("alt", "width", "height", "loading", "decoding"):
                check(bool(image.get(attribute)), f"{rel}: image {src} missing {attribute}", errors)
            parsed_src = urlsplit(src)
            if not parsed_src.scheme and not parsed_src.netloc and parsed_src.path:
                target = (path.parent / unquote(parsed_src.path)).resolve()
                dimensions = actual_image_dimensions(target)
                if dimensions:
                    declared = (int(image.get("width", 0) or 0), int(image.get("height", 0) or 0))
                    check(declared == dimensions, f"{rel}: image {src} declares {declared}, actual {dimensions}", errors)
        check(len(signals.json_ld) == 1, f"{rel}: expected one JSON-LD block", errors)
        for block in signals.json_ld:
            try:
                payload = json.loads(block)
            except json.JSONDecodeError as exc:
                errors.append(f"{rel}: invalid JSON-LD ({exc})")
                continue
            expected_type = "Course" if rel == "index.html" else "TechArticle"
            check(payload.get("@type") == expected_type, f"{rel}: wrong JSON-LD type", errors)
            author = payload.get("author", {})
            check(author.get("name") == "Jason Xun", f"{rel}: JSON-LD author name mismatch", errors)
            check(author.get("@id") == "https://estelledc.github.io/#person", f"{rel}: JSON-LD author id mismatch", errors)
        check("localhost" not in source, f"{rel}: localhost leaked into public HTML", errors)
        check("intern-journal" not in source, f"{rel}: private repository name leaked", errors)
        if rel == "404.html":
            check('content="noindex,follow"' in source, "404.html: missing noindex directive", errors)

    home_path = SITE / "index.html"
    if home_path.exists():
        home = home_path.read_text(encoding="utf-8")
        home_signals = Signals()
        home_signals.feed(home)
        for section_id in ("showcase-title", "problem", "system", "role", "learning-paths", "evidence", "limitations"):
            check(section_id in home_signals.ids, f"homepage: missing #{section_id}", errors)
        for class_name in ("jx-chip", "measurement-proof", "showcase-metrics", "jx-proof", "jx-case-limit", "nav-compact"):
            check(class_name in home_signals.classes, f"homepage: missing .{class_name}", errors)
        for href in PORTFOLIO_LINKS:
            check(href in home_signals.hrefs, f"homepage: missing portfolio link {href}", errors)
        for boundary in ("Jason 负责系统判断", "AI 负责放大执行效率", "非官方站点", "没有新增实验测量数据"):
            check(boundary in home, f"homepage: missing public boundary '{boundary}'", errors)
        for entry in ("学概念", "做题", "看测量", "SMITH ↔ VNA"):
            check(entry in home, f"homepage: missing core entry '{entry}'", errors)
        check("mathjax@3" not in home, "homepage: MathJax must be conditionally omitted", errors)
        check("mermaid@10" not in home, "homepage: Mermaid must be conditionally omitted", errors)
        sidebar_match = re.search(r'<aside class="sidebar".*?</aside>', home, re.DOTALL)
        check(bool(sidebar_match), "homepage: sidebar missing", errors)
        if sidebar_match:
            check(sidebar_match.group(0).count("<a ") <= 12, "homepage: sidebar navigation is no longer compact", errors)
        metric_match = re.search(r'data-metric="page-count">(\d+)<', home)
        check(bool(metric_match), "homepage: missing page-count metric", errors)
        if metric_match:
            check(int(metric_match.group(1)) == len([path for path in html_files if path.name != "404.html"]), "homepage: page-count metric is stale", errors)

    image_path = SITE / "assets/images/og-microwave.png"
    check(image_path.exists(), "social preview missing from site output", errors)
    if image_path.exists():
        with Image.open(image_path) as image:
            check(image.size == (1200, 630), f"social preview is {image.size}, expected 1200x630", errors)

    sitemap_path = SITE / "sitemap.xml"
    robots_path = SITE / "robots.txt"
    check(sitemap_path.exists(), "sitemap.xml missing", errors)
    check(robots_path.exists(), "robots.txt missing", errors)
    if sitemap_path.exists():
        sitemap_urls = set(re.findall(r"<loc>([^<]+)</loc>", sitemap_path.read_text(encoding="utf-8")))
        check(sitemap_urls == indexable_canonicals, "sitemap URLs do not match indexable canonical pages", errors)
    if robots_path.exists():
        check(f"Sitemap: {SITE_URL}/sitemap.xml" in robots_path.read_text(encoding="utf-8"), "robots sitemap is wrong", errors)

    project_status = (ROOT / "docs/PROJECT_STATUS.md").read_text(encoding="utf-8")
    check("QUESTION_AUDIT 63 条题" in project_status, "63-record claim lost its repository evidence", errors)
    check((ROOT / "assets/jx/VERSION").read_text(encoding="utf-8").strip() == "2.2.0", "Jason DS version must be 2.2.0", errors)
    motion_css = (ROOT / "assets/style.css").read_text(encoding="utf-8")
    check("@media (hover: hover) and (pointer: fine)" in motion_css, "fine-pointer hover gate is missing", errors)
    check("@media (prefers-reduced-motion: reduce)" in motion_css, "reduced-motion handling is missing", errors)
    check(not re.search(r"\btransition\s*:\s*all\b", motion_css, re.I), "transition: all is forbidden", errors)
    check("transition: none !important" not in motion_css, "global motion reset removes equivalent feedback", errors)
    app_js = (ROOT / "assets/app.js").read_text(encoding="utf-8")
    check('securityLevel: "strict"' in app_js, "Mermaid must use strict security mode", errors)
    check('reduceMotion ? "auto" : "smooth"' in app_js, "formula quick view must respect reduced motion", errors)

    for workflow in sorted((ROOT / ".github/workflows").glob("*.y*ml")):
        for action_ref in ACTION_REF_RE.findall(workflow.read_text(encoding="utf-8")):
            if action_ref.startswith(("./", "docker://")):
                continue
            ref = action_ref.rsplit("@", 1)[-1] if "@" in action_ref else ""
            check(
                bool(re.fullmatch(r"[0-9a-f]{40}", ref)),
                f"{workflow.relative_to(ROOT)}: action is not pinned to a full commit SHA ({action_ref})",
                errors,
            )

    if errors:
        print("SHOWCASE AUDIT FAILED:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(
        "Showcase audit passed "
        f"({len(html_files)} pages, {len(canonicals)} unique canonicals, 1200x630 social preview)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
