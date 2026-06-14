# 贡献指南

感谢你愿意继续完善《微波技术基础》复习站点。本仓库是 **Markdown 内容 + Python 静态构建** 的课程笔记项目，不是传统 Web 应用；贡献方式以文档、配图和构建脚本为主。

- 在线站点：<https://estelledc.github.io/hust-eic-microwave-from-scratch/>
- 维护者文档：[docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md) · 索引：[docs/README.md](docs/README.md)
- **Agent 接手**：[docs/AGENTS.md](docs/AGENTS.md) · [docs/PR_CHECKLIST.md](docs/PR_CHECKLIST.md)
- 入门任务：[docs/good-first-issues.md](docs/good-first-issues.md)
- 设计参考：[docs/REFERENCES.md](docs/REFERENCES.md)

## 开始之前

1. 阅读 [README.md](README.md) 了解项目结构与本地预览。
2. 首次贡献建议从 [good first issue](docs/good-first-issues.md) 中选一项，或先在 Issue 中说明打算改什么。
3. 内容写作规范见 [docs/MANUAL_CONTENT_STANDARD.md](docs/MANUAL_CONTENT_STANDARD.md)（禁止批量生成、无来源扩写）。

## 开发环境

```bash
# 克隆（fork 后替换为你的 remote）
git clone https://github.com/<你的用户名>/hust-eic-microwave-from-scratch.git
cd hust-eic-microwave-from-scratch

python -m pip install -r requirements.txt   # Windows / macOS / Linux 通用
python build.py
python -m http.server -d site 8000           # 浏览器打开 http://localhost:8000
```

Windows 用户若使用虚拟环境，将上述 `python` 换为 `.venv\Scripts\python` 即可。

## 分支与命名

- **默认 base 分支**：`main`（不是 `master`）
- **分支前缀**（与 [executablebooks](https://github.com/executablebooks/.github/blob/master/CONTRIBUTING.md) 等文档项目惯例对齐，并本地化）：

| 前缀 | 用途 | 示例 |
|------|------|------|
| `content/` | 知识点、作业解答、guide 正文 | `content/smith-chart-example` |
| `docs/` | 维护文档、CONTRIBUTING、AGENTS | `docs/update-agents-handoff` |
| `fix/` | 构建、链接、nav、脚本 bug | `fix/nav-smith-topic-label` |
| `feat/` | 新专题、新脚本能力 | `feat/plot-lec08-stub` |
| `chore/` | 依赖、CI、gitattributes | `chore/pr-check-workflow` |

Agent 分支建议：`cursor/YYYY-MM-DD-简短描述` 或 `codex/YYYY-MM-DD-简短描述`，便于与人工 PR 区分。

## 提交流程（Fork → PR）

借鉴 [first-contributions](https://github.com/firstcontributions/first-contributions) 的「小步闭环」与 EBP 的 PR 规范：

1. **Fork** 仓库到你的 GitHub 账号。
2. **创建分支**（不要直接在 `main` 上改）：
   ```bash
   git checkout -b content/add-smith-example
   ```
3. **修改并自检**（见下方清单与 [docs/PR_CHECKLIST.md](docs/PR_CHECKLIST.md)）。
4. **提交**（Conventional Commits 风格，与 Node.js / Ockam 等社区惯例一致）：
   ```bash
   git add content/guide/Smith圆图专题/01-六口诀读图.md
   git commit -m "content(guide): 补充 Smith 圆图读数例题"
   ```
   常用 type：`content` · `docs` · `fix` · `feat` · `chore` · `plot`
5. **Push 并开 PR**：
   ```bash
   git push -u origin HEAD
   gh pr create --base main --title "content(guide): 补充 Smith 圆图读数例题" --body-file .github/PULL_REQUEST_TEMPLATE.md
   ```
   若未安装 `gh`，可在 GitHub 网页上创建 Pull Request，模板会自动填充。

## PR 自检清单

合并前请确认（CI 也会跑部分检查）：

- [ ] `python build.py` 成功（当前约 169 页）
- [ ] `python scripts/tools/check_cross_refs.py` 三类缺失均为 0
- [ ] 若改 `content/guide/exam-review.md` 或公式入口：`python scripts/tools/check_exam_integration.py`
- [ ] 新增/改名 Markdown 文件时，检查 `nav.json` 的 `directories` / `pages` / `filenames` 是否需要更新
- [ ] 图片路径使用 `assets/images/` 或 `assets/illustrations/`，Markdown 内用相对路径
- [ ] 未提交 `site/` 构建产物（仅 `site/.gitkeep` 保留）
- [ ] 中文排版：公式用 `$...$` / `$$...$$`，专有名词与课程口径一致（如 $Z_c$、VSWR、Smith 圆图）
- [ ] 若改 content：说明预览方式（本地 `http.server` 或 Pages 链接）

## 改什么、改哪里

| 目标 | 主要路径 | 备注 |
|------|----------|------|
| 知识点讲义 | `content/knowledge/` | 8 阶段；每阶段有 README 与 99 自检 |
| 作业解答 | `content/solutions/` | 按讲次；符号导读在 `00-符号与导读.md` |
| 学习指南 | `content/guide/` | 阅读地图、公式记忆、Smith 圆图专题 |
| 实验 | `content/experiments/` | 与 knowledge 07 阶段对照 |
| 侧栏标题 | `nav.json` | 与 `build.py` 的 `compact_nav_label` 联动 |
| 配图 | `scripts/plots/` → `assets/images/` | 见下方 |
| 构建逻辑 | `build.py` | 改动需抽查首页 / Hub / 精读页 |

### 添加配图

```bash
python scripts/plots/plot_smith_charts.py      # Smith 圆图
python scripts/plots/plot_lec04_working_states.py
# 输出默认写入 assets/images/，在 Markdown 中引用
python build.py
```

共用工具：`scripts/plots/smith_chart_utils.py`。

## Issue 与 Labels

仓库已有 labels（可用 `gh label list` 查看）：

| Label | 用途 |
|-------|------|
| `good first issue` | 新手友好，见 [docs/good-first-issues.md](docs/good-first-issues.md) |
| `documentation` | CONTRIBUTING、AGENTS、维护文档 |
| `help wanted` | 需要额外讨论或人手 |
| `enhancement` | 新功能或内容扩展 |

开 Issue 时请使用 `.github/ISSUE_TEMPLATE/` 中的模板，便于维护者 triage。

## CI

- **Pages 部署**：`.github/workflows/pages.yml`（push `main` 时构建 + 部署）
- **PR 验证**：`.github/workflows/pr-check.yml`（对 PR 跑 build + 交叉引用，不部署）

## 禁止事项

- **不要** `git push --force` 到 `main`
- **不要** 删除已有 `content/` 正文（可改写、可增补）
- **不要** 提交 `sources/` 本地课件（已在 `.gitignore`）
- **不要** 批量 AI 生成未校验的题解数值
- **不要** 在未跑 build 的情况下 claim「已完成」

## 获取帮助

- 项目状态与 WIP：[docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md)
- 分支清理记录：[docs/MAINTAINERS.md](docs/MAINTAINERS.md)
- 发布说明：[.github/PUBLISHING.md](.github/PUBLISHING.md)
