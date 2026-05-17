# -*- coding: utf-8 -*-
"""Split 第三次作业解答-Lec13-16.md into per-question files (第2～12 题; 第1 题不覆盖)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "content" / "solutions" / "第三次作业" / "Lec13-16"
MAIN = DIR / "第三次作业解答-Lec13-16.md"

HEAD_RE = re.compile(
    r"^##\s*第\s*(\d+)\s*题(（选做）)?\s*[：:]\s*(.*)$", re.M
)

NAV_PFX = (
    "**导航：** [总目录](../《微波技术基础》第三次作业标准解答.md) · "
    "[符号与导读](../第三次作业解答-00-符号与导读.md) · "
    "[Lec10–11](../Lec10-11/第三次作业解答-Lec10-11.md) · "
    "[Lec11～12](../Lec11-12/第三次作业解答-Lec11-12.md) · "
    "[Lec13–Lec16 主册](./第三次作业解答-Lec13-16.md)"
)

# 分题 1～12 速链，相对路径同目录
ALL_Q = " · ".join(
    f"[**{i}**](第三次作业解答-Lec13-16-第{i}题.md)" for i in range(1, 13)
)

APPENDIX = " · [附录](../第三次作业解答-附录.md)"

HINT = (
    "> 矩形波导 $k_{\\mathrm c}$、$\\lambda_{\\mathrm c}$ 与主册导读见 "
    "[Lec13–Lec16 主册](第三次作业解答-Lec13-16.md) 最前与总述段落。"
)


def nav_line(n: int) -> str:
    parts = [NAV_PFX, f"**分题** {ALL_Q}"]
    if n > 1:
        prev_ = n - 1
        parts.append(
            f"**上一题** [第{prev_}题](第三次作业解答-Lec13-16-第{prev_}题.md)"
        )
    if n < 12:
        nxt_ = n + 1
        parts.append(
            f"**下一题** [第{nxt_}题](第三次作业解答-Lec13-16-第{nxt_}题.md)"
        )
    return " · ".join(parts) + APPENDIX + "\n"


def split_questions(text: str) -> list[tuple[int, str, str]]:
    matches = list(HEAD_RE.finditer(text))
    if not matches:
        raise SystemExit("no ## 第 N 题 found")
    out: list[tuple[int, str, str]] = []
    for i, m in enumerate(matches):
        num = int(m.group(1))
        h2_line = m.group(0)
        start = m.end()
        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(text)
        block = text[start:end]
        out.append((num, h2_line, block))
    return out


def to_h1(h2_line: str) -> str:
    """## 第 N 题[（选做）]：…  ->  # 第三次作业（Lec13–Lec16）第 N 题[（选做）]：…"""
    m = re.match(
        r"^##\s*第\s*(\d+)\s*题(（选做）)?\s*[：:]\s*(.*)$",
        h2_line.strip(),
    )
    if not m:
        return h2_line.replace("##", "#", 1)
    n, opt, rest = m.group(1), m.group(2) or "", m.group(3)
    return f"# 第三次作业（Lec13–Lec16）第 {n} 题{opt}：{rest}"


def run() -> None:
    raw = MAIN.read_text(encoding="utf-8")
    chunks = split_questions(raw)
    for num, h2_line, body in chunks:
        if num == 1:
            print("skip 第1题 (保持现有 第三次作业解答-Lec13-16-第1题.md)")
            continue
        h1 = to_h1(h2_line)
        out_path = DIR / f"第三次作业解答-Lec13-16-第{num}题.md"
        content = f"{h1}\n\n{nav_line(num)}\n\n{HINT}\n\n---\n\n{body.lstrip()}"
        out_path.write_text(content, encoding="utf-8", newline="\n")
        print("wrote", out_path.name)


if __name__ == "__main__":
    run()
