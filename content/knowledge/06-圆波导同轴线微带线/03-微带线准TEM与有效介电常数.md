# 03 · 微带线准 TEM 与有效介电常数

---

## 本节先抓住一句话

微带线由"导体带 + 介质基片 + 接地板"组成。它的"主模"看起来像 TEM——电场基本横向、磁场基本横向——但因为**电磁场跨在两种介质里**（空气和基片介质），严格的 TEM 数学条件不成立。我们叫它**准 TEM**，并用一个等效相对介电常数 $\varepsilon_{\mathrm{eff}}$ 把它当 TEM 来近似处理。

---

## 为什么不能是纯 TEM

纯 TEM 模要求：所有沿 $z$ 方向传播的波，相速都等于该填充介质的 $1/\sqrt{\mu\varepsilon}$。

微带线场分布跨过两种介质：
- 上方空气：$\varepsilon=\varepsilon_0$，相速 $=c$。
- 下方基片：$\varepsilon=\varepsilon_r\varepsilon_0$，相速 $=c/\sqrt{\varepsilon_r}$。

如果硬要 TEM，那两个区域必须用不同的 $\beta$，但同一个模沿 $z$ 只能有一个 $\beta$。结论是：严格 TEM 在微带不可能存在，必须有少量纵向场分量 $E_z$、$H_z$（量级远小于横向）来"调和"两个区域，让最终的 $\beta$ 落在 $k_0$ 与 $k_0\sqrt{\varepsilon_r}$ 之间。

---

## 准 TEM 的工程定义

低频时（远低于第一个高阶模截止），微带主模的纵向场量很小，整体行为非常接近 TEM。我们把它定义为**准 TEM**：

- 横向场图像与 TEM 几乎一样，可以画"集中在带子下方介质中"的电力线。
- 沿 $z$ 的相速介于 $c/\sqrt{\varepsilon_r}$ 和 $c$ 之间。
- 把整个微带等效成一根均匀填充某种"等效介质"的传输线，这个等效介质的相对介电常数就是 $\varepsilon_{\mathrm{eff}}$。

---

## 等效相对介电常数 $\varepsilon_{\mathrm{eff}}$

定义：把准 TEM 模的实际相速映射到一个**均匀填充**的等效 TEM 线时所需的相对介电常数：

$$
v_{\mathrm p}=\frac{c}{\sqrt{\varepsilon_{\mathrm{eff}}}},
\qquad
\lambda=\frac{\lambda_0}{\sqrt{\varepsilon_{\mathrm{eff}}}}.
$$

物理边界：

$$
1<\varepsilon_{\mathrm{eff}}<\varepsilon_r.
$$

- 极限 1：场全在空气中（基片很薄、$\varepsilon_r$ 接近 1）。
- 极限 $\varepsilon_r$：场全在基片中（导体很宽 $W\gg h$，电力线"扁平"地集中在基片里）。

工程上常见的窄/宽情况：
- 窄带（$W/h$ 小）：$\varepsilon_{\mathrm{eff}}$ 偏小，趋近 $(\varepsilon_r+1)/2$。
- 宽带（$W/h$ 大）：$\varepsilon_{\mathrm{eff}}$ 偏大，趋近 $\varepsilon_r$。

常用工程近似（Hammerstad）：

$$
\varepsilon_{\mathrm{eff}}\approx\frac{\varepsilon_r+1}{2}+\frac{\varepsilon_r-1}{2}\,\frac{1}{\sqrt{1+12h/W}}.
$$

记不住推导没关系，记住"加权平均"的画面：$\varepsilon_{\mathrm{eff}}$ 是空气和基片对场的"占比加权平均"。

---

## 填充因子 $q$

把 $\varepsilon_{\mathrm{eff}}$ 写成线性插值：

$$
\varepsilon_{\mathrm{eff}}=1+q(\varepsilon_r-1),
\qquad
q=\frac{\varepsilon_{\mathrm{eff}}-1}{\varepsilon_r-1}.
$$

