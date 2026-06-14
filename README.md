# hust-eic-microwave-review

《微波技术基础》复习资料，按“物理直觉 -> 数学公式 -> 题目解法 -> 常见误区”的顺序整理。

内容面向刚开始学习微波技术的读者：尽量先用图像解释传播、反射、匹配、波导中的场、谐振器和网络参数，再给出公式推导与作业题校验。

**在线站点**：<https://estelledc.github.io/hust-eic-microwave-from-scratch/>

## 内容入口

- [课程地图](content/index.md)：首页任务入口与快速导航。
- [阅读地图](content/guide/reading-map.md)：十轮读法与详细学习路线。
- [初学者手册](content/guide/beginner-handbook.md)：先补传输线、反射系数、Smith 圆图和波导的核心直觉。
- [知识点讲义](content/knowledge/README.md)：按传播、反射匹配、波导场、截止色散、矩形/圆波导、谐振器、网络参数和测量重排。
- [作业解答](content/solutions/index.md)：逐题给出思路图、公式推导、标准答案和易错点。
- [讲次与知识点矩阵](content/appendices/讲次-作业-教材章节-知识点矩阵.md)：用于查漏补缺。

## 阅读建议

1. 先看图，再看公式。微波题里的符号很多，但多数题都在回答同一个问题：波沿哪里走、哪里反射、参考面怎么换。
2. 公式不要孤立背。每个公式都要能说出它对应的物理画面，例如驻波比对应波腹/波节，Smith 圆图旋转对应沿线移动。
3. 做题时先归一化，再判断用阻抗还是导纳；涉及并联支节时通常先切到导纳视角。
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
python scripts/tools/check_exam_integration.py   # 改考前复习相关时
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
| `docs/` | 审计、维护、Agent 交接文档 |
| `.github/` | Pages 部署、PR 校验、Issue/PR 模板 |

详见 [docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md)。

## 贡献

欢迎 fork 后提 PR。默认 base 分支为 **`main`**。

| 文档 | 读者 |
|------|------|
| [CONTRIBUTING.md](CONTRIBUTING.md) | 人类贡献者：fork、分支、build、PR |
| [docs/good-first-issues.md](docs/good-first-issues.md) | 12 个入门任务（含验收标准） |
| [docs/MAINTAINERS.md](docs/MAINTAINERS.md) | 维护者：分支卫生、labels |

### 用 Agent 贡献

后继同学可用 Cursor / Codex 等接手小任务：

1. 让 Agent 阅读 [AGENTS.md](AGENTS.md)（详版：[docs/AGENTS.md](docs/AGENTS.md)）
2. 从 [docs/good-first-issues.md](docs/good-first-issues.md) 复制 **Agent prompt** 执行
3. 提交前走 [docs/PR_CHECKLIST.md](docs/PR_CHECKLIST.md)，再 `gh pr create --base main`

PR 模板：`.github/PULL_REQUEST_TEMPLATE.md` · CI：`.github/workflows/pr-check.yml`

### 设计参考

贡献流程设计来源与本地化说明：[docs/REFERENCES.md](docs/REFERENCES.md)

## 更多文档

- 站点调研：[docs/SITE_RESEARCH_AND_OPTIMIZATION.md](docs/SITE_RESEARCH_AND_OPTIMIZATION.md)
- 发布说明：[.github/PUBLISHING.md](.github/PUBLISHING.md)
