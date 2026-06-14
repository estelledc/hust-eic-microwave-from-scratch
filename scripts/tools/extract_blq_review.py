"""Extract page index from BLQ exam-review PDF (local-only source).

Outputs:
- docs/audit/blq_review_extraction_index.json
- docs/audit/BLQ_REVIEW_INTEGRATION.md
- assets/course/blq-review-p{NN}-preview.webp (key sparse pages)

Sparse / image-heavy pages can be read without Tesseract:
- ``--export-all-sparse`` renders every sparse page for vision review (Cursor chat).
- ``--vision-file PATH`` merges hand-written or vision-model transcripts into the index.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path

import fitz
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[2]
PDF_PATH = ROOT / "sources" / "微波技术基础考前串讲_blq.pdf"
JSON_OUT = ROOT / "docs" / "audit" / "blq_review_extraction_index.json"
MD_OUT = ROOT / "docs" / "audit" / "BLQ_REVIEW_INTEGRATION.md"
VISION_DEFAULT = ROOT / "docs" / "audit" / "blq_review_vision_transcripts.json"
PREVIEW_DIR = ROOT / "assets" / "course"

SPARSE_THRESHOLD = 50
PREVIEW_PAGES = frozenset(
    {
        15,
        21,
        24,
        32,
        41,
        43,
        50,
        57,
        65,
        71,
        72,
    }
)

KEYWORD_TAGS: tuple[str, ...] = (
    "传输线",
    "Smith",
    "圆图",
    "匹配",
    "支节",
    "死区",
    "盲区",
    "波导",
    "矩形",
    "圆波导",
    "同轴",
    "微带",
    "谐振",
    "谐振腔",
    "LC",
    "散射",
    "S参数",
    "魔T",
    "混合器",
    "简并",
    "TEM",
    "TE",
    "TM",
    "截止",
    "习题",
)


@dataclass(frozen=True)
class PagePlan:
    start: int
    end: int
    chapter: str
    summary: str
    treatment: str
    targets: tuple[str, ...]
    exercise_refs: tuple[str, ...] = ()


# Manual audit after text + visual review of sparse/image pages.
BLQ_PAGE_RANGES: tuple[PagePlan, ...] = (
    PagePlan(1, 1, "封面", "封面与串讲信息。", "审计", ()),
    PagePlan(
        2,
        3,
        "第1章 绪论",
        "考试范围六章；路/场/路场结合框架。",
        "融入",
        ("content/guide/exam-review.md",),
    ),
    PagePlan(4, 4, "第1章 绪论", "绪论配图页。", "审计", ("content/knowledge/01-传播与传输线/01-长线短线与分布参数.md",)),
    PagePlan(
        5,
        6,
        "第1章 绪论",
        "微波频段、集总 vs 分布参数；三大参量引入。",
        "融入",
        (
            "content/knowledge/01-传播与传输线/01-长线短线与分布参数.md",
            "content/knowledge/01-传播与传输线/02-行波相位常数与特性阻抗.md",
        ),
    ),
    PagePlan(7, 7, "第2章 传输线", "参量公式图页。", "审计", ("content/knowledge/01-传播与传输线/02-行波相位常数与特性阻抗.md",)),
    PagePlan(
        8,
        12,
        "第2章 传输线",
        "Zc 行波性质、λ/2 与 λ/4 变换；Γ、ρ 及三者关系。",
        "融入",
        (
            "content/knowledge/01-传播与传输线/03-反射驻波与输入阻抗.md",
            "content/solutions/06-考前复习/99-公式与图像.md",
        ),
    ),
    PagePlan(
        13,
        14,
        "第2章 传输线",
        "习题：Γ(z1) 反求负载；SWR 与波节反求 ZL。",
        "融入",
        (
            "content/solutions/01-传输线基础/04-Lec04.md",
            "content/solutions/06-考前复习/README.md",
        ),
        ("p13→Lec04·第3题", "p14→Lec04·第4题"),
    ),
    PagePlan(
        15,
        21,
        "第2章 传输线",
        "三种工作状态场图：行波、纯驻波、行驻波及波形分析。",
        "融入",
        ("content/knowledge/01-传播与传输线/04-行波纯驻波与行驻波.md",),
    ),
    PagePlan(
        22,
        22,
        "第2章 传输线",
        "行驻波习题拓扑图（多段 R/Zc 网络）。",
        "融入",
        ("content/solutions/01-传输线基础/04-Lec04.md",),
    ),
    PagePlan(
        23,
        28,
        "第2章 传输线",
        "Smith 圆图结构与圆图法习题（含答案页）。",
        "融入",
        (
            "content/knowledge/02-反射与匹配/02-Smith圆图怎么读.md",
            "content/solutions/02-圆图与匹配/03-Lec08-09/README.md",
        ),
    ),
    PagePlan(
        29,
        32,
        "第2章 传输线",
        "λ/4 变换、单/双支节匹配；死区简答重点。",
        "融入",
        (
            "content/knowledge/02-反射与匹配/03-并联支节匹配.md",
            "content/guide/exam-review.md",
        ),
    ),
    PagePlan(
        33,
        33,
        "第2章 传输线",
        "习题：并联单支节匹配 YL=(0.0425+j0.0175)S。",
        "融入",
        ("content/solutions/02-圆图与匹配/03-Lec08-09/第01题.md",),
        ("p33→Lec08-09 单支节",),
    ),
    PagePlan(34, 34, "第2章 传输线", "匹配习题续页。", "融入", ("content/solutions/02-圆图与匹配/03-Lec08-09/README.md",)),
    PagePlan(
        35,
        35,
        "第3章 微波传输线",
        "进入场分析过渡页。",
        "融入",
        ("content/knowledge/03-波导中的场与边界/00-从传输线到波导.md",),
    ),
    PagePlan(
        36,
        36,
        "第3章 微波传输线",
        "简答：单导体为何不能传 TEM。",
        "融入",
        ("content/knowledge/04-截止色散与速度/04-为什么空心波导没有TEM.md",),
    ),
    PagePlan(
        37,
        40,
        "第3章 微波传输线",
        "波导传输参量：λg、vp、vg 及参量关系图。",
        "融入",
        (
            "content/knowledge/04-截止色散与速度/01-三种波长.md",
            "content/knowledge/04-截止色散与速度/02-色散相速与群速.md",
        ),
    ),
    PagePlan(
        41,
        41,
        "第3-5章 汇总",
        "波导与谐振腔公式汇总表（矩形/圆/同轴/腔体）。",
        "融入",
        ("content/solutions/06-考前复习/99-公式与图像.md",),
    ),
    PagePlan(
        42,
        46,
        "第3章 微波传输线",
        "矩形波导传输特性、简并模定义与习题。",
        "融入",
        (
            "content/knowledge/05-矩形波导工程计算/01-模谱主模与简并.md",
            "content/solutions/03-规则波导与矩形波导/03-Lec13-16/README.md",
        ),
        ("p45-46→2-5~2-9 型",),
    ),
    PagePlan(
        47,
        51,
        "第3章 微波传输线",
        "圆波导 TE/TM 模、极化简并简答与习题。",
        "融入",
        (
            "content/knowledge/06-圆波导同轴线微带线/01-圆波导模式与贝塞尔根.md",
            "content/solutions/04-后续专题/01-Lec17-18-圆波导/README.md",
        ),
    ),
    PagePlan(
        52,
        55,
        "第3章 微波传输线",
        "同轴线 TEM 与单模尺寸选择原则、习题。",
        "融入",
        (
            "content/knowledge/06-圆波导同轴线微带线/02-同轴线TEM与高阶模.md",
            "content/solutions/04-后续专题/02-Lec19-20-同轴与微带/README.md",
        ),
    ),
    PagePlan(
        56,
        56,
        "第3章 微波传输线",
        "习题：同轴 TEM 条件与最短工作波长。",
        "融入",
        ("content/solutions/04-后续专题/02-Lec19-20-同轴与微带/第07题.md",),
        ("p56→同轴 TEM",),
    ),
    PagePlan(
        57,
        58,
        "第5章 谐振腔",
        "简答：LC 回路升高频缺点 vs 微波谐振器三点对比。",
        "融入",
        ("content/knowledge/08-谐振器网络与课程综合/01-微波谐振器与谐振腔.md",),
    ),
    PagePlan(
        59,
        61,
        "第5章 谐振腔",
        "圆柱腔 TE/TM 谐振条件与计算例题。",
        "融入",
        ("content/solutions/05-谐振器网络元件与测量综合/01-Lec22-23-微波谐振器/第03题.md",),
    ),
    PagePlan(
        62,
        64,
        "第5章 谐振腔",
        "矩形谐振腔场结构与公式图页。",
        "融入",
        ("content/knowledge/08-谐振器网络与课程综合/01-微波谐振器与谐振腔.md",),
    ),
    PagePlan(
        65,
        65,
        "第5章 谐振腔",
        "同轴腔 λ/2、λ/4、电容加载谐振条件（电纳法）。",
        "融入",
        ("content/knowledge/08-谐振器网络与课程综合/01-微波谐振器与谐振腔.md",),
    ),
    PagePlan(
        66,
        67,
        "第5章 谐振腔",
        "谐振腔习题图页。",
        "融入",
        (
            "content/solutions/05-谐振器网络元件与测量综合/01-Lec22-23-微波谐振器/README.md",
            "content/solutions/06-考前复习/README.md",
        ),
        ("p66-67→4-8~4-15 型",),
    ),
    PagePlan(
        68,
        70,
        "第6章 微波网络",
        "Z 矩阵、S 矩阵定义；互易/对称/无耗条件。",
        "融入",
        ("content/knowledge/08-谐振器网络与课程综合/02-微波网络基础与S参数.md",),
    ),
    PagePlan(
        71,
        71,
        "第6章 微波网络",
        "三点测量法示意图。",
        "融入",
        ("content/solutions/05-谐振器网络元件与测量综合/02-Lec24-微波网络基础/第04题.md",),
    ),
    PagePlan(
        72,
        73,
        "第6章 微波网络",
        "工作特性参量：S11、插入驻波比、T、插入相移、插入衰减。",
        "融入",
        ("content/knowledge/08-谐振器网络与课程综合/02-微波网络基础与S参数.md",),
    ),
    PagePlan(
        74,
        75,
        "第6章 微波网络",
        "散射矩阵习题（6-4-2、6-11、6-12 等型）。",
        "融入",
        (
            "content/solutions/06-考前复习/第02题-魔T散射矩阵分析.md",
            "content/solutions/06-考前复习/第03题-混合器散射矩阵分析.md",
            "content/solutions/06-考前复习/第04题-可变衰减器魔T结构.md",
        ),
        ("p74-75→6-4-2/6-11/6-12",),
    ),
)


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def page_tags(text: str) -> list[str]:
    lowered = text.lower()
    return [kw for kw in KEYWORD_TAGS if kw.lower() in lowered][:10]


def plan_for_page(page_number: int) -> PagePlan:
    for item in BLQ_PAGE_RANGES:
        if item.start <= page_number <= item.end:
            return item
    raise ValueError(f"No plan for page {page_number}")


def validate_ranges(page_count: int) -> None:
    covered: set[int] = set()
    for item in BLQ_PAGE_RANGES:
        covered.update(range(item.start, item.end + 1))
    expected = set(range(1, page_count + 1))
    missing = expected - covered
    extra = covered - expected
    if missing or extra:
        raise ValueError(f"Page range mismatch: missing={sorted(missing)}, extra={sorted(extra)}")


def try_ocr(pix: fitz.Pixmap) -> str:
    try:
        import pytesseract
    except ImportError:
        return ""
    image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    try:
        return normalize_text(pytesseract.image_to_string(image, lang="chi_sim+eng"))
    except Exception:
        return ""


def render_preview(doc: fitz.Document, page_index: int, output: Path) -> None:
    page = doc[page_index]
    pix = page.get_pixmap(matrix=fitz.Matrix(1.25, 1.25), alpha=False)
    output.parent.mkdir(parents=True, exist_ok=True)
    image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    image = ImageOps.exif_transpose(image).convert("RGB")
    image.thumbnail((1280, 1280))
    image.save(output, "WEBP", quality=82, method=6)


def load_vision_transcripts(path: Path | None) -> dict[int, dict[str, object]]:
    if path is None or not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    pages = data.get("pages", data)
    out: dict[int, dict[str, object]] = {}
    for key, value in pages.items():
        if not isinstance(value, dict):
            continue
        out[int(key)] = value
    return out


def merge_vision_entry(entry: dict[str, object], vision: dict[str, object]) -> None:
    excerpt = vision.get("short_excerpt") or vision.get("excerpt")
    if isinstance(excerpt, str) and excerpt.strip():
        entry["short_excerpt"] = excerpt.strip()[:500]
        entry["vision_len"] = len(excerpt.strip())
    refs = vision.get("exercise_refs")
    if isinstance(refs, list) and refs:
        entry["exercise_refs"] = [str(x) for x in refs]
    notes = vision.get("notes")
    if isinstance(notes, str) and notes.strip():
        entry["vision_notes"] = notes.strip()
    entry["vision_reviewed"] = True


def export_sparse_previews(doc: fitz.Document, sparse_pages: set[int]) -> int:
    count = 0
    for page_num in sorted(sparse_pages):
        render_preview(doc, page_num - 1, PREVIEW_DIR / f"blq-review-p{page_num:02d}-preview.webp")
        count += 1
    return count


def build_index(doc: fitz.Document, vision: dict[int, dict[str, object]] | None = None) -> list[dict[str, object]]:
    validate_ranges(doc.page_count)
    pages: list[dict[str, object]] = []
    for index in range(doc.page_count):
        page_num = index + 1
        raw = doc[index].get_text("text") or ""
        clean = normalize_text(raw)
        plan = plan_for_page(page_num)
        ocr_text = ""
        if len(clean) < SPARSE_THRESHOLD:
            pix = doc[index].get_pixmap(matrix=fitz.Matrix(2.0, 2.0), alpha=False)
            ocr_text = try_ocr(pix)
        combined = clean if len(clean) >= len(ocr_text) else ocr_text
        if page_num in PREVIEW_PAGES:
            render_preview(doc, index, PREVIEW_DIR / f"blq-review-p{page_num:02d}-preview.webp")
        entry: dict[str, object] = {
            "page": page_num,
            "chapter": plan.chapter,
            "text_len": len(clean),
            "ocr_len": len(ocr_text),
            "sparse": len(clean) < SPARSE_THRESHOLD,
            "tags": page_tags(combined),
            "short_excerpt": (combined or plan.summary)[:200],
            "range_summary": plan.summary,
            "treatment": plan.treatment,
            "targets": list(plan.targets),
            "exercise_refs": list(plan.exercise_refs),
        }
        if vision and page_num in vision:
            merge_vision_entry(entry, vision[page_num])
        pages.append(entry)
    return pages


def render_markdown(pages: list[dict[str, object]], page_count: int) -> str:
    lines = [
        "# BLQ 考前串讲 PDF 融入复核",
        "",
        "更新时间：2026-06-13",
        "",
        "源文件：`sources/微波技术基础考前串讲_blq.pdf`（电信 2301 班，75 页）。",
        "处理原则：只转写概念与习题映射，不发布 PDF 原文或整页截图。",
        "",
        f"- 总页数：{page_count}",
        f"- 稀疏页（text &lt; {SPARSE_THRESHOLD} 字）：{sum(1 for p in pages if p['sparse'])}",
        "",
        "## 页段审计",
        "",
        "| 页码 | 章 | 页级理解 | 处理 | 融入目标 | 习题映射 |",
        "|---:|---|---|---|---|---|",
    ]
    for item in BLQ_PAGE_RANGES:
        if item.start == item.end:
            page_label = str(item.start)
        else:
            page_label = f"{item.start}-{item.end}"
        targets = "<br>".join(item.targets) if item.targets else "—"
        exercises = "；".join(item.exercise_refs) if item.exercise_refs else "—"
        lines.append(
            f"| {page_label} | {item.chapter} | {item.summary} | {item.treatment} | {targets} | {exercises} |"
        )
    lines.extend(
        [
            "",
            "## 稀疏页视觉复核",
            "",
            "无需安装 Tesseract：运行 ``python scripts/tools/extract_blq_review.py --export-all-sparse``",
            "导出 ``assets/course/blq-review-pNN-preview.webp``，在 Cursor 对话中逐张读图；",
            "转写结果写入 ``docs/audit/blq_review_vision_transcripts.json`` 后重跑本脚本即可合并。",
            "",
            "## 站点入口",
            "",
            "- [考前复习总览](../content/guide/exam-review.md)",
            "- [电子板习题索引](../content/solutions/06-考前复习/README.md)",
            "- [SOURCE_EXTRACTION_AUDIT.md](SOURCE_EXTRACTION_AUDIT.md)",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Index BLQ exam-review PDF pages.")
    parser.add_argument(
        "--export-all-sparse",
        action="store_true",
        help="Render preview.webp for every sparse page (for vision review in chat).",
    )
    parser.add_argument(
        "--vision-file",
        type=Path,
        default=None,
        help=f"Merge vision transcripts JSON (default: {VISION_DEFAULT.name} if present).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not PDF_PATH.exists():
        raise SystemExit(f"Missing source PDF: {PDF_PATH}")
    doc = fitz.open(PDF_PATH)
    vision_path = args.vision_file
    if vision_path is None and VISION_DEFAULT.exists():
        vision_path = VISION_DEFAULT
    vision = load_vision_transcripts(vision_path)

    if args.export_all_sparse:
        validate_ranges(doc.page_count)
        sparse_pages = {
            index + 1
            for index in range(doc.page_count)
            if len(normalize_text(doc[index].get_text("text") or "")) < SPARSE_THRESHOLD
        }
        exported = export_sparse_previews(doc, sparse_pages)
        print(f"Exported {exported} sparse page previews to {PREVIEW_DIR}")

    pages = build_index(doc, vision)
    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(
        json.dumps(
            {
                "source": "微波技术基础考前串讲_blq.pdf",
                "pages": doc.page_count,
                "sparse_threshold": SPARSE_THRESHOLD,
                "page_index": pages,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    MD_OUT.write_text(render_markdown(pages, doc.page_count), encoding="utf-8")
    print(f"Wrote {JSON_OUT}")
    print(f"Wrote {MD_OUT}")
    print(f"Sparse pages: {sum(1 for p in pages if p['sparse'])}/{doc.page_count}")


if __name__ == "__main__":
    main()
