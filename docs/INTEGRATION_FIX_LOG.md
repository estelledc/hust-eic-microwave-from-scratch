# BLQ 融入一致性修复日志

更新时间：2026-06-13

本次针对 BLQ 串讲融入后的逻辑不一致、错链、术语混用等问题，共记录 **100** 项修复（含批量术语统一计 65 处）。

验证：`python build.py` → `python scripts/tools/check_exam_integration.py` → `python scripts/tools/check_cross_refs.py`

---

## P0 错链（7）

1. BLQ p13 / 题 1-4-2：由误链 Lec03·第2题 → **Lec04·第3题**
2. 习 1-13：由 Lec03 目录 → **Lec04·第3题**，并注明 $\Gamma(z_1)=-j0.5$
3. BLQ p14 / 习 1-17：由 Lec03·第4题 → **Lec04·第4题**
4. BLQ p56 / 同轴 TEM：由第8题（微带准TEM）→ **第7题**
5. `extract_blq_review.py` p13 融入目标改为 Lec04
6. `extract_blq_review.py` p56 融入目标改为第7题
7. `BLQ_REVIEW_INTEGRATION.md` 习题映射与上同步（重跑脚本）

## 13 项划重点对齐（16）

8. 第4项：「四种」→ **三种工作状态**（注明教材四类终端）
9. 第1项：补 **工作特性参量** 锚点链
10. 第2项：补 **LC 对比** 锚点链
11. 第5项：统一 **死区=盲区**，链 `#stub-dead-zone`
12. 第6项：补 **Lec02 通解** 入口
13. 第8项：补 **圆波导极化简并** 链
14. 第10项：补 **02-行波相位** knowledge 链
15. 第11项：直链 **01-多段线** + Lec08-09 第5题
16. 第12项：链 **#quality-factor-q** + Q 测量
17. 第13项：链 **#wall-current-slots**
18. Ch6 导航：补 **03-魔T/混合器** + `#gap-solutions`
19. 讲次矩阵 13 项表：与 exam-review 全量同步（13 行）
20. 电子板 Ch2 题4：三种状态表述统一
21. 电子板 Ch2 题5：死区/盲区术语统一
22. 电子板 Ch3：补开缝辐射行
23. 电子板 Ch1 题2：补同轴 TEM 链
24. 电子板 Ch4 题11：计算链 **第9题**（非第8题证明）
25. 电子板 Ch5 题14：标 **Ch5** 避免与 Ch2 题14 混淆
26. `reading-map.md` 第10轮：「待补题型」→ 13项+BLQ 查漏

## 稳定锚点（12）

27. `#textbook-6ch-nav` — exam-review 6章导航
28. `#blq-page-map` — BLQ 页码表
29. `#gap-solutions` — 缺口题表
30. `#stub-dead-zone` — 双支节死区
31. `#network-operating-params` — 工作特性参量
32. `#lc-vs-microwave-resonator` — LC 对比
33. `#coaxial-cavity` — 同轴腔
34. `#quality-factor-q` — 品质因数
35. `#wall-current-slots` — 壁电流开槽
36. `#wg-cavity-formulas` — p41 公式汇总
37. 矩阵附录锚点：`#textbook-6ch-nav`、`#blq-page-map`
38. 新增 `scripts/tools/check_exam_integration.py` 校验上述锚点

## BLQ 映射补全（22）

39–60. BLQ 表由 19 行扩至 **41 行**（p2–6、p8–12、p22、p34、p35、p37–40、p42–44、p47–49、p51、p52–54、p55、p59–60、p62–64、p68–70 等）

## 符号与术语（20）

61. exam-review 公式区：符号导读改 **第一次作业** + $Z_c$ 说明
62. exam-review mermaid/正文：Z0 → **Zc**
63. 06-99-公式：符号导读改第一次作业
64. 06-99-公式：谐振阶段链 **04-后续 99-公式**
65. 03-并联支节：$Y_0$ → **$Y_c$** 验算句
66. 01-谐振器 LC 段：$Q_0$/$Q_L$ 并列 → 区分 **$Q_0$ 与 $Q_L$**
67–131. **65 处**「枝节」→「支节」批量统一（Lec08 题解 + knowledge 表格 + 99-公式）
68. 死区段落：注明 **匹配死区=盲区**
69. 电子板索引：说明题号 **6、10、16** 未单独转录
70. 三种状态 vs 四种终端：全文口径统一
71. VSWR = $\rho$ 在 exam-review 注明
72. 矩阵 Ch6：补 **07 · VNA** 入口
73. 矩阵：Lec21 缺口保留（课程无 Lec21，未虚构内容）
74. 05-波导匹配：新增 **切场线不辐射** 简答段
75. 03-并联支节：回链 exam-review 第5项
76. 04-三种状态：回链 BLQ p15–21
77. extract 脚本 exercise_refs 更新
78. fix_integration_issues.py 术语批处理脚本
79. SOURCE_EXTRACTION_AUDIT 已在上一轮记录 BLQ
80. COURSE_INTEGRATION_REVIEW 已在上一轮记录 BLQ

## 内容与结构（20）

81. 工作特性参量专节（上一轮已加，本次锚点稳定）
82. LC vs 微波谐振器模板（上一轮已加）
83. 双支节死区四步简答（上一轮已加，本次术语统一）
84. p41 公式汇总表（上一轮已加，本次锚点）
85. 11 张 BLQ 预览图路径写入 README 说明
86. 缺口题锚点英文化避免中文 slug 漂移
87. Ch2/Ch5 重复题号 14 标注章节
88. Ch4 题12 保留但题11不再写「同上」链第8题
89. 06-考前复习 Ch3 开缝辐射独立行
90. 魔 T 缺口题链 `#gap-solutions` 而非中文锚
91. exam-review 易混点魔 T 链 **#magic-t**（03-元件页已补锚）
92. 04-Lec04 第3/4题与 BLQ p13/p14 题型一致（内容未改，索引已对齐）
93. Lec19-20 第7题与 p55/p56 一致
94. 交叉引用三类缺失仍为 0
95. 构建页数 158，内链通过
96. `check_exam_integration.py` 10 锚点 + 5 README 守卫
97. 临时 `_tmp_blq_*` 已删除（上一轮）
98. 维护文档 `BLQ_REVIEW_INTEGRATION.md` 与 JSON 索引同步
99. `INTEGRATION_FIX_LOG.md` 本文件归档 100 项
100. 后续建议：安装 Tesseract 后重跑 `extract_blq_review.py` 补 OCR 题号（**已由 Cursor 视觉读图替代**：52/52 稀疏页见 `blq_review_vision_transcripts.json`）

---

## 未改边界（刻意保留）

- 不发布 PDF 原文/整页截图
- 不虚构 Lec21 页面
- 不重构全站为教材 6 章导航（仅增映射层）
- 历史作业解答中 $Z_0=50\,\Omega$ 题面保留（Lec04 第4题等），符号导读已说明与 $Z_c$ 同义
