# 项目结构与状态说明

更新时间：2026-05-18

本文件记录 `/Users/jason/intern-journal/explorations/content/hust-eic-microwave-from-scratch` 当前项目边界、目录职责、验证结果与待处理问题。当前目标是把本项目整理成独立 Git/GitHub 仓库，并逐步做成可发布的 `github.io` 学习网站。推荐 GitHub 仓库名为 `hust-eic-microwave-review`。

下一阶段重构与完善计划见 [REFACTOR_PLAN.md](REFACTOR_PLAN.md)，逐节/逐题反查清单见 [KNOWLEDGE_AUDIT.md](KNOWLEDGE_AUDIT.md) 与 [QUESTION_AUDIT.md](QUESTION_AUDIT.md)。

## 项目边界

- 项目工作目录：`/Users/jason/intern-journal/explorations/content/hust-eic-microwave-from-scratch`（嵌入实习日志的 explorations）
- 当前项目内嵌一个独立 `.git/`，分支：`main`
- GitHub remote：尚未绑定；后续建议绑定为 `hust-eic-microwave-review`。

## 当前目录结构

| 路径 | 状态 |
|------|------|
| `content/knowledge/` | 按第一性原理路线重排的知识点讲义，正式内容源 |
| `content/solutions/` | 四次作业标准解答，正式内容源 |
| `content/guide/` | 初学者学习手册，正式内容源 |
| `content/appendices/` | 知识点矩阵、Word 回填、真源说明 |
| `assets/images/` | 正文配图 |
| `assets/illustrations/` | 轻量概念图 |
| `assets/style.css`、`assets/app.js` | 静态网页书样式与交互 |
| `build.py` | Markdown 到静态网页书的构建脚本 |
| `scripts/plots/` | 配图生成脚本，输出到 `assets/images/` |
| `scripts/tools/` | 内容维护辅助脚本 |
| `docs/QUESTION_AUDIT.md` | 作业题逐题校验清单 |
| `docs/KNOWLEDGE_AUDIT.md` | 知识点零基础完整性审校清单 |
| `site/` | 当前静态网页输出目录 |

`sources/` 原始材料只保留在本地，通过 `.gitignore` 排除，不上传到 GitHub，也不纳入正式网页书构建。

## 已完成整理

- 参考 `estelledc/hust-eic-os-review`，完成第一阶段目录重构。
- 将 `知识点/` 拆入 `content/knowledge/` 与 `content/appendices/`。
- 将 `解答/` 迁入 `content/solutions/`。
- 将 `figures/` 迁入 `assets/images/`。
- 将 `plots/` 迁入 `scripts/plots/`，并更新脚本输出路径。
- 将拆题工具迁入 `scripts/tools/`，并更新目标目录。
- 将 Word、实验指导书、提取草稿和历史媒体保留在本地 `sources/`，并从 Git 跟踪中排除。
- 清理 `.DS_Store`、`__pycache__/`、`*.pyc` 等缓存类文件。
- 明确后续网页书公式渲染优先使用 MathJax，迁移阶段不改写公式源码。
- 明确网页渲染效果是后续核心验收项，尤其是公式渲染、公式溢出、正文行宽和图片版式。
- 明确发布前必须对每道作业题重新校验，不能只依赖旧稿。
- 明确知识点讲义需要补充到零基础读者可读：前置概念、符号解释、公式来源、例题衔接和常见误区必须覆盖。
- 明确写作风格应通俗、灵活、问题驱动，避免死板堆公式。
- 生成 [QUESTION_AUDIT.md](QUESTION_AUDIT.md) 与 [KNOWLEDGE_AUDIT.md](KNOWLEDGE_AUDIT.md)，作为后续逐题、逐节审校入口。
- 新增 `build.py`，可将 `content/` 中的公开 Markdown 构建为 `site/` 静态网页。
- 网页模板已接入 MathJax，支持行内公式和块级公式渲染。
- 知识点页和作业解答页已补充项目内配图；题解页按“每题至少一张思路图”的标准做过自动覆盖检查。

## 验证状态

最近一次构建与链接检查：

| 范围 | 结果 |
|------|------|
| 静态站点构建 | `Built 79 pages into site` |
| `site/` 本地引用 | 检查 7679 个 `href/src`，缺失 0 个 |
| 知识点 Markdown 图片覆盖 | 缺图 0 页 |
| 作业解答 Markdown 图片覆盖 | 缺图 0 处 |
| 公开站点维护词扫描 | 未发现 `/Users/jason`、`localhost`、`GitHub`、`仓库`、`源文件`、`build.py` 等发布污染词 |
| 浏览器抽查 | 首页、知识点总览、Lec04 题解、Lec11–12 公式页已抽查；图片无破损，MathJax 有渲染，桌面/手机无横向溢出 |

本地 `sources/` 原始材料不纳入正式链接检查，也不进入发布站点。

Python 语法检查命令：

```bash
python3 -m py_compile scripts/plots/*.py scripts/tools/*.py
```

## 待处理问题

详细行动项见 [REFACTOR_PLAN.md](REFACTOR_PLAN.md) 的 P0/P1/P2/P3 分阶段清单。

| 优先级 | 问题 | 对应计划 |
|--------|------|---------|
| P0 | 旧重构残留三个空目录已清理（2026-05-18） | REFACTOR_PLAN P0-1 ✅ |
| P0 | 审校清单已同步当前路径（2026-05-18） | REFACTOR_PLAN P0-2 / P0-3 ✅ |
| P1 | `solutions/04-后续专题/` 仅单文件 639 行未拆题 | REFACTOR_PLAN P1-6 |
| P1 | `knowledge/` 缺第六阶段（圆波导/同轴/微带），与第四次作业不对称 | REFACTOR_PLAN P1-5 |
| P2 | 知识点逐节反查（对照作业题验证公式与符号） | REFACTOR_PLAN P2-8 + KNOWLEDGE_AUDIT |
| P2 | 作业题逐题校验（题面/公式/数值/单位/双向链） | REFACTOR_PLAN P2-9 + QUESTION_AUDIT |
| P3 | 尚未创建 GitHub remote 和 Pages 发布流程 | REFACTOR_PLAN P3-12 |

## 后续变更检查清单

1. 修改 Markdown 链接后，运行本地链接检查。
2. 修改 `scripts/plots/` 或 `scripts/tools/` 下 Python 脚本后，运行 `python3 -m py_compile scripts/plots/*.py scripts/tools/*.py`。
3. 静态网页书生成后，检查 MathJax 是否正确渲染行内和块级公式。
4. 发布前逐题核对作业解答，确认题面、公式、数值、单位和最终结论无误。
5. 发布前逐节检查知识点讲义，确认零基础读者能读懂。
6. 发布前检查文字风格，避免死板堆公式，确保解释通俗且可跟读。
7. 发布前确认 `site/` 可被静态服务器直接访问。
