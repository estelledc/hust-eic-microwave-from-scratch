#!/usr/bin/env python3
"""Patch solutions/ pages with back-references to knowledge/.

Idempotent: skips files that already contain a markdown link to knowledge/.

Strategy:
- After the first H1 line, ensure a blockquote ":knowledge:" line exists with
  a markdown link to the most relevant knowledge page (per `MAPPING` below).
- Mapping is by file path; one knowledge target per source file.

Run:
    python3 scripts/tools/patch_back_refs.py
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "content"

# Map solution file (relative to content/) -> knowledge page (relative to content/)
MAPPING: dict[str, str] = {
    # 第一次作业 · 传输线基础
    "solutions/01-传输线基础/01-Lec01.md": "knowledge/01-传播与传输线/01-长线短线与分布参数.md",
    "solutions/01-传输线基础/02-Lec02.md": "knowledge/01-传播与传输线/02-行波相位常数与特性阻抗.md",
    "solutions/01-传输线基础/03-Lec03.md": "knowledge/01-传播与传输线/03-反射驻波与输入阻抗.md",
    "solutions/01-传输线基础/04-Lec04.md": "knowledge/01-传播与传输线/04-行波纯驻波与行驻波.md",
    "solutions/01-传输线基础/05-Lec05.md": "knowledge/01-传播与传输线/05-开短路线周期性与测量.md",

    # 第二次作业 · 圆图与匹配
    "solutions/02-圆图与匹配/01-Lec06.md": "knowledge/02-反射与匹配/01-多段线并联与四分之一波长.md",
    "solutions/02-圆图与匹配/02-Lec07.md": "knowledge/02-反射与匹配/02-Smith圆图怎么读.md",
    "solutions/02-圆图与匹配/03-Lec08-09/第01题.md": "knowledge/02-反射与匹配/03-并联支节匹配.md",
    "solutions/02-圆图与匹配/03-Lec08-09/第02题.md": "knowledge/02-反射与匹配/03-并联支节匹配.md",
    "solutions/02-圆图与匹配/03-Lec08-09/第03题.md": "knowledge/02-反射与匹配/03-并联支节匹配.md",
    "solutions/02-圆图与匹配/03-Lec08-09/第04题.md": "knowledge/02-反射与匹配/03-并联支节匹配.md",
    "solutions/02-圆图与匹配/03-Lec08-09/第05题.md": "knowledge/02-反射与匹配/03-并联支节匹配.md",
    "solutions/02-圆图与匹配/03-Lec08-09/第06题.md": "knowledge/02-反射与匹配/03-并联支节匹配.md",
    "solutions/02-圆图与匹配/03-Lec08-09/第07题.md": "knowledge/02-反射与匹配/03-并联支节匹配.md",

    # 第三次作业 · 规则波导
    "solutions/03-规则波导与矩形波导/01-Lec10-11.md": "knowledge/03-波导中的场与边界/README.md",
    "solutions/03-规则波导与矩形波导/02-Lec11-12.md": "knowledge/04-截止色散与速度/README.md",
    "solutions/03-规则波导与矩形波导/03-Lec13-16/第01题.md": "knowledge/05-矩形波导工程计算/02-单模工作区与介质填充.md",
    "solutions/03-规则波导与矩形波导/03-Lec13-16/第02题.md": "knowledge/05-矩形波导工程计算/03-导波波长相速群速算例.md",
    "solutions/03-规则波导与矩形波导/03-Lec13-16/第03题.md": "knowledge/05-矩形波导工程计算/01-模谱主模与简并.md",
    "solutions/03-规则波导与矩形波导/03-Lec13-16/第04题.md": "knowledge/05-矩形波导工程计算/04-可传输模判定与枚举.md",
    "solutions/03-规则波导与矩形波导/03-Lec13-16/第05题.md": "knowledge/05-矩形波导工程计算/03-导波波长相速群速算例.md",
    "solutions/03-规则波导与矩形波导/03-Lec13-16/第06题.md": "knowledge/05-矩形波导工程计算/02-单模工作区与介质填充.md",
    "solutions/03-规则波导与矩形波导/03-Lec13-16/第07题.md": "knowledge/05-矩形波导工程计算/05-波导段反射驻波与匹配.md",
    "solutions/03-规则波导与矩形波导/03-Lec13-16/第08题.md": "knowledge/05-矩形波导工程计算/05-波导段反射驻波与匹配.md",
    "solutions/03-规则波导与矩形波导/03-Lec13-16/第09题.md": "knowledge/05-矩形波导工程计算/05-波导段反射驻波与匹配.md",
    "solutions/03-规则波导与矩形波导/03-Lec13-16/第10题.md": "knowledge/05-矩形波导工程计算/04-可传输模判定与枚举.md",
    "solutions/03-规则波导与矩形波导/03-Lec13-16/第11题.md": "knowledge/05-矩形波导工程计算/02-单模工作区与介质填充.md",
    "solutions/03-规则波导与矩形波导/03-Lec13-16/第12题.md": "knowledge/05-矩形波导工程计算/05-波导段反射驻波与匹配.md",

    # 第四次作业 · 后续专题
    "solutions/04-后续专题/01-Lec17-18-圆波导/第01题.md": "knowledge/06-圆波导同轴线微带线/01-圆波导模式与贝塞尔根.md",
    "solutions/04-后续专题/01-Lec17-18-圆波导/第02题.md": "knowledge/06-圆波导同轴线微带线/01-圆波导模式与贝塞尔根.md",
    "solutions/04-后续专题/01-Lec17-18-圆波导/第03题.md": "knowledge/06-圆波导同轴线微带线/01-圆波导模式与贝塞尔根.md",
    "solutions/04-后续专题/01-Lec17-18-圆波导/第04题.md": "knowledge/06-圆波导同轴线微带线/01-圆波导模式与贝塞尔根.md",
    "solutions/04-后续专题/01-Lec17-18-圆波导/第05题.md": "knowledge/06-圆波导同轴线微带线/01-圆波导模式与贝塞尔根.md",
    "solutions/04-后续专题/01-Lec17-18-圆波导/第06题.md": "knowledge/06-圆波导同轴线微带线/04-从矩形到圆与微带的对照.md",
    "solutions/04-后续专题/02-Lec19-20-同轴与微带/第07题.md": "knowledge/06-圆波导同轴线微带线/02-同轴线TEM与高阶模.md",
    "solutions/04-后续专题/02-Lec19-20-同轴与微带/第08题.md": "knowledge/06-圆波导同轴线微带线/03-微带线准TEM与有效介电常数.md",
    "solutions/04-后续专题/02-Lec19-20-同轴与微带/第09题.md": "knowledge/06-圆波导同轴线微带线/03-微带线准TEM与有效介电常数.md",
}


def relpath(src: Path, target_rel: str) -> str:
    """Compute relative path from src's parent to content/<target_rel>."""
    target_abs = (CONTENT / target_rel).resolve()
    return str(Path("/" / target_abs.relative_to(ROOT)).relative_to(
        Path("/") / src.parent.relative_to(ROOT)
    )) if False else _rel(src.parent, target_abs)


