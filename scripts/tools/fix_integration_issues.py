"""One-off batch fixes for exam/BLQ integration consistency."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "content"

REPLACEMENTS: tuple[tuple[str, str, str], ...] = (
    # (glob under content, old, new) — 枝节→支节 in Lec08 solutions
    ("solutions/02-圆图与匹配/**/*.md", "枝节", "支节"),
    ("knowledge/02-反射与匹配/03-并联支节匹配.md", "单枝节", "单支节"),
    ("knowledge/02-反射与匹配/03-并联支节匹配.md", "双枝节", "双支节"),
    ("knowledge/05-矩形波导工程计算/05-波导段反射驻波与匹配.md", "短路枝节", "短路支节"),
    ("solutions/02-圆图与匹配/99-公式与图像.md", "外圆枝节", "外圆支节"),
)


def apply_replacements() -> int:
    count = 0
    for pattern, old, new in REPLACEMENTS:
        for path in CONTENT.glob(pattern):
            text = path.read_text(encoding="utf-8")
            if old not in text:
                continue
            path.write_text(text.replace(old, new), encoding="utf-8")
            count += text.count(old)
    return count


def main() -> None:
    n = apply_replacements()
    print(f"Applied {n} terminology replacements")


if __name__ == "__main__":
    main()
