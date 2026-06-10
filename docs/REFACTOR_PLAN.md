# 重构与完善计划

更新时间：2026-06-10

本文件记录《微波技术基础》复习书项目的重构与内容完善工作。P0–P2 主体已完成；当前维护重点为壳层呈现（P3）与文档/工程卫生。

## 当前现状（2026-06-10）

### 已就绪

- **8 阶段**知识点：`01-传播与传输线` … `08-谐振器网络与课程综合`
- **5 次作业**逐题拆分：`solutions/01` … `05`；第四次作业已拆为 Lec17-18 / Lec19-20 模块
- **2 个实验**模块 + 指南/附录矩阵
- `build.py` 构建 **151 页**；MathJax + Mermaid + 全文搜索 + jx 设计系统
- 交叉引用：[`CROSS_REF_REPORT.md`](CROSS_REF_REPORT.md) 三类缺失均为 ✅
- knowledge 逐节反查闭环（2026-06-03）；solutions 逐题校验清单以「已校验」为主
- GitHub Pages：Actions 工作流 + remote `estelledc/hust-eic-microwave-from-scratch`

### 壳层重构（2026-06-10 已完成）

| 项 | 状态 |
|----|------|
| `PageKind`（home / hub / article / solution） | ✅ |
| `render_home_page()` 课程地图（Hero + 卡片） | ✅ |
| Hub 页去 pager / 右侧 TOC（`layout-hub`） | ✅ |
| `content/guide/reading-map.md` 承接原首页长文 | ✅ |
| 首页搜索注入 + `extract_card_intro()` | ✅ |
| 侧栏 Markdown + build.py 说明 | ✅ |
| `site/` 停止 Git 跟踪（仅 `.gitkeep`） | ✅ |

---

## 归档：P0–P2（已完成，2026-05 ~ 2026-06）

<details>
<summary>P0 卫生清理</summary>

- P0-1 删除旧 `Lec*` 空目录 ✅
- P0-2 / P0-3 审校清单路径同步 ✅
- P0-4 PROJECT_STATUS 工作目录与待办更新（本轮再次同步）

</details>

<details>
<summary>P1 结构补齐</summary>

- P1-5 `knowledge/06-圆波导同轴线微带线/` ✅
- P1-6 拆 `solutions/04-后续专题/` ✅
- P1-7 更新 solutions/index、knowledge/README、appendices 矩阵 ✅

</details>

<details>
<summary>P2 内容深化</summary>

- P2-8 knowledge 逐节反查 ✅（2026-06-03 全量）
- P2-9 solutions 逐题校验 ✅（QUESTION_AUDIT 已校验）
- P2-10 `check_cross_refs.py` + CROSS_REF_REPORT ✅

</details>

<details>
<summary>P3 发布工程（2026-05 已完成部分）</summary>

- P3-11 build 全验证 ✅
- P3-12 GitHub remote + Pages Actions ✅
- P3-13 docs/ 不重命名 ✅（见 [.github/PUBLISHING.md](../.github/PUBLISHING.md)）

</details>

---

## P4 · 后续可选（非阻塞）

### P4-1 导航元数据外置 ✅（2026-06-10）

侧栏目录短标签已外置到根目录 [`nav.json`](../nav.json)（`directories` / `pages` / `filenames`）。`build.py` 启动时加载；新增页面时优先改 JSON，不必改 Python。

### P4-2 维护文档路径清理 ✅（2026-06-10）

[`content/appendices/Word大纲回填指南.md`](../content/appendices/Word大纲回填指南.md) 已对齐 01–08 知识点阶段与 01–05 作业目录。

### P4-3 呈现层增强（来自 SITE_RESEARCH 候选）

- 公式密集页「公式卡片」抽取视图
- Smith 圆图 / 波导计算小型计算器（需先定验算路径）

---

## 执行节奏（维护期）

每次内容或壳层改动后：

1. `python build.py` → 确认页数与首页/Hub/精读页行为
2. `python3 scripts/tools/check_cross_refs.py`
3. `python3 -m py_compile build.py scripts/plots/*.py scripts/tools/*.py`
4. 只提交 `content/`、`assets/`、`build.py`、`.github/`、`docs/` — **不提交 `site/`**

---

## 取舍说明

- **Markdown 仍为内容真源**；首页卡片 intro 从 README 抽取，大改时用 build 常量 fallback。
- **与 OS 卫星站对齐的是任务入口 + 开源可达性**，不引入 71 主题 / Lab Studio。
- **搜索、进度条、打印样式**（SITE_RESEARCH R4–R10）保持不动。
