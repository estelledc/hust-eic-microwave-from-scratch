# hust-eic-microwave-from-scratch

华中科技大学《微波技术基础》开放学习站点：按「物理直觉 → 数学公式 → 题目解法 → 常见误区」组织知识点、作业解答与实验模块。

面向自学者与后续维护者：内容可 fork 后提 PR 持续完善；站点经 GitHub Actions 发布到 Pages。

**在线站点**：<https://estelledc.github.io/hust-eic-microwave-from-scratch/>

## 学习者入口

- [课程地图](content/index.md)：首页任务入口与快速导航（由 `build.py` 生成）。
- [学习指南](content/guide/index.md)：阅读地图、课程复习索引、公式记忆与 Smith 圆图专题。
- [阅读地图](content/guide/reading-map.md)：十轮读法与按任务进入的详细路线。
- [初学者手册](content/guide/beginner-handbook.md)：传输线、反射系数、Smith 圆图与波导的核心直觉。
- [知识点讲义](content/knowledge/README.md)：8 阶段第一性原理路线。
- [作业解答](content/solutions/index.md)：逐题思路、公式推导、标准答案与易错点。
- [讲次与知识点矩阵](content/appendices/讲次-作业-教材章节-知识点矩阵.md)：Lec / 作业 / 教材章对照。

## 阅读建议

1. 先看图，再看公式。多数题在回答：波沿哪里走、哪里反射、参考面怎么换。
2. 公式不要孤立背。每个公式对应一个物理画面（驻波比 ↔ 波腹/波节，Smith 圆图旋转 ↔ 沿线移动）。
3. 做题先归一化，再判断用阻抗还是导纳；并联支节通常先切到导纳视角。
4. 波导题先判截止，再谈相速、群速、导波波长和单模范围。

## 本地预览

```bash
python -m pip install -r requirements.txt   # 首次
python build.py
python -m http.server -d site 8000        # http://localhost:8000
```

构建结果输出到 `site/`（不纳入 Git，由 CI 发布）。

常用检查：

```bash
python scripts/tools/check_cross_refs.py
python scripts/tools/check_exam_integration.py   # 改课程复习索引或公式入口时
python -m py_compile build.py scripts/plots/*.py scripts/tools/*.py
```

## 项目结构

| 路径 | 说明 |
|------|------|
| `content/` | Markdown 内容源（knowledge / solutions / guide / experiments） |
| `build.py` | 构建静态网页书 |
| `nav.json` | 侧栏短标题 |
| `scripts/plots/` | matplotlib 配图 → `assets/images/` |
| `scripts/tools/` | 交叉引用与维护脚本 |
| `docs/` | 维护、审计、Agent 交接文档 |
| `.github/` | Pages 部署、PR 校验、Issue/PR 模板 |

详见 [docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md)。

## 贡献与维护

欢迎 fork 后提 PR。默认 base 分支为 **`main`**。

| 文档 | 读者 |
|------|------|
| [CONTRIBUTING.md](CONTRIBUTING.md) | 人类贡献者：fork、分支、build、PR |
| [docs/good-first-issues.md](docs/good-first-issues.md) | **18** 个入门任务（P0/P1/P2 分层；含验收标准、Agent prompt；P0 已开 GitHub Issue） |
| [docs/MAINTAINERS.md](docs/MAINTAINERS.md) | 维护者：分支卫生、labels |
| [docs/AGENTS.md](docs/AGENTS.md) | Agent playbook（根 [AGENTS.md](AGENTS.md) 为快捷入口） |

### 用 Agent 贡献

1. 让 Agent 阅读 [AGENTS.md](AGENTS.md)（详版：[docs/AGENTS.md](docs/AGENTS.md)）
2. 从 [docs/good-first-issues.md](docs/good-first-issues.md) 复制 **Agent prompt** 执行
3. 提交前走 [docs/PR_CHECKLIST.md](docs/PR_CHECKLIST.md)，再 `gh pr create --base main`

PR 模板：`.github/PULL_REQUEST_TEMPLATE.md` · CI：`.github/workflows/pr-check.yml`

### 设计参考

贡献流程设计来源与本地化说明：[docs/REFERENCES.md](docs/REFERENCES.md)

## 更多文档

- 站点调研与可选优化：[docs/SITE_RESEARCH_AND_OPTIMIZATION.md](docs/SITE_RESEARCH_AND_OPTIMIZATION.md)
- 发布说明：[.github/PUBLISHING.md](.github/PUBLISHING.md)
