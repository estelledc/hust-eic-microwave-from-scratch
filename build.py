#!/usr/bin/env python3
"""Build the microwave review Markdown sources into a static web book."""

from __future__ import annotations

import html
import json
import os
import re
import shutil
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Callable
from urllib.parse import unquote

try:
    import markdown
except ImportError as exc:  # pragma: no cover - exercised by users without deps
    raise SystemExit(
        "Missing dependency: markdown. Run `python3 -m pip install -r requirements.txt` first."
    ) from exc

try:
    from PIL import Image, ImageChops
except ImportError as exc:  # pragma: no cover - exercised by users without deps
    Image = None
    ImageChops = None
    PIL_IMPORT_ERROR = exc
else:
    PIL_IMPORT_ERROR = None


ROOT = Path(__file__).resolve().parent
SITE_DIR = ROOT / "site"
NAV_CONFIG_PATH = ROOT / "nav.json"
PUBLIC_ROOTS = (
    Path("content/index.md"),
    Path("content/guide"),
    Path("content/knowledge"),
    Path("content/solutions"),
    Path("content/experiments"),
    Path("content/appendices/讲次-作业-教材章节-知识点矩阵.md"),
)
STATIC_DIRS = ("assets/images", "assets/illustrations")
SITE_TITLE = "微波技术基础"
GITHUB_REPO_URL = "https://github.com/estelledc/hust-eic-microwave-from-scratch"
GITHUB_CORNER_HTML = f"""<a href="{GITHUB_REPO_URL}" class="github-corner" target="_blank" rel="noopener" aria-label="在 GitHub 查看源码">
  <svg width="80" height="80" viewBox="0 0 250 250" aria-hidden="true">
    <path d="M0,0 L115,115 L130,115 L142,142 L250,250 L250,0 Z" fill="var(--accent, #0f766e)"></path>
    <path d="M128.3,109.0 C113.8,99.7 119.0,89.6 119.0,89.6 C122.0,82.7 120.5,78.6 120.5,78.6 C119.2,72.0 123.4,76.3 123.4,76.3 C127.3,80.9 125.5,87.3 125.5,87.3 C122.9,97.6 130.6,101.9 134.4,103.2" fill="#fff" class="octo-arm"></path>
    <path d="M115.0,115.0 C114.9,115.1 118.7,116.5 119.8,115.4 L133.7,101.6 C136.9,99.2 139.9,98.4 142.2,98.6 C133.8,88.0 127.5,74.4 143.8,58.0 C148.5,53.4 154.0,51.2 159.7,51.0 C160.3,49.4 163.2,43.6 171.4,40.1 C171.4,40.1 176.1,42.5 178.8,56.2 C183.1,58.6 187.2,61.8 190.9,65.4 C194.5,69.0 197.7,73.2 200.1,77.5 C213.8,80.2 216.3,84.9 216.3,84.9 C212.7,93.1 206.9,96.0 205.4,96.6 C205.1,102.4 203.0,107.8 198.3,112.5 C181.9,128.9 168.3,122.5 157.7,114.1 C157.9,116.9 156.7,120.9 152.7,124.9 L141.0,136.5 C139.8,137.7 141.6,141.9 141.8,141.8 Z" fill="#fff" class="octo-body"></path>
  </svg>
</a>
<style>
  .github-corner {{ position: fixed; top: 0; right: 0; z-index: 99; border: 0; }}
  .github-corner svg {{ display: block; }}
  .github-corner:hover .octo-arm {{
    animation: octocat-wave 560ms ease-in-out;
  }}
  @keyframes octocat-wave {{
    0%, 100% {{ transform: rotate(0); }}
    20%, 60% {{ transform: rotate(-25deg); }}
    40%, 80% {{ transform: rotate(10deg); }}
  }}
  .octo-arm {{ transform-origin: 130px 106px; }}
  @media (max-width: 500px) {{
    .github-corner:hover .octo-arm {{ animation: none; }}
    .github-corner .octo-arm {{ animation: octocat-wave 560ms ease-in-out; }}
    .github-corner svg {{ width: 60px; height: 60px; }}
  }}
</style>
"""
EXP_IMAGE_DIR = Path("assets/images/exp")
READING_CHARS_PER_MINUTE = 520
TRIM_IMAGE_SUFFIXES = {".webp"}
WEBP_QUALITY = 85
TRIM_DIFF_THRESHOLD = 12
TRIM_PADDING = 12
TRIM_MIN_MARGIN = 8

