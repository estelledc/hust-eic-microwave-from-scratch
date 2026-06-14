# 类似站点调研与十轮优化记录

更新时间：2026-06-01

本记录用于跟踪“调研类似站点和学习笔记，对本站做十轮优化”的依据、决策和落地状态。调研对象优先选课程资料、RF/微波工具站、工程学习笔记和开放教材站点。

## 调研对象

| 站点 | 可借鉴点 | 对本站的启发 |
|------|----------|--------------|
| [RF Toolbox](https://www.rftoolbox.ca/) | 工具、教程、参考条目放在同一入口；用户可按任务直接进入 | 首页应提供“我现在要做什么”的任务入口，而不只给章节目录 |
| [Engineering LibreTexts · Smith Chart](https://eng.libretexts.org/Bookshelves/Electrical_Engineering/Electronics/Microwave_and_RF_Design_III_-_Networks_%28Steer%29/03%3A_Chapter_3/3.04%3A_Section_4-) | 章节内先解释概念，再配合图和设计动作 | 知识点页要保留“物理图像 -> 公式 -> 操作”的顺序 |
| [Engineering LibreTexts · Transmission Lines and Smith Charts](https://eng.libretexts.org/Bookshelves/Electrical_Engineering/Electronics/Microwave_and_RF_Design_III_-_Networks_%28Steer%29/03%3A_Chapter_3/3.05%3A_Section_5-) | 把传输线移动和 Smith 圆图轨迹联系起来 | 搜索和页面路径应帮助读者在“传输线/圆图/匹配”之间跳转 |
| [All About Circuits · Smith Chart Examples](https://www.allaboutcircuits.com/technical-articles/learn-to-use-the-impedance-smith-chart-through-examples/) | 以例子驱动读图，避免只讲定义 | 题解页顶部的“对应知识点”很关键，应在搜索结果中更容易被找到 |
| [MIT OCW · Electromagnetics and Applications](https://ocw.mit.edu/courses/6-013-electromagnetics-and-applications-spring-2009/) | 开放课强调 lecture notes、readings、assignments 的并列导航 | 本站也应突出“知识点、作业、实验、附录”四类学习任务 |

## 十轮优化清单

| 轮次 | 优化点 | 当前状态 | 验证方式 |
|------|--------|----------|----------|
| R1 | 调研记录沉淀为项目文档 | 已落地 | 本文件存在且列出来源与启发 |
| R2 | 首页增加按任务进入的快速入口 | Markdown ✅ / 壳层 ✅（2026-06-10） | `reading-map.md` 保留任务表；`render_home_page()` 卡片化 |
| R3 | 首页增加十分钟定位法 | Markdown ✅ / 壳层 ✅ | 策略区 + `reading-map.md`；首页搜索可命中 |
| R4 | 每页显示分组、阅读时间、页序和路径 | 已落地 | 构建后页面出现 `.page-meta` |
| R5 | 页面顶部增加阅读进度条 | 已落地 | 滚动页面时 `.reading-progress span` 变化 |
| R6 | 搜索结果显示命中数量和分组标签 | 已落地 | 输入关键词后显示 `.search-status` 与分组徽标 |
| R7 | 搜索支持键盘上下选择与 Enter 打开 | 已落地 | 搜索框中按方向键可移动高亮结果 |
| R8 | 搜索结果做 HTML 转义，避免索引文本污染页面 | 已落地 | `assets/app.js` 使用 `escapeHtml()` |
| R9 | Markdown 图片构建时自动加懒加载和异步解码 | 已落地 | 构建后 `<img>` 带 `loading="lazy"` 与 `decoding="async"` |
| R10 | 增加打印样式，方便考前打印单页讲义 | 已落地 | `assets/style.css` 有 `@media print` |

## 后续候选优化

- 给公式密集页增加“公式卡片”抽取视图，适合考前速查。
- 给 Smith 圆图与波导计算题增加小型可交互计算器，但要先确认数值公式和验算路径。
- 用浏览器抽查桌面和移动端，重点看首页课程地图卡片、搜索浮层、Hub 页与精读页壳层是否一致。

## 壳层重构（2026-06-10）

- `build.py` 增加 `PageKind` 与 `render_home_page()`：首页 Hero + 知识点/作业/实验/指南卡片。
- 原首页长文迁至 `content/guide/reading-map.md`。
- Hub 页（各 `README.md` / `index.md`）使用 `layout-hub`，去掉 pager 与右侧 TOC。
- `site/` 构建产物不再 Git 跟踪；CI 为唯一发布真源。

## 本轮验证

已完成：

- `.venv/bin/python build.py`：构建 151 页到 `site/`。
- 本地链接检查：扫描 148 个 HTML、24175 个本地 `href/src`，缺失 0 个。
- Python 语法检查：`build.py` 与 `scripts/` 下 14 个 Python 文件语法错误 0 个。
- `python3 scripts/tools/check_cross_refs.py`：knowledge / solutions / experiments 交叉引用缺失均为 0。
- 浏览器抽查：桌面首页可见页面元信息；搜索 `Smith` 显示命中数量、分组标签并支持键盘高亮；390px 移动视口无横向溢出。
