# 第四次作业 · Lec19-20（同轴线与微带线）

**导航：** [作业总目录](../README.md) · [符号与导读](../00-符号与导读.md) · [Lec17–18 圆波导](../01-Lec17-18-圆波导/README.md) · **Lec19–20** · [**7**](第07题.md) · [**8**](第08题.md) · [**9**](第09题.md)

---

**对应大纲**：Lec19–Lec20，同轴线与微带线。

同轴线是双导体均匀填充结构，**主模 TEM 无截止**；高阶 \(\mathrm{TE}_{11}\) 的截止波长近似

$$
\lambda_{\mathrm c,\mathrm{TE}_{11}}\approx \pi(a+b).
$$

微带线半填充（导体带 + 介质基片 + 接地板），主模为**准 TEM**，用等效相对介电常数描述：

$$
\beta=k_0\sqrt{\varepsilon_{\mathrm{eff}}},
\qquad
v_{\mathrm p}=\frac{c}{\sqrt{\varepsilon_{\mathrm{eff}}}},
\qquad
\varepsilon_{\mathrm{eff}}=1+q(\varepsilon_r-1).
$$

知识点详见 [knowledge/06 · 02 同轴线 TEM 与高阶模](../../../knowledge/06-圆波导同轴线微带线/02-同轴线TEM与高阶模.md) 与 [03 微带线准 TEM 与有效介电常数](../../../knowledge/06-圆波导同轴线微带线/03-微带线准TEM与有效介电常数.md)。

---

## 第 7 题：同轴只传 TEM 的条件与最短工作波长

- **要点**：要求所有高次模截止，即 \(\lambda_0>\lambda_{\mathrm c,\mathrm{TE}_{11}}\approx \pi(a+b)\)；\(a=5\) cm、\(b=5.6a=28\) cm 时 \(\lambda_{\min}\approx 1.04\) m，\(f_{\max}\approx 290\) MHz。
- **完整版**：[第07题](第07题.md)

---

## 第 8 题：微带准 TEM 与纵向场分量证明

- **要点**：反证法——若严格 TEM 则空气区 \(\beta=k_0\) 与介质区 \(\beta=k_0\sqrt{\varepsilon_r}\) 必须同时满足，\(\varepsilon_r\ne 1\) 时矛盾，故必有 \(E_z\ne 0\) 或 \(H_z\ne 0\)。
- **完整版**：[第08题](第08题.md)

---

## 第 9 题：等效相对介电常数与填充因子

- **要点**：\(\varepsilon_{\mathrm{eff}}=(\beta/k_0)^2=(c/v_{\mathrm p})^2=(\lambda_0/\lambda_{\mathrm g})^2\)；填充因子 \(q=(\varepsilon_{\mathrm{eff}}-1)/(\varepsilon_r-1)\in(0,1)\)；\(\varepsilon_{\mathrm{eff}}=1+q(\varepsilon_r-1)\) 是空气与介质的加权平均。
- **完整版**：[第09题](第09题.md)
