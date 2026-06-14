## 离线 PDF · {{EDITION}}

本 Release 提供《微波技术基础》学习站点的**离线 PDF**，便于下载后在无网络环境阅读。

### 推荐下载

- **`microwave-complete-*.pdf`（全书合集）**：四分卷合并为单文件，含分组目录与各卷分节页，适合离线通读与全文检索。

### 分卷下载

- **学习指南卷**：课程地图、阅读地图、零基础手册、考前复习索引、Smith 圆图专题、公式记忆、讲次矩阵等
- **知识点讲义卷**：8 阶段第一性原理路线（传播线 → 匹配 → 波导 → 工程计算 → 综合）
- **作业解答卷**：五次作业标准解答与考前复习题解
- **实验环节卷**：矢网与传输线、元件参数测量等实验模块

每卷含目录页；全书合集目录按四分卷分组。正文含站点配图与 MathJax 公式（导出时已渲染）。

### 不含内容

- 原始课件 PDF、BLQ 串讲原文、`sources/` 本地资料
- 交互功能：站内搜索、侧栏跳转、明暗主题切换
- 在线-only 外链（GitHub 角标等在 PDF 中已隐藏）

### 使用建议

1. **离线通读**：优先下载全书合集
2. 零基础：先读**指南卷**中的「初学者手册」与「阅读地图」
3. 跟课：按**知识点卷**阶段顺序 + **作业解答卷**对应讲次
4. 考前：指南卷「考前复习」+ 题解卷「06-考前复习」

### 版本与更新

- 版本标识：`{{EDITION}}`（与文件名 `microwave-*-{{EDITION}}.pdf` 一致）
- 源站点：<https://estelledc.github.io/hust-eic-microwave-from-scratch/>
- 建议更新频率：学期内内容大改或考前集中修订时发新版；详见 [docs/PDF_RELEASE.md](https://github.com/estelledc/hust-eic-microwave-from-scratch/blob/main/docs/PDF_RELEASE.md)

### 文件列表

| 文件 | 说明 |
|------|------|
| `microwave-complete-*.pdf` | **全书合集（推荐）** |
| `microwave-guide-*.pdf` | 学习指南 |
| `microwave-knowledge-*.pdf` | 知识点讲义 |
| `microwave-solutions-*.pdf` | 作业解答 |
| `microwave-experiments-*.pdf` | 实验环节 |
| `microwave-complete-*.pdf` | 全书合集（四分卷 + 总目录） |
| `manifest.json` | 构建元数据（页数、体积） |

### 字体说明

本版起修复 headless 打印中文乱码：构建时嵌入 **Noto Sans SC**，CI 安装 **fonts-noto-cjk**。若旧版 PDF 中文异常，请下载本 Release 最新文件。

如有排版或缺页问题，请在 [Issues](https://github.com/estelledc/hust-eic-microwave-from-scratch/issues) 反馈并注明 PDF 文件名与页码。
