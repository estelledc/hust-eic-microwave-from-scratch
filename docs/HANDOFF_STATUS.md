# 交接会话状态（Agent / 维护者）

更新时间：2026-06-14

本文件汇总**本次项目交接**期间各 Agent 子任务的结果与**当前是否仍有进行中的工作**，避免多人/多 Agent 重复改同一文件。

> 日常贡献请读 [good-first-issues.md](good-first-issues.md)；Agent 请读 [AGENTS.md](AGENTS.md)。

## 当前结论：**无进行中的 Agent 任务**

| 类别 | 状态 |
|------|------|
| 代码 / 文档交接 | ✅ 已全部 push 至 `main` |
| GitHub Pages | ✅ CI 绿 |
| 离线 PDF | ✅ 有效版本 **[pdf-v2026.06.1](https://github.com/estelledc/hust-eic-microwave-from-scratch/releases/tag/pdf-v2026.06.1)**（全书合集 + 四分卷，中文已修） |
| 废弃 PDF | ⚠️ `pdf-v2026.06` 有乱码，Release 页已标废弃；**勿再创建 `pdf-v2026.06.2` tag**（曾 CI 失败/重复构建） |
| 本地 git WIP | 仅 `scripts/plots/*.py` 行尾符差异，**故意未提交** |
| 后续工作 | 9 个 open [Good First Issues](good-first-issues.md)（#30–#38），供后继同学认领 |

---

## 子任务清单（本会话）

| 任务 | 结果 | 关键 commit / 产物 |
|------|------|-------------------|
| 贡献者 / PR / Issue 模板 | ✅ | `e3e1a77` |
| Push + 远程 stale 分支清理 + labels | ✅ | `304ca89..e3e1a77`，labels `content`/`plots`/`tooling`/`nav` |
| 文档精简（维护视角） | ✅ | `e612490`、`fc6b1ad` |
| Good First Issues（18 项 + #30–#38） | ✅ | `cb01d84` |
| BLQ / 课件出处清理 | ✅ | `35e49ad` |
| Internal links CI 修复 | ✅ | `2a644ba`、`ab1ea73`、`46ec921` |
| docs 目录重组（`audit/`） | ✅ | `fc6b1ad` |
| 离线 PDF 首版 | ✅ | `5eb6a84` |
| PDF 中文乱码 + 全书合集 | ✅ | `63f4bb2`、`0fd417b` → Release **pdf-v2026.06.1** |
| PDF 文档指向修正 | ✅ | `8eef3b0` |
| 删除历史 git tag | ✅ | `pre-jason-ds-*`、`pre-opendesign-*` |
| 并行 PDF 协调（b7bd128e） | ⏹ 已由单线 Release 取代 | 无需再跑 |

**已取消 / 勿重复：**

- 勿并行修改 `build_pdf.py`、`pdf-release.yml` 并 push 多个 `pdf-v*` tag
- 勿批量 commit `scripts/plots/`（见 [PROJECT_STATUS.md](PROJECT_STATUS.md) WIP 表）

---

## 给后继 Agent 的三步

1. 读 [AGENTS.md](AGENTS.md) 与 [docs/README.md](README.md)
2. 从 [good-first-issues.md](good-first-issues.md) 或 GitHub Issues #30–#38 选一项
3. PR 前跑 [PR_CHECKLIST.md](PR_CHECKLIST.md)；PDF 发版见 [PDF_RELEASE.md](PDF_RELEASE.md)（仅维护者）

---

## PDF Release 真源

| Tag | 用途 |
|-----|------|
| **pdf-v2026.06.1** | **Latest**，推荐下载 |
| pdf-v2026.06 | 废弃（乱码、无全集） |

发新版：`git tag pdf-vYYYY.MM.x && git push origin pdf-vYYYY.MM.x`（workflow 会先 create release 再 upload）。
