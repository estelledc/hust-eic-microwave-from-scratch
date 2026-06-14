# 离线 PDF Release 说明

面向读者与维护者：如何把本站 Markdown 内容导出为可下载的 PDF 分卷，并通过 GitHub Release 发布。

## 采用方案

**方案 B：HTML 站点 → Playwright/Chromium 打印 PDF → PyMuPDF 合并**

| 考量 | 说明 |
|------|------|
| 与现有构建一致 | 先 `python build.py` 生成 `site/`，PDF 与在线 Pages 版式一致 |
| 中文与公式 | 复用站点 CSS + MathJax（CDN）；打印前等待公式排版完成 |
| 图片 | `assets/images/` 已在 HTML 中引用，Chromium 打印时嵌入 |
| 站外出处 | 仅导出 `content/` 公开页；不含 `sources/`、BLQ 原文或课件 PDF |
| 体量 | 约 **169** 篇 HTML；分 4 卷 + 可选全书合集，避免单文件过大 |

不推荐 Pandoc 直转 Markdown：公式、Mermaid、侧栏结构与现有 CSS 难以一次对齐。

## 分卷说明

| 卷 | 文件名前缀 | 包含分组 | 约篇数 |
|----|------------|----------|--------|
| 学习指南 | `microwave-guide-*.pdf` | 首页、学习指南、附录 | ~15 |
| 知识点讲义 | `microwave-knowledge-*.pdf` | 8 阶段知识点 | ~55 |
| 作业解答 | `microwave-solutions-*.pdf` | 五次作业 + 考前复习 | ~85 |
| 实验环节 | `microwave-experiments-*.pdf` | 实验模块 | ~12 |
| 全书合集（可选） | `microwave-complete-*.pdf` | 以上全部 | ~169 |

每卷开头自动生成**目录页**；正文页脚带页码。卷内顺序与站点侧栏一致（同 `build.py` 的 `collect_pages()`）。

## 本地生成

### 依赖

```bash
python -m pip install -r requirements-pdf.txt
playwright install chromium
```

### 命令

```bash
# 构建站点并导出全部分卷（默认不含全书合集）
python scripts/tools/build_pdf.py --rebuild

# 指定版本后缀（与 Release 文件名一致）
python scripts/tools/build_pdf.py --rebuild --edition 2026.06

# 额外生成单 PDF 全书（体积大、耗时长）
python scripts/tools/build_pdf.py --rebuild --edition 2026.06 --include-complete

# 只构建某一卷
python scripts/tools/build_pdf.py --volume knowledge --edition 2026.06

# 冒烟测试：每卷仅前 2 篇
python scripts/tools/build_pdf.py --sample 2
```

产物目录：`dist/pdf/`（已加入 `.gitignore`），并写入 `manifest.json`（页数、体积、分卷列表）。

### 体积与页数（经验值）

- 单卷 PDF 页数通常为「文章数 × 2～6」页（含公式与配图）。
- 四分卷合计约 **400～900** 页、**30～80 MiB**（视配图与公式密度而定）。
- 全书合集可能 **100+ MiB**，仅建议在 Release 或 `--include-complete` 时使用。

## CI / GitHub Release

Workflow： [`.github/workflows/pdf-release.yml`](../.github/workflows/pdf-release.yml)

### 触发方式

| 触发 | 行为 |
|------|------|
| **Actions → PDF Release → Run workflow** | 手动构建；可填 `edition`、勾选 `include_complete` |
| **推送 tag `pdf-v*`** | 自动构建并创建/更新 Release，上传 PDF |
| **Release published** | 将 `dist/pdf/*.pdf` 附加到该 Release |

### 维护者发版流程

```bash
# 1. 确保 main 已合并最新内容
git checkout main && git pull

# 2. 打 tag 并推送（触发 CI）
git tag pdf-v2026.06
git push origin pdf-v2026.06

# 或本地构建后手动发 Release：
python scripts/tools/build_pdf.py --rebuild --edition 2026.06
gh release create pdf-v2026.06 dist/pdf/*.pdf \
  --title "离线 PDF · 2026.06" \
  --notes-file docs/PDF_RELEASE_NOTES_TEMPLATE.md
```

### Release 说明模板

发版时可复制 [PDF_RELEASE_NOTES_TEMPLATE.md](PDF_RELEASE_NOTES_TEMPLATE.md) 并替换版本号。

## 更新频率建议

- **学期中**：内容有大改（新题解、新阶段）时发一版，版本号用 `pdf-vYYYY.MM` 或补丁 `pdf-vYYYY.MM.1`。
- **考前**：若 `06-考前复习` 或 `guide/exam-review.md` 有更新，单独发一版并注明日期。
- **小修**：仅错字、链接修正可并入下次月度版，不必每 PR 都发 PDF。

## 故障排查

| 现象 | 处理 |
|------|------|
| `playwright` 未安装浏览器 | 运行 `playwright install chromium` |
| 公式为空白 | 检查网络（MathJax CDN）；CI 需能访问 jsdelivr |
| 某页超时 | 单独打开对应 `site/...html` 预览；Mermaid 页等待更久 |
| 与 Pages 不一致 | 先 `python build.py` 再导出，或加 `--rebuild` |

## 相关文件

| 路径 | 说明 |
|------|------|
| `scripts/tools/build_pdf.py` | PDF 构建入口 |
| `assets/pdf.css` | 打印/PDF 额外样式 |
| `requirements-pdf.txt` | Playwright 等 PDF 专用依赖 |
| `build.py` | 站点构建（PDF 前置步骤） |
