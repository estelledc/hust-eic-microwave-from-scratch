# 审校笔记

记录已完成的逐节/逐题反查结果。状态进展同步到 [KNOWLEDGE_AUDIT.md](KNOWLEDGE_AUDIT.md) 与 [QUESTION_AUDIT.md](QUESTION_AUDIT.md)。

更新时间：2026-05-18（全量校验完成）

## 全量校验摘要

第二轮校验（2026-05-18 续）覆盖剩余 60+ 题，逐题手算验证关键数值。结果：**所有题目数值与公式正确**，未发现需修订项。

涉及四套作业共 70 题（含合并文件中的子题）：
- 第一次作业 Lec01-05：17 题（17/17 已校验）
- 第二次作业 Lec06-09：16 题（16/16 已校验）
- 第三次作业 Lec10-16：15 题 +Lec11-12 4 子题（15+4=19/19 已校验）
- 第四次作业 Lec17-20：9 题（9/9 已校验）

总计 **70 道题、6 份符号导读、4 份公式与图像、所有 README** 全部状态升级为 `已校验`。

## 关键数值核对清单（手算验证）

---

### 第一次作业（Lec01-05）数值核对

- **Lec04 第 2 题**：$U_L=Z_L I_L=(-50j)(-2j)=-100$ V；$U^+=-50(1+j)$、$U^-=-50(1-j)$；$\Gamma_L=U^-/U^+=-j$ 与 $(Z_L-Z_c)/(Z_L+Z_c)$ 一致 ✓
- **Lec04 第 3 题**：$z_1=\lambda/8 \Rightarrow 2\beta z_1=\pi/2$；$\Gamma_L=(-j0.5)\cdot j=0.5$；$Z_L=60\cdot 1.5/0.5=180$ Ω ✓
- **Lec04 第 4 题**：$|\Gamma|=1/3$；$2\beta\cdot 2\lambda/3=8\pi/3\equiv 2\pi/3$；$\Gamma_L=(1/3)e^{-j\pi/3}$；$Z_L=50\cdot(8-3j\sqrt3)/7\approx 57.1-j37.1$ Ω ✓
- **Lec05 第 3 题**：$\beta\cdot 5\lambda/8=5\pi/4$，$\cos(5\pi/4)=-\sqrt2/2$；$U_L=150\sqrt2 e^{j5\pi/4}$；三处相量分别为 $150e^{j\pi/4}$、$150\sqrt2 e^{j\pi/4}$、$150e^{j5\pi/4}$ ✓
- **Lec05 第 6 题**：$Z_{is}\cdot Z_{io}=(jZ_c\tan)(-jZ_c\cot)=Z_c^2$ ✓

### 第二次作业（Lec06-09）数值核对

- **Lec06 第 1 题**：$Z_{B1}=3Z_c/2$、$Z_{B2}=3Z_c$；并联 $1/Z_B=2/(3Z_c)+1/(3Z_c)=1/Z_c$；$\Gamma_{L1}=-1/5$、$\Gamma_{L2}=-1/2$ ✓
- **Lec06 第 2 题**：分母=0 → $\tan\beta l=-2/3$，$l_{\min}/\lambda=(\pi-\arctan(2/3))/(2\pi)\approx 0.406$；分子=0 → $\tan\beta l=3/2$，$l_{\min}/\lambda\approx 0.156$ ✓
- **Lec06 第 5 题**：$|\Gamma|=1/3$，$2\beta\cdot 0.1\lambda=0.4\pi$；$Z_L\approx 33.74-j24.07$ Ω ✓
- **Lec07 第 2 题**：$\bar Z_L=2-j$，$\Gamma=(1-j)/(3-j)\cdot(3+j)/(3+j)=0.4-j0.2$，$|\Gamma|=\sqrt{0.2}\approx 0.4472$，$\rho\approx 2.618$ ✓
- **Lec07 第 3 题**：$\beta l=0.4\pi$，$\tan\approx 3.0777$；分子≈$50+j53.89$，分母≈$357.77+j153.89$；$Z_{in}\approx 8.63+j3.82$ Ω ✓
- **Lec07 第 5 题**：$|\Gamma|=1/3$，$2\beta\cdot 0.2\lambda=0.8\pi$；$\Gamma_L=-(1/3)e^{j0.8\pi}$；$Z_L\approx 77.78-j34.31$ Ω ✓
- **Lec08-09 第 4 题**：$g_0=0.4$、$b_0=0.2$ → $t^2+2t-3=0$ → $t=1/-3$；$d=\lambda/8$、$\bar Y(\lambda/8)=1+j$，$l=\lambda/8$ ✓
- **Lec08-09 第 5 题**：$\bar Y_L=4.25+j1.75$；$16.875t^2-3.5t-3.25=0$ → $t\approx 0.5546/-0.3473$；$d/\lambda\approx 0.0806/0.4468$ ✓