EXCLUDED_PARTS = {".git", ".venv", "sources", "site"}
LINK_RE = re.compile(r"(!?)\[([^\]]+)\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
MATH_PATTERNS = [
    re.compile(r"\$\$(.+?)\$\$", re.DOTALL),
    re.compile(r"\\\[(.+?)\\\]", re.DOTALL),
    re.compile(r"\\\((.+?)\\\)", re.DOTALL),
    re.compile(r"(?<!\\)\$(?!\$)([^\n$]+?)(?<!\\)\$"),
]

HOME_MAINLINE = "波沿结构传播 → 不连续反射 → 边界筛模 → 端口网络与测量"
HOME_SEARCH_EXTRA = (
    "十轮读法 十分钟定位法 四格纸面 第一次打开 只做这三步 "
    "按当前任务进入 考前扫盲区 传播 反射 边界 端口 测量"
)
KNOWLEDGE_STAGES: tuple[tuple[str, str, str], ...] = (
    ("01-传播与传输线", "01 · 传播与传输线", "长线、行波、反射与开短路线"),
    ("02-反射与匹配", "02 · 反射与匹配", "Smith 圆图与阻抗匹配"),
    ("03-波导中的场与边界", "03 · 波导中的场与边界", "TEM/TE/TM 与金属边界"),
    ("04-截止色散与速度", "04 · 截止、色散与速度", "三种波长与相群速"),
    ("05-矩形波导工程计算", "05 · 矩形波导工程计算", "模谱、单模区与工程算例"),
    ("06-圆波导同轴线微带线", "06 · 圆/同轴/微带", "圆波导、同轴线与微带"),
    ("07-实验测量与微波元件", "07 · 实验测量与元件", "S 参数、VNA 与常用元件"),
    ("08-谐振器网络与课程综合", "08 · 谐振器/网络/综合", "谐振腔、网络与测量综合"),
)
HOMEWORK_CARDS: tuple[tuple[str, str, str], ...] = (
    ("第一次作业", "Lec01–Lec05 · 传输线基础", "content/solutions/01-传输线基础/README.md"),
    ("第二次作业", "Lec06–Lec09 · 圆图与匹配", "content/solutions/02-圆图与匹配/README.md"),
    ("第三次作业", "Lec10–Lec16 · 规则波导", "content/solutions/03-规则波导与矩形波导/README.md"),
    ("第四次作业", "Lec17–Lec20 · 圆波导/同轴/微带", "content/solutions/04-后续专题/README.md"),
    ("第五次作业", "Lec22–Lec28 · 谐振器/网络/测量", "content/solutions/05-谐振器网络元件与测量综合/README.md"),
)
EXPERIMENT_CARDS: tuple[tuple[str, str, str], ...] = (
    ("实验一", "矢网与传输线测量", "content/experiments/01-矢网与传输线/README.md"),
    ("实验二", "谐振器、耦合器与功分器", "content/experiments/02-元件参数测量/README.md"),
)
GUIDE_CARDS: tuple[tuple[str, str, str], ...] = (
    ("零基础手册", "第一次打开该看哪一章", "content/guide/beginner-handbook.md"),
    ("详细导读", "十轮读法与任务入口表", "content/guide/reading-map.md"),
    ("讲次矩阵", "考前按讲次查漏", "content/appendices/讲次-作业-教材章节-知识点矩阵.md"),
)
HOME_STRATEGY_BULLETS: tuple[str, ...] = (
    "顶部搜索框输入 TE10、Smith、S11、λ/4 等符号或题号，30 秒内定位到页。",
    "做题先在纸上画四格：题型、前提、公式、检查，再代数值。",
    "零基础第一轮：扫主线 → 补三张图像 → 做一道题的完整闭环。",
    "精读页先看「零基础读前翻译」，题解页先看「对应知识点」。",
    "临考前用讲次矩阵反查还没掌握的题型，不要只背公式表。",
)


class PageKind(str, Enum):
    HOME = "home"
    HUB = "hub"
    ARTICLE = "article"
    SOLUTION = "solution"


@dataclass(frozen=True)
class Page:
    source: Path
    output: Path
    title: str
    group: str

    @property
    def rel_source(self) -> Path:
        return self.source.relative_to(ROOT)

    @property
    def rel_output(self) -> Path:
        return self.output.relative_to(SITE_DIR)


def is_markdown_source(path: Path) -> bool:
    if path.suffix.lower() != ".md":
        return False
    return not any(part in EXCLUDED_PARTS for part in path.relative_to(ROOT).parts)


def output_path_for(source: Path) -> Path:
    rel = source.relative_to(ROOT)
    if rel == Path("content/index.md"):
        return SITE_DIR / "index.html"
    if source.name.lower() in {"readme.md", "index.md"}:
        return SITE_DIR / rel.parent / "index.html"
    return SITE_DIR / rel.with_suffix(".html")


def strip_inline_markdown(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()


def title_for(source: Path) -> str:
    text = source.read_text(encoding="utf-8")
    match = HEADING_RE.search(text)
    if match:
        return strip_inline_markdown(match.group(1))
    if source.name.lower() == "readme.md":
        return source.parent.name or SITE_TITLE
    return source.stem


def group_for(source: Path) -> str:
    rel = source.relative_to(ROOT)
    if rel == Path("content/index.md"):
        return "首页"
    if rel.parts[:2] == ("content", "knowledge"):
        return "知识点讲义"
    if rel.parts[:2] == ("content", "solutions"):
        return "作业解答"
    if rel.parts[:2] == ("content", "experiments"):
        return "实验环节"
    if rel.parts[:2] == ("content", "guide"):
        return "学习指南"
    if rel.parts[:2] == ("content", "appendices"):
        return "附录"
    return "其他"


def natural_key(text: str) -> tuple[tuple[int, int | str], ...]:
    chunks = re.split(r"(\d+)", text)
    return tuple((1, int(chunk)) if chunk.isdigit() else (0, chunk) for chunk in chunks)


def section_order(rel: Path) -> tuple[int, int, tuple[tuple[int, int | str], ...]]:
    if rel == Path("content/index.md"):
        return (0, 0, ())

    if rel.parts[:2] == ("content", "knowledge"):
        stages = {
            "README.md": 0,
            "01-传播与传输线": 1,
            "02-反射与匹配": 2,
            "03-波导中的场与边界": 3,
            "04-截止色散与速度": 4,
            "05-矩形波导工程计算": 5,
            "06-圆波导同轴线微带线": 6,
            "07-实验测量与微波元件": 7,
            "08-谐振器网络与课程综合": 8,
        }
        stage = rel.parts[2] if len(rel.parts) > 2 else rel.name
        return (stages.get(stage, 99), 0, natural_key(rel.as_posix()))

    if rel.parts[:2] == ("content", "solutions"):
        homework = rel.parts[2] if len(rel.parts) > 2 else rel.name
        homework_order = {
            "index.md": 0,
            "01-传输线基础": 1,
            "02-圆图与匹配": 2,
            "03-规则波导与矩形波导": 3,
            "04-后续专题": 4,
            "05-谐振器网络元件与测量综合": 5,
        }.get(homework, 99)
        name = rel.name
        local_order = 5
        if name == "index.md" or "标准解答" in name:
            local_order = 0
        elif "00-符号" in name:
            local_order = 1
        elif len(rel.parts) > 3 and rel.parts[-2].startswith("Lec"):
            local_order = 2
        elif "附录" in name:
            local_order = 9
        return (homework_order, local_order, natural_key(rel.as_posix()))

    return (99, 0, natural_key(rel.as_posix()))


def page_sort_key(page: Page) -> tuple[int, tuple[int, int, tuple[tuple[int, int | str], ...]]]:
    order = {
        "首页": 0,
        "学习指南": 1,
        "知识点讲义": 2,
        "作业解答": 3,
        "实验环节": 4,
        "附录": 5,
        "其他": 9,
    }
    return (order.get(page.group, 9), section_order(page.rel_source))


def collect_pages() -> list[Page]:
    sources: list[Path] = []
    for public_root in PUBLIC_ROOTS:
        source = ROOT / public_root
        if source.is_dir():
            sources.extend(source.rglob("*.md"))
        else:
            sources.append(source)
    seen: set[Path] = set()
    pages: list[Page] = []
    for source in sources:
        source = source.resolve()
        if source in seen or not source.exists() or not is_markdown_source(source):
            continue
        seen.add(source)
        pages.append(
            Page(
                source=source,
                output=output_path_for(source),
                title=title_for(source),
                group=group_for(source),
            )
        )
    return sorted(pages, key=page_sort_key)


def path_to_page(pages: list[Page]) -> dict[Path, Page]:
    return {page.source.resolve(): page for page in pages}


def relative_url(from_output: Path, to_output: Path) -> str:
    rel = os.path.relpath(to_output, from_output.parent)
    return Path(rel).as_posix()


def root_prefix(page: Page) -> str:
    rel = os.path.relpath(SITE_DIR, page.output.parent)
    if rel == ".":
        return ""
    return Path(rel).as_posix().rstrip("/") + "/"


def resolve_directory_target(path: Path) -> Path | None:
    for name in ("README.md", "index.md"):
        candidate = path / name
        if candidate.exists():
            return candidate.resolve()
    md_files = sorted(path.glob("*.md"), key=lambda p: ("标准解答" not in p.name, p.name))
    if md_files:
        return md_files[0].resolve()
    return None


def rewrite_markdown_links(text: str, source: Path, page: Page, pages_by_source: dict[Path, Page]) -> str:
    def repl(match: re.Match[str]) -> str:
        bang, label, raw_target = match.groups()
        target = raw_target.strip()
        if not target or target.startswith(("#", "http://", "https://", "mailto:", "tel:")):
            return match.group(0)

        title = ""
        if " " in target and not target.startswith("<"):
            maybe_target, maybe_title = target.split(" ", 1)
            if maybe_title.startswith(("\"", "'")):
                target, title = maybe_target, " " + maybe_title

        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]

        link_path, sep, fragment = target.partition("#")
        normalized = unquote(link_path.replace("\\", "/"))
        candidate = (source.parent / normalized).resolve()

        mapped_source: Path | None = None
        if candidate.is_dir():
            mapped_source = resolve_directory_target(candidate)
        elif candidate.suffix.lower() == ".md" and candidate.exists():
            mapped_source = candidate

        if mapped_source and mapped_source in pages_by_source:
            target_page = pages_by_source[mapped_source]
            new_target = relative_url(page.output, target_page.output)
            if sep:
                new_target += "#" + fragment
            return f"{bang}[{label}]({new_target}{title})"

        return match.group(0)

    return LINK_RE.sub(repl, text)


def protect_math(text: str) -> tuple[str, dict[str, str]]:
    replacements: dict[str, str] = {}

    def store(match: re.Match[str]) -> str:
        token = f"@@MATH{len(replacements)}@@"
        replacements[token] = match.group(0)
        return token

    for pattern in MATH_PATTERNS:
        text = pattern.sub(store, text)
    return text, replacements


def restore_math(rendered: str, replacements: dict[str, str]) -> str:
    for token, formula in replacements.items():
        rendered = rendered.replace(token, html.escape(formula, quote=False))
    return rendered


def render_markdown(text: str) -> tuple[str, str]:
    protected, math_tokens = protect_math(text)
    md = markdown.Markdown(
        extensions=[
            "markdown.extensions.extra",
            "markdown.extensions.toc",
            "markdown.extensions.sane_lists",
        ],
        extension_configs={
            "markdown.extensions.toc": {
                "permalink": "§",
                "toc_depth": "2-3",
            }
        },
        output_format="html5",
    )
    html_body = md.convert(protected)
    return restore_math(html_body, math_tokens), restore_math(md.toc, math_tokens)


def enhance_html_body(body: str) -> str:
    return re.sub(
        r"<img(?![^>]*\bloading=)([^>]*)>",
        r'<img loading="lazy" decoding="async"\1>',
        body,
    )


FORMULA_APPENDIX_NAME = "99-公式与图像.md"
SELF_CHECK_NAME = "99-自检清单与常见误区.md"
FORMULA_HINT_MAX_LEN = 140
DISPLAY_MATH_RE = re.compile(r"\$\$(.+?)\$\$|\\\[(.+?)\\\]", re.DOTALL)
FORMULA_IMAGE_SECTION_RE = re.compile(
    r"^#{2,3}\s+.*(?:图像|配图|原书图|跨链|学习建议)",
    re.MULTILINE,
)
BOLD_LINE_RE = re.compile(r"^\*\*[^*\n]+?\*\*[^\n]*\s*$", re.MULTILINE)
HEADING_LINE_RE = re.compile(r"^#{2,3}\s+", re.MULTILINE)
H2_LINE_RE = re.compile(r"^##\s+", re.MULTILINE)


@dataclass(frozen=True)
class FormulaCard:
    title: str
    hint: str
    math_markdown: str


def extract_display_math_blocks(text: str) -> list[str]:
    blocks: list[str] = []
    for pattern in MATH_PATTERNS[:2]:
        blocks.extend(match.group(0) for match in pattern.finditer(text))
    return blocks


def formula_card_hint(text_before_math: str) -> str:
    lines = [
        line.strip()
        for line in text_before_math.strip().splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    if not lines:
        return ""
    hint = strip_inline_markdown("\n".join(lines[-3:]))
    if len(hint) > FORMULA_HINT_MAX_LEN:
        return hint[: FORMULA_HINT_MAX_LEN - 1].rstrip() + "…"
    return hint


def title_from_chunk_prefix(chunk: str, fallback: str) -> str:
    bold_matches = list(BOLD_LINE_RE.finditer(chunk))
    if bold_matches:
        return strip_inline_markdown(bold_matches[-1].group(0))
    for line in chunk.strip().splitlines():
        cleaned = strip_inline_markdown(line.strip())
        if cleaned and not cleaned.startswith("|"):
            return cleaned[:60]
    return fallback


def chunk_to_formula_card(title: str, chunk: str) -> FormulaCard | None:
    math_blocks = extract_display_math_blocks(chunk)
    if not math_blocks:
        return None
    first_math = DISPLAY_MATH_RE.search(chunk)
    hint = formula_card_hint(chunk[: first_math.start()]) if first_math else ""
    cleaned_title = strip_inline_markdown(title.strip()) or "公式"
    return FormulaCard(
        title=cleaned_title,
        hint=hint,
        math_markdown="\n\n".join(math_blocks),
    )


def split_region_into_formula_cards(region_title: str, body: str) -> list[FormulaCard]:
    cards: list[FormulaCard] = []
    sub_matches = list(re.finditer(r"^###\s+(.+?)\s*$", body, re.MULTILINE))
    if sub_matches:
        for index, match in enumerate(sub_matches):
            title = match.group(1).strip()
            start = match.end()
            end = sub_matches[index + 1].start() if index + 1 < len(sub_matches) else len(body)
            card = chunk_to_formula_card(title, body[start:end])
            if card:
                cards.append(card)
        if cards:
            return cards

    bold_matches = list(BOLD_LINE_RE.finditer(body))
    if bold_matches:
        for index, match in enumerate(bold_matches):
            title = strip_inline_markdown(match.group(0))
            start = match.end()
            end = bold_matches[index + 1].start() if index + 1 < len(bold_matches) else len(body)
            card = chunk_to_formula_card(title, body[start:end])
            if card:
                cards.append(card)
        if len(cards) >= 2:
            return cards
        cards = []

    math_matches = list(DISPLAY_MATH_RE.finditer(body))
    if not math_matches:
        card = chunk_to_formula_card(region_title, body)
        return [card] if card else []

    prev_end = 0
    for index, match in enumerate(math_matches):
        prefix = body[prev_end : match.start()]
        title = title_from_chunk_prefix(
            prefix,
            region_title if index == 0 else f"{region_title} {index + 1}",
        )
        card = chunk_to_formula_card(title, prefix + match.group(0))
        if card:
            cards.append(card)
        prev_end = match.end()
    return cards


def extract_formula_regions_appendix(text: str) -> list[tuple[str, str]]:
    regions: list[tuple[str, str]] = []

    speed_section = re.search(r"^###\s+([^\n]*公式速查[^\n]*)\s*$", text, re.MULTILINE)
    if speed_section:
        start = speed_section.end()
        end_match = FORMULA_IMAGE_SECTION_RE.search(text, start)
        end = end_match.start() if end_match else len(text)
        regions.append((speed_section.group(1).strip(), text[start:end]))
        return regions

    if re.search(r"^##\s+[^\n]*公式卡", text, re.MULTILINE):
        for match in re.finditer(r"^##\s+([^\n]*公式卡[^\n]*)\s*$", text, re.MULTILINE):
            start = match.end()
            next_heading = H2_LINE_RE.search(text, start)
            end = start + next_heading.start() if next_heading else len(text)
            body = text[start:end]
            if extract_display_math_blocks(body):
                regions.append((match.group(1).strip(), body))
        return regions

    for match in re.finditer(r"^###\s+([^\n]+)\s*$", text, re.MULTILINE):
        title = match.group(1).strip()
        if any(keyword in title for keyword in ("图像", "学习建议", "导航")):
            continue
        if not any(keyword in title for keyword in ("公式", "关系")):
            continue
        start = match.end()
        next_heading = HEADING_LINE_RE.search(text, start)
        end = next_heading.start() if next_heading else len(text)
        body = text[start:end]
        if extract_display_math_blocks(body):
            regions.append((title, body))

    return regions


def extract_formula_cards_appendix(text: str) -> list[FormulaCard]:
    cards: list[FormulaCard] = []
    for region_title, body in extract_formula_regions_appendix(text):
        cards.extend(split_region_into_formula_cards(region_title, body))
    return cards


def extract_formula_cards_self_check(text: str) -> list[FormulaCard]:
    cards: list[FormulaCard] = []

    required_section = re.search(r"^##\s+2\.\s*必背公式\s*$", text, re.MULTILINE)
    if required_section:
        start = required_section.end()
        next_heading = H2_LINE_RE.search(text, start)
        section_body = text[start : start + next_heading.start()] if next_heading else text[start:]
        cards.extend(split_region_into_formula_cards("必背公式", section_body))

    for match in re.finditer(r"^###\s+必背公式\s*$", text, re.MULTILINE):
        start = match.end()
        next_heading = HEADING_LINE_RE.search(text, start)
        chunk = text[start : start + next_heading.start()] if next_heading else text[start:]
        parent = ""
        parent_match = None
        for parent_match in re.finditer(r"^##\s+(.+?)\s*$", text[: match.start()], re.MULTILINE):
            pass
        if parent_match:
            parent = strip_inline_markdown(parent_match.group(1))
        title = f"{parent} · 必背公式" if parent else "必背公式"
        card = chunk_to_formula_card(title, chunk)
        if card:
            cards.append(card)

    return cards


def extract_formula_cards(source: Path, raw: str) -> list[FormulaCard]:
    name = source.name
    if name == FORMULA_APPENDIX_NAME:
        return extract_formula_cards_appendix(raw)
    if name == SELF_CHECK_NAME:
        return extract_formula_cards_self_check(raw)
    return []


def render_formula_cards_html(cards: list[FormulaCard]) -> str:
    parts: list[str] = []
    for index, card in enumerate(cards, start=1):
        md_parts = [f"### {card.title}"]
        if card.hint:
            md_parts.append(card.hint)
        md_parts.append(card.math_markdown)
        card_html, _ = render_markdown("\n\n".join(md_parts))
        parts.append(f'<section class="formula-card" id="formula-card-{index}">{card_html}</section>')
    return "\n".join(parts)


def render_formula_quick_view(body: str, cards: list[FormulaCard]) -> str:
    if len(cards) < 2:
        return body
    grid_html = render_formula_cards_html(cards)
    return (
        '<div class="formula-quick-toolbar">'
        '<button type="button" class="formula-quick-toggle" data-formula-quick-toggle '
        'aria-pressed="false" aria-controls="formula-quick-grid">公式速查</button>'
        "</div>"
        f'<div class="formula-quick-grid" id="formula-quick-grid" hidden aria-hidden="true" '
        f'data-math-pending role="region" aria-label="公式速查">{grid_html}</div>'
        f'<div class="article-body">{body}</div>'
    )


def plain_text(source: Path, limit: int | None = None) -> str:
    text = source.read_text(encoding="utf-8")
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\[[^\]]+\]\([^)]+\)", " ", text)
    text = re.sub(r"[#>*_`|\\-]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit] if limit else text


def reading_minutes(source: Path) -> int:
    text = plain_text(source)
    if not text:
        return 1
    return max(1, round(len(text) / READING_CHARS_PER_MINUTE))


def page_number_text(page: Page, pages: list[Page]) -> str:
    return f"{pages.index(page) + 1} / {len(pages)}"


def page_meta(page: Page, pages: list[Page]) -> str:
    return "\n".join(
        [
            '<div class="page-meta" aria-label="页面信息">',
            f'<span>{html.escape(page.group)}</span>',
            f'<span>约 {reading_minutes(page.source)} 分钟</span>',
            f'<span>第 {page_number_text(page, pages)} 页</span>',
            f'<span>{html.escape(display_path(page))}</span>',
            "</div>",
        ]
    )


NavNode = dict[str, object]

_NAV_CONFIG: dict[str, dict[str, str]] | None = None


def nav_config() -> dict[str, dict[str, str]]:
    global _NAV_CONFIG
    if _NAV_CONFIG is None:
        if NAV_CONFIG_PATH.exists():
            loaded = json.loads(NAV_CONFIG_PATH.read_text(encoding="utf-8"))
            _NAV_CONFIG = {
                "directories": loaded.get("directories", {}),
                "pages": loaded.get("pages", {}),
                "filenames": loaded.get("filenames", {}),
            }
        else:
            _NAV_CONFIG = {"directories": {}, "pages": {}, "filenames": {}}
    return _NAV_CONFIG


def directory_nav_label(name: str) -> str:
    return nav_config()["directories"].get(name, name)


def compact_nav_label(page: Page) -> str:
    rel = page.rel_source
    title = page.title
    pages = nav_config()["pages"]

    if rel.as_posix() in pages:
        return pages[rel.as_posix()]

    name = rel.name
    filename_labels = nav_config()["filenames"]
    if name in filename_labels:
        return filename_labels[name]
    if name.lower() == "readme.md":
        return "总览"
    if "标准解答" in name:
        return "总览"
    if "00-符号" in name:
        return "符号导读"
    if "附录" in name:
        return "公式图像"
    if name.startswith("99-"):
        return "自检与误区" if "自检" in name else "公式图像"

    question = re.search(r"第\s*(\d+)\s*题", title)
    if question:
        suffix = "（选做）" if "选做" in title else ""
        return f"第{question.group(1)}题{suffix}"

    label = title
    label = re.sub(r"^《微波技术基础》[· ]*", "", label)
    label = re.sub(r"^第[一二三四五]次作业\s*[·:：]\s*", "", label)
    label = re.sub(r"^Lec\d+(?:[-～–]Lec?\d+)?\s*[·:：]\s*", "", label)
    label = label.replace("（初学者版）", "")
    label = label.replace("术语与路线图", "路线图")
    return label.strip()


def nav_segments(page: Page) -> list[str]:
    rel = page.rel_source
    if rel == Path("content/index.md"):
        return ["首页"]
    if rel.parts[:2] == ("content", "guide"):
        return [compact_nav_label(page)]
    if rel.parts[:2] == ("content", "appendices"):
        return [compact_nav_label(page)]
    if rel.parts[:2] == ("content", "knowledge"):
        if rel == Path("content/knowledge/README.md"):
            return ["知识点总览"]
        if len(rel.parts) >= 3:
            if rel.name.lower() == "readme.md":
                return [directory_nav_label(rel.parts[2])]
            return [directory_nav_label(rel.parts[2]), compact_nav_label(page)]
    if rel.parts[:2] == ("content", "solutions"):
        if rel == Path("content/solutions/index.md"):
            return ["作业总览"]
        if len(rel.parts) >= 3:
            segments = [directory_nav_label(rel.parts[2])]
            if len(rel.parts) >= 5:
                segments.append(directory_nav_label(rel.parts[3]))
            if rel.name.lower() == "readme.md":
                return segments
            segments.append(compact_nav_label(page))
            return segments
    if rel.parts[:2] == ("content", "experiments"):
        if rel == Path("content/experiments/index.md"):
            return ["实验总览"]
        if len(rel.parts) >= 3:
            # Top-level experiment files (00-符号与导读.md, 99-公式与图像.md) live directly under experiments/
            if len(rel.parts) == 3:
                return [compact_nav_label(page)]
            segments = [directory_nav_label(rel.parts[2])]
            if rel.name.lower() == "readme.md":
                return segments
            segments.append(compact_nav_label(page))
            return segments
    return [compact_nav_label(page)]


def add_nav_node(tree: dict[str, NavNode], segments: list[str], page: Page) -> None:
    current = tree
    for segment in segments:
        node = current.setdefault(segment, {"page": None, "children": {}})
        current = node["children"]  # type: ignore[assignment]
    node["page"] = page


def node_contains_page(node: NavNode, page: Page) -> bool:
    if node.get("page") == page:
        return True
    children = node.get("children", {})
    return any(node_contains_page(child, page) for child in children.values())  # type: ignore[union-attr]


def render_nav_nodes(
    nodes: dict[str, NavNode],
    current_page: Page,
    from_page: Page,
    depth: int = 0,
) -> str:
    chunks: list[str] = ['<ol class="nav-list">']
    for label, node in nodes.items():
        children = node.get("children", {})
        linked_page = node.get("page")
        active = node_contains_page(node, current_page)
        if children:
            open_attr = " open" if active or depth == 0 else ""
            chunks.append(f'<li><details class="nav-subgroup depth-{depth}"{open_attr}>')
            summary_label = html.escape(label)
            if isinstance(linked_page, Page):
                href = relative_url(from_page.output, linked_page.output)
                current = " active" if linked_page == current_page else ""
                chunks.append(
                    f'<summary><a class="nav-summary-link{current}" href="{href}">{summary_label}</a></summary>'
                )
            else:
                chunks.append(f"<summary>{summary_label}</summary>")
            chunks.append(render_nav_nodes(children, current_page, from_page, depth + 1))
            chunks.append("</details></li>")
        elif isinstance(linked_page, Page):
            item_active = " active" if linked_page == current_page else ""
            href = relative_url(from_page.output, linked_page.output)
            path_hint = html.escape(display_path(linked_page))
            chunks.append(
                f'<li class="nav-item{item_active}"><a href="{href}" title="{path_hint}">{html.escape(label)}</a></li>'
            )
    chunks.append("</ol>")
    return "\n".join(chunks)


def render_nav(page: Page, pages: list[Page]) -> str:
    groups: dict[str, list[Page]] = {}
    for item in pages:
        groups.setdefault(item.group, []).append(item)

    chunks: list[str] = []
    for group, items in groups.items():
        if group == "首页" and len(items) == 1:
            item = items[0]
            active = " active" if item.source == page.source else ""
            chunks.append(
                f'<a class="nav-root-link{active}" href="{relative_url(page.output, item.output)}">首页</a>'
            )
            continue
        open_attr = " open" if group == page.group else ""
        chunks.append(f'<details class="nav-group"{open_attr}>')
        chunks.append(f"<summary>{html.escape(group)}</summary>")
        tree: dict[str, NavNode] = {}
        for item in items:
            add_nav_node(tree, nav_segments(item), item)
        chunks.append(render_nav_nodes(tree, page, page))
        chunks.append("</details>")
    return "\n".join(chunks)


def display_path(page: Page) -> str:
    rel = page.rel_source
    if rel == Path("content/index.md"):
        return "首页"
    labels = {
        "guide": "学习指南",
        "knowledge": "知识点讲义",
        "solutions": "作业解答",
        "experiments": "实验环节",
        "appendices": "附录",
    }
    parts = list(rel.parts)
    if parts and parts[0] == "content":
        parts = parts[1:]
    visible: list[str] = []
    for part in parts[:-1]:
        visible.append(labels.get(part, part))
    visible.append(page.title)
    return " / ".join(visible)


def breadcrumbs(page: Page) -> str:
    if page.rel_source == Path("content/index.md"):
        return '<span class="crumb-current">首页</span>'
    visible = display_path(page).split(" / ")
    return "\n".join(
        f'<span class="crumb">{html.escape(part)}</span>' for part in visible
    )


def page_footer(page: Page, pages: list[Page]) -> str:
    index = pages.index(page)
    prev_page = pages[index - 1] if index > 0 else None
    next_page = pages[index + 1] if index + 1 < len(pages) else None
    prev_html = (
        f'<a class="pager-link prev" href="{relative_url(page.output, prev_page.output)}">'
        f'<span>上一篇</span><strong>{html.escape(prev_page.title)}</strong></a>'
        if prev_page
        else '<span class="pager-link disabled"></span>'
    )
    next_html = (
        f'<a class="pager-link next" href="{relative_url(page.output, next_page.output)}">'
        f'<span>下一篇</span><strong>{html.escape(next_page.title)}</strong></a>'
        if next_page
        else '<span class="pager-link disabled"></span>'
    )
    return f'<nav class="pager" aria-label="章节导航">{prev_html}{next_html}</nav>'


def brand_tagline(page: Page) -> str:
    rel = page.rel_source.as_posix()
    if rel == "content/index.md" or rel.startswith("content/guide/"):
        return "把看不见的波画出来"
    if "01-传播与传输线" in rel:
        return "长线不是长，是相位开始说话"
    if "02-反射与匹配" in rel:
        if "03-并联支节匹配" in rel:
            return "让反射波悄悄消失"
        return "Smith 圆图是一张反射地图"
    if "03-波导中的场与边界" in rel:
        return "金属管会挑选能通过的波型"
    if "04-截止色散与速度" in rel:
        return "相速能超车，能量不超速"
    if "05-矩形波导工程计算" in rel:
        return "TE10 是矩形波导的主角"
    if rel.startswith("content/solutions/"):
        return "先看物理图像，再算标准答案"
    if rel.startswith("content/appendices/"):
        return "用一张表串起讲次和题目"
    return "微波里的波，会反射，也会被波导筛选"


def page_kind(page: Page) -> PageKind:
    rel = page.rel_source
    if rel == Path("content/index.md"):
        return PageKind.HOME
    if rel.name.lower() in {"readme.md", "index.md"}:
        return PageKind.HUB
    if rel.parts[:2] == ("content", "solutions"):
        return PageKind.SOLUTION
    return PageKind.ARTICLE


def extract_card_intro(source: Path, fallback: str = "", min_chars: int = 40) -> str:
    if not source.exists():
        return fallback
    text = source.read_text(encoding="utf-8")
    paragraphs: list[str] = []
    current: list[str] = []
    in_frontmatter = False
    frontmatter_ready = False

    for line in text.splitlines():
        stripped = line.strip()
        if stripped == "---" and not frontmatter_ready:
            in_frontmatter = not in_frontmatter
            if not in_frontmatter:
                frontmatter_ready = True
            continue
        if in_frontmatter:
            continue
        if stripped.startswith("#"):
            continue
        if stripped.startswith("!["):
            continue
        if stripped.startswith("|"):
            continue
        if stripped.startswith("---"):
            continue
        if not stripped:
            if current:
                paragraphs.append(" ".join(current))
                current = []
            continue
        if stripped.startswith(("-", "*")) and not current:
            continue
        if stripped.startswith(">"):
            current.append(strip_inline_markdown(stripped.lstrip(">").strip()))
            continue
        current.append(strip_inline_markdown(stripped))

    if current:
        paragraphs.append(" ".join(current))

    for paragraph in paragraphs:
        cleaned = re.sub(r"\s+", " ", paragraph).strip()
        if len(cleaned) >= min_chars:
            if len(cleaned) > 200:
                return cleaned[:199] + "…"
            return cleaned
    return fallback


def page_href(from_page: Page, source_rel: str, pages_by_source: dict[Path, Page]) -> str:
    source = (ROOT / source_rel).resolve()
    target = pages_by_source.get(source)
    if target:
        return relative_url(from_page.output, target.output)
    return source_rel


def render_card_grid(
    cards: list[tuple[str, str, str]],
    from_page: Page,
    pages_by_source: dict[Path, Page],
) -> str:
    chunks = ['<div class="home-cards">']
    for title, intro, source_rel in cards:
        href = page_href(from_page, source_rel, pages_by_source)
        chunks.append(
            f'<a class="card-link" href="{html.escape(href, quote=True)}">'
            f"<strong>{html.escape(title)}</strong>"
            f"<span>{html.escape(intro)}</span>"
            "</a>"
        )
    chunks.append("</div>")
    return "\n".join(chunks)


def render_home_body(page: Page, pages_by_source: dict[Path, Page]) -> str:
    stage_cards: list[tuple[str, str, str]] = []
    for directory, label, fallback in KNOWLEDGE_STAGES:
        readme = ROOT / "content" / "knowledge" / directory / "README.md"
        intro = extract_card_intro(readme, fallback=fallback)
        stage_cards.append((label, intro, f"content/knowledge/{directory}/README.md"))

    hero_ctas = [
        ("传播与传输线", page_href(page, "content/knowledge/01-传播与传输线/README.md", pages_by_source)),
        ("作业解答", page_href(page, "content/solutions/index.md", pages_by_source)),
        ("实验环节", page_href(page, "content/experiments/index.md", pages_by_source)),
    ]
    cta_html = "".join(
        f'<a class="home-cta{" home-cta-primary" if index == 0 else ""}" href="{html.escape(href, quote=True)}">'
        f"{html.escape(label)}</a>"
        for index, (label, href) in enumerate(hero_ctas)
    )
    strategy_items = "".join(
        f"<li>{html.escape(item)}</li>" for item in HOME_STRATEGY_BULLETS
    )
    reading_map_href = page_href(page, "content/guide/reading-map.md", pages_by_source)
    matrix_href = page_href(
        page, "content/appendices/讲次-作业-教材章节-知识点矩阵.md", pages_by_source
    )

    return f"""
<div class="home-dashboard">
  <section class="home-hero">
    <p class="home-kicker">华中科技大学 · 电信本科</p>
    <h1>{html.escape(SITE_TITLE)}</h1>
    <p class="home-lead">{html.escape(HOME_MAINLINE)}</p>
    <div class="home-cta-row">{cta_html}</div>
  </section>

  <section class="learning-section">
    <div class="learning-section-head">
      <h2>知识点讲义</h2>
      <a href="{html.escape(page_href(page, "content/knowledge/README.md", pages_by_source), quote=True)}">总览 →</a>
    </div>
    {render_card_grid(stage_cards, page, pages_by_source)}
  </section>

  <section class="learning-section">
    <div class="learning-section-head">
      <h2>作业解答</h2>
      <a href="{html.escape(page_href(page, "content/solutions/index.md", pages_by_source), quote=True)}">目录 →</a>
    </div>
    {render_card_grid(list(HOMEWORK_CARDS), page, pages_by_source)}
  </section>

  <section class="learning-section learning-section-split">
    <div>
      <div class="learning-section-head">
        <h2>实验环节</h2>
        <a href="{html.escape(page_href(page, "content/experiments/index.md", pages_by_source), quote=True)}">总览 →</a>
      </div>
      {render_card_grid(list(EXPERIMENT_CARDS), page, pages_by_source)}
    </div>
    <div>
      <div class="learning-section-head">
        <h2>学习指南</h2>
        <a href="{html.escape(page_href(page, "content/guide/index.md", pages_by_source), quote=True)}">指南 →</a>
      </div>
      {render_card_grid(list(GUIDE_CARDS), page, pages_by_source)}
    </div>
  </section>

  <section class="learning-section home-strategy">
    <div class="learning-section-head">
      <h2>学习策略</h2>
      <a href="{html.escape(reading_map_href, quote=True)}">详细导读 →</a>
    </div>
    <ul class="home-strategy-list">{strategy_items}</ul>
    <p class="home-strategy-foot">
      考前还可打开 <a href="{html.escape(matrix_href, quote=True)}">讲次-作业-知识点矩阵</a> 做最后查漏。
    </p>
  </section>
</div>
"""


def render_sidebar(page: Page, pages: list[Page]) -> str:
    nav = render_nav(page, pages)
    return f"""{nav}
      <p class="sidebar-source-note">本站源代码以 Markdown 编写，由 <a href="{GITHUB_REPO_URL}" target="_blank" rel="noopener">build.py</a> 重新生成。</p>"""


def render_page(
    page: Page,
    pages: list[Page],
    pages_by_source: dict[Path, Page],
    *,
    show_meta: bool = True,
    show_pager: bool = True,
    show_toc: bool = True,
    shell_class: str = "",
    body_override: str | None = None,
    breadcrumbs_override: str | None = None,
    title_override: str | None = None,
) -> str:
    raw = page.source.read_text(encoding="utf-8")
    rewritten = rewrite_markdown_links(raw, page.source, page, pages_by_source)
    body, toc = render_markdown(rewritten)
    body = enhance_html_body(body)
    if body_override is not None:
        body = body_override
    formula_cards = extract_formula_cards(page.source, raw)
    article_content = body
    article_attrs = ""
    if len(formula_cards) >= 2 and body_override is None:
        article_content = render_formula_quick_view(body, formula_cards)
        article_attrs = f' data-formula-cards="{len(formula_cards)}"'
    prefix = root_prefix(page)
    sidebar = render_sidebar(page, pages)
    crumbs = breadcrumbs_override if breadcrumbs_override is not None else breadcrumbs(page)
    footer = page_footer(page, pages) if show_pager else ""
    meta = page_meta(page, pages) if show_meta else ""
    title = html.escape(title_override or page.title)
    site_title = html.escape(SITE_TITLE)
    tagline = html.escape(brand_tagline(page))
    toc_html = toc if toc.strip() else '<p class="toc-empty">本页没有二级目录。</p>'
    toc_panel = ""
    if show_toc:
        toc_panel = f"""    <aside class="toc-panel" aria-label="页内目录">
      <strong>本页</strong>
      {toc_html}
    </aside>"""
    shell_classes = "shell"
    if shell_class:
        shell_classes += f" {shell_class}"
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} · {site_title}</title>
  <link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="{prefix}assets/jx/tokens.css">
  <link rel="stylesheet" href="{prefix}assets/jx/base.css">
  <link rel="stylesheet" href="{prefix}assets/jx/components.css">
  <link rel="stylesheet" href="{prefix}assets/style.css">
  <script>
    window.MathJax = {{
      tex: {{
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
        processEscapes: true
      }},
      options: {{
        skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
      }},
      chtml: {{
        mtextInheritFont: true,
        scale: 1.04
      }}
    }};
    window.SITE_ROOT = "{prefix}";
  </script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <script defer src="{prefix}assets/app.js"></script>
