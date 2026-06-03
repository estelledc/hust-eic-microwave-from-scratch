#!/usr/bin/env python3
"""Build the microwave review Markdown sources into a static web book."""

from __future__ import annotations

import html
import json
import os
import re
import shutil
from dataclasses import dataclass
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


def directory_nav_label(name: str) -> str:
    labels = {
        "01-传播与传输线": "01 · 传播与传输线",
        "02-反射与匹配": "02 · 反射与匹配",
        "03-波导中的场与边界": "03 · 波导中的场与边界",
        "04-截止色散与速度": "04 · 截止、色散与速度",
        "05-矩形波导工程计算": "05 · 矩形波导工程计算",
        "06-圆波导同轴线微带线": "06 · 圆/同轴/微带",
        "07-实验测量与微波元件": "07 · 实验测量与元件",
        "08-谐振器网络与课程综合": "08 · 谐振器/网络/综合",
        "01-传输线基础": "01 · 传输线作业",
        "02-圆图与匹配": "02 · 圆图匹配作业",
        "03-规则波导与矩形波导": "03 · 波导作业",
        "04-后续专题": "04 · 后续专题",
        "05-谐振器网络元件与测量综合": "05 · 谐振器网络综合",
        "01-矢网与传输线": "实验一 · 矢网与传输线",
        "02-元件参数测量": "实验二 · 元件参数测量",
        "03-Lec08-09": "Lec08-09",
        "03-Lec13-16": "Lec13-16",
        "01-Lec22-23-微波谐振器": "Lec22-23 · 谐振器",
        "02-Lec24-微波网络基础": "Lec24 · 网络基础",
        "03-Lec25-26-常用微波元件": "Lec25-26 · 常用元件",
        "04-Lec27-28-微波测量综合": "Lec27-28 · 测量综合",
    }
    return labels.get(name, name)


def compact_nav_label(page: Page) -> str:
    rel = page.rel_source
    title = page.title

    exact = {
        Path("content/knowledge/README.md"): "知识点总览",
        Path("content/solutions/index.md"): "作业总览",
        Path("content/experiments/index.md"): "实验总览",
        Path("content/appendices/讲次-作业-教材章节-知识点矩阵.md"): "讲次知识矩阵",
    }
    if rel in exact:
        return exact[rel]

    name = rel.name
    filename_labels = {
        "01-长线短线与分布参数.md": "长线/短线",
        "02-行波相位常数与特性阻抗.md": "行波与特性阻抗",
        "03-反射驻波与输入阻抗.md": "反射与驻波",
        "04-行波纯驻波与行驻波.md": "三种工作状态",
        "05-开短路线周期性与测量.md": "开短路与周期性",
        "01-多段线并联与四分之一波长.md": "多段线与 λ/4",
        "02-Smith圆图怎么读.md": "Smith 圆图",
        "03-并联支节匹配.md": "并联支节匹配",
        "00-从传输线到波导.md": "从传输线到波导",
        "01-TEM-TE-TM波型.md": "TEM / TE / TM",
        "02-纵向分量与分离变量.md": "纵向场与分离变量",
        "03-金属边界与截止.md": "边界与截止",
        "04-从纵向场到全场.md": "纵向场到全场",
        "00-从截止到色散.md": "从截止到色散",
        "01-三种波长.md": "三种波长",
        "02-色散相速与群速.md": "相速与群速",
        "03-波导色散与材料色散.md": "结构色散 vs 材料色散",
        "04-为什么空心波导没有TEM.md": "空心波导无 TEM",
        "00-工程计算路线图.md": "工程路线",
        "01-模谱主模与简并.md": "模谱与主模",
        "02-单模工作区与介质填充.md": "单模工作区",
        "03-导波波长相速群速算例.md": "λg 与速度算例",
        "04-可传输模判定与枚举.md": "可传输模枚举",
        "05-波导段反射驻波与匹配.md": "波导段匹配",
        "01-Lec01.md": "Lec01 · 长短线",
        "02-Lec02.md": "Lec02 · 行波",
        "03-Lec03.md": "Lec03 · 反射驻波",
        "04-Lec04.md": "Lec04 · 工作状态",
        "05-Lec05.md": "Lec05 · 开短路",
        "01-Lec06.md": "Lec06 · 多段线",
        "02-Lec07.md": "Lec07 · Smith 图",
        "01-Lec10-11.md": "Lec10-11 · 波型方程",
        "02-Lec11-12.md": "Lec11-12 · 波长色散",
        "01-S参数与矢量网络分析仪.md": "S 参数与 VNA",
        "02-微带线工作状态再认识.md": "微带线工作状态",
        "03-谐振器Q值与功率传输法.md": "谐振器 Q 值",
        "04-定向耦合器与功率分配器.md": "耦合器与功分器",
        "01-微波谐振器与谐振腔.md": "谐振器与谐振腔",
        "02-微波网络基础与S参数.md": "网络基础与 S 参数",
        "03-常用微波元件网络化描述.md": "常用元件",
        "04-微波测量与课程综合.md": "测量与综合",
        "01-AV36580面板速查.md": "AV36580 面板",
        "02-RF带通滤波器S参数.md": "滤波器 S 参数",
        "03-微带线开短匹配测量.md": "微带线开/短/匹配",
        "04-思考题与报告.md": "思考题与报告",
        "01-谐振器Q值扫频测量.md": "Q 值扫频",
        "02-定向耦合器特性.md": "耦合器特性",
        "03-功率分配器测量.md": "功分器测量",
    }
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


