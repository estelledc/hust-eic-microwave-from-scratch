"""Validate exam/BLQ integration links and anchors after content fixes."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "content"
SITE = ROOT / "site"

# markdown path (under content/) -> required anchor ids that must exist in built HTML
ANCHOR_CHECKS: tuple[tuple[str, str], ...] = (
    ("guide/exam-review.md", "textbook-6ch-nav"),
    ("guide/exam-review.md", "老师-13-项划重点"),
    ("solutions/06-考前复习/README.md", "topic-index"),
    ("solutions/06-考前复习/README.md", "gap-solutions"),
    ("knowledge/02-反射与匹配/03-并联支节匹配.md", "stub-dead-zone"),
    ("knowledge/08-谐振器网络与课程综合/02-微波网络基础与S参数.md", "network-operating-params"),
    ("knowledge/08-谐振器网络与课程综合/01-微波谐振器与谐振腔.md", "lc-vs-microwave-resonator"),
    ("knowledge/08-谐振器网络与课程综合/01-微波谐振器与谐振腔.md", "coaxial-cavity"),
    ("knowledge/08-谐振器网络与课程综合/01-微波谐振器与谐振腔.md", "quality-factor-q"),
    ("knowledge/05-矩形波导工程计算/05-波导段反射驻波与匹配.md", "wall-current-slots"),
    ("solutions/06-考前复习/99-公式与图像.md", "wg-cavity-formulas"),
    ("knowledge/08-谐振器网络与课程综合/03-常用微波元件网络化描述.md", "magic-t"),
)

# Critical solution links that must appear in 06-考前复习 README
README_MUST_CONTAIN: tuple[str, ...] = (
    "04-Lec04.md",
    "第07题.md",
    "stub-dead-zone",
    "network-operating-params",
    "wall-current-slots",
)


def md_to_site_html(md_rel: str) -> Path:
    source = ROOT / "content" / md_rel.replace("content/", "")
    rel = source.relative_to(ROOT)
    if rel == Path("content/index.md"):
        return SITE / "index.html"
    if source.name.lower() in {"readme.md", "index.md"}:
        return SITE / rel.parent / "index.html"
    return SITE / rel.with_suffix(".html")


def main() -> int:
    errors: list[str] = []
    if not SITE.exists():
        errors.append("site/ not built — run build.py first")
    else:
        for md_rel, anchor in ANCHOR_CHECKS:
            html_path = md_to_site_html(md_rel)
            if not html_path.exists():
                errors.append(f"missing HTML: {html_path}")
                continue
            html = html_path.read_text(encoding="utf-8")
            if f'id="{anchor}"' not in html and f"id='{anchor}'" not in html:
                errors.append(f"anchor #{anchor} not in {html_path.name}")

    readme = (CONTENT / "solutions/06-考前复习/README.md").read_text(encoding="utf-8")
    for needle in README_MUST_CONTAIN:
        if needle not in readme:
            errors.append(f"06-考前复习/README.md missing: {needle}")

    # Legacy BLQ page-map guard removed (topic-index replaces blq-page-map)

    if errors:
        print("INTEGRATION CHECK FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"Integration check passed ({len(ANCHOR_CHECKS)} anchors, {len(README_MUST_CONTAIN)} README guards)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
