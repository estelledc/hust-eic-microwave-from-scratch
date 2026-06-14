# 文档目录索引

更新时间：2026-06-14

`docs/` 不进站点构建，供贡献者、Agent 与维护者查阅。按读者角色选读，避免在审计考古文档里迷路。

## 我该读哪个？

| 你是谁 | 先读 | 再读 |
|--------|------|------|
| **第一次贡献** | [CONTRIBUTING.md](../CONTRIBUTING.md) | [good-first-issues.md](good-first-issues.md) → [PR_CHECKLIST.md](PR_CHECKLIST.md) |
| **Cursor / Codex Agent** | 根目录 [AGENTS.md](../AGENTS.md) | [AGENTS.md](AGENTS.md)（详版）→ GFI 条目 → PR_CHECKLIST |
| **写知识点 / 题解** | [MANUAL_CONTENT_STANDARD.md](MANUAL_CONTENT_STANDARD.md) | [good-first-issues.md](good-first-issues.md) 中 content 类任务 |
| **维护者 / 后继负责人** | [HANDOFF_STATUS.md](HANDOFF_STATUS.md) | [PROJECT_STATUS.md](PROJECT_STATUS.md) → [MAINTAINERS.md](MAINTAINERS.md) |
| **发离线 PDF** | [PDF_RELEASE.md](PDF_RELEASE.md) | [PDF_RELEASE_NOTES_TEMPLATE.md](PDF_RELEASE_NOTES_TEMPLATE.md) |

## 贡献者入口（保留在 `docs/` 根目录）

| 文件 | 用途 |
|------|------|
| [AGENTS.md](AGENTS.md) | Agent playbook：目录、必跑命令、禁止事项 |
| [PR_CHECKLIST.md](PR_CHECKLIST.md) | 提交 PR 前逐步自检 |
| [good-first-issues.md](good-first-issues.md) | 18 个入门任务（含 Agent prompt、验收标准） |
| [REFERENCES.md](REFERENCES.md) | 贡献流程设计参考来源 |
| [MANUAL_CONTENT_STANDARD.md](MANUAL_CONTENT_STANDARD.md) | 人工精写内容标准（禁止批量生成） |

## 维护者文档

| 文件 | 用途 |
|------|------|
| [HANDOFF_STATUS.md](HANDOFF_STATUS.md) | **交接会话汇总**：各 Agent 子任务是否完成、PDF 有效 tag、勿重复工作 |
| [PROJECT_STATUS.md](PROJECT_STATUS.md) | 目录职责、验证记录、WIP、待维护项 |
| [MAINTAINERS.md](MAINTAINERS.md) | 分支卫生、labels、发布与 Agent 指向 |
| [CROSS_REF_REPORT.md](CROSS_REF_REPORT.md) | `check_cross_refs.py` 自动生成；交叉引用健康度 |
| [PDF_RELEASE.md](PDF_RELEASE.md) | 离线 PDF 分卷构建与 GitHub Release 流程 |

## 历史审计（`docs/audit/`）

2026-06 内容反查、课件融入、站点调研等**已闭环**记录。日常贡献**不必**阅读；数值争议、来源追溯、考古时见 [audit/README.md](audit/README.md)。

**不要读**：把 audit 当任务清单——待办已迁入 [good-first-issues.md](good-first-issues.md) 与 [PROJECT_STATUS.md](PROJECT_STATUS.md)。

## 已删除的一次性文档（2026-06-14）

| 路径 | 原因 |
|------|------|
| `docs/plans/2026-06-03-*.md` | 会话计划已落地 |
| `docs/INTEGRATION_FIX_LOG.md` | BLQ 修复日志已合入正文 |
| `docs/REFACTOR_PLAN.md` | P0–P4 已完成，由 PROJECT_STATUS + audit 承接 |