</head>
<body>
  {GITHUB_CORNER_HTML}
  <a class="skip-link" href="#content">跳到正文</a>
  <div class="reading-progress" aria-hidden="true"><span></span></div>
  <header class="topbar">
    <button class="icon-button menu-button" type="button" data-sidebar-toggle aria-label="打开目录">☰</button>
    <a class="brand" href="{prefix}index.html">
      <span class="brand-mark">λg</span>
      <span><strong>{site_title}</strong><small>{tagline}</small></span>
    </a>
    <label class="search-box">
      <span class="search-icon">⌕</span>
      <input id="siteSearch" type="search" placeholder="搜索知识点、题号、公式符号" autocomplete="off">
    </label>
    <a class="jx-return-to-hub" href="https://estelledc.github.io/" rel="home">回 Jason 主站</a>
    <button class="icon-button" type="button" data-theme-toggle aria-label="切换明暗主题">◐</button>
  </header>
  <div id="searchResults" class="search-results" hidden></div>
  <div class="{shell_classes}">
    <aside class="sidebar" data-sidebar>
      <div class="sidebar-head">
        <strong>目录</strong>
        <button class="icon-button" type="button" data-sidebar-close aria-label="关闭目录">×</button>
      </div>
      {sidebar}
    </aside>
    <main id="content" class="content">
      <div class="breadcrumbs">{crumbs}</div>
      {meta}
      <article class="article"{article_attrs}>
        {article_content}
      </article>
      {footer}
    </main>
{toc_panel}
  </div>
  <footer class="jx-footer">
    <div class="jx-footer__colophon">
      <strong>微波技术教材</strong>
      <span lang="en">HUST EIC · MMXXVI</span>
    </div>
    <nav class="jx-footer__index">
      <a href="{prefix}content/guide/">指南</a>
      <a href="{prefix}content/knowledge/">知识点</a>
      <a href="{prefix}content/solutions/">作业解答</a>
      <a href="{GITHUB_REPO_URL}">github</a>
    </nav>
    <time class="jx-footer__stamp" datetime="2026-05-31" lang="en">2026·05·31</time>
  </footer>
