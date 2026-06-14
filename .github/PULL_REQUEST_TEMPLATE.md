## 变更类型

请勾选（可多选）：

- [ ] `content` — 知识点 / 作业解答 / guide / 实验正文
- [ ] `docs` — CONTRIBUTING、AGENTS、维护文档
- [ ] `scripts/plots` — 配图脚本
- [ ] `scripts/tools` — 检查/维护脚本
- [ ] `fix` — build、nav、链接、CI
- [ ] `nav` — `nav.json` 侧栏标题
- [ ] `assets` — 图片/样式（非 plot 自动生成）

## 关联 Issue

- Closes #<!-- 编号，无则删 -->
- Related to #<!-- 可选 -->

## 变更摘要

<!-- 用 1–3 句话说明改了什么、为什么 -->

## 自检清单

合并前请确认（与 [CONTRIBUTING.md](../CONTRIBUTING.md) 一致）：

- [ ] `python build.py` 成功
- [ ] `python scripts/tools/check_cross_refs.py` — 三类缺失均为 0
- [ ] 若改考前复习/公式入口：`python scripts/tools/check_exam_integration.py`
- [ ] 若改 Python：`python -m py_compile build.py scripts/plots/*.py scripts/tools/*.py`
- [ ] 新增/改名 Markdown 时已检查 `nav.json`
- [ ] 图片路径在 `assets/images/` 或 `assets/illustrations/`
- [ ] 未提交 `site/` 构建产物
- [ ] 中文排版与课程符号口径一致（$Z_c$、Smith 圆图、TE/TM 等）
- [ ] 未删除已有 content 正文（仅增补/修正）

## 预览说明（若改 content）

<!-- 例如：本地 http://localhost:8000/content/guide/Smith圆图专题/01-六口诀读图.html -->

- 预览方式：
- 建议 review 页面：

## 截图（可选）

<!-- 侧栏、公式渲染、配图变更时可附截图 -->

## 备注

<!-- Agent 贡献请注明使用了 docs/AGENTS.md 中哪条 playbook -->