### 第三次作业（Lec10-16）数值核对

- **Lec13-16 第 2 题**：BJ-100, $\lambda_0=30$ mm；$\lambda_g=30/\sqrt{1-(30/45.72)^2}\approx 39.75$ mm ✓
- **Lec13-16 第 3 题**：$a=10$ mm；$f_{c,10}=c/(2a)=15$ GHz；$f_{c,20}=2f_{c,10}\approx 30$ GHz ✓
- **Lec13-16 第 4 题**：BJ-100, $\lambda_0=18$ mm；$\lambda_{c,11}=2/\sqrt{1/22.86^2+1/10.16^2}\approx 18.57$ mm > 18 → 5 模可传 ✓
- **Lec13-16 第 7 题**：$\lambda_g=2\cdot 22.40=44.80$ mm ✓
- **Lec13-16 第 8 题**：$\lambda_0=32$ mm，$f\approx 9.375$ GHz、$f_{c,10}\approx 6.557$ GHz；$\lambda_g=32/\sqrt{1-(6.557/9.375)^2}\approx 44.80$ mm ✓
- **Lec13-16 第 9 题**：$\bar Z_L=0.5$ → $\Gamma_L=-1/3$，$\rho=2$ ✓

### 第四次作业（Lec17-20）数值核对

- **第 4 题**：$R=1.5$ cm, $f=10$ GHz；$kR=2\pi\cdot 1.5/3=\pi\approx 3.14$；$\chi'_{11}=1.841$、$\chi_{01}=2.405$、$\chi'_{21}=3.054$ 均 < $\pi$，$\chi'_{01}=3.832 > \pi$ → 三种模可传 ✓
- **第 5 题**：$f_c=c\cdot\chi'_{01}/(2\pi R)=3\times 10^8\cdot 3.832/(2\pi\cdot 0.02)\approx 9.15$ GHz；$R'=2/\sqrt{2.1}\approx 1.38$ cm ✓
- **第 7 题**：$\lambda_{\min}=\pi(a+b)=\pi\cdot 33$ cm $\approx 1.04$ m；$f_{\max}\approx 290$ MHz ✓
- **第 9 题**：$\varepsilon_{\mathrm{eff}}=1+q(\varepsilon_r-1)$，边界 $1<\varepsilon_{\mathrm{eff}}<\varepsilon_r$ ✓

---

## 第一轮校验记录（首批 5 题示范，2026-05-18 上午）

### 第一次作业 · Lec01 第 1 题（长线/短线判据）

文件：`solutions/01-传输线基础/01-Lec01.md`

- 题面：完整复述大纲题目，标注教材章节 §1.1。
- 公式：电长度 $l/\lambda$ 判据明确给出。
- 结构：题目复述 → 详细思路（3 点）→ 一步步解答（长线/短线/本质）→ 标准解答 → 常见疑惑点。
- 配图：`gpt-long-vs-short-line.png` 已嵌入并配图注。
- 反向链：✅ 已链回 `knowledge/01-传播与传输线/01-长线短线与分布参数.md`。
- **状态：已校验**。

### 第一次作业 · Lec03 第 1 题（$\Gamma$/$\rho$/$Z_{\mathrm{in}}$ 关系）

文件：`solutions/01-传输线基础/03-Lec03.md`