</body>
</html>
"""


def render_home_page(page: Page, pages: list[Page], pages_by_source: dict[Path, Page]) -> str:
    return render_page(
        page,
        pages,
        pages_by_source,
        show_meta=False,
        show_pager=False,
        show_toc=False,
        shell_class="layout-home",
        body_override=render_home_body(page, pages_by_source),
        breadcrumbs_override='<span class="crumb-current">课程地图</span>',
        title_override="课程地图",
    )


def render_hub_page(page: Page, pages: list[Page], pages_by_source: dict[Path, Page]) -> str:
    return render_page(
        page,
        pages,
        pages_by_source,
        show_pager=False,
        show_toc=False,
        shell_class="layout-hub",
    )


def copy_static_assets() -> None:
    for static_dir in STATIC_DIRS:
        src = ROOT / static_dir
        if not src.exists():
            continue
        dst = SITE_DIR / static_dir
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, dst, dirs_exist_ok=True)
    shutil.copy2(ROOT / "assets" / "style.css", SITE_DIR / "assets" / "style.css")
    shutil.copy2(ROOT / "assets" / "app.js", SITE_DIR / "assets" / "app.js")
    shutil.copy2(ROOT / "assets" / "favicon.svg", SITE_DIR / "assets" / "favicon.svg")
    jx_src = ROOT / "assets" / "jx"
    if jx_src.exists():
        shutil.copytree(jx_src, SITE_DIR / "assets" / "jx", dirs_exist_ok=True)
    trim_experiment_images()


def trim_uniform_margin(path: Path) -> bool:
    if Image is None or ImageChops is None:
        raise SystemExit(
            "Missing dependency: Pillow. Run `python3 -m pip install -r requirements.txt` first."
        ) from PIL_IMPORT_ERROR

    with Image.open(path) as image:
        rgb = image.convert("RGB")
        width, height = rgb.size
        background = Image.new("RGB", rgb.size, rgb.getpixel((0, 0)))
        diff = ImageChops.difference(rgb, background)
        mask = diff.point(lambda value: 255 if value > TRIM_DIFF_THRESHOLD else 0).convert("L")
        bbox = mask.getbbox()

        if bbox is None:
            return False

        left, top, right, bottom = bbox
        max_margin = max(left, top, width - right, height - bottom)
        if max_margin < TRIM_MIN_MARGIN:
            return False

        crop_box = (
            max(0, left - TRIM_PADDING),
            max(0, top - TRIM_PADDING),
            min(width, right + TRIM_PADDING),
            min(height, bottom + TRIM_PADDING),
        )
        if crop_box == (0, 0, width, height):
            return False

        cropped = image.crop(crop_box)
        cropped.save(path, quality=WEBP_QUALITY, method=6)
        return True


def trim_experiment_images() -> None:
    image_dir = SITE_DIR / EXP_IMAGE_DIR
    if not image_dir.exists():
        return

    trimmed = 0
    for image_path in sorted(image_dir.iterdir(), key=lambda path: natural_key(path.name)):
        if image_path.suffix.lower() not in TRIM_IMAGE_SUFFIXES:
            continue
        try:
            if trim_uniform_margin(image_path):
                trimmed += 1
        except OSError as exc:
            rel_path = image_path.relative_to(ROOT)
            raise SystemExit(f"Could not trim image margins for {rel_path}: {exc}") from exc

    if trimmed:
        print(f"Trimmed margins on {trimmed} experiment images")


def build_search_index(pages: list[Page]) -> None:
    records = []
    for page in pages:
        search_text = plain_text(page.source, 8000)
        if page_kind(page) == PageKind.HOME:
            search_text = f"{search_text} {HOME_SEARCH_EXTRA} {HOME_MAINLINE}"
            for _, label, fallback in KNOWLEDGE_STAGES:
                search_text += f" {label} {fallback}"
            for title, intro, _ in HOMEWORK_CARDS:
                search_text += f" {title} {intro}"
        card_titles = " ".join(card.title for card in extract_formula_cards(page.source, page.source.read_text(encoding="utf-8")))
        if card_titles:
            search_text = f"{search_text} {card_titles}"
        records.append(
            {
                "title": "课程地图" if page_kind(page) == PageKind.HOME else page.title,
                "group": page.group,
                "path": display_path(page),
                "url": page.rel_output.as_posix(),
                "text": plain_text(page.source, 180),
                "search": search_text,
            }
        )
    (SITE_DIR / "search-index.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def write_pages(pages: list[Page]) -> None:
    pages_by_source = path_to_page(pages)
    for page in pages:
        page.output.parent.mkdir(parents=True, exist_ok=True)
        kind = page_kind(page)
        if kind == PageKind.HOME:
            html = render_home_page(page, pages, pages_by_source)
        elif kind == PageKind.HUB:
            html = render_hub_page(page, pages, pages_by_source)
        else:
            html = render_page(page, pages, pages_by_source)
        page.output.write_text(html, encoding="utf-8")


def clean_site() -> None:
    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    (SITE_DIR / ".gitkeep").touch()
    (SITE_DIR / "assets").mkdir(parents=True, exist_ok=True)


def main() -> None:
    pages = collect_pages()
    clean_site()
    copy_static_assets()
    write_pages(pages)
    build_search_index(pages)
    print(f"Built {len(pages)} pages into {SITE_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