def render_page(page: Page, pages: list[Page], pages_by_source: dict[Path, Page]) -> str:
    raw = page.source.read_text(encoding="utf-8")
    rewritten = rewrite_markdown_links(raw, page.source, page, pages_by_source)
    body, toc = render_markdown(rewritten)
    body = enhance_html_body(body)
    prefix = root_prefix(page)
    nav = render_nav(page, pages)
    crumbs = breadcrumbs(page)
    footer = page_footer(page, pages)
    meta = page_meta(page, pages)
    title = html.escape(page.title)
    site_title = html.escape(SITE_TITLE)
    tagline = html.escape(brand_tagline(page))
    toc_html = toc if toc.strip() else '<p class="toc-empty">本页没有二级目录。</p>'
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
  <div class="shell">
    <aside class="sidebar" data-sidebar>
      <div class="sidebar-head">
        <strong>目录</strong>
        <button class="icon-button" type="button" data-sidebar-close aria-label="关闭目录">×</button>
      </div>
      {nav}
    </aside>
    <main id="content" class="content">
      <div class="breadcrumbs">{crumbs}</div>
      {meta}
      <article class="article">
        {body}
      </article>
      {footer}
    </main>
    <aside class="toc-panel" aria-label="页内目录">
      <strong>本页</strong>
      {toc_html}
    </aside>
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
      <a href="https://github.com/estelledc/hust-eic-microwave-from-scratch">github</a>
    </nav>
    <time class="jx-footer__stamp" datetime="2026-05-31" lang="en">2026·05·31</time>
  </footer>
</body>
</html>
"""


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
    records = [
        {
            "title": page.title,
            "group": page.group,
            "path": display_path(page),
            "url": page.rel_output.as_posix(),
            "text": plain_text(page.source, 180),
            "search": plain_text(page.source, 8000),
        }
        for page in pages
    ]
    (SITE_DIR / "search-index.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def write_pages(pages: list[Page]) -> None:
    pages_by_source = path_to_page(pages)
    for page in pages:
        page.output.parent.mkdir(parents=True, exist_ok=True)
        page.output.write_text(render_page(page, pages, pages_by_source), encoding="utf-8")


def clean_site() -> None:
    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
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
