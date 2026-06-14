# 项目结构与状态说明

更新时间：2026-06-14

本文件记录项目边界、目录职责、验证结果与待处理问题。站点已通过 GitHub Actions 发布到 GitHub Pages；仓库 remote 为 `estelledc/hust-eic-microwave-from-scratch`。

**贡献者交接**（2026-06-14）：已添加 [CONTRIBUTING.md](../CONTRIBUTING.md)、[AGENTS.md](../AGENTS.md)、[good-first-issues.md](good-first-issues.md)、GitHub Issue/PR 模板与 `pr-check.yml`。设计参考见 [REFERENCES.md](REFERENCES.md)。

**文档清理**（2026-06-14）：从「考试复习交接」转为「长期维护」视角。删除已完成的一次性计划与修复日志（见下表）；历史审计迁入 [audit/](audit/README.md)。`content/guide/exam-review.md` 侧栏标题改为「课程复习索引」，正文保留 13 项考点与串讲导航。

逐节/逐题反查清单见 [audit/KNOWLEDGE_AUDIT.md](audit/KNOWLEDGE_AUDIT.md) 与 [audit/QUESTION_AUDIT.md](audit/QUESTION_AUDIT.md)。P0–P4 重构与壳层增强已于 2026-06 完成（`PageKind`、首页课程地图、`nav.json` 外置等）；结构与完成度以本文件与 audit 文档为真源。文档索引：[README.md](README.md)。

## 项目边界

- 项目工作目录：本地 clone 路径（如 `C:/Users/.../微波`）
- 默认分支：`main`
- GitHub remote：`https://github.com/estelledc/hust-eic-microwave-from-scratch.git`
- 发布方式：`.github/workflows/pages.yml` → `python build.py` → GitHub Pages（Source 选 **GitHub Actions**）

## 当前目录结构

| 路径 | 状态 |
|------|------|
| `content/knowledge/` | 8 阶段知识点讲义（第一性原理路线），正式内容源 |
| `content/solutions/` | 5 次正式作业 + `06-考前复习` 串讲索引（已拆题），正式内容源 |
| `content/experiments/` | 2 个实验模块，正式内容源 |
| `content/guide/` | 学习指南、阅读地图、课程复习索引、公式记忆、Smith 圆图专题 |
| `content/appendices/` | 知识点矩阵、Word 回填、真源说明（仅矩阵进站点） |
| `assets/` | 样式、交互、配图、jx 设计令牌 |
| `build.py` | Markdown → 静态网页书（含 PageKind 壳层分叉） |
| `scripts/plots/` | 配图生成，输出到 `assets/images/` |
| `scripts/tools/` | 交叉引用检查、拆题等维护脚本 |
| `docs/` | 贡献者入口 + 维护状态；历史审计在 `docs/audit/`（见 [README.md](README.md)） |
| `CONTRIBUTING.md` / `AGENTS.md` | 人类与 Agent 贡献入口 |
| `.github/` | Pages、PR 校验、Issue/PR 模板 |
| `site/` | **构建输出**（`.gitignore` 忽略，仅保留 `site/.gitkeep`） |

`sources/` 原始材料只保留在本地，通过 `.gitignore` 排除，不上传到 GitHub，也不纳入正式网页书构建。

## 2026-06-14 文档清理记录

| 操作 | 路径 | 原因 |
|------|------|------|
| 删除 | `docs/plans/2026-06-03-*.md`（4 文件） | 2026-06 知识深化会话计划，任务已落地 |
| 删除 | `docs/INTEGRATION_FIX_LOG.md` | BLQ 融入 100 项修复的一次性日志，修复已合入正文 |
| 删除 | `docs/REFACTOR_PLAN.md` | P0–P4 均已完成，职责由本文件 + AUDIT 文档承接 |
| 更新 | `README.md`、`content/guide/index.md`、`reading-map.md`、`exam-review.md` | 学习者/维护者双入口，弱化纯考试语气 |
| 更新 | `nav.json` | `exam-review.md` 侧栏标题 →「课程复习索引」 |
| 更新 | `content/knowledge/**/README.md` | 「本轮反查状态」→「内容校验状态」（已完成，非 WIP） |
| 迁入 | 10 个审计文件 → `docs/audit/` | 贡献者入口与历史审计分离；新增 `docs/README.md` |

