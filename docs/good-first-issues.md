# Good First Issues

面向新贡献者与 Agent 的入门任务清单。2026-06-14 基于全仓扫描（`build.py` 169 页、交叉引用 0 缺失、`grep` 待补项、plot 脚本与 `nav.json` 对照）整理。

完整 PR 流程：[CONTRIBUTING.md](../CONTRIBUTING.md) · Agent：[AGENTS.md](AGENTS.md) · 自检：[PR_CHECKLIST.md](PR_CHECKLIST.md)

**优先级**：P0 立即可做 · P1 有价值 · P2 进阶

---

## 探索摘要（2026-06-14）

| 发现 | 说明 |
|------|------|
| `nav.json` 缺 knowledge 06 单讲页 | 侧栏对 06 阶段 4 讲 + 99 自检仍用长文件名 |
| plot 脚本 docstring 不统一 | 9 个 `plot_*.py` 中 6 个缺 `Run:` / 输出目录说明 |
| Lec05 第 5 题无配图 | 依赖教材图 1-1，站点仅有填空表、无拓扑示意 |
| 圆柱腔 / TE10 色散图无 regenerate 说明 | 图已引用，但 knowledge 页未写 plot 命令 |
| Word 回填指南缺 guide 专章 | 8 阶段路径已对齐，但未列公式记忆 / Smith 专题 / 考前复习 |

---

## P0 · 立即可做

### GFI-01 · 为 knowledge 06 阶段补 nav.json 侧栏短标题

