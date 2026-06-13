# 来源抽取与融入审计

更新时间：2026-06-13

本文件记录 `sources/` 本地资料如何被消化进站点。原始 PDF/DOCX 不发布、不纳入版本控制；站点只使用重构后的 Markdown、审计摘要和精选 WebP 图片。

页级复核详见 `docs/COURSE_INTEGRATION_REVIEW.md`；完整逐页 JSON 索引见 `docs/source_extraction_index.json`。JSON 每页只保存标题候选、关键词标签和短摘要，不保存完整课件正文。

## 课件 PDF 映射

| 源文件 | 页数 | 主题 | 融入阶段 | 目标页面 | 精选页 | 发布预览 | 采用内容 | 舍弃内容 | 复核状态 |
|---|---:|---|---|---|---:|---|---|---|---|
| 传输线理论1.pdf | 92 | 传输线理论、长线模型、反射与驻波 | knowledge/01 | content/knowledge/01-传播与传输线/README.md<br>content/knowledge/01-传播与传输线/99-自检清单与常见误区.md | 55 | `assets/images/course/course-transmission-line-theory-source-preview.webp` | 概念主线、核心公式、例题套路、可解释图像 | 封面目录、重复板书、整页原文截图 | 已抽取页码与候选图，人工重构入现有页 |
| 传输线理论 - 圆图.pdf | 39 | Smith 圆图、归一化阻抗、沿线旋转 | knowledge/02 | content/knowledge/02-反射与匹配/02-Smith圆图怎么读.md<br>content/knowledge/02-反射与匹配/99-自检清单与常见误区.md | 28 | `assets/images/course/course-smith-chart-source-preview.webp` | 概念主线、核心公式、例题套路、可解释图像 | 封面目录、重复板书、整页原文截图 | 已抽取页码与候选图，人工重构入现有页 |
| 阻抗匹配实例.pdf | 31 | 阻抗匹配实例、支节匹配与工程流程 | knowledge/02 | content/knowledge/02-反射与匹配/03-并联支节匹配.md<br>content/knowledge/02-反射与匹配/99-自检清单与常见误区.md | 8 | `assets/images/course/course-impedance-matching-examples-source-preview.webp` | 概念主线、核心公式、例题套路、可解释图像 | 封面目录、重复板书、整页原文截图 | 已抽取页码与候选图，人工重构入现有页 |
| 矩形波导1.pdf | 38 | 矩形波导、截止、模式、单模窗口 | knowledge/03-05 | content/knowledge/03-波导中的场与边界/README.md<br>content/knowledge/04-截止色散与速度/README.md<br>content/knowledge/05-矩形波导工程计算/README.md | 6 | `assets/images/course/course-rectangular-waveguide-source-preview.webp` | 概念主线、核心公式、例题套路、可解释图像 | 封面目录、重复板书、整页原文截图 | 已抽取页码与候选图，人工重构入现有页 |
| 圆波导.pdf | 31 | 圆波导、贝塞尔根、主模与单模边界 | knowledge/06 | content/knowledge/06-圆波导同轴线微带线/01-圆波导模式与贝塞尔根.md<br>content/knowledge/06-圆波导同轴线微带线/99-自检清单与常见误区.md | 16 | `assets/images/course/course-circular-waveguide-source-preview.webp` | 概念主线、核心公式、例题套路、可解释图像 | 封面目录、重复板书、整页原文截图 | 已抽取页码与候选图，人工重构入现有页 |
| 同轴线.pdf | 20 | 同轴线 TEM、高阶模上限、结构选择 | knowledge/06 | content/knowledge/06-圆波导同轴线微带线/02-同轴线TEM与高阶模.md<br>content/knowledge/06-圆波导同轴线微带线/04-从矩形到圆与微带的对照.md | 3 | `assets/images/course/course-coaxial-line-source-preview.webp` | 概念主线、核心公式、例题套路、可解释图像 | 封面目录、重复板书、整页原文截图 | 已抽取页码与候选图，人工重构入现有页 |
| 微波传输线1-2.pdf | 24 | 微波传输线类型与导波结构对照 | knowledge/06 | content/knowledge/06-圆波导同轴线微带线/04-从矩形到圆与微带的对照.md<br>content/knowledge/README.md | 4 | `assets/images/course/course-microwave-transmission-lines-source-preview.webp` | 概念主线、核心公式、例题套路、可解释图像 | 封面目录、重复板书、整页原文截图 | 已抽取页码与候选图，人工重构入现有页 |
| 微波集成传输线.pdf | 41 | 微带线、集成传输线、准 TEM 与有效介电常数 | knowledge/06 | content/knowledge/06-圆波导同轴线微带线/03-微带线准TEM与有效介电常数.md<br>content/knowledge/06-圆波导同轴线微带线/04-从矩形到圆与微带的对照.md | 40 | `assets/images/course/course-integrated-microwave-lines-source-preview.webp` | 概念主线、核心公式、例题套路、可解释图像 | 封面目录、重复板书、整页原文截图 | 已抽取页码与候选图，人工重构入现有页 |
| 微波谐振腔.pdf | 70 | 微波谐振器、谐振腔、品质因数 | knowledge/07-08 | content/knowledge/07-实验测量与微波元件/03-谐振器Q值与功率传输法.md<br>content/knowledge/08-谐振器网络与课程综合/01-微波谐振器与谐振腔.md | 8 | `assets/images/course/course-microwave-resonator-source-preview.webp` | 概念主线、核心公式、例题套路、可解释图像 | 封面目录、重复板书、整页原文截图 | 已抽取页码与候选图，人工重构入现有页 |
| 微波网络基础2.pdf | 39 | 微波网络参数、S 参数、测量读数 | knowledge/07-08 | content/knowledge/07-实验测量与微波元件/01-S参数与矢量网络分析仪.md<br>content/knowledge/08-谐振器网络与课程综合/02-微波网络基础与S参数.md | 23 | `assets/images/course/course-microwave-network-source-preview.webp` | 概念主线、核心公式、例题套路、可解释图像 | 封面目录、重复板书、整页原文截图 | 已抽取页码与候选图，人工重构入现有页 |