def _rel(start: Path, target: Path) -> str:
    import os
    return os.path.relpath(target, start)


def patch_file(src: Path, target_rel: str) -> tuple[bool, str]:
    text = src.read_text()
    knowledge_link = _rel(src.parent, (CONTENT / target_rel).resolve())

    # Already has any link to knowledge/?
    if re.search(r"\]\([^)]*knowledge/[^)]+\)", text):
        return False, "already has knowledge link"

    # Find first H1 (line starting with `# `)
    lines = text.splitlines()
    h1_idx = next((i for i, ln in enumerate(lines) if ln.startswith("# ")), None)
    if h1_idx is None:
        return False, "no H1 found"

    # Find target name for label
    target_name = (CONTENT / target_rel).stem
    blockquote = f"> 对应知识点：[{target_name}]({knowledge_link})"

    # Insert after H1, with blank line before/after
    insert_at = h1_idx + 1
    # Skip blank lines after H1 if any
    while insert_at < len(lines) and lines[insert_at].strip() == "":
        insert_at += 1
    new_lines = lines[:insert_at] + [blockquote, ""] + lines[insert_at:]
    src.write_text("\n".join(new_lines) + "\n")
    return True, f"inserted -> {knowledge_link}"


def main() -> None:
    patched = 0
    skipped = 0
    for rel, target in MAPPING.items():
        src = CONTENT / rel
        if not src.exists():
            print(f"  SKIP missing: {rel}")
            continue
        ok, msg = patch_file(src, target)
        if ok:
            patched += 1
            print(f"  PATCH {rel}: {msg}")
        else:
            skipped += 1
            print(f"  skip  {rel}: {msg}")
    print(f"---\nPatched {patched}, skipped {skipped}")


if __name__ == "__main__":
    main()