$q$ 称为**填充因子**，取值 $0<q<1$，代表"场在基片介质中所占的有效比例"：

- $q\to 0$：场几乎全在空气，$\varepsilon_{\mathrm{eff}}\to 1$。
- $q\to 1$：场几乎全在基片，$\varepsilon_{\mathrm{eff}}\to\varepsilon_r$。

实际微带常见 $q$ 在 0.5–0.9 之间。$W/h$ 越大，$q$ 越接近 1。

---

## 特性阻抗近似式

特性阻抗也可以用相同的"等效介质"想法写：先算"全空气线"的特性阻抗 $Z_{0,\mathrm{air}}$，再除以 $\sqrt{\varepsilon_{\mathrm{eff}}}$：

$$
Z_c=\frac{Z_{0,\mathrm{air}}}{\sqrt{\varepsilon_{\mathrm{eff}}}}.
$$

工程常用近似（Hammerstad，$W/h\le 1$）：

$$
Z_{0,\mathrm{air}}\approx 60\ln\!\left(\frac{8h}{W}+\frac{W}{4h}\right).
$$

$W/h\ge 1$ 时换另一支公式。具体推导和分支不强求，做题时直接查图或用 EM 仿真。

---

## 频率上限：色散与高阶模

微带准 TEM 的两个上限：

1. **色散开始变得不可忽略**：频率升高后，纵向场分量比例增加，$\varepsilon_{\mathrm{eff}}$ 不再是常数（弱色散）。常用判据是 $f<f_{\mathrm{T}}$，$f_{\mathrm{T}}$ 大致由基片厚度 $h$ 决定。
2. **激发高阶表面波模**：基片厚度足够时会出现 $\mathrm{TM}_0$、$\mathrm{TE}_1$ 等表面波模，截止频率近似

$$
f_{\mathrm c,\mathrm{TM}_0}\approx \frac{c\arctan(\varepsilon_r)}{\sqrt{2\pi h\sqrt{\varepsilon_r-1}}}\quad(\text{粗略量级估计})
$$

工程上微带电路通常在 $f<f_{\mathrm c,\mathrm{TM}_0}/2$ 工作以保留充足裕度。

---

## 易错点

1. 把准 TEM 当纯 TEM 用，套 $v_p=c/\sqrt{\varepsilon_r}$——错。应该套 $v_p=c/\sqrt{\varepsilon_{\mathrm{eff}}}$。
2. 把 $\varepsilon_{\mathrm{eff}}$ 当成与 $W$、$h$ 无关的纯材料量——它**与几何相关**，是有效场分布的加权。
3. 忘记 $1<\varepsilon_{\mathrm{eff}}<\varepsilon_r$ 的边界，算出 $\varepsilon_{\mathrm{eff}}>\varepsilon_r$ 或 $<1$ 一定是公式代错。
4. 把"准 TEM 没色散"当成结论——准 TEM **低频**近似无色散，但频率升高就有弱色散，且会激发表面波。

---

## Mini 自检

1. 为什么微带线主模不是严格 TEM？
2. 同样基片 $\varepsilon_r=2.2$，$W/h=1$ 和 $W/h=10$ 哪个 $\varepsilon_{\mathrm{eff}}$ 大？为什么？
3. 填充因子 $q=0.7$、$\varepsilon_r=4$，$\varepsilon_{\mathrm{eff}}$ 是多少？
4. $\varepsilon_{\mathrm{eff}}=2.5$、$\varepsilon_r=4$ 的微带，相速是 $c$ 的多少倍？

---

## 相关链接

- 上一节：[02 · 同轴线 TEM 与高阶模](02-同轴线TEM与高阶模.md)
- 下一节：[04 · 从矩形到圆与微带的对照](04-从矩形到圆与微带的对照.md)
- 作业：[第四次作业 · Lec19-20](../../solutions/04-后续专题/README.md) 第 8、9 题
- 对照纯 TEM：[同轴线 TEM](02-同轴线TEM与高阶模.md)
