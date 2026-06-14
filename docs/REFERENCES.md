# 贡献流程设计参考

记录本仓库 CONTRIBUTING / AGENTS / GitHub 模板的设计来源，便于后续维护者理解「为什么这样设计」，而非盲目照搬。

更新时间：2026-06-14

## 调研项目摘要

| # | 项目 | URL | 借鉴做法 | 适合本仓库？ |
|---|------|-----|----------|--------------|
| 1 | **agents.md 开放格式** | https://agents.md · https://github.com/agentsmd/agents.md | 根目录 `AGENTS.md` 专供 Agent；与 README 分工；强调**可执行命令**与测试/PR 说明 | ✅ 高度适合。本仓库无 npm test，改为 `build.py` + `check_cross_refs.py` |
| 2 | **Vercel Next.js** | https://github.com/vercel/next.js/blob/canary/AGENTS.md | 目录结构树、按路径读 README、分场景 build/test 命令、PR 前必须跑的检查 | ✅ 借鉴结构；去掉 monorepo/pnpm 部分 |
| 3 | **Executable Books Project** | https://github.com/executablebooks/.github/blob/master/CONTRIBUTING.md | 文档优先、分支命名、Opening a PR、review checklist、Conventional Commits | ✅ 与本项目「Markdown 文档站」同类 |
| 4 | **first-contributions** | https://github.com/firstcontributions/first-contributions | `.github/PULL_REQUEST_TEMPLATE.md`、小步 fork 流程、新手友好 checklist | ✅ 借鉴 PR 模板与「第一次 PR」心理；内容改为微波站点自检 |
| 5 | **Node.js** | https://github.com/nodejs/node/blob/main/.github/PULL_REQUEST_TEMPLATE.md | PR 模板顶部链到 CONTRIBUTING；提交前测试命令；notable-change label | ⚠️ 部分借鉴：链到 CONTRIBUTING + 本地验证命令；不需要 DCO 全文 |
| 6 | **Jupyter Book** | https://jupyterbook.org · EBP workflows | GitHub Actions 构建 + deploy-pages；贡献指南链到组织级 CONTRIBUTING | ✅ 已有 `pages.yml`；补充 PR 专用 `pr-check.yml` |
| 7 | **Material for MkDocs** | https://github.com/squidfunk/mkdocs-material | `mkdocs gh-deploy` / Actions 发布文档站 | ⚠️ 构建工具不同（我们用 `build.py`），只借鉴「CI=本地命令一致」 |
| 8 | **agent-handoff-kit** | https://github.com/jimozo/agent-handoff-kit | 分支前缀 `cursor/`、`codex/`；SESSION 日志；禁止 dirty tree 乱 add | ✅ 写入 AGENTS.md 分支建议与 WIP 警告 |
| 9 | **Ockam / goodfirstissue.dev 观察** | https://nus-cs3281.github.io/2023/students/observations.html | 持续供应 `good first issue`；CI 在 PR 时跑；commit type 规范 | ✅ `docs/good-first-issues.md` + 现有 labels |

## 本地化决策

| 参考做法 | 本仓库落地 | 未采用原因 |
|----------|------------|------------|
| EBP pre-commit hooks | 未强制 | 纯 Markdown 为主，维护成本高 |
| Node DCO 段落 | 未放入 PR 模板 | 课程笔记 fork，非基金会级治理 |
| MkDocs / Jupyter Book 构建 | 保持 `python build.py` | 已有成熟构建，不引入 Sphinx |
| 多 AGENTS.md 嵌套 | 仅 `AGENTS.md` + `docs/AGENTS.md` 详版 | 体量适中，scripts 说明写在 docs 即可 |
| first-contributions 英文 emoji checklist | 中文微波术语 checklist | 读者与贡献者以中文为主 |

## 本仓库文件与参考的对应关系

| 本文件 | 主要参考 |
|--------|----------|
| [CONTRIBUTING.md](../CONTRIBUTING.md) | EBP + first-contributions + AlgoCademy 协作指南 |
| [docs/AGENTS.md](AGENTS.md) | agents.md + Next.js AGENTS.md + agent-handoff-kit |
| [docs/PR_CHECKLIST.md](PR_CHECKLIST.md) | EBP «Check-list - What to look for» |
| [.github/PULL_REQUEST_TEMPLATE.md](../.github/PULL_REQUEST_TEMPLATE.md) | first-contributions + Node.js |
| [.github/ISSUE_TEMPLATE/*.yml](../.github/ISSUE_TEMPLATE/) | GitHub 官方 YAML issue forms + `good first issue` 标签实践 |
| [docs/good-first-issues.md](good-first-issues.md) | firsttimersonly.com + Ockam 观察 + Agent prompt（agents.md 强调 concrete examples） |

## 后续可继续调研

- [Markbind](https://markbind.org/) 文档站贡献指南（若扩展 Markbind 构建）
- [GitHub docs](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions) 官方 healthy contributions 清单
- 课程类 repo：`nus-cs3281` 等教学开源项目的 handoff 实践

维护者更新模板时，请同步修改本页「本地化决策」表。
