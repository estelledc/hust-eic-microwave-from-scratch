#!/usr/bin/env python3
"""Audit the hiring-facing public showcase contract in built site/."""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote

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
        self.hrefs: set[str] = set()
        self.classes: set[str] = set()
        self.json_ld: list[str] = []
        self._in_json_ld = False
        self._json_buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        if values.get("id"):
            self.ids.add(values["id"])
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


def main() -> int:
    errors: list[str] = []
    html_files = sorted(SITE.rglob("*.html"))
    check(bool(html_files), "site/ has no generated HTML pages", errors)
    canonicals: set[str] = set()

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
        check(len(signals.json_ld) == 1, f"{rel}: expected one JSON-LD block", errors)
        for block in signals.json_ld:
            try:
                payload = json.loads(block)
            except json.JSONDecodeError as exc:
                errors.append(f"{rel}: invalid JSON-LD ({exc})")
                continue
            expected_type = "Course" if rel == "index.html" else "TechArticle"
            check(payload.get("@type") == expected_type, f"{rel}: wrong JSON-LD type", errors)
        check("localhost" not in source, f"{rel}: localhost leaked into public HTML", errors)
        check("intern-journal" not in source, f"{rel}: private repository name leaked", errors)

    home_path = SITE / "index.html"
    if home_path.exists():
        home = home_path.read_text(encoding="utf-8")
        home_signals = Signals()
        home_signals.feed(home)
        for section_id in ("showcase-title", "problem", "system", "role", "learning-paths", "evidence", "limitations"):
            check(section_id in home_signals.ids, f"homepage: missing #{section_id}", errors)
        for class_name in ("jx-chip", "signal-board", "showcase-metrics", "jx-proof", "jx-case-limit"):
            check(class_name in home_signals.classes, f"homepage: missing .{class_name}", errors)
        for href in PORTFOLIO_LINKS:
            check(href in home_signals.hrefs, f"homepage: missing portfolio link {href}", errors)
        for boundary in ("Jason 负责系统判断", "AI 负责放大执行效率", "非官方站点", "没有新增实验测量数据"):
            check(boundary in home, f"homepage: missing public boundary '{boundary}'", errors)
        metric_match = re.search(r'data-metric="page-count">(\d+)<', home)
        check(bool(metric_match), "homepage: missing page-count metric", errors)
        if metric_match:
            check(int(metric_match.group(1)) == len(html_files), "homepage: page-count metric is stale", errors)

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
        check(sitemap_urls == canonicals, "sitemap URLs do not match canonical pages", errors)
    if robots_path.exists():
        check(f"Sitemap: {SITE_URL}/sitemap.xml" in robots_path.read_text(encoding="utf-8"), "robots sitemap is wrong", errors)

    project_status = (ROOT / "docs/PROJECT_STATUS.md").read_text(encoding="utf-8")
    check("QUESTION_AUDIT 63 条题" in project_status, "63-record claim lost its repository evidence", errors)

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
