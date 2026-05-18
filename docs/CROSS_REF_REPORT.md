# 交叉引用健康度报告

由 `scripts/tools/check_cross_refs.py` 自动生成。

扫描结果：
- knowledge 单讲页面（不含 README/00/99）：29
- solutions 题目页面（不含 README/00/99）：37
- experiments 实验页面（不含 README/index/00/99）：8

## knowledge 页未引用任何 solutions / experiments 页

✅ 所有单讲页面都引到了至少一道作业或一个实验流程。

## solutions 题未引用任何 knowledge 页

✅ 所有作业题都引到了至少一节知识点。

## experiments 页未引用任何 knowledge 页

✅ 所有实验页都引到了至少一节知识点。

## 修复建议

- knowledge 单讲页缺反向链：通常在文末『作业怎么答』或『相关链接』段补 `../../solutions/.../第NN题.md` 或 `../../experiments/.../X.md`。
- solutions 题缺前置链：在题首『对应知识点』段补 `../../knowledge/.../NN-XXX.md`。
- experiments 页缺前置链：在题首『对应知识点』段补 `../../knowledge/.../NN-XXX.md`。
- 修复后重跑本脚本验证。
