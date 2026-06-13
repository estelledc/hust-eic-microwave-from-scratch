#!/usr/bin/env python3
"""Cross-reference health check for the microwave review.

For each knowledge/ page (excluding READMEs and 99-自检清单), verify it links
to at least one solutions/ page. For each solutions/ leaf (excluding READMEs
and 00/99 helper pages), verify it links to at least one knowledge/ page.

Outputs a markdown report to docs/CROSS_REF_REPORT.md.

Run:
    python3 scripts/tools/check_cross_refs.py
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "content"
REPORT = ROOT / "docs" / "CROSS_REF_REPORT.md"

LINK_RE = re.compile(r"\]\(([^)]+)\)")

SKIP_NAMES = {"README.md", "index.md"}
SKIP_PREFIXES = ("00-", "99-")


def is_target_page(p: Path) -> bool:
    if p.name in SKIP_NAMES:
        return False
    return not p.name.startswith(SKIP_PREFIXES)


def md_links(text: str) -> list[str]:
    return [m.group(1).split("#", 1)[0] for m in LINK_RE.finditer(text)]


def page_links_to(page: Path, target_dir: Path) -> list[str]:
    """Return resolved links from `page` that point inside `target_dir`."""
    text = page.read_text(encoding="utf-8")
    out = []
    for raw in md_links(text):
        if raw.startswith(("http://", "https://", "mailto:", "#")):
            continue
        try:
            resolved = (page.parent / raw).resolve()
        except OSError:
            continue
        try:
            resolved.relative_to(target_dir)
        except ValueError:
            continue
        out.append(str(resolved.relative_to(ROOT)))
    return out


def main() -> None:
    knowledge_dir = CONTENT / "knowledge"
    solutions_dir = CONTENT / "solutions"
    experiments_dir = CONTENT / "experiments"

    knowledge_pages = sorted(p for p in knowledge_dir.rglob("*.md") if is_target_page(p))
    solutions_pages = sorted(p for p in solutions_dir.rglob("*.md") if is_target_page(p))
    experiments_pages = sorted(p for p in experiments_dir.rglob("*.md") if is_target_page(p))

    # A knowledge page counts as "linked to applied content" if it points to
    # either a solutions/ page or an experiments/ page.
    knowledge_unlinked = []
    for kp in knowledge_pages:
        sol_links = page_links_to(kp, solutions_dir)
        exp_links = page_links_to(kp, experiments_dir)
        if not (sol_links or exp_links):
            knowledge_unlinked.append(kp.relative_to(ROOT))

    solutions_no_knowledge_link = []
    for sp in solutions_pages:
        if not page_links_to(sp, knowledge_dir):
            solutions_no_knowledge_link.append(sp.relative_to(ROOT))

    experiments_no_knowledge_link = []
    for ep in experiments_pages:
        if not page_links_to(ep, knowledge_dir):
            experiments_no_knowledge_link.append(ep.relative_to(ROOT))

    lines = ["# 交叉引用健康度报告", "", "由 `scripts/tools/check_cross_refs.py` 自动生成。"]
    lines.append("")
    lines.append(f"扫描结果：")
    lines.append(f"- knowledge 单讲页面（不含 README/00/99）：{len(knowledge_pages)}")
    lines.append(f"- solutions 题目页面（不含 README/00/99）：{len(solutions_pages)}")
    lines.append(f"- experiments 实验页面（不含 README/index/00/99）：{len(experiments_pages)}")
    lines.append("")

    lines.append("## knowledge 页未引用任何 solutions / experiments 页")
    lines.append("")
    if knowledge_unlinked:
        lines.append(f"共 {len(knowledge_unlinked)} 页：")
        lines.append("")
        for p in knowledge_unlinked:
            lines.append(f"- `{p}`")
    else:
        lines.append("✅ 所有单讲页面都引到了至少一道作业或一个实验流程。")
    lines.append("")

    lines.append("## solutions 题未引用任何 knowledge 页")
    lines.append("")
    if solutions_no_knowledge_link:
        lines.append(f"共 {len(solutions_no_knowledge_link)} 题：")
        lines.append("")
        for p in solutions_no_knowledge_link:
            lines.append(f"- `{p}`")
    else:
        lines.append("✅ 所有作业题都引到了至少一节知识点。")
    lines.append("")

    lines.append("## experiments 页未引用任何 knowledge 页")
    lines.append("")
    if experiments_no_knowledge_link:
        lines.append(f"共 {len(experiments_no_knowledge_link)} 页：")
        lines.append("")
        for p in experiments_no_knowledge_link:
            lines.append(f"- `{p}`")
    else:
        lines.append("✅ 所有实验页都引到了至少一节知识点。")
    lines.append("")

    lines.append("## 修复建议")
    lines.append("")
    lines.append("- knowledge 单讲页缺反向链：通常在文末『作业怎么答』或『相关链接』段补 `../../solutions/.../第NN题.md` 或 `../../experiments/.../X.md`。")
    lines.append("- solutions 题缺前置链：在题首『对应知识点』段补 `../../knowledge/.../NN-XXX.md`。")
    lines.append("- experiments 页缺前置链：在题首『对应知识点』段补 `../../knowledge/.../NN-XXX.md`。")
    lines.append("- 修复后重跑本脚本验证。")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Report written to {REPORT.relative_to(ROOT)}")
    print(f"Knowledge pages without solution/experiment link: {len(knowledge_unlinked)}")
    print(f"Solution pages without knowledge link: {len(solutions_no_knowledge_link)}")
    print(f"Experiment pages without knowledge link: {len(experiments_no_knowledge_link)}")


if __name__ == "__main__":
    main()