## 实验二资料映射

实验二以 `sources/微波实验2/微波技术基础实验报告二（重构）.md` 为主输入，DOCX 只用于确认段落和表格结构。站点页面保留数据链，不发布原始报告文件。

| 发布图片 | 来源 | 用途 |
|---|---|---|
| `assets/images/exp2/exp2-q-halfpower-method.webp` | `sources/微波实验2/media/fig_q_halfpower.png` | exp2-q-halfpower-method |
| `assets/images/exp2/exp2-coupler-port-map.webp` | `sources/微波实验2/media/fig_coupler_ports.png` | exp2-coupler-port-map |
| `assets/images/exp2/exp2-wilkinson-topology.webp` | `sources/微波实验2/media/fig_wilkinson.png` | exp2-wilkinson-topology |
| `assets/images/exp2/exp2-setup-resonator.webp` | `sources/微波实验2/media/fig_setup_resonator.png` | exp2-setup-resonator |
| `assets/images/exp2/exp2-setup-coupler.webp` | `sources/微波实验2/media/fig_setup_coupler.png` | exp2-setup-coupler |
| `assets/images/exp2/exp2-setup-divider.webp` | `sources/微波实验2/media/fig_setup_divider.png` | exp2-setup-divider |
| `assets/images/exp2/exp2-resonator-s21-curve.webp` | `sources/微波实验2/media/image4.jpeg` | exp2-resonator-s21-curve |
| `assets/images/exp2/exp2-resonator-bandwidth-search.webp` | `sources/微波实验2/media/image5.jpeg` | exp2-resonator-bandwidth-search |
| `assets/images/exp2/exp2-coupler-coupling-s21.webp` | `sources/微波实验2/media/image6.jpeg` | exp2-coupler-coupling-s21 |
| `assets/images/exp2/exp2-coupler-through-s21.webp` | `sources/微波实验2/media/image11.jpeg` | exp2-coupler-through-s21 |
| `assets/images/exp2/exp2-divider-port2-loss.webp` | `sources/微波实验2/media/image15.jpeg` | exp2-divider-port2-loss |
| `assets/images/exp2/exp2-divider-port3-loss.webp` | `sources/微波实验2/media/image17.jpeg` | exp2-divider-port3-loss |
| `assets/images/exp2/exp2-divider-isolation.webp` | `sources/微波实验2/media/image19.jpeg` | exp2-divider-isolation |

## 实验二报告结构

- Markdown 行数：499
- DOCX 段落数：121
- DOCX 表格数：10
- 主要标题：微波技术基础 实验报告；实验二　微波元件特性参数测量；一、实验目的；二、实验原理；2.1 微波谐振器品质因数 Q 的测量；2.2 微波定向耦合器；2.3 微波功率分配器；三、实验设备及装置图；3.1 实验设备；3.2 实验装置图；四、实验内容及步骤；4.1 微带谐振器品质因数的扫频测量；4.2 微波定向耦合器测量；4.3 微波功率分配器测量；五、实验结果；5.1 微带谐振器品质因数测量结果

