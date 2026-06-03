# hust-eic-microwave-review

《微波技术基础》复习资料，按“物理直觉 -> 数学公式 -> 题目解法 -> 常见误区”的顺序整理。

内容面向刚开始学习微波技术的读者：尽量先用图像解释传播、反射、匹配、波导中的场、谐振器和网络参数，再给出公式推导与作业题校验。

## 内容入口

- [学习首页](content/index.md)：从零开始的阅读顺序。
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

安装依赖后可构建静态页面：

```bash
.venv/bin/python build.py
```

构建结果会输出到 `site/`，其中的 `index.html` 可作为网页书入口。

常用检查：

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python - <<'PY'
import build
print(len(build.collect_pages()))
PY

python3 scripts/tools/check_cross_refs.py
```

站点调研和十轮优化记录见 [docs/SITE_RESEARCH_AND_OPTIMIZATION.md](docs/SITE_RESEARCH_AND_OPTIMIZATION.md)。
