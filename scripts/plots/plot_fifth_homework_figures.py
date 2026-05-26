"""Generate teaching figures for 第五次作业 Lec22-Lec28."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
FIG = ROOT / "assets" / "images"
C0 = 3.0e8
A_BJ = 22.86e-3


def set_cn_font() -> None:
    plt.rcParams["font.sans-serif"] = [
        "Microsoft YaHei",
        "SimHei",
        "Noto Sans CJK SC",
        "Arial Unicode MS",
        "Heiti TC",
        "DejaVu Sans",
    ]
    plt.rcParams["axes.unicode_minus"] = False


def save(fig: plt.Figure, name: str) -> Path:
    FIG.mkdir(parents=True, exist_ok=True)
    path = FIG / name
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def box(ax: plt.Axes, xy: tuple[float, float], w: float, h: float, text: str, fc: str = "#f2f6ff") -> None:
    rect = patches.FancyBboxPatch(
        xy,
        w,
        h,
        boxstyle="round,pad=0.04,rounding_size=0.04",
        linewidth=1.1,
        edgecolor="#31415f",
        facecolor=fc,
    )
    ax.add_patch(rect)
    ax.text(xy[0] + w / 2, xy[1] + h / 2, text, ha="center", va="center", fontsize=9)


def arrow(ax: plt.Axes, start: tuple[float, float], end: tuple[float, float], text: str = "") -> None:
    ax.annotate("", xy=end, xytext=start, arrowprops=dict(arrowstyle="->", lw=1.3, color="#31415f"))
    if text:
        ax.text((start[0] + end[0]) / 2, (start[1] + end[1]) / 2 + 0.05, text, ha="center", fontsize=8)


def q22_01() -> Path:
    fig, ax = plt.subplots(figsize=(7.8, 3.8))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.set_title("第5次 Lec22-23 第1题：矩形腔 / 圆柱腔 模式指标", fontsize=12)

    ax.add_patch(patches.Rectangle((0.6, 1.1), 3.2, 2.1, fill=False, lw=1.8, ec="#2a6fbb"))
    ax.plot([1.65, 1.65], [1.1, 3.2], "--", color="#2a6fbb", lw=1)
    ax.plot([2.7, 2.7], [1.1, 3.2], "--", color="#2a6fbb", lw=1)
    ax.plot([0.6, 3.8], [2.15, 2.15], ":", color="#2a6fbb", lw=1)
    ax.text(2.2, 3.5, "矩形腔", ha="center", fontsize=10, weight="bold")
    ax.text(2.2, 0.55, "m: a方向半波数\nn: b方向半波数\np: l方向半波数", ha="center", fontsize=9)
    ax.annotate("a", (3.95, 2.15), (4.55, 2.15), arrowprops=dict(arrowstyle="<->", color="#2a6fbb"), fontsize=9)
    ax.annotate("b", (0.6, 3.45), (0.6, 3.2), arrowprops=dict(arrowstyle="->", color="#2a6fbb"), fontsize=9)
    ax.annotate("l", (3.2, 3.0), (4.35, 3.75), arrowprops=dict(arrowstyle="->", color="#2a6fbb"), fontsize=9)

    center = (7.2, 2.2)
    ax.add_patch(patches.Circle(center, 1.15, fill=False, lw=1.8, ec="#bb5a2a"))
    for r in [0.38, 0.75]:
        ax.add_patch(patches.Circle(center, r, fill=False, lw=0.8, ec="#bb5a2a", ls="--"))
    for ang in np.linspace(0, 2 * np.pi, 8, endpoint=False):
        ax.plot([center[0], center[0] + 1.15 * np.cos(ang)], [center[1], center[1] + 1.15 * np.sin(ang)], color="#bb5a2a", lw=0.7, alpha=0.6)
    ax.text(7.2, 3.5, "圆柱腔", ha="center", fontsize=10, weight="bold")
    ax.text(7.2, 0.45, "m: 角向阶数\nn: 径向贝塞尔根序号\np: 轴向半波数", ha="center", fontsize=9)
    return save(fig, "fifth_lec22_q01_mode_indices.webp")


def q22_02() -> Path:
    l = np.linspace(0.010, 0.050, 500)
    f = C0 / 2 * np.sqrt((1 / A_BJ) ** 2 + (1 / l) ** 2) / 1e9
    def length_for(freq_ghz: float) -> float:
        return 1 / np.sqrt((2 * freq_ghz * 1e9 / C0) ** 2 - (1 / A_BJ) ** 2)
    l10 = length_for(10)
    l12 = length_for(12)
    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.plot(l * 1e3, f, color="#2a6fbb", lw=2)
    ax.axhline(10, ls="--", color="#4e8f4b")
    ax.axhline(12, ls="--", color="#bb5a2a")
    ax.axvline(l10 * 1e3, ls="--", color="#4e8f4b")
    ax.axvline(l12 * 1e3, ls="--", color="#bb5a2a")
    ax.annotate("", xy=(l12 * 1e3, 11.12), xytext=(l10 * 1e3, 11.12), arrowprops=dict(arrowstyle="<->", lw=1.3))
    ax.text(
        (l10 + l12) * 500,
        11.48,
        "活塞向内移动约 5.0 mm",
        ha="center",
        fontsize=9,
        bbox=dict(boxstyle="round,pad=0.18", facecolor="white", edgecolor="none", alpha=0.8),
    )
    ax.text(l10 * 1e3 + 0.4, 9.6, "10 GHz\nl≈19.9 mm", fontsize=8)
    ax.text(l12 * 1e3 + 0.4, 12.2, "12 GHz\nl≈14.9 mm", fontsize=8)
    ax.set_xlabel("腔长 l (mm)")
    ax.set_ylabel("TE101 谐振频率 (GHz)")
    ax.set_title("第5次 Lec22-23 第2题：TE101 腔长与短路活塞调谐", fontsize=12)
    ax.grid(True, alpha=0.25)
    return save(fig, "fifth_lec22_q02_te101_tuning.webp")


def q22_03() -> Path:
    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.set_title("第5次 Lec22-23 第3题：圆柱腔谐振波长的两项来源", fontsize=12)
    box(ax, (0.4, 2.9), 2.2, 1.0, "TE011\nχ'01=3.832\np=1", "#fff4e8")
    box(ax, (3.9, 2.9), 2.2, 1.0, "TE111\nχ'11=1.841\np=1", "#fff4e8")
    box(ax, (7.0, 2.9), 2.2, 1.0, "TM010\nχ01=2.405\np=0", "#fff4e8")
    for x in [1.5, 5.0, 8.1]:
        arrow(ax, (x, 2.85), (x, 2.1))
    box(ax, (0.55, 1.0), 2.0, 0.82, "横向根项\n(χ/R)^2\n+\n轴向项\n(π/l)^2", "#f2f6ff")
    box(ax, (4.05, 1.0), 2.0, 0.82, "横向根项\n(χ/R)^2\n+\n轴向项\n(π/l)^2", "#f2f6ff")
    box(ax, (7.15, 1.0), 2.0, 0.82, "只有横向根项\n(2.405/R)^2", "#f2f6ff")
    ax.text(5, 0.25, r"$\lambda_r=2\pi/\sqrt{k_c^2+(p\pi/l)^2}$", ha="center", fontsize=13)
    return save(fig, "fifth_lec22_q03_cylindrical_resonance.webp")


def q22_04() -> Path:
    fig, ax = plt.subplots(figsize=(7.6, 3.7))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.set_title("第5次 Lec22-23 第4题：Q0 推导路线", fontsize=12)
    box(ax, (0.35, 3.0), 2.0, 0.9, "TE101 场型\nEy, Hx, Hz", "#eaf4ff")
    box(ax, (3.0, 3.0), 2.0, 0.9, "体积分\n储能 W", "#eaf4ff")
    box(ax, (5.65, 3.0), 2.1, 0.9, "壁面积分\nPc=Rs/2∮|Ht|²dS", "#fff4e8")
    box(ax, (8.2, 3.0), 1.45, 0.9, "Q0=ωW/Pc", "#edf8ed")
    for x1, x2 in [(2.35, 3.0), (5.0, 5.65), (7.75, 8.2)]:
        arrow(ax, (x1, 3.45), (x2, 3.45))

    ax.add_patch(patches.Rectangle((2.0, 0.75), 5.5, 1.35, fill=False, lw=1.7, ec="#31415f"))
    ax.add_patch(patches.Rectangle((2.0, 0.75), 5.5, 1.35, fill=False, lw=8, ec="#bb5a2a", alpha=0.18))
    ax.text(4.75, 1.42, "六个金属壁面的切向 H 场产生导体损耗", ha="center", fontsize=10)
    ax.text(4.75, 0.25, r"$R_s=\omega\mu\delta/2$，因此 $\delta$ 越小，$Q_0$ 越高", ha="center", fontsize=10)
    return save(fig, "fifth_lec22_q04_q_wall_loss.webp")


def q24_01() -> Path:
    fig, ax = plt.subplots(figsize=(7.8, 3.6))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.set_title("第5次 Lec24 第1题：Z 矩阵 vs S 矩阵", fontsize=12)
    box(ax, (0.6, 2.7), 3.7, 1.4, "Z 矩阵\nV = Z I\n开路条件定义\nZ11, Z22: 输入阻抗\nZ21, Z12: 转移阻抗", "#fff4e8")
    box(ax, (5.7, 2.7), 3.7, 1.4, "S 矩阵\nb = S a\n匹配负载条件定义\nS11, S22: 反射\nS21, S12: 传输", "#eaf4ff")
    arrow(ax, (4.35, 3.4), (5.65, 3.4), "高频测量更常用")
    ax.text(5, 1.15, "端口参考面固定后，矩阵元素才有明确物理含义", ha="center", fontsize=11)
    return save(fig, "fifth_lec24_q01_z_s_matrix_meaning.webp")


def q24_02() -> Path:
    fig, ax = plt.subplots(figsize=(7.2, 3.5))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.set_title("第5次 Lec24 第2题：三类网络条件不要混淆", fontsize=12)
    box(ax, (0.5, 2.65), 2.4, 1.25, "无耗\nS†S=I\n功率守恒", "#edf8ed")
    box(ax, (3.8, 2.65), 2.4, 1.25, "互易\nS12=S21\n传输对称", "#eaf4ff")
    box(ax, (7.0, 2.65), 2.4, 1.25, "对称\nS11=S22\n端口互换不变", "#fff4e8")
    ax.text(5, 1.35, "三者是不同条件：无耗≠互易，互易≠端口匹配，对称≠无损", ha="center", fontsize=11)
    return save(fig, "fifth_lec24_q02_network_properties.webp")


def q24_03() -> Path:
    fig, ax = plt.subplots(figsize=(7.5, 2.8))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3)
    ax.set_title("第5次 Lec24 第3题：理想匹配传输线的 S 矩阵", fontsize=12)
    ax.plot([1.2, 8.8], [1.5, 1.5], color="#2a6fbb", lw=5, solid_capstyle="round")
    ax.text(1.0, 1.95, "端口1\n匹配", ha="center", fontsize=9)
    ax.text(9.0, 1.95, "端口2\n匹配", ha="center", fontsize=9)
    arrow(ax, (1.35, 1.9), (8.55, 1.9), r"$e^{-j\beta l}$")
    arrow(ax, (8.55, 1.1), (1.35, 1.1), r"$e^{-j\beta l}$")
    ax.text(5, 0.25, r"$S_{11}=S_{22}=0,\quad S_{21}=S_{12}=e^{-j\beta l}$", ha="center", fontsize=12)
    return save(fig, "fifth_lec24_q03_transmission_line_smatrix.webp")


def q24_04() -> Path:
    fig, ax = plt.subplots(figsize=(8.0, 3.8))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.set_title("第5次 Lec24 第4题：三负载法", fontsize=12)
    box(ax, (0.45, 2.7), 2.0, 1.1, "T2 短路\nΓ2=-1\n测 Γ1s", "#fff4e8")
    box(ax, (3.0, 2.7), 2.0, 1.1, "T2 开路\nΓ2=+1\n测 Γ1o", "#fff4e8")
    box(ax, (5.55, 2.7), 2.0, 1.1, "T2 匹配\nΓ2=0\n测 Γ1c", "#edf8ed")
    box(ax, (7.9, 2.7), 1.65, 1.1, "联立\n求 S11,S22\n和 Δ", "#eaf4ff")
    for x1, x2 in [(2.45, 3.0), (5.0, 5.55), (7.55, 7.9)]:
        arrow(ax, (x1, 3.25), (x2, 3.25))
    ax.text(5, 1.25, r"$\Gamma_1=\dfrac{S_{11}-\Delta\Gamma_2}{1-S_{22}\Gamma_2},\quad \Delta=S_{11}S_{22}-S_{12}^2$", ha="center", fontsize=12)
    return save(fig, "fifth_lec24_q04_three_load_method.webp")


def q24_05() -> Path:
    fig, ax = plt.subplots(figsize=(7.8, 3.6))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.set_title("第5次 Lec24 第5题：两次加载测量反求 S 矩阵", fontsize=12)
    box(ax, (0.6, 2.8), 3.6, 1.15, "正向测量\n1端激励，2端接 ΓLa\n测 Γa, Ta", "#eaf4ff")
    box(ax, (5.8, 2.8), 3.6, 1.15, "反向测量\n2端激励，1端接 ΓLa\n测 Γb, Tb", "#eaf4ff")
    ax.text(5, 1.65, r"$T_a=\dfrac{S_{21}}{1-S_{22}L},\quad T_b=\dfrac{S_{12}}{1-S_{11}L}$", ha="center", fontsize=12)
    ax.text(5, 0.85, r"先由 $\Gamma_a,\Gamma_b,T_aT_b,L$ 求 $S_{11},S_{22}$，再回代求 $S_{21},S_{12}$", ha="center", fontsize=10)
    return save(fig, "fifth_lec24_q05_loaded_two_port_retrieval.webp")


def q25_01() -> Path:
    fig, ax = plt.subplots(figsize=(8, 3.7))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.set_title("第5次 Lec25-26 第1题：按端口数组织常用微波元件", fontsize=12)
    labels = [
        ("一端口\n负载/短路/电抗\n看 S11", 0.45, "#fff4e8"),
        ("二端口\n衰减器/滤波器\n看 S11,S21,S22", 2.9, "#eaf4ff"),
        ("三端口\n功分器/T结\n看分配与隔离", 5.35, "#edf8ed"),
        ("四端口\n耦合器/环行器\n看 C,I,D", 7.8, "#f5edff"),
    ]
    for text, x, color in labels:
        box(ax, (x, 1.55), 1.8, 1.7, text, color)
    return save(fig, "fifth_lec25_q01_component_ports.webp")


def q25_02() -> Path:
    fig, ax = plt.subplots(figsize=(7.5, 3.6))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.set_title("第5次 Lec25-26 第2题：定向耦合器 C / I / D", fontsize=12)
    ax.add_patch(patches.Rectangle((2.0, 2.35), 5.8, 0.35, color="#2a6fbb", alpha=0.75))
    ax.add_patch(patches.Rectangle((2.0, 1.35), 5.8, 0.35, color="#bb5a2a", alpha=0.75))
    ax.text(1.45, 2.55, "1 输入", ha="right", fontsize=9)
    ax.text(8.05, 2.55, "3 直通", ha="left", fontsize=9)
    ax.text(1.45, 1.55, "4 隔离", ha="right", fontsize=9)
    ax.text(8.05, 1.55, "2 耦合", ha="left", fontsize=9)
    arrow(ax, (2.2, 2.9), (7.5, 2.9), "主线")
    arrow(ax, (7.2, 1.1), (4.2, 1.1), "耦合端")
    ax.text(5, 0.35, r"$C=20.5\,dB,\ I=43\,dB,\ D=I-C=22.5\,dB$", ha="center", fontsize=12)
    return save(fig, "fifth_lec25_q02_coupler_metrics.webp")


def q25_03() -> Path:
    fig, ax = plt.subplots(figsize=(7.8, 3.7))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.set_title("第5次 Lec25-26 第3题：Wilkinson 功分器", fontsize=12)
    ax.plot([1.5, 4.1], [2.5, 2.5], color="#2a6fbb", lw=4)
    ax.plot([4.1, 7.2], [2.5, 3.55], color="#2a6fbb", lw=4)
    ax.plot([4.1, 7.2], [2.5, 1.45], color="#2a6fbb", lw=4)
    ax.plot([7.2, 7.2], [1.45, 3.55], color="#bb5a2a", lw=2)
    ax.text(1.25, 2.5, "1", ha="right", va="center", fontsize=11)
    ax.text(7.45, 3.55, "2\n-3.4 dB", va="center", fontsize=9)
    ax.text(7.45, 1.45, "3\n-3.7 dB", va="center", fontsize=9)
    ax.text(5.6, 3.25, r"$\sqrt{2}Z_0$", fontsize=10)
    ax.text(5.6, 1.65, r"$\sqrt{2}Z_0$", fontsize=10)
    ax.text(7.35, 2.45, r"$R=2Z_0$", fontsize=10)
    ax.text(5, 0.45, "幅度偏差 0.3 dB；附加插损 0.4 dB / 0.7 dB", ha="center", fontsize=11)
    return save(fig, "fifth_lec25_q03_wilkinson_metrics.webp")


def q25_04() -> Path:
    x = np.linspace(0, 10, 400)
    fig, axs = plt.subplots(1, 3, figsize=(8.5, 3.0), sharey=True)
    for ax in axs:
        ax.set_ylim(-35, 2)
        ax.set_xlabel("f")
        ax.grid(True, alpha=0.25)
    axs[0].plot(x, -10 + 0 * x, color="#2a6fbb", lw=2)
    axs[0].set_title("衰减器\nS21≈常数", fontsize=10)
    axs[1].plot(x, -1 + 0 * x, color="#2a6fbb", lw=2)
    axs[1].set_title("移相器\n看 ∠S21", fontsize=10)
    axs[2].plot(x, -30 + 29 * np.exp(-((x - 5) / 2.0) ** 6), color="#2a6fbb", lw=2)
    axs[2].set_title("滤波器\n通带/阻带", fontsize=10)
    axs[0].set_ylabel("S 参数幅度 (dB)")
    fig.suptitle("第5次 Lec25-26 第4题：二端口元件不能只看 S21，还要看 S11/S22", fontsize=12)
    return save(fig, "fifth_lec25_q04_two_port_metrics.webp")


def q25_05() -> Path:
    fig, ax = plt.subplots(figsize=(7.4, 3.5))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.set_title("第5次 Lec25-26 第5题：非互易的 S 矩阵特征", fontsize=12)
    box(ax, (0.7, 2.8), 2.8, 1.05, "隔离器\nS21≈1\nS12≈0", "#eaf4ff")
    arrow(ax, (0.95, 2.35), (3.2, 2.35), "正向通过")
    arrow(ax, (3.2, 1.95), (0.95, 1.95), "反向隔离")
    ax.text(5.1, 2.45, r"$S_{ij}\ne S_{ji}$", fontsize=16, ha="center")
    center = (8.0, 2.35)
    ax.add_patch(patches.Circle(center, 0.95, fill=False, lw=1.6, ec="#bb5a2a"))
    for ang0, ang1 in [(110, 10), (230, 130), (350, 250)]:
        r = 0.95
        ax.annotate("", xy=(center[0] + r * np.cos(np.deg2rad(ang1)), center[1] + r * np.sin(np.deg2rad(ang1))),
                    xytext=(center[0] + r * np.cos(np.deg2rad(ang0)), center[1] + r * np.sin(np.deg2rad(ang0))),
                    arrowprops=dict(arrowstyle="->", color="#bb5a2a", lw=1.2))
    ax.text(8.0, 0.85, "环行器：1→2→3→1", ha="center", fontsize=9)
    return save(fig, "fifth_lec25_q05_nonreciprocal.webp")


def q27_01() -> Path:
    fig, ax = plt.subplots(figsize=(6.5, 3.4))
    vals = [0.50, 0.10, 1.22]
    labels = ["Pout/Pin\n(S21=-3dB)", "|Γ|\n(S11=-20dB)", "SWR ρ"]
    colors = ["#2a6fbb", "#bb5a2a", "#4e8f4b"]
    ax.bar(labels, vals, color=colors, alpha=0.8)
    ax.set_ylim(0, 1.45)
    ax.set_title("第5次 Lec27-28 第1题：dB 读数换算", fontsize=12)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.04, f"{v:.2f}", ha="center", fontsize=10)
    ax.grid(axis="y", alpha=0.25)
    return save(fig, "fifth_lec27_q01_db_conversion.webp")


def q27_02() -> Path:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.2, 3.5))
    theta = np.linspace(0, 2 * np.pi, 400)
    ax1.plot(np.cos(theta), np.sin(theta), color="#31415f")
    ax1.scatter([1, -1, 0], [0, 0, 0], c=["#bb5a2a", "#2a6fbb", "#4e8f4b"], s=70)
    ax1.text(1.08, 0, "开路", fontsize=9)
    ax1.text(-1.38, 0, "短路", fontsize=9)
    ax1.text(0.08, 0.08, "匹配", fontsize=9)
    ax1.set_aspect("equal")
    ax1.axis("off")
    ax1.set_title("Smith 圆图", fontsize=10)
    states = ["开路", "短路", "匹配"]
    vals = [0, 0, -25]
    ax2.bar(states, vals, color=["#bb5a2a", "#2a6fbb", "#4e8f4b"])
    ax2.set_ylim(-30, 3)
    ax2.axhline(0, color="gray", lw=0.8)
    ax2.set_ylabel("S11 (dB)")
    ax2.set_title("S11 对数幅度", fontsize=10)
    fig.suptitle("第5次 Lec27-28 第2题：开路/短路/匹配的典型表现", fontsize=12)
    return save(fig, "fifth_lec27_q02_smith_open_short_match.webp")


def q27_03() -> Path:
    f0, f1, f2 = 1.50, 1.485, 1.512
    f = np.linspace(1.45, 1.55, 600)
    q = f0 / (f2 - f1)
    p = 1 / (1 + 4 * q**2 * ((f - f0) / f0) ** 2)
    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.plot(f, 10 * np.log10(p), color="#2a6fbb", lw=2)
    ax.axhline(-3, ls="--", color="#bb5a2a", label="-3 dB")
    for x, lab in [(f1, "f1=1.485"), (f0, "f0=1.50"), (f2, "f2=1.512")]:
        ax.axvline(x, ls=":", color="#31415f")
        ax.text(x, -18, lab, rotation=90, va="bottom", ha="right", fontsize=8)
    ax.set_xlabel("频率 (GHz)")
    ax.set_ylabel("相对峰值 (dB)")
    ax.set_title("第5次 Lec27-28 第3题：3 dB 带宽法 QL≈55.6", fontsize=12)
    ax.grid(True, alpha=0.25)
    return save(fig, "fifth_lec27_q03_q_bandwidth.webp")


def q27_04() -> Path:
    fig, ax = plt.subplots(figsize=(8.0, 3.8))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.set_title("第5次 Lec27-28 第4题：二端口 VNA 测四端口耦合器", fontsize=12)
    box(ax, (0.5, 3.0), 1.5, 0.7, "VNA P1", "#eaf4ff")
    box(ax, (0.5, 1.4), 1.5, 0.7, "VNA P2", "#eaf4ff")
    ax.add_patch(patches.Rectangle((4.0, 1.45), 2.2, 1.8, fill=False, lw=1.6, ec="#31415f"))
    ax.text(5.1, 2.35, "定向耦合器", ha="center", fontsize=10)
    ax.text(3.55, 2.35, "1", fontsize=10)
    ax.text(6.35, 2.9, "3\n50Ω", fontsize=9)
    ax.text(6.35, 1.75, "2/4\n接VNA或50Ω", fontsize=8)
    arrow(ax, (2.0, 3.35), (4.0, 2.6), "激励")
    arrow(ax, (2.0, 1.75), (4.0, 1.8), "测耦合/隔离")
    ax.text(5, 0.45, "未测端口全部接 50Ω，否则反射会污染 S 参数读数", ha="center", fontsize=10)
    return save(fig, "fifth_lec27_q04_vna_coupler_setup.webp")


def q27_05() -> Path:
    fig, ax = plt.subplots(figsize=(8.0, 3.4))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.set_title("第5次 Lec27-28 第5题：课程主线关系", fontsize=12)
    box(ax, (0.35, 1.5), 1.65, 0.9, "特性阻抗\nZ0", "#fff4e8")
    box(ax, (2.65, 1.5), 1.65, 0.9, "反射系数\nΓ", "#eaf4ff")
    box(ax, (4.95, 1.5), 1.65, 0.9, "S 参数\nSij", "#edf8ed")
    box(ax, (7.25, 1.5), 2.0, 0.9, "VNA 读数\ndB/相位/Smith", "#f5edff")
    arrow(ax, (2.0, 1.95), (2.65, 1.95), "失配")
    arrow(ax, (4.3, 1.95), (4.95, 1.95), "端口化")
    arrow(ax, (6.6, 1.95), (7.25, 1.95), "显示")
    ax.text(5, 0.55, r"$\Gamma=(Z_L-Z_0)/(Z_L+Z_0)$，$S_{11}$ 是输入反射，$S_{21}$ 是传输波幅比", ha="center", fontsize=10)
    return save(fig, "fifth_lec27_q05_course_chain.webp")


def main() -> None:
    set_cn_font()
    makers = [
        q22_01,
        q22_02,
        q22_03,
        q22_04,
        q24_01,
        q24_02,
        q24_03,
        q24_04,
        q24_05,
        q25_01,
        q25_02,
        q25_03,
        q25_04,
        q25_05,
        q27_01,
        q27_02,
        q27_03,
        q27_04,
        q27_05,
    ]
    for maker in makers:
        print("wrote", maker())


if __name__ == "__main__":
    main()
