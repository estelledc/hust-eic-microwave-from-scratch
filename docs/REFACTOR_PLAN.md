# 重构与完善计划

更新时间：2026-05-18

本文件记录《微波技术基础》复习书项目的下一轮重构与内容完善工作。前一轮（2026-05-17 之前）已完成第一性原理目录重排和零基础首版讲义，本轮聚焦：清理重构残留、补齐结构对称性、深化逐题校验、推动发布。

## 当前现状（2026-05-18 评估）

### 已就绪
- 五阶段知识点骨架：`01-传播与传输线` / `02-反射与匹配` / `03-波导中的场与边界` / `04-截止色散与速度` / `05-矩形波导工程计算`
- 三次作业逐题拆分：`solutions/01-传输线基础` / `02-圆图与匹配` / `03-规则波导与矩形波导`
- 写作模式扎实：物理直觉 → 图 → 公式定义 → 推导步骤 → 易错 → mini 自检 → 反向跨链
- `build.py` 一次构建 79 页，本地 `site/` 链接零缺失
- MathJax 接入，配图覆盖率达标

### 待修问题
| 类别 | 问题 |
|------|------|
| 烂尾残留 | `knowledge/Lec10-11-波导基础` / `Lec11-12-波导波长与色散` / `Lec13-16-矩形波导综合` 三个空目录只剩 `_assets/.gitkeep`（被 `03/04/05/` 替代后未清） |
| 文档过期 | `KNOWLEDGE_AUDIT.md` 路径仍写旧名（Lec01-05-传输线基础…），与现路径 `01-传播与传输线` 不一致；`QUESTION_AUDIT.md` 同病；`PROJECT_STATUS.md` 工作目录写 `/Users/jason/Documents/vrShare/微波`（已迁） |
| 结构不对称 | `solutions/04-后续专题/README.md` 单文件 639 行（圆波导+同轴+微带），其他作业已拆题；`knowledge/` 缺与之对称的第六阶段 |
| 内容深度 | knowledge 各页标"首版完成"，未做逐题反向校验；solutions 全部 `待校验` |

---

## P0 · 卫生清理（半天）

### P0-1 删 3 个空目录
- `content/knowledge/Lec10-11-波导基础/`
- `content/knowledge/Lec11-12-波导波长与色散/`
- `content/knowledge/Lec13-16-矩形波导综合/`

### P0-2 重写 KNOWLEDGE_AUDIT.md
路径切到当前真实结构，状态字段三档：`首版完成` / `待逐题反查` / `待复核`。

### P0-3 重写 QUESTION_AUDIT.md
路径同步到 `01-传输线基础/01-Lec01.md` 等真实拆题文件。

### P0-4 修 PROJECT_STATUS.md
工作目录改为 `explorations/content/hust-eic-microwave-from-scratch`；P1 中已完成的项移到"已完成整理"。

---

## P1 · 结构补齐（1-2 天）

### P1-5 新建 `knowledge/06-圆波导同轴线微带线/`
对称 `solutions/04-后续专题/`，至少 6 个文件：
- `README.md` 阶段总览（学习路线 + 作业入口）
- `01-圆波导模式与贝塞尔根.md`（$\chi_{mn}$、$\chi'_{mn}$、TE11 主模、简并）
- `02-同轴线TEM与高阶模.md`（TEM 主模、TE11 上限、单模带宽）
- `03-微带线准TEM与有效介电常数.md`（$\varepsilon_{\mathrm{eff}}$、特征阻抗近似式）
- `04-从矩形到圆与微带的对照.md`（截止/色散/单模条件横向对比）
- `99-自检清单与常见误区.md`

### P1-6 拆 `solutions/04-后续专题/README.md`
拆为：
- `04-后续专题/01-Lec17-18-圆波导/README.md` + `第NN题.md`
- `04-后续专题/02-Lec19-20-同轴与微带/README.md` + `第NN题.md`
- `04-后续专题/00-符号与导读.md`
- `04-后续专题/99-公式与图像.md`

### P1-7 更新 `solutions/index.md` 与 `knowledge/README.md`
- 加入第六阶段入口
- 第四次作业链接切到拆题后路径
- `appendices/讲次-作业-教材章节-知识点矩阵.md` 补第三阶段（Lec17-20）

---

## P2 · 内容深化（按章批，每章 1-2 天）

### P2-8 knowledge 逐节反查
按 `KNOWLEDGE_AUDIT.md` 顺序，每页：
1. 对照对应作业题，验证公式符号、坐标方向、归一化口径一致
2. 补"前置概念"段落（不假设读者会的最小集）
3. mini 自检题补完整答案（目前只有提示）

### P2-9 solutions 逐题校验
按 `QUESTION_AUDIT.md` 顺序，每题：
1. 题面对照原作业（无题面则补）
2. 公式/数值/单位/符号方向核对
3. 新增"对应知识点"段落（双向链）

### P2-10 链接覆盖检查脚本
`scripts/tools/check_cross_refs.py`：
- knowledge/ 每页是否引到至少一道作业
- solutions/ 每题是否引到至少一节知识点
- 输出缺链清单到 `docs/CROSS_REF_REPORT.md`

---

## P3 · 发布工程（半天）

### P3-11 重跑 `build.py` 全验证
- `site/` 与 `content/` 同步
- 链接零缺失
- MathJax 渲染抽查

### P3-12 GitHub 推送 + Pages
- 创建仓库 `hust-eic-microwave-review`
- GitHub Actions 自动构建发布
- README.md 加访问链接

### P3-13 docs/ → meta/ 重命名
避免与 GitHub Pages 默认 `docs/` 输出目录歧义。

---

## 执行节奏

| 时间 | 范围 |
|------|------|
| 今天 | P0 全部 + P1-5 起骨架 |
| 本周 | P1 完成 + P2 启动第 1 阶段（传输线 knowledge + solutions） |
| 下周 | P2 滚动推进 + P3 发布 |

每个阶段结束后：
1. 运行 `python build.py` 重建 site/
2. `python3 -m py_compile scripts/plots/*.py scripts/tools/*.py`
3. 抽查渲染：首页、知识点总览、刚改过的页面

---

## 取舍说明

- **本轮不动写作风格**：knowledge 已有的"直觉先行+物理画面+条件式标注"在抽样页面（如 `04-截止色散与速度/02-色散相速与群速.md`、`02-反射与匹配/02-Smith圆图怎么读.md`）质量已达标，本轮重点是补全和校验，不重写。
- **本轮不引入新教材版本对照**：教材章节按现 appendices 矩阵中的"建议章节"保留，逐题校验时若发现矛盾再回填到当日 daily 而非批量改写。
- **不做发布前的视觉风格统一**：CSS/排版属 P3 之后的工作，本轮不涉及。