| 字段 | 内容 |
|------|------|
| **类型** | tooling |
| **难度** | ⭐ 入门 |
| **涉及文件** | `nav.json` |
| **建议分支** | `fix/nav-knowledge-06-filenames` |
| **Labels** | `good first issue`, `documentation`, `nav` |
| **GitHub** | [#30](https://github.com/estelledc/hust-eic-microwave-from-scratch/issues/30) |

**背景**：`nav.json` 的 `directories` 已有 `"06-圆波导同轴线微带线"`，但 `filenames` 缺少该阶段 4 个单讲页与 99 自检，侧栏显示完整中文文件名。

**具体任务**

- [ ] 对照 `content/knowledge/06-圆波导同轴线微带线/*.md` 列出全部 `.md`（除 README）
- [ ] 在 `nav.json` → `filenames` 增加短标题（参考 05 阶段风格，如「圆波导贝塞尔根」「同轴 TEM」）
- [ ] `python build.py` 后抽查 06 阶段侧栏
- [ ] 确认不与其它阶段同名 `99-自检清单与常见误区.md` 冲突（按目录上下文解析）

**验收标准**：06 阶段侧栏 5 个子页均为短标题；构建通过；无 nav 回归。

**Agent prompt：**

```
在仓库 hust-eic-microwave-from-scratch 中，先读 docs/AGENTS.md 与 nav.json。
对照 content/knowledge/06-圆波导同轴线微带线/ 下各 .md，在 nav.json 的 filenames 中补全侧栏短标题（directories 已有 06 目录项）。
python build.py && python scripts/tools/check_cross_refs.py。
分支 fix/nav-knowledge-06-filenames，按 docs/PR_CHECKLIST.md 开 PR。
```

---

### GFI-02 · 统一 plot 脚本文件头 docstring

| 字段 | 内容 |
|------|------|
| **类型** | docs |
| **难度** | ⭐ 入门 |
| **涉及文件** | `scripts/plots/plot_lec04_working_states.py`, `plot_lec06_q1_voltage_current.py`, `plot_fifth_homework_figures.py`, `plot_lec13_16_homework_figures.py`, `plot_third_homework_rect_wg.py` |
| **建议分支** | `docs/plot-script-headers` |
| **Labels** | `good first issue`, `documentation`, `plots` |
| **GitHub** | [#31](https://github.com/estelledc/hust-eic-microwave-from-scratch/issues/31) |

**背景**：`plot_smith_charts.py` / `plot_cylindrical_cavity_mode_chart.py` 已有「用途 + Run + 输出」三行头注释；其余 6 个脚本缺 `Run:` 或输出路径说明，维护者难以 regenerate。

**具体任务**

- [ ] 以 `plot_smith_charts.py` 为模板，补全各脚本顶部 docstring（用途、Run 命令、输出到 `assets/images/` 的文件名）
- [ ] 不改绘图逻辑与输出文件名
- [ ] `python -m py_compile scripts/plots/*.py`

**验收标准**：9 个 `plot_*.py` 均有统一结构 docstring；py_compile 通过。

**Agent prompt：**

```
阅读 scripts/plots/plot_smith_charts.py 的文件头格式，为 scripts/plots/ 下缺 Run 说明的 plot_*.py 补全 docstring（用途、Run 命令、输出目录/文件名）。
不要改绘图逻辑。python -m py_compile scripts/plots/*.py。分支 docs/plot-script-headers。
先读 docs/AGENTS.md。
```

---

### GFI-03 · Lec05 第 5 题补多段线拓扑示意图

| 字段 | 内容 |
|------|------|
| **类型** | plots |
| **难度** | ⭐⭐ 简单 |
| **涉及文件** | `scripts/plots/plot_lec05_multiline_topology.py`（新建）, `content/solutions/01-传输线基础/05-Lec05.md`, `content/solutions/01-传输线基础/99-公式与图像.md` |
| **建议分支** | `feat/plot-lec05-q5-topology` |
| **Labels** | `good first issue`, `plots`, `content` |
| **GitHub** | [#32](https://github.com/estelledc/hust-eic-microwave-from-scratch/issues/32) |

**背景**：`QUESTION_AUDIT.md` 标记 Lec05 第 5 题为「方法已校验、依赖教材图 1-1」；题解仅有填空表，零基础读者无法对照网络拓扑。

**具体任务**

- [ ] 阅读 `05-Lec05.md` 第 5 题，设计一版**与课程常见图 1-1 同构**的多段线示意（标注 $Z_c$、$\beta l$、终端负载类型）
- [ ] 新建 matplotlib 脚本，输出 `assets/images/lec05_q5_multiline_topology.webp`
- [ ] 在题解「详细思路」前插入配图与图注（说明参数需对照教材填空）
- [ ] 在 `99-公式与图像.md` 增加一行索引
- [ ] `python build.py` 通过

**验收标准**：第 5 题有清晰拓扑图；不改变「无统一数值答案」的结论；build 通过。

**Agent prompt：**

```
先读 docs/AGENTS.md、content/solutions/01-传输线基础/05-Lec05.md 第 5 题。
参考 scripts/plots/plot_second_homework_schematics.py 风格，新建 plot 脚本生成 lec05_q5_multiline_topology.webp，并在题解与 99-公式与图像.md 引用。
勿编造与 AUDIT 冲突的数值答案。python build.py。分支 feat/plot-lec05-q5-topology。
```

---

### GFI-04 · 圆柱腔模式图补「配图来源」说明

| 字段 | 内容 |
|------|------|
| **类型** | docs |
| **难度** | ⭐⭐ 简单 |
| **涉及文件** | `content/knowledge/08-谐振器网络与课程综合/01-微波谐振器与谐振腔.md`, `scripts/plots/plot_cylindrical_cavity_mode_chart.py` |
| **建议分支** | `docs/cavity-plot-readme` |
| **Labels** | `good first issue`, `documentation`, `plots` |
| **GitHub** | [#33](https://github.com/estelledc/hust-eic-microwave-from-scratch/issues/33) |

**背景**：`gpt-cylindrical-cavity-mode-chart.webp` 已在 knowledge 08 与考前复习引用，但正文未说明如何 regenerate；维护者需翻脚本目录才能找到命令。

**具体任务**

- [ ] 阅读 `plot_cylindrical_cavity_mode_chart.py` 确认输出文件名
- [ ] 在 `01-微波谐振器与谐振腔.md` 模式图图注下增加 collapsible「维护者 · 配图来源」（含 `python scripts/plots/plot_cylindrical_cavity_mode_chart.py`）
- [ ] 本地运行脚本确认可执行
- [ ] `python build.py`

**验收标准**：knowledge 页可见 regenerate 命令；脚本运行成功；build 通过。

**Agent prompt：**

```
阅读 scripts/plots/plot_cylindrical_cavity_mode_chart.py，在 content/knowledge/08-谐振器网络与课程综合/01-微波谐振器与谐振腔.md 圆柱腔模式图附近增加维护者 collapsible（配图来源 + Run 命令）。
运行 plot 脚本验证。python build.py。先读 docs/AGENTS.md。分支 docs/cavity-plot-readme。
```

---

### GFI-05 · Smith 专题 02 补 BLQ p34 单支节手算例题

| 字段 | 内容 |
|------|------|
| **类型** | content |
| **难度** | ⭐⭐ 简单 |
| **涉及文件** | `content/guide/Smith圆图专题/02-导纳与支节匹配.md`, `content/knowledge/02-反射与匹配/03-并联支节匹配.md#blq-p34-stub-example` |
| **建议分支** | `content/smith-blq-p34-example` |
| **Labels** | `good first issue`, `content` |
| **GitHub** | [#34](https://github.com/estelledc/hust-eic-microwave-from-scratch/issues/34) |

**背景**：`02-导纳与支节匹配.md` 有操作流与 Lec08 链，但缺一道**完整数值 walkthrough**；knowledge 03 已有 BLQ p34 算例（$Z_L=50+\mathrm j25\,\Omega$），专题页应摘一版「圆图七步」口语化步骤。

**具体任务**

- [ ] 阅读 knowledge `03-并联支节匹配.md#blq-p34-stub-example` 与 Lec08 第 4 题
- [ ] 在 Smith 专题 02 末尾增「算例 · BLQ p34」小节（归一化 → $g=1$ → 读 $b$ → 定 $l$，数值与 knowledge 一致）
- [ ] 链到 Lec08 第 4 题与已有 `smith_lec08_q4_single_stub.webp`
- [ ] 不重复 01 页已有 Lec07 Q1 算例
- [ ] `python build.py` + `check_cross_refs.py`

**验收标准**：专题 02 含完整手算步骤；数值与 knowledge canonical 一致；交叉引用仍为 0。

**Agent prompt：**

```
先读 docs/AGENTS.md、content/knowledge/02-反射与匹配/03-并联支节匹配.md#blq-p34-stub-example。
在 content/guide/Smith圆图专题/02-导纳与支节匹配.md 末尾增加 BLQ p34 单支节手算 walkthrough（圆图七步，数值与 knowledge 一致），链到 Lec08 第 4 题。
python build.py && python scripts/tools/check_cross_refs.py。分支 content/smith-blq-p34-example。
```

---

### GFI-06 · TE10 色散图在 knowledge 04 补引用与 regenerate 说明

| 字段 | 内容 |
|------|------|
| **类型** | content |
| **难度** | ⭐⭐ 简单 |
| **涉及文件** | `content/knowledge/04-截止色散与速度/02-色散相速与群速.md`, `scripts/plots/plot_third_homework_rect_wg.py`, `content/solutions/03-规则波导与矩形波导/99-公式与图像.md` |
| **建议分支** | `content/te10-dispersion-plot-link` |
| **Labels** | `good first issue`, `content`, `plots` |
| **GitHub** | [#38](https://github.com/estelledc/hust-eic-microwave-from-scratch/issues/38) |

**背景**：`lec_rect_wg_te10_dispersion.webp` 已在第三次作业 99 页引用，但 knowledge 04「色散相速与群速」正文无图、无 plot 命令，学习者读讲义时看不到 $v_p v_g=c^2$ 的图形验算。

**具体任务**

- [ ] 在 `02-色散相速与群速.md` 合适段落插入 `lec_rect_wg_te10_dispersion.webp` 与简短读图说明
- [ ] 增加维护者 collapsible：`python scripts/plots/plot_third_homework_rect_wg.py`
- [ ] 与 solutions 99 页交叉链接
- [ ] `python build.py`

**验收标准**：knowledge 04 可见色散图与 regenerate 命令；build 通过。

**Agent prompt：**

```
阅读 scripts/plots/plot_third_homework_rect_wg.py 与 content/solutions/03-规则波导与矩形波导/99-公式与图像.md 中对 lec_rect_wg_te10_dispersion.webp 的说明。
在 content/knowledge/04-截止色散与速度/02-色散相速与群速.md 插入该图、读图要点与维护者 regenerate 命令。python build.py。先读 docs/AGENTS.md。分支 content/te10-dispersion-plot-link。
```

---

### GFI-07 · 实验二 README 与 knowledge 07 README 双向链

| 字段 | 内容 |
|------|------|
| **类型** | content |
| **难度** | ⭐ 入门 |
| **涉及文件** | `content/experiments/02-元件参数测量/README.md`, `content/knowledge/07-实验测量与微波元件/README.md` |
| **建议分支** | `content/exp02-knowledge-bridge` |
| **Labels** | `good first issue`, `content` |
| **GitHub** | [#35](https://github.com/estelledc/hust-eic-microwave-from-scratch/issues/35) |

**背景**：knowledge 07 README「配套实验」表已链到实验二，但实验二 README「配套讲义」只链到 07 的单讲页，未链回 07 阶段总览；实验一已有类似结构但可对称完善。

**具体任务**

- [ ] 在实验二 README「配套讲义」首行增加 knowledge 07 README 链接
- [ ] 在 knowledge 07 README「配套实验」表确认实验二条目描述一致（必要时微调一句）
- [ ] `python scripts/tools/check_cross_refs.py` — 仍为 0 缺失

**验收标准**：两 README 互相可见「阶段总览 ↔ 实验总览」链接；交叉引用检查通过。

**Agent prompt：**

```
在 content/experiments/02-元件参数测量/README.md 与 content/knowledge/07-实验测量与微波元件/README.md 之间补双向总览链接（参考实验一写法）。
python scripts/tools/check_cross_refs.py。先读 docs/AGENTS.md。分支 content/exp02-knowledge-bridge。
```

---

### GFI-08 · Word 大纲回填指南补 guide 专章路径

| 字段 | 内容 |
|------|------|
| **类型** | docs |
| **难度** | ⭐⭐ 简单 |
| **涉及文件** | `content/appendices/Word大纲回填指南.md` |
| **建议分支** | `docs/word-guide-guide-sections` |
| **Labels** | `good first issue`, `documentation` |
| **GitHub** | [#36](https://github.com/estelledc/hust-eic-microwave-from-scratch/issues/36) |

**背景**：Word 指南已对齐 01–08 knowledge 与 01–05 作业，但未列 `content/guide/` 下公式记忆、Smith 圆图专题、考前复习索引——维护 Word 大纲时易遗漏。

**具体任务**

- [ ] 新增「Guide 专章（可选列）」表格：公式记忆 5 子页、Smith 圆图专题 3 页、exam-review、reading-map
- [ ] 路径与 `nav.json` / 当前目录名一致
- [ ] grep 全文确认无旧目录名残留

**验收标准**：Word 指南含 guide 专章表；路径与仓库一致。

**Agent prompt：**

```
对照 content/guide/ 与 nav.json，在 content/appendices/Word大纲回填指南.md 末尾增加 Guide 专章路径表（公式记忆、Smith 圆图专题、课程复习索引、阅读地图）。
grep 旧路径名确保无残留。分支 docs/word-guide-guide-sections。先读 docs/AGENTS.md。
```

---

### GFI-09 · PROJECT_STATUS 验证状态同步

| 字段 | 内容 |
|------|------|
| **类型** | docs |
| **难度** | ⭐ 入门 |
| **涉及文件** | `docs/PROJECT_STATUS.md`, `docs/CROSS_REF_REPORT.md` |
| **建议分支** | `docs/sync-project-status` |
| **Labels** | `good first issue`, `documentation` |
| **GitHub** | [#37](https://github.com/estelledc/hust-eic-microwave-from-scratch/issues/37) |

**背景**：PROJECT_STATUS 验证表需与最新 build / cross_refs 结果一致，便于 Agent 交接。

**具体任务**

- [ ] 运行 `python build.py`（Windows 需 `$env:PYTHONUTF8=1`）与 `check_cross_refs.py`
- [ ] 更新 PROJECT_STATUS「验证状态」表：页数、交叉引用 0、日期
- [ ] 若 CROSS_REF_REPORT 有变，同步一句摘要

**验收标准**：PROJECT_STATUS 日期与命令输出一致。

**Agent prompt：**

```
运行 python build.py 与 python scripts/tools/check_cross_refs.py，将 docs/PROJECT_STATUS.md 验证状态表更新为最新（169 页、交叉引用 0、日期 2026-06-14）。
先读 docs/AGENTS.md。分支 docs/sync-project-status。
```

---

## P1 · 有价值

### GFI-10 · Smith 01 补 VSWR 读半径小例题

| 字段 | 内容 |
|------|------|
| **类型** | content |
| **难度** | ⭐⭐ 简单 |
| **涉及文件** | `content/guide/Smith圆图专题/01-六口诀读图.md`, `content/solutions/02-圆图与匹配/02-Lec07.md` |
| **建议分支** | `content/smith-vswr-example` |
| **Labels** | `good first issue`, `content` |
| **GitHub** | — |

**背景**：01 页已有 $\bar z\to\Gamma$ 算例；「五种题型」表中 VSWR 读半径仍缺独立数值例题（Lec07 第 2 题 $\rho=2.618$ 可摘练）。

**具体任务**

- [ ] 在 01 页「五种题型」后增 VSWR 读 $|\Gamma|$ 短例题（链 Lec07，不与 Q1 重复）
- [ ] 可选引用 `smith_lec07_q2.webp` 若已有
- [ ] build + cross_refs

**验收标准**：有 VSWR 专用步骤；数值与 Lec07 一致。

**Agent prompt：**

```
在 content/guide/Smith圆图专题/01-六口诀读图.md 增加 VSWR/ρ 读半径小例题，数值摘自 02-Lec07.md，不与页内 Q1 重复。python build.py。先读 docs/AGENTS.md。分支 content/smith-vswr-example。
```

---

### GFI-11 · 接入 plot_lec04 三种工作状态包络图

| 字段 | 内容 |
|------|------|
| **类型** | content |
| **难度** | ⭐⭐ 简单 |
| **涉及文件** | `content/knowledge/01-传播与传输线/04-行波纯驻波与行驻波.md`, `content/solutions/01-传输线基础/99-公式与图像.md`, `scripts/plots/plot_lec04_working_states.py` |
| **建议分支** | `content/lec04-envelope-plot-link` |
| **Labels** | `good first issue`, `content`, `plots` |
| **GitHub** | — |

**背景**：`plot_lec04_working_states.py` 输出 `lec04_working_states_envelope.webp`，但 knowledge 04 页引用的是 `gpt-hw1-lec04-q1-working-states.webp`；脚本产物未被文档索引，维护者易以为 orphan。

**具体任务**

- [ ] 在 knowledge 04 或 99-公式与图像 增加对 `lec04_working_states_envelope.webp` 的说明（与 gpt 图分工：脚本版为 regenerate 真源）
- [ ] 补 plot 脚本 docstring（可与 GFI-02 合并）
- [ ] 运行 plot 脚本确认输出

**验收标准**：99 页或 knowledge 页索引脚本输出；docstring 含 Run 命令。

**Agent prompt：**

```
阅读 scripts/plots/plot_lec04_working_states.py，在 content/solutions/01-传输线基础/99-公式与图像.md 与/或 knowledge/01-传播与传输线/04-行波纯驻波与行驻波.md 增加 lec04_working_states_envelope.webp 索引与 regenerate 说明。python build.py。先读 docs/AGENTS.md。
```

---

### GFI-12 · Lec24 第 5 题扩展「易错点」小节

| 字段 | 内容 |
|------|------|
| **类型** | content |
| **难度** | ⭐⭐ 简单 |
| **涉及文件** | `content/solutions/05-谐振器网络元件与测量综合/02-Lec24-微波网络基础/第05题.md` |
| **建议分支** | `content/hw5-lec24-q5-mistakes` |
| **Labels** | `good first issue`, `content`, `help wanted` |
| **GitHub** | — |

**背景**：第 5 题「结论与易错点」仅 1 条；可对照 knowledge 08 网络基础补端口加载 / $S$ 与 $\Gamma$ 口径 3–5 条 bullet。

**具体任务**

- [ ] 阅读题解与 `knowledge/08/02-微波网络基础与S参数.md`
- [ ] 在题解末尾扩展易错点（单位、dB、加载条件），**不改** `\boxed{}` 数值
- [ ] build 通过

**验收标准**：≥3 条易错点；答案数值不变。

**Agent prompt：**

```
在 content/solutions/05-谐振器网络元件与测量综合/02-Lec24-微波网络基础/第05题.md 扩展易错点 bullet（端口加载、S 与 Γ 条件），不得改答案。python build.py。先读 docs/AGENTS.md。
```

---

### GFI-13 · Lec13-16 README 补 plot 脚本 regenerate 索引

| 字段 | 内容 |
|------|------|
| **类型** | docs |
| **难度** | ⭐⭐ 简单 |
| **涉及文件** | `content/solutions/03-规则波导与矩形波导/03-Lec13-16/README.md`, `scripts/plots/plot_lec13_16_homework_figures.py` |
| **建议分支** | `docs/lec13-plot-index` |
| **Labels** | `good first issue`, `documentation`, `plots` |
| **GitHub** | — |

**背景**：12 题均有 `lec13_16_q*.webp`，但 README 未说明批量 regenerate 命令，换题改图时维护成本高。

**具体任务**

- [ ] 在 README 末尾增「维护者 · 配图」collapsible
- [ ] 列出 `python scripts/plots/plot_lec13_16_homework_figures.py` 与输出前缀 `lec13_16_q`
- [ ] 运行脚本抽查 1–2 张图

**验收标准**：README 含 regenerate 说明；脚本可运行。

**Agent prompt：**

```
在 content/solutions/03-规则波导与矩形波导/03-Lec13-16/README.md 增加维护者配图来源（plot_lec13_16_homework_figures.py）。运行脚本验证。先读 docs/AGENTS.md。分支 docs/lec13-plot-index。
```

---

### GFI-14 · 公式记忆 02 补 TE10 数值验算小题

| 字段 | 内容 |
|------|------|
| **类型** | content |
| **难度** | ⭐⭐ 简单 |
| **涉及文件** | `content/guide/公式记忆/02-波导与色散.md`, `content/solutions/03-规则波导与矩形波导/03-Lec13-16/第02题.md` |
| **建议分支** | `content/formula-mem-te10-numeric` |
| **Labels** | `good first issue`, `content` |
| **GitHub** | — |

**背景**：公式记忆 02 有公式卡但缺与 WR-90 @ 10 GHz 对齐的**短数值验算**（Lec13 第 2 题 $\lambda_g\approx 39.75\,\mathrm{mm}$）。

**具体任务**

- [ ] 在 §5 例题区增「例 · TE10 @ 10 GHz」3–5 步手算
- [ ] 链到 Lec13 第 2 题；数值一致
- [ ] build 通过

**验收标准**：有完整数值链；与题解一致。

**Agent prompt：**

```
在 content/guide/公式记忆/02-波导与色散.md §5 增加 TE10 @ 10 GHz 短算例，数值与 03-Lec13-16/第02题.md 一致。python build.py。先读 docs/AGENTS.md。分支 content/formula-mem-te10-numeric。
```

---

### GFI-15 · PR 模板与 CONTRIBUTING 自检项对齐

| 字段 | 内容 |
|------|------|
| **类型** | docs |
| **难度** | ⭐ 入门 |
| **涉及文件** | `.github/PULL_REQUEST_TEMPLATE.md`, `CONTRIBUTING.md` |
| **建议分支** | `docs/pr-template-tweak` |
| **Labels** | `good first issue`, `documentation` |
| **GitHub** | — |

**背景**：PR 模板已基本中文化；CONTRIBUTING 若新增 `check_exam_integration` 触发场景，模板应同步勾选说明。

**具体任务**

- [ ] 对照 CONTRIBUTING 自检清单与 PR 模板 checkbox
- [ ] 补缺失项或 clarify 文案；不删已有项
- [ ] 最小 diff

**验收标准**：模板覆盖 CONTRIBUTING 全部验证项。

**Agent prompt：**

```
对照 CONTRIBUTING.md 与 docs/PR_CHECKLIST.md，检查 .github/PULL_REQUEST_TEMPLATE.md 是否覆盖全部变更类型与验证项，做最小必要中文润色。分支 docs/pr-template-tweak。
```

---

## P2 · 进阶

### GFI-16 · Lec13-16 选做题补工程量级示意图

| 字段 | 内容 |
|------|------|
| **类型** | plots |
| **难度** | ⭐⭐⭐ 中等 |
| **涉及文件** | `scripts/plots/plot_lec13_16_homework_figures.py`, `content/solutions/03-规则波导与矩形波导/03-Lec13-16/第12题.md` |
| **建议分支** | `feat/plot-lec13-q12-breakdown` |
| **Labels** | `good first issue`, `plots`, `content` |
| **GitHub** | — |

**背景**：第 12 题（击穿量级估计）有文字推导，图示可加强「$E$–$f$–尺寸」量级直觉。

**具体任务**

- [ ] 阅读第 12 题与现有 `fig_q12()`
- [ ] 完善 matplotlib 示意或补读图注释
- [ ] Markdown 引用路径正确；build 通过

**验收标准**：第 12 题图示更清晰；不改已校验数值结论。

**Agent prompt：**

```
阅读 scripts/plots/plot_lec13_16_homework_figures.py 与 03-Lec13-16/第12题.md，完善击穿估计示意图并更新引用。遵循现有 lec13 plot 风格。python build.py。先读 docs/AGENTS.md。
```

---

### GFI-17 · build.py 为 Markdown 图片补 alt 属性

| 字段 | 内容 |
|------|------|
| **类型** | UX |
| **难度** | ⭐⭐⭐ 中等 |
| **涉及文件** | `build.py`, `assets/css/`（若需样式） |
| **建议分支** | `feat/image-alt-from-caption` |
| **Labels** | `good first issue`, `help wanted` |
| **GitHub** | — |

**背景**：build 已为 `<img>` 加 `loading="lazy"`，但未从 Markdown `*图：...*` 题注生成 `alt`，屏幕阅读器体验可改进。

**具体任务**

- [ ] 阅读 build.py 中 Markdown→HTML 图片处理
- [ ] 实现：紧跟图片后的斜体题注提取为 `alt`（或首行 figcaption）
- [ ] 抽查 3 页 HTML 源码；全站 build 通过
- [ ] 不破坏无题注图片

**验收标准**：带题注的图片在 HTML 中有 meaningful `alt`；169 页 build 成功。

**Agent prompt：**

```
阅读 build.py 图片渲染逻辑，为带 *图：...* 题注的 Markdown 图片生成 alt 属性。python build.py 全站通过。先读 docs/AGENTS.md 禁止事项（勿改 content 正文）。分支 feat/image-alt-from-caption。
```

---

### GFI-18 · AGENTS.md 补 check_exam_integration 触发场景表

| 字段 | 内容 |
|------|------|
| **类型** | docs |
| **难度** | ⭐⭐ 简单 |
| **涉及文件** | `docs/AGENTS.md`, `scripts/tools/check_exam_integration.py` |
| **建议分支** | `docs/agents-exam-integration-table` |
| **Labels** | `good first issue`, `documentation` |
| **GitHub** | — |

**背景**：必跑命令已列 `check_exam_integration.py`，但 Agent 不清楚改哪些文件必须跑它。

**具体任务**

- [ ] 阅读脚本内 `ANCHOR_CHECKS` / `README_MUST_CONTAIN`
- [ ] 在 AGENTS.md 增「何时跑 exam integration」小表（exam-review、公式记忆 canonical、06-考前复习 README 等）
- [ ] 运行脚本确认当前通过

**验收标准**：AGENTS 有明确触发路径表；脚本 exit 0。

**Agent prompt：**

```
阅读 scripts/tools/check_exam_integration.py，在 docs/AGENTS.md 增加「何时运行 check_exam_integration」对照表。运行脚本验证通过。分支 docs/agents-exam-integration-table。
```

---

## 已完成 / 归档

| 编号 | 标题 | 说明 |
|------|------|------|
| — | 课程复习页维护者说明 | 2026-06-14 已在 `exam-review.md` 完成 |
| — | nav.json 与 Smith 专题对齐 | 2026-06-14 审计：`01/02/99` 三页已在 filenames |
| — | knowledge 06 完成度表 | README 已有「内容校验状态」段 |
| — | Word 指南 8 阶段路径 | 2026-06 已对齐；GFI-08 补 guide 专章 |

---

## 如何认领

1. 在 GitHub Issue 中回复「我来做这个」，或让 Agent 按 **Agent prompt** 执行
2. 开分支 → 完成 → PR 关联 Issue（`Closes #N`）
3. 维护者 merge 后关闭 Issue

**Labels**：`good first issue` · `content` · `plots` · `documentation` · `nav` · `tooling` · `help wanted` — 见 [MAINTAINERS.md](MAINTAINERS.md)

**统计**：开放 **18** 项（P0×9 · P1×6 · P2×3）+ 4 项归档