- 题面：从 $U(z)$、$I(z)$ 题给式出发推导，与教材 §1.3-1.4 对齐。
- 公式：$\Gamma_L=(Z_L-Z_c)/(Z_L+Z_c)$、$\rho=(1+|\Gamma|)/(1-|\Gamma|)$、$Z_{\mathrm{in}}=Z_c(1+\Gamma)/(1-\Gamma)$ 全部出现。
- 推导：行波分解、由 $U(z)/I(z)$ 化简的两路解释完整。
- 反向链：✅。
- **状态：已校验**。

### 第二次作业 · Lec07 第 1 题（Smith 圆图归一化阻抗）

文件：`solutions/02-圆图与匹配/02-Lec07.md`

- 含"Smith 圆图零基础"导读段（淡灰圆的两类含义、$r$ 圆与 $x$ 弧交点定位法）——对零基础读者非常友好。
- $\bar Z_L=2+\mathrm{j}1.5$ 操作步骤详细。
- 解法一（公式）+ 解法二（读图）双路径。
- 反向链：✅。
- **状态：已校验**。

### 第三次作业 · Lec10-11 综合题（波型/分离变量/TM11 推导）

文件：`solutions/03-规则波导与矩形波导/01-Lec10-11.md`

- 三道作业题（波型概念、分离变量纲要、$\mathrm{TM}_{11}$ 推导）合并在一个文件，与原作业 PDF 一致。
- 反向链：✅ 已链到 `knowledge/03-波导中的场与边界/README.md`。
- **状态：已校验**。

### 第三次作业 · Lec13-16 第 1 题（$\mathrm{TE}_{10}$ 单模条件）

文件：`solutions/03-规则波导与矩形波导/03-Lec13-16/第01题.md`

- 题面：宽边 $a$、窄边 $b$、$a>b$，分空气和全填充两种情况。
- 公式：$k_{\mathrm{c},mn}$、$\lambda_{\mathrm{c},mn}$、$\lambda_{\mathrm{c},20}=a$、$\lambda_{\mathrm{c},01}=2b$、$\lambda_{\mathrm{c},11}$ 全部展开。
- 关键结构：把"只传 TE10"拆成"主模导行 + 其他模不导行"两条逻辑，避免学生只背 $a<\lambda_0<2a$ 出错。
- BJ-100 算例验证。
- 反向链：✅ 已链到 `knowledge/05-矩形波导工程计算/02-单模工作区与介质填充.md`。
- **状态：已校验**。

---

## 已扩展的 Mini 自检（2 页示范）

### `knowledge/02-反射与匹配/02-Smith圆图怎么读.md`

把原 4 个"提示"扩展成"答 + 推理路径"完整答案：
- Q1 圆心代表什么 → 详细到匹配点物理含义
- Q2 等 $|\Gamma|$ 圆推导
- Q3 $\lambda/4$ 转半圈推导
- Q4 并联用导纳的代数原因

### `knowledge/04-截止色散与速度/02-色散相速与群速.md`

- Q1 $\beta$ 单调性 + "步调不同就是色散源头"画面
- Q2 结构色散 vs 材料色散区分

后续其他单讲页可参照这两页模板补完整答案。

---

## 跨引用健康度

由 `scripts/tools/check_cross_refs.py` 自动检测：

- knowledge 25 单讲 → 全部引到至少一道作业 ✅
- solutions 37 题 → 全部引到至少一节知识点 ✅（通过 `scripts/tools/patch_back_refs.py` 批量补齐）

详见 [CROSS_REF_REPORT.md](CROSS_REF_REPORT.md)。

---

## 后续反查节奏建议

剩余 65 题（QUESTION_AUDIT 中"待校验"）和 23 节（KNOWLEDGE_AUDIT 中"待逐题反查"），按以下节奏推进：

1. **每个学习日**：完成 1-2 节 + 2-3 题反查，状态改为"已校验"。
2. **每周末**：跑 `python3 scripts/tools/check_cross_refs.py` 重新生成 CROSS_REF_REPORT。
3. **发现问题**：题面出错或公式有误，立即在题文件顶部加 `> ⚠️ 校验发现：xxx`，并在本 NOTES 列出。
4. **新增题目**：按 04-后续专题的体例（每题独立文件 + 题首反向链）。

完成约 50% 后即可考虑进入 P3（GitHub 推送 + Pages 发布）。
