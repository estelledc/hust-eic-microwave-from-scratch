# 学习指南

面向初学者的学习路线与站点用法。第一次打开建议先读 [零基础学习手册](beginner-handbook.md)，再按知识点、作业和实验三条线交叉推进。

## 学习者入口

| 入口 | 适合解决什么问题 |
|---|---|
| [阅读地图](reading-map.md) | **十轮读法**（复习任务轴）、任务入口表、十分钟定位法 |
| [课程复习索引](exam-review.md) | 13 项核心考点、教材 6 章导航、公式速查与串讲习题入口 |
| [公式记忆专章](公式记忆/README.md) | 八阶段公式默写：参量释义、口诀、闭卷 checklist |
| [Smith 圆图专题](Smith圆图专题/README.md) | 六口诀读图、导纳/支节匹配、易错自检 |
| [零基础学习手册](beginner-handbook.md) | **十轮学习法**（零基础手册）；章节顺序、公式与实验衔接 |
| [知识点总览](../knowledge/README.md) | 传输线→波导→谐振器→网络→测量主线；含 **十轮深读地图** |
| [作业解答总览](../solutions/index.md) | 按讲次做题、查标准流程和常见误区 |
| [实验环节总览](../experiments/index.md) | VNA 读数 → 换算 → 结论 → 误差来源 |

## 维护者与贡献者

| 文档 | 用途 |
|------|------|
| [CONTRIBUTING.md](https://github.com/estelledc/hust-eic-microwave-from-scratch/blob/main/CONTRIBUTING.md) | Fork、分支、`build.py`、提 PR |
| [docs/good-first-issues.md](https://github.com/estelledc/hust-eic-microwave-from-scratch/blob/main/docs/good-first-issues.md) | 12 个入门任务（含 Agent prompt） |
| [docs/AGENTS.md](https://github.com/estelledc/hust-eic-microwave-from-scratch/blob/main/docs/AGENTS.md) | Agent playbook 与禁止事项 |
| [docs/PR_CHECKLIST.md](https://github.com/estelledc/hust-eic-microwave-from-scratch/blob/main/docs/PR_CHECKLIST.md) | 提交前逐步自检 |
| [docs/PROJECT_STATUS.md](https://github.com/estelledc/hust-eic-microwave-from-scratch/blob/main/docs/PROJECT_STATUS.md) | 目录职责、验证记录、待维护项 |

改 `content/guide/exam-review.md` 或串讲习题索引后，请跑 `python scripts/tools/check_exam_integration.py`。

## 三套「十轮」，先用哪张表？ {#三套十轮先用哪张表}

站点里有三套面向读者的十轮路线，**名称不同、不要混用**：

| 名称 | 入口 | 适合谁 | 第 10 轮在做什么 |
|------|------|--------|------------------|
| **十轮学习法** | [零基础学习手册](beginner-handbook.md#05-十轮学习法从零到能做题) | 第一次学微波 | 做谐振器/网络/测量综合题 |
| **十轮读法** | [阅读地图](reading-map.md#十轮读法复习任务轴) | 按任务复习全课 | 全课复盘（矩阵 + BLQ 查漏） |
| **十轮深读地图** | [知识点总览 · 十轮深读](../knowledge/README.md#十轮深读地图公式与工程) | 想把「看过」变成「会用」 | 画一张传输线→测量综合闭环图 |

维护文档里的「十轮内容优化」指 2026-06 站点内容审计轮次，**不是**上面三张读者用表；见仓库 `docs/AUDIT_NOTES.md`。

## 学习主轴与坐标系 {#learning-spine}

**推荐主轴**：按 [知识点 01–08 阶段](../knowledge/README.md) 推进（传播 → 反射 → 波导边界 → 色散 → 工程 → 多结构 → 测量 → 网络综合）。侧栏按内容类型分组，下列坐标系是同一内容的不同投影：

| 坐标系 | 何时用 | 入口 |
|--------|--------|------|
| **8 阶段知识点** | 建立物理图像、跟课主线 | [知识点总览](../knowledge/README.md) |
| **Lec01–Lec28** | 按讲次定位作业与串讲 | [讲次-作业-知识点矩阵](../appendices/讲次-作业-教材章节-知识点矩阵.md) |
| **作业 01–05** | 做题验算 | [作业解答总览](../solutions/index.md) |
| **串讲习题索引** | 电子板串讲与缺口大题 | [06-考前复习 · 串讲习题](../solutions/06-考前复习/README.md) |
| **教材 BLQ 6 章** | 按教材章复习 | [课程复习 · 6 章导航](exam-review.md#textbook-6ch-nav) |
| **公式记忆 01–05** | 闭卷默写 | [公式记忆专章](公式记忆/README.md) |

跨体系对照的站内胶水层是 **[讲次矩阵](../appendices/讲次-作业-教材章节-知识点矩阵.md)**（附录分组）；不必强行让文件夹编号与阶段编号一一对应，从第三次作业起以矩阵为准。

## 使用顺序

1. 先读 [零基础学习手册](beginner-handbook.md)，明确全课程路线。
2. 每学一章，先看知识点总览，再看对应作业。
3. 遇到仪器截图或实验报告，回到实验环节按「读数 → 换算 → 结论 → 误差来源」写。
4. 综合复习时读 [课程复习索引](exam-review.md)，刷 [串讲习题索引](../solutions/06-考前复习/README.md)，最后用各阶段 `99` 自检清单查漏。
