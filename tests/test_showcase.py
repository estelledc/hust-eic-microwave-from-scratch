from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

import build


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


if __name__ == "__main__":
    unittest.main()
