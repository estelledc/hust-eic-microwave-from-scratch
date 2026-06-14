# 维护者说明

面向仓库维护者与课程后继负责人。贡献者入口见 [CONTRIBUTING.md](../CONTRIBUTING.md)。

## 仓库信息

| 项 | 值 |
|----|-----|
| GitHub | `estelledc/hust-eic-microwave-from-scratch` |
| 默认分支 | `main` |
| Pages | GitHub Actions → `.github/workflows/pages.yml` |
| 本地路径示例 | `C:/Users/zx775/Documents/vrShare/微波` |

## Labels（已有 + 建议）

`gh label list` 当前已有：`bug`, `documentation`, `good first issue`, `help wanted`, `enhancement` 等。

建议 PR/Issue 时额外使用（可选新建）：

| Label | 用途 |
|-------|------|
| `content` | 知识点 / 题解 / guide 正文 |
| `plots` | `scripts/plots/` 配图 |

Good first issue 候选：[docs/good-first-issues.md](good-first-issues.md)

## 分支卫生（2026-06-14 交接记录）

### 已合并入 `main`、可删除的本地分支

| 分支 | 说明 |
|------|------|
| `chore/gitattributes-lf` | 已合并；remote 已 prune |
| `codex/knowledge-content-enrichment` | 已合并 |
| `feat/formula-quick-view` | 已合并 |
| `feat/github-corner` | 已合并 |
| `feat/smith-chart-topic` | PR #29 squash 后 tip 不在 main 历史，内容已在 main |
| `codex/local-wip-before-main-update` | 过期 WIP |
| `docs/knowledge-draft-paper-complete` | 过期 |

维护者本地清理示例：

```bash
git fetch --prune
git branch -d chore/gitattributes-lf codex/knowledge-content-enrichment feat/formula-quick-view feat/github-corner feat/smith-chart-topic codex/local-wip-before-main-update docs/knowledge-draft-paper-complete
```

### 远程 stale 分支（建议维护者删除）

| 远程分支 | 说明 |
|----------|------|
| `origin/codex/knowledge-content-enrichment` | 已合并 |
| `origin/feat/formula-quick-view` | 已合并 |
| `origin/fix/exam-review-ci-links` | 已合并 |
| `origin/feat/smith-chart-topic` | 已由 #29 取代 |

```bash
git push origin --delete codex/knowledge-content-enrichment feat/formula-quick-view fix/exam-review-ci-links feat/smith-chart-topic
```

**不要** force push `main`。

## WIP 提醒

`scripts/plots/*.py` 与 `scripts/tools/split_lec13_16_questions.py` 可能存在 **CRLF/LF 行尾差异**（`git diff` 为空）。合并 PR 前勿批量提交；若统一行尾，单独 `chore/` PR + `.gitattributes` 说明。

## 发布

见 [.github/PUBLISHING.md](../.github/PUBLISHING.md)。合并 `main` 后 Actions 自动部署。

## Agent 贡献

后继同学用 Cursor/Codex 时指向：

1. [docs/AGENTS.md](AGENTS.md)
2. [docs/PR_CHECKLIST.md](PR_CHECKLIST.md)
3. [docs/good-first-issues.md](good-first-issues.md) 中的 Agent prompt

设计依据：[docs/REFERENCES.md](REFERENCES.md)