## 已完成整理

- 参考 `estelledc/hust-eic-os-review`，完成第一阶段目录重构。
- 知识点按 8 阶段第一性原理路线重排；第四次作业已拆题；第六阶段 `06-圆波导同轴线微带线/` 已建立。
- `build.py` 引入 `PageKind`：首页课程地图、Hub 总览页、Article/Solution 精读页分模板渲染。
- 首页长文迁至 `content/guide/reading-map.md`；`content/index.md` 为占位，首页由 `render_home_page()` 生成。
- 侧栏增加 Markdown + `build.py` 开源说明；GitHub Corner 已接入。
- 交叉引用脚本 [`check_cross_refs.py`](../scripts/tools/check_cross_refs.py) 三类缺失均为 0（见 [CROSS_REF_REPORT.md](CROSS_REF_REPORT.md)）。
- knowledge 全量反查闭环（2026-06-03）；QUESTION_AUDIT 63 条题为「已校验」。
- `site/` 构建产物不再纳入 Git 跟踪，避免与 CI 发布真源漂移。

## 验证状态

最近一次构建与检查（2026-06-14）：

| 范围 | 结果 |
|------|------|
| 静态站点构建 | `Built 169 pages into site` |
| 交叉引用 | knowledge / solutions / experiments 缺失均为 0 |
| 首页壳层 | Hero + 卡片；无 `.page-meta` / `.pager` / `.toc-panel` |
| Hub 页 | `layout-hub`，无 pager |
| 精读页 | 保留 meta、TOC、pager |
| CI | `pages.yml` 部署；`pr-check.yml` 对 PR 跑 build + 校验 |

本地预览：

```bash
python3 -m pip install -r requirements.txt   # 首次
python build.py
python -m http.server -d site 8000
```

Python 语法检查：

```bash
python3 -m py_compile build.py scripts/plots/*.py scripts/tools/*.py
```

## 当前 WIP（git）

| 项 | 说明 |
|----|------|
| 未提交改动 | `scripts/plots/*.py`、`scripts/tools/split_lec13_16_questions.py` 可能仅有 CRLF/LF 行尾差异，无逻辑 diff |
| 建议 | Agent/贡献者勿批量 `git add scripts/`；行尾统一应单独 `chore/` PR |

## 待处理问题

| 优先级 | 问题 | 说明 |
|--------|------|------|
| P3 | `compact_nav_label` 硬编码导航标签 | ✅ 已外置到 `nav.json`（2026-06-10） |
| 维护 | `content/appendices/Word大纲回填指南.md` 部分路径仍写旧目录名 | 见 [good-first-issues.md](good-first-issues.md) GFI-03 |
| 维护 | 远程 stale 分支 | ✅ 已于 2026-06-14 删除（见 [MAINTAINERS.md](MAINTAINERS.md)） |
| 可选 | 公式卡片视图、Smith 圆图小计算器 | 见 [audit/SITE_RESEARCH_AND_OPTIMIZATION.md](audit/SITE_RESEARCH_AND_OPTIMIZATION.md) |

## 后续变更检查清单

1. 修改 Markdown 链接后，运行 `python build.py` 与 CI 内链校验。
2. 修改 `scripts/` 下 Python 后，运行 `python3 -m py_compile`。
3. 修改 `build.py` 壳层后，抽查首页、Hub 总览、一篇 knowledge 精读页。
4. 修改内容后，运行 `python3 scripts/tools/check_cross_refs.py`。
5. **不要**提交 `site/` 构建产物；只改 `content/`、`assets/`、`build.py`。
