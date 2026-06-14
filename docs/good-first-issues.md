# Good First Issues

面向新贡献者与 Agent 的入门任务清单。在 GitHub 开 Issue 时可复制对应条目，并打上 `good first issue` label。

完整 PR 流程：[CONTRIBUTING.md](../CONTRIBUTING.md) · Agent：[AGENTS.md](AGENTS.md) · 自检：[PR_CHECKLIST.md](PR_CHECKLIST.md)

---

## GFI-01 · 补 Smith 圆图专题例题

| 字段 | 内容 |
|------|------|
| **难度** | ⭐ 入门 |
| **涉及路径** | `content/guide/Smith圆图专题/01-六口诀读图.md` |
| **建议分支** | `content/smith-worked-example-01` |
| **验收标准** | 新增 1 道 Lec07 风格小题（已知 $\bar z$ 求 $\Gamma$），含步骤与链到 [Lec07 解答](../content/solutions/02-圆图与匹配/02-Lec07.md)；`build.py` 通过 |
| **Labels** | `good first issue`, `documentation` |

**Agent prompt：**

```
在仓库 hust-eic-microwave-from-scratch 中，阅读 docs/AGENTS.md 与 content/guide/Smith圆图专题/README.md。
在 content/guide/Smith圆图专题/01-六口诀读图.md 末尾增加一道 Lec07 风格的归一化阻抗求反射系数例题（含完整步骤，数值与 02-Lec07.md 中某题不重复）。
跑 python build.py 和 python scripts/tools/check_cross_refs.py，按 docs/PR_CHECKLIST.md 开分支 content/smith-worked-example-01 并准备 PR。
```

---

## GFI-02 · 统一 plot 脚本文件头注释

| 字段 | 内容 |
|------|------|
| **难度** | ⭐ 入门 |
| **涉及路径** | `scripts/plots/plot_*.py` |
| **建议分支** | `docs/plot-script-headers` |
| **验收标准** | 每个 plot 脚本顶部 docstring 含：用途、运行命令、输出目录；风格与 `plot_smith_charts.py` 一致 |
| **Labels** | `good first issue`, `documentation` |

**Agent prompt：**

```
阅读 scripts/plots/plot_smith_charts.py 的文件头格式，为 scripts/plots/ 下其余 plot_*.py 补全相同结构的 docstring（Run 命令、输出到 assets/images）。
不要改绘图逻辑。跑 python -m py_compile scripts/plots/*.py，提交 fix/plot-script-headers 分支。
```

---

## GFI-03 · 修复 appendices Word 指南中的旧路径

| 字段 | 内容 |
|------|------|
| **难度** | ⭐⭐ 简单 |
| **涉及路径** | `content/appendices/Word大纲回填指南.md` |
| **建议分支** | `fix/appendix-word-guide-paths` |
| **验收标准** | 文中目录名与当前 `content/knowledge/` 8 阶段一致；无死链 |
| **Labels** | `good first issue`, `documentation` |

**Agent prompt：**

```
对照 content/knowledge/README.md 的 8 阶段目录名，修正 content/appendices/Word大纲回填指南.md 中的过时路径引用。
grep 全文旧目录名，逐处替换。python build.py 通过即可（该文件不进站点也可只做路径一致性）。
```

---

## GFI-04 · 为 knowledge 06 阶段补「待完善」标注

| 字段 | 内容 |
|------|------|
| **难度** | ⭐⭐ 简单 |
| **涉及路径** | `content/knowledge/06-圆波导同轴线微带线/README.md` |
| **建议分支** | `docs/knowledge-06-status` |
| **验收标准** | README 增加「完成度」表：各单讲页是否含逐题反查/一致性复核；列出 1–2 条待补项 |
| **Labels** | `good first issue`, `documentation` |

**Agent prompt：**

```
阅读 content/knowledge/README.md 中「本轮反查状态」写法，为 content/knowledge/06-圆波导同轴线微带线/README.md 增加完成度表（对照该目录下各 .md 是否已有反查段落）。
参考 docs/KNOWLEDGE_AUDIT.md。提交 docs/knowledge-06-status 分支。
```

---

## GFI-05 · nav.json 与 Smith 圆图专题文件名对齐审计

| 字段 | 内容 |
|------|------|
| **难度** | ⭐⭐ 简单 |
| **涉及路径** | `nav.json`, `content/guide/Smith圆图专题/` |
| **建议分支** | `fix/nav-smith-audit` |
| **验收标准** | `nav.json` 的 `filenames` 覆盖专题下全部 `.md`；构建后侧栏标题正确 |
| **Labels** | `good first issue`, `enhancement` |

**Agent prompt：**

```
列出 content/guide/Smith圆图专题/ 下所有 .md，与 nav.json 的 filenames/pages 对照，补缺失项。
python build.py 后本地预览 Smith 圆图专题侧栏。分支 fix/nav-smith-audit。
```

---

## GFI-06 · 实验一 README 与 knowledge 07 互链

| 字段 | 内容 |
|------|------|
| **难度** | ⭐⭐ 简单 |
| **涉及路径** | `content/experiments/01-矢网与传输线/README.md`, `content/knowledge/07-实验测量与微波元件/README.md` |
| **建议分支** | `content/exp01-knowledge-bridge` |
| **验收标准** | 两 README 互相增加「对应阶段/实验模块」链接；check_cross_refs 仍 0 缺失 |
| **Labels** | `good first issue`, `documentation` |

