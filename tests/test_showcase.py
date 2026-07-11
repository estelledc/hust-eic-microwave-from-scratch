from __future__ import annotations

import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

import build


class ImageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.images: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "img":
            self.images.append({key: value or "" for key, value in attrs})


class ShowcaseContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.pages = build.collect_pages()
        cls.pages_by_source = build.path_to_page(cls.pages)
        cls.home = next(
            page for page in cls.pages if page.rel_source == Path("content/index.md")
        )
        cls.home_html = build.render_home_page(
            cls.home, cls.pages, cls.pages_by_source
        )

    def test_current_evidence_baseline(self) -> None:
        self.assertEqual(len(self.pages), 169)
        self.assertEqual(len(build.KNOWLEDGE_STAGES), 8)
        self.assertEqual(len(build.HOMEWORK_CARDS), 5)
        self.assertEqual(len(build.EXPERIMENT_CARDS), 2)
        self.assertEqual(build.AUDITED_QUESTION_COUNT, 63)

    def test_homepage_contains_case_study_contract(self) -> None:
        for marker in (
            'id="problem"',
            'id="system"',
            'id="role"',
            'id="evidence"',
            'id="limitations"',
            "Jason 负责系统判断",
            "AI 负责放大执行效率",
            "非官方站点",
            "没有新增实验测量数据",
        ):
            self.assertIn(marker, self.home_html)

    def test_homepage_metadata_is_share_ready(self) -> None:
        self.assertIn(f'<link rel="canonical" href="{build.SITE_URL}/">', self.home_html)
        self.assertIn('property="og:image"', self.home_html)
        self.assertIn('name="twitter:card" content="summary_large_image"', self.home_html)
        match = re.search(
            r'<script type="application/ld\+json">(.+?)</script>', self.home_html
        )
        self.assertIsNotNone(match)
        payload = json.loads(match.group(1))
        self.assertEqual(payload["@type"], "Course")
        self.assertTrue(payload["isAccessibleForFree"])
        self.assertEqual(payload["author"]["name"], "Jason Xun")
        self.assertEqual(payload["author"]["@id"], "https://estelledc.github.io/#person")
        self.assertIn('<meta name="author" content="Jason Xun">', self.home_html)

    def test_nested_canonical_is_encoded_and_directory_clean(self) -> None:
        nested = next(
            page
            for page in self.pages
            if page.rel_source == Path("content/knowledge/01-传播与传输线/README.md")
        )
        canonical = build.canonical_url(nested)
        self.assertTrue(canonical.endswith("/content/knowledge/01-%E4%BC%A0%E6%92%AD%E4%B8%8E%E4%BC%A0%E8%BE%93%E7%BA%BF/"))
        self.assertNotIn("index.html", canonical)

    def test_portfolio_escape_routes_are_visible(self) -> None:
        for href in (
            build.PORTFOLIO_URL,
            build.ABOUT_URL,
            build.RESUME_URL,
            build.GITHUB_REPO_URL,
        ):
            self.assertIn(f'href="{href}"', self.home_html)

    def test_homepage_makes_smith_and_vna_the_core_proof(self) -> None:
        for marker in (
            'class="signal-board measurement-proof"',
            "CORE PROOF · REFLECTION",
            "SMITH ↔ VNA",
            "smith_lec07_q0_anatomy.webp",
            "exp2-resonator-s21-curve.webp",
            "不是新增实验测量数据",
        ):
            self.assertIn(marker, self.home_html)
        parser = ImageParser()
        parser.feed(self.home_html)
        self.assertEqual(len(parser.images), 2)
        for image in parser.images:
            for attribute in ("alt", "width", "height", "loading", "decoding"):
                self.assertTrue(image.get(attribute), (attribute, image))

    def test_homepage_has_three_task_first_entries(self) -> None:
        cta = self.home_html.split('<div class="home-cta-row">', 1)[1].split("</div>", 1)[0]
        self.assertEqual(cta.count('class="home-cta'), 3)
        for label in ("学概念", "做题", "看测量"):
            self.assertIn(label, cta)

    def test_sidebar_uses_compact_hubs_and_current_context(self) -> None:
        sidebar = self.home_html.split('<aside class="sidebar"', 1)[1].split("</aside>", 1)[0]
        self.assertIn('class="nav-compact"', sidebar)
        self.assertIn('class="nav-hubs"', sidebar)
        self.assertLessEqual(sidebar.count("<a "), 12)
        self.assertNotIn('class="nav-subgroup', sidebar)

    def test_heavy_renderers_are_loaded_only_for_matching_content(self) -> None:
        self.assertNotIn("mathjax@3", self.home_html)
        self.assertNotIn("mermaid@10", self.home_html)

        math_only = next(
            page for page in self.pages
            if any(pattern.search(page.source.read_text(encoding="utf-8")) for pattern in build.MATH_PATTERNS)
            and "```mermaid" not in page.source.read_text(encoding="utf-8").lower()
        )
        math_html = build.render_page(math_only, self.pages, self.pages_by_source)
        self.assertIn("mathjax@3", math_html)
        self.assertNotIn("mermaid@10", math_html)

        mermaid_page = next(
            page for page in self.pages
            if "```mermaid" in page.source.read_text(encoding="utf-8").lower()
        )
        mermaid_html = build.render_page(mermaid_page, self.pages, self.pages_by_source)
        self.assertIn("mermaid@10", mermaid_html)

    def test_accessibility_and_security_contracts_are_explicit(self) -> None:
        css = (build.ROOT / "assets/style.css").read_text(encoding="utf-8")
        app = (build.ROOT / "assets/app.js").read_text(encoding="utf-8")
        self.assertIn("@media (max-width: 360px)", css)
        self.assertIn("@media (prefers-reduced-motion: reduce)", css)
        self.assertIn("summary:focus-visible", css)
        self.assertIn('securityLevel: "strict"', app)


if __name__ == "__main__":
    unittest.main()
