# Agent 工作指南

> 面向 Cursor、Codex、Claude Code 等编码 Agent 的项目说明。人类贡献者也可参考 [CONTRIBUTING.md](../CONTRIBUTING.md)。

本文件结构参考 [agents.md 开放格式](https://agents.md/) 与 [Vercel Next.js AGENTS.md](https://github.com/vercel/next.js/blob/canary/AGENTS.md)：先给**可执行的命令**，再给**边界与 playbook**。

## 项目是什么

华中科技大学电信学院《微波技术基础》**静态学习站点**：Markdown 源文件经 `build.py` 生成为 `site/` 下的 HTML 网页书，通过 GitHub Pages 发布。

- Remote：`estelledc/hust-eic-microwave-from-scratch`
- 默认分支：`main`
- 站点语言：简体中文 + MathJax 公式

## 目录结构（改前先读最近 README）

```
微波/
├── content/           # 正式内容源（会进站点）
│   ├── knowledge/     # 8 阶段知识点
│   ├── solutions/     # 作业解答 + 06-考前复习
│   ├── guide/         # 学习指南、阅读地图、课程复习索引、公式记忆
│   ├── experiments/   # 实验模块
│   └── appendices/    # 仅矩阵等少数页进站点
├── assets/images/     # plot 脚本输出 + 配图
├── build.py           # 构建入口
├── nav.json           # 侧栏短标题
├── scripts/plots/     # matplotlib 配图
├── scripts/tools/     # check_cross_refs 等
└── docs/              # 维护文档（不进站点，除被链接引用）
```

编辑 `content/knowledge/02-反射与匹配/` 前，先读该目录 `README.md` 与 [MANUAL_CONTENT_STANDARD.md](MANUAL_CONTENT_STANDARD.md)。

## 当前 WIP 状态

提交 PR 前执行 `git status`。截至 2026-06-14 交接时：

| 状态 | 说明 |
|------|------|
| 分支 | `main`，与 `origin/main` 同步 |
| 未提交改动 | `scripts/plots/*.py`、`scripts/tools/split_lec13_16_questions.py` 有 **行尾符（LF/CRLF）** 差异，无逻辑 diff；Agent 勿批量 `git add scripts/` 除非确实改了脚本逻辑 |
| 构建 | `python build.py` → **169 pages**；交叉引用缺失 **0** |
| 待维护 | 见 [good-first-issues.md](good-first-issues.md)（**18** 项，P0×9）、[PROJECT_STATUS.md](PROJECT_STATUS.md) |

## 必跑命令

```bash
# 首次
python -m pip install -r requirements.txt

# 每次改 content / build.py / nav.json 后
python build.py
python scripts/tools/check_cross_refs.py

# 改 exam-review 或公式 canonical 入口时
python scripts/tools/check_exam_integration.py

# 改 Python 脚本后
python -m py_compile build.py scripts/plots/*.py scripts/tools/*.py

# 本地预览
python -m http.server -d site 8000
```

Windows：上述 `python` 可换为 `.venv\Scripts\python`。

## 命名与风格

- **符号**：特性阻抗 $Z_c$（同 $Z_0$）；$z$ 自负载向源；VSWR 记 $\rho$
- **内容**：物理直觉 → 公式 → 题解 → 易错点；见 `MANUAL_CONTENT_STANDARD.md`
- **Commit**：`<type>(<scope>): <中文或英文简述>`，如 `content(guide): 补充支节匹配例题`
- **分支**：`content/` · `docs/` · `fix/` · `feat/` · Agent 可用 `cursor/YYYY-MM-DD-简述`

## Playbook

### 加一章知识点

1. 在对应 `content/knowledge/XX-阶段/` 新建 `.md`
2. 更新该阶段 `README.md` 推荐阅读顺序
3. 若侧栏标题需缩短：编辑 `nav.json` → `filenames`
4. `python build.py` + `check_cross_refs.py`

### 加一题作业解答

1. 在 `content/solutions/` 对应讲次下编辑或新建
2. 文首链到「对应知识点」
3. 数值变更需手算或脚本校验，更新 `docs/QUESTION_AUDIT.md` 状态（若维护者要求）

### 加 Smith 圆图配图

1. 改或扩 `scripts/plots/plot_smith_charts.py` / `smith_chart_utils.py`
2. `python scripts/plots/plot_smith_charts.py`
3. 在 Markdown 引用 `assets/images/smith_*.webp`

### 修 nav 不一致

1. 对照 `nav.json` 与 `build.py` 中 `NAV_CONFIG_PATH`
2. 构建后抽查侧栏与页面 title

## 开 PR（Agent 流程）

1. 从 `main` 拉分支，**不要**在 dirty 的 plot 脚本上顺手提交行尾符改动
2. 完成 [PR_CHECKLIST.md](PR_CHECKLIST.md) 全部项
3. Push 并创建 PR：

```bash
git checkout -b content/smith-add-worked-example
git add content/guide/Smith圆图专题/01-六口诀读图.md
git commit -m "content(guide): 补充 Smith 圆图读数例题"
git push -u origin HEAD

gh pr create --base main \
  --title "content(guide): 补充 Smith 圆图读数例题" \
  --body "## 变更类型
- [x] content

## 关联 Issue
Closes #（如有）

## 自检
- [x] python build.py
- [x] check_cross_refs.py 通过
"
```

4. 等 `pr-check.yml` CI 绿后再请人类 review

## Good First Issues

复制即用任务列表：[good-first-issues.md](good-first-issues.md)（**18** 项：P0×9 / P1×6 / P2×3；每项含 **Agent prompt**、验收标准、建议分支）。

**Agent 接手流程**：先读本文件 → 打开 GFI 条目或对应 GitHub Issue → 按 Agent prompt 执行 → [PR_CHECKLIST.md](PR_CHECKLIST.md) → 开 PR 并 `Closes #N`。

## 禁止事项

- 不要 `git push --force` 到 `main`
- 不要删除 `content/` 已有正文
- 不要提交 `site/`（除 `.gitkeep`）
- 不要提交 `sources/` 课件
- 不要无证据 claim build 通过——必须贴命令输出
- 不要在未读 `git status` 时用 `git add -A` 扫进无关 WIP

## 相关文档

| 文档 | 用途 |
|------|------|
| [PR_CHECKLIST.md](PR_CHECKLIST.md) | 逐步自检 |
| [REFERENCES.md](REFERENCES.md) | 贡献流程设计参考来源 |
| [MAINTAINERS.md](MAINTAINERS.md) | 分支卫生、label 建议 |
| [PROJECT_STATUS.md](PROJECT_STATUS.md) | 完成度与验证记录 |