## 融入原则

1. 只把课件中的概念、图像和例题结构转写成站点语言，不整页搬运 PPT 原文。
2. 同一概念优先融入现有知识点页，不新增独立课件库。
3. 实验数据必须写成“读数 → 换算 → 结论 → 误差来源”。
4. 课件和实验二补强后必须更新交叉链接，保证能从知识点、实验页和作业页互相到达。

## 考前复习资料映射

`sources/考试前复习/` 含课堂串讲整理 Markdown（`复习重点.md`、`电子板复习题.md`），不发布、不纳入版本控制。2026-06-13 已按站点语言融入：

| 源文件 | 主题 | 融入页面 | 采用内容 | 舍弃内容 |
|---|---|---|---|---|
| 复习重点.md | 考试结构、6 章公式、13 项划重点 | `content/guide/exam-review.md` | 考试结构、划重点清单、公式速查、易混点（同轴主模按 TEM 口径校正） | 原文逐段粘贴 |
| 复习重点.md | 圆柱腔模式图、同轴腔型式 | `content/knowledge/08-谐振器网络与课程综合/01-微波谐振器与谐振腔.md` | 四类干扰模式、λ/2·λ/4·电容加载同轴腔 | 语音识别噪声 |
| 复习重点.md | 魔 T / 混合器 S 矩阵 | `content/knowledge/08-谐振器网络与课程综合/03-常用微波元件网络化描述.md` | 四端口 S 矩阵与端口分析步骤 | — |
| 电子板复习题.md | 串讲习题索引 | `content/solutions/06-考前复习/README.md` | 6 章题号→作业/缺口解答映射 | 原图 IMG 编号 |
| 电子板复习题.md | 缺口大题 | `content/solutions/06-考前复习/第01–04题*.md` | 模式图、魔 T、混合器、可变衰减器标准解答 | — |
| — | 模式图配图 | `assets/images/gpt-cylindrical-cavity-mode-chart.webp` | 示意模式图（脚本生成，非教材原图） | 教材扫描图 |

### BLQ 考前串讲 PDF（2026-06-13）

`sources/微波技术基础考前串讲_blq.pdf`（75 页，电信 2301 班）为第二串讲源。抽取脚本：`scripts/tools/extract_blq_review.py`；逐页索引：`docs/blq_review_extraction_index.json`；页段审计：`docs/BLQ_REVIEW_INTEGRATION.md`。

| 源文件 | 主题 | 融入页面 | 采用内容 | 舍弃内容 |
|---|---|---|---|---|
| blq.pdf | 教材 6 章导航、13 项划重点补强 | `content/guide/exam-review.md` | 6 章页码表、双支节死区、LC 对比、工作特性参量入口 | PDF 原文、整页截图 |
| blq.pdf p57–58 | LC vs 微波谐振器简答 | `content/knowledge/08-谐振器网络与课程综合/01-微波谐振器与谐振腔.md` | 缺点 2 条 + 对比 3 条 + 参量变化 | 重复板书 |
| blq.pdf p65 | 同轴腔电纳法 | 同上 · 同轴腔小节 | 电容加载谐振条件表述 | 公式 OCR 噪声 |
| blq.pdf p72–73 | 工作特性参量 | `content/knowledge/08-谐振器网络与课程综合/02-微波网络基础与S参数.md` | 插入反射/SWR/T/θ/A 五参量表 | — |
| blq.pdf p32 | 双支节死区简答 | `content/knowledge/02-反射与匹配/03-并联支节匹配.md` | 定义、成因、间距、工程处理 | — |
| blq.pdf p41 | 波导/谐振腔公式汇总 | `content/solutions/06-考前复习/99-公式与图像.md` | 一行式速查表 | 原图 |
| blq.pdf 习题页 | 页码→题解映射 | `content/solutions/06-考前复习/README.md` | BLQ 页码索引表 | 图像页原题扫描 |
| blq.pdf | 6 章↔Lec↔阶段 | `content/appendices/讲次-作业-教材章节-知识点矩阵.md` | 对照表 | — |
| — | 关键页预览 | `assets/course/blq-review-p*-preview.webp` | 维护者复核用（稀疏页全量 + 关键页） | 课件源预览仍在 `assets/images/course/course-*` |

索引入口：[考前复习总览](../content/guide/exam-review.md)、[电子板习题索引](../content/solutions/06-考前复习/README.md)、[BLQ 页码映射](../content/solutions/06-考前复习/README.md#blq-串讲页码映射)。