**Agent prompt：**

```
参考 content/experiments/README 或 07 阶段已有 bridge 写法，在实验一 README 与 knowledge 07 README 之间补双向链接。
跑 python scripts/tools/check_cross_refs.py 确认 experiment↔knowledge 无新增缺失。
```

---

## GFI-07 · 第五次作业某一题增加「易错点」小节

| 字段 | 内容 |
|------|------|
| **难度** | ⭐⭐ 简单 |
| **涉及路径** | `content/solutions/05-谐振器网络元件与测量综合/` 任选一题 |
| **建议分支** | `content/hw5-common-mistakes` |
| **验收标准** | 选定题目增加 3–5 条易错点（单位/端口/ dB 等）；不改原数值答案 |
| **Labels** | `good first issue`, `help wanted` |

**Agent prompt：**

```
在 content/solutions/05-谐振器网络元件与测量综合/ 中选一道已校验题（见 docs/QUESTION_AUDIT.md），在题解末尾加「易错点」bullet，口径与 knowledge 99-自检一致。不得改答案数值。
```

---

## GFI-08 · 新增 cylindrical cavity plot 文档说明

| 字段 | 内容 |
|------|------|
| **难度** | ⭐⭐ 简单 |
| **涉及路径** | `scripts/plots/plot_cylindrical_cavity_mode_chart.py`, `content/knowledge/08-谐振器网络与课程综合/` |
| **建议分支** | `docs/cavity-plot-readme` |
| **验收标准** | 在 08 阶段相关页或 scripts 注释中说明如何 regenerate `gpt-cylindrical-cavity-mode-chart.webp` |
| **Labels** | `good first issue`, `documentation` |

**Agent prompt：**

```
阅读 scripts/plots/plot_cylindrical_cavity_mode_chart.py，在 content/knowledge/08-谐振器网络与课程综合/01-微波谐振器与谐振腔.md 合适位置增加「配图来源」一句+运行命令。跑 plot 脚本验证可执行。
```

---

## GFI-09 · check_cross_refs 报告摘要进 PROJECT_STATUS

| 字段 | 内容 |
|------|------|
| **难度** | ⭐ 入门 |
| **涉及路径** | `docs/PROJECT_STATUS.md`, `docs/CROSS_REF_REPORT.md` |
| **建议分支** | `docs/sync-cross-ref-status` |
| **验收标准** | PROJECT_STATUS 验证表更新页数（169）与交叉引用 0 缺失；注明更新日期 |
| **Labels** | `good first issue`, `documentation` |

**Agent prompt：**

```
运行 python build.py 和 check_cross_refs.py，将 docs/PROJECT_STATUS.md 中「验证状态」表的页数与交叉引用结果更新为最新，日期 2026-06-14。
```

---

## ~~GFI-10 · 课程复习页增加「维护者说明」段~~ ✅（2026-06-14 已完成）

已在 `content/guide/exam-review.md` 页末加入 collapsible「维护者说明」。后续贡献者可跳过此项，选用 GFI-11 等开放任务。

<details>
<summary>原任务描述（归档）</summary>

| 字段 | 内容 |
|------|------|
| **涉及路径** | `content/guide/exam-review.md` |
| **验收标准** | 页末增加简短「维护者」段：串讲真源在本地 sources/，站点链到公式记忆 canonical 入口 |

</details>

---

## GFI-11 · 为 Lec13-16 某一题补 schematic 图

| 字段 | 内容 |
|------|------|
| **难度** | ⭐⭐⭐ 中等 |
| **涉及路径** | `scripts/plots/plot_lec13_16_homework_figures.py`, `content/solutions/03-规则波导与矩形波导/03-Lec13-16/` |
| **建议分支** | `feat/plot-lec13-qN-schematic` |
| **验收标准** | 新增或完善一题示意图 webp，Markdown 引用路径正确，build 通过 |
| **Labels** | `good first issue`, `enhancement` |

**Agent prompt：**

```
阅读 scripts/plots/plot_lec13_16_homework_figures.py 与 content/solutions/03-规则波导与矩形波导/03-Lec13-16/ 中缺图的题目，选一题补 matplotlib 示意图，输出到 assets/images/，在题解中引用。遵循 smith_chart_utils 以外的现有 plot 风格。
```

---

## GFI-12 · PR 模板中文化微调

| 字段 | 内容 |
|------|------|
| **难度** | ⭐ 入门 |
| **涉及路径** | `.github/PULL_REQUEST_TEMPLATE.md` |
| **建议分支** | `docs/pr-template-tweak` |
| **验收标准** | 模板字段清晰、与 CONTRIBUTING 自检一致；无英文遗漏（除 type 名） |
| **Labels** | `good first issue`, `documentation` |

**Agent prompt：**

```
对照 CONTRIBUTING.md 自检清单，检查 .github/PULL_REQUEST_TEMPLATE.md 是否覆盖全部变更类型与验证项，做最小必要中文润色，不要删 checklist 项。
```

---

## 如何认领

1. 在 GitHub Issue 中回复「我来做这个」或让 Agent 按上表 **Agent prompt** 执行
2. 开分支 → 完成 → PR 关联 Issue
3. 维护者 merge 后关闭 Issue

建议仓库额外 label（可选创建）：`content`、`plots` — 见 [MAINTAINERS.md](MAINTAINERS.md)
