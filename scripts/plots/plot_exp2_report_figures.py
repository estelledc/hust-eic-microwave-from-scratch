"""实验二《微波元件特性参数测量》报告配图生成。

生成 6 张图到 微波实验2/media/：
  原理示意：fig_q_halfpower / fig_coupler_ports / fig_wilkinson
  接法示意：fig_setup_resonator / fig_setup_coupler / fig_setup_divider

从 repo 根运行：python scripts/plots/plot_exp2_report_figures.py
所有标签用中文（Microsoft YaHei / SimHei），数学符号用 LaTeX。
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np

# 中文字体：优先 Microsoft YaHei，回退 SimHei
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "SimSun"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["mathtext.fontset"] = "cm"

OUT = Path(__file__).resolve().parents[2] / "微波实验2" / "media"
OUT.mkdir(parents=True, exist_ok=True)
DPI = 170

BLUE = "#1f5fb0"
ORANGE = "#e07b1a"
GREEN = "#2a8a4a"
GREY = "#555555"


def save(fig, name: str) -> None:
    p = OUT / name
    fig.savefig(p, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", p)


# ---------------------------------------------------------------------------
# 1) 半功率点法谐振曲线示意
# ---------------------------------------------------------------------------
def draw_q_halfpower():
    f0 = 1.0
    # 用洛伦兹型构造 |S21| 谐振峰（dB），峰值 A0，3dB 带宽给定
    A0 = -3.0          # 峰值幅度 (dB)，示意
    bw = 0.18          # 3dB 带宽（归一化）
    f = np.linspace(f0 - 0.6, f0 + 0.6, 1200)
    # 功率传输：P/Pmax = 1/(1+(2Q(f-f0)/f0)^2)，令半功率半宽=bw/2
    half = bw / 2.0
    power_ratio = 1.0 / (1.0 + ((f - f0) / half) ** 2)
    s21 = A0 + 10 * np.log10(power_ratio)

    f1, f2 = f0 - half, f0 + half
    a3 = A0 - 3.0

    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    ax.plot(f, s21, color=BLUE, lw=2.4, label=r"$|S_{21}|$ 谐振曲线")

    # 峰值点
    ax.plot([f0], [A0], "o", color=ORANGE, ms=7, zorder=5)
    ax.annotate(r"峰值 $A_0$  ($f_0$)", xy=(f0, A0), xytext=(f0 + 0.06, A0 + 1.2),
                fontsize=11, color=ORANGE,
                arrowprops=dict(arrowstyle="->", color=ORANGE))

    # -3dB 水平线
    ax.axhline(a3, color=GREEN, ls="--", lw=1.4)
    ax.text(f0 - 0.58, a3 + 0.3, r"半功率线：峰值 $-3\,$dB", color=GREEN, fontsize=10.5)

    # f1 f2 垂直线
    for fx, lbl in [(f1, r"$f_1$"), (f2, r"$f_2$")]:
        ax.plot([fx, fx], [a3, -22], color=GREY, ls=":", lw=1.3)
        ax.plot([fx], [a3], "o", color=GREEN, ms=5, zorder=5)
        ax.text(fx, -22.8, lbl, ha="center", fontsize=12, color=GREY)

    # 带宽双箭头
    ax.annotate("", xy=(f1, a3 - 1.6), xytext=(f2, a3 - 1.6),
                arrowprops=dict(arrowstyle="<->", color="black", lw=1.6))
    ax.text(f0, a3 - 2.9, r"$\Delta f_{3\mathrm{dB}}=f_2-f_1$", ha="center", fontsize=12)

    # Q 公式
    ax.text(f0 - 0.585, -7.5, r"$Q_L=\dfrac{f_0}{\Delta f_{3\mathrm{dB}}}$",
            fontsize=15, color=BLUE,
            bbox=dict(boxstyle="round,pad=0.35", fc="#eaf1fb", ec=BLUE))

    ax.set_xlabel("频率 $f$（归一化，峰值居中 $f_0$）", fontsize=11)
    ax.set_ylabel(r"$|S_{21}|$  (dB)", fontsize=11)
    ax.set_title("半功率点法：3 dB 带宽与有载品质因数 $Q_L$", fontsize=12.5)
    ax.set_ylim(-24, 2)
    ax.set_xticks([f1, f0, f2])
    ax.set_xticklabels([r"$f_1$", r"$f_0$", r"$f_2$"], fontsize=11)
    ax.grid(True, alpha=0.25)
    ax.legend(loc="upper right", fontsize=10)
    plt.tight_layout()
    save(fig, "fig_q_halfpower.png")


# ---------------------------------------------------------------------------
# 2) 定向耦合器四端口原理图
# ---------------------------------------------------------------------------
def draw_coupler_ports():
    fig, ax = plt.subplots(figsize=(7.6, 4.4))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis("off")

    # 主线（下）与副线（上），耦合段 x in [3.5, 8.5]
    xl, xr = 1.0, 11.0
    y_main, y_aux = 2.3, 4.3
    cx0, cx1 = 3.5, 8.5

    # 主线
    ax.plot([xl, xr], [y_main, y_main], color=BLUE, lw=3)
    # 副线
    ax.plot([xl, xr], [y_aux, y_aux], color=ORANGE, lw=3)
    # 耦合段高亮（两线靠近）
    ax.add_patch(patches.Rectangle((cx0, y_main + 0.15), cx1 - cx0, y_aux - y_main - 0.3,
                                   fill=True, fc="#f4f4f4", ec="#bbbbbb", ls="--", lw=1.2, zorder=0))
    ax.text((cx0 + cx1) / 2, (y_main + y_aux) / 2, r"$\lambda/4$ 平行耦合段",
            ha="center", va="center", fontsize=11, color=GREY)

    # 端口标记
    def port(x, y, num, name, color, dx):
        ax.plot([x], [y], "o", color=color, ms=9, zorder=5)
        ax.text(x + dx, y + 0.35, f"端口{num}", ha="center", fontsize=11, fontweight="bold")
        ax.text(x + dx, y - 0.55, name, ha="center", fontsize=10.5, color=color)

    port(xl, y_main, 1, "输入", BLUE, 0.0)
    port(xr, y_main, 3, "直通", BLUE, 0.0)
    port(xl, y_aux, 4, "隔离", GREY, 0.0)
    port(xr, y_aux, 2, "耦合", ORANGE, 0.0)

    # 主线功率流箭头
    ax.annotate("", xy=(2.6, y_main), xytext=(1.4, y_main),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.2))
    ax.annotate("", xy=(10.5, y_main), xytext=(9.3, y_main),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.2))
    # 耦合到副线（指向端口2方向）
    ax.annotate("", xy=(9.3, y_aux), xytext=(8.0, y_aux),
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=2.2))
    # 电/磁耦合叠加（耦合段中部竖直箭头）
    for xx in (5.0, 6.5):
        ax.annotate("", xy=(xx, y_aux - 0.2), xytext=(xx, y_main + 0.2),
                    arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.6))
    ax.text(5.75, y_main + 0.05 + (y_aux - y_main) / 2 - 1.05, "电耦合 + 磁耦合\n（同向叠加 → 定向）",
            ha="center", va="top", fontsize=9.5, color=GREEN)

    # 隔离端弱信号
    ax.text(xl + 0.0, y_aux + 0.95, r"$P_4\approx 0$（隔离）", ha="left", fontsize=9.5, color=GREY)

    ax.set_title("平行耦合线定向耦合器：四端口约定与定向耦合机理", fontsize=12.5)
    plt.tight_layout()
    save(fig, "fig_coupler_ports.png")


# ---------------------------------------------------------------------------
# 3) Wilkinson 功分器拓扑
# ---------------------------------------------------------------------------
def draw_wilkinson():
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis("off")

    xin = 1.2
    xnode = 4.0
    xout = 9.6
    y0 = 4.0
    yup, ydn = 5.8, 2.2

    # 输入线
    ax.plot([xin, xnode], [y0, y0], color=BLUE, lw=3)
    ax.plot([xin], [y0], "o", color=BLUE, ms=9, zorder=5)
    ax.text(xin, y0 + 0.5, "端口1", ha="center", fontsize=11, fontweight="bold")
    ax.text(xin, y0 - 0.7, "输入", ha="center", fontsize=10.5, color=BLUE)
    ax.annotate("", xy=(2.6, y0), xytext=(1.5, y0),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.2))

    # 分叉到两臂
    ax.plot([xnode, xnode], [ydn, yup], color="black", lw=2)
    # 上臂 λ/4
    ax.plot([xnode, xout], [yup, yup], color=ORANGE, lw=3)
    # 下臂 λ/4
    ax.plot([xnode, xout], [ydn, ydn], color=GREEN, lw=3)

    # λ/4 标注
    for yy, col in [(yup, ORANGE), (ydn, GREEN)]:
        ax.text((xnode + xout) / 2, yy + 0.35, r"$\lambda/4$ 臂，$Z=\sqrt{2}\,Z_0$",
                ha="center", fontsize=10.5, color=col)

    # 输出端口
    for yy, num, name, col in [(yup, 2, "输出", ORANGE), (ydn, 3, "输出", GREEN)]:
        ax.plot([xout], [yy], "o", color=col, ms=9, zorder=5)
        ax.text(xout + 0.5, yy + 0.35, f"端口{num}", ha="center", fontsize=11, fontweight="bold")
        ax.text(xout + 0.5, yy - 0.55, name, ha="center", fontsize=10.5, color=col)

    # 隔离电阻 R=2Z0 跨接两输出
    xr = xout + 1.6
    ax.plot([xout, xr], [yup, yup], color=GREY, lw=2)
    ax.plot([xout, xr], [ydn, ydn], color=GREY, lw=2)
    # 电阻框
    ax.add_patch(patches.Rectangle((xr - 0.28, (yup + ydn) / 2 - 0.9), 0.56, 1.8,
                                   fill=True, fc="white", ec=GREY, lw=2))
    ax.plot([xr, xr], [yup, (yup + ydn) / 2 + 0.9], color=GREY, lw=2)
    ax.plot([xr, xr], [ydn, (yup + ydn) / 2 - 0.9], color=GREY, lw=2)
    ax.text(xr + 0.45, (yup + ydn) / 2, r"$R=2Z_0$", ha="left", va="center",
            fontsize=12, color=GREY)
    ax.text(xr + 0.45, (yup + ydn) / 2 - 0.95, "隔离电阻", ha="left", va="center",
            fontsize=9.5, color=GREY)

    ax.text(xnode + 0.1, y0 - 1.15, "功分点", ha="left", fontsize=9.5, color="black")
    ax.set_title("两路等分 Wilkinson 功分器拓扑（理论各臂 $-3\\,$dB）", fontsize=12.5)
    plt.tight_layout()
    save(fig, "fig_wilkinson.png")


# ---------------------------------------------------------------------------
# 通用：VNA 接法图
# ---------------------------------------------------------------------------
def _vna_box(ax, x, y, w, h):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                fill=True, fc="#eef3fb", ec=BLUE, lw=2))
    ax.text(x + w / 2, y + h - 0.5, "矢量网络分析仪 AV36580", ha="center", fontsize=11,
            fontweight="bold", color=BLUE)
    # 两个端口在底边
    p1 = (x + w * 0.28, y)
    p2 = (x + w * 0.72, y)
    for (px, py), lbl in [(p1, "端口1"), (p2, "端口2")]:
        ax.plot([px], [py], "o", color=BLUE, ms=9, zorder=6)
        ax.text(px, py + 0.35, lbl, ha="center", fontsize=10, color=BLUE)
    return p1, p2


def _dut_box(ax, x, y, w, h, label, fc="#fdf2e6", ec=ORANGE):
    ax.add_patch(patches.Rectangle((x, y), w, h, fill=True, fc=fc, ec=ec, lw=2))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=11,
            fontweight="bold")


def _load(ax, x, y, label="50 Ω\n匹配负载"):
    ax.add_patch(patches.Rectangle((x - 0.55, y - 0.45), 1.1, 0.9, fill=True,
                                   fc="#eef7ef", ec=GREEN, lw=1.8))
    ax.text(x, y, label, ha="center", va="center", fontsize=8.5, color=GREEN)


def draw_setup_resonator():
    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis("off")
    p1, p2 = _vna_box(ax, 1.0, 4.2, 8.0, 2.4)
    # DUT 谐振器
    dx, dy, dw, dh = 3.2, 1.0, 3.6, 1.2
    _dut_box(ax, dx, dy, dw, dh, "微带谐振器")
    in_pt = (dx, dy + dh / 2)
    out_pt = (dx + dw, dy + dh / 2)
    ax.text(dx - 0.1, dy + dh + 0.3, "①入", ha="right", fontsize=9, color=GREY)
    ax.text(dx + dw + 0.1, dy + dh + 0.3, "②出", ha="left", fontsize=9, color=GREY)
    # 连线 VNA端口1->入, VNA端口2->出
    ax.plot([p1[0], p1[0], in_pt[0]], [p1[1], in_pt[1], in_pt[1]], color="black", lw=1.8)
    ax.plot([p2[0], p2[0], out_pt[0]], [p2[1], out_pt[1], out_pt[1]], color="black", lw=1.8)
    ax.set_title("装置图一　微带谐振器 $Q$ 值测量连接（测 $S_{21}$）", fontsize=12)
    plt.tight_layout()
    save(fig, "fig_setup_resonator.png")


def draw_setup_coupler():
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7.5)
    ax.axis("off")
    p1, p2 = _vna_box(ax, 1.0, 4.8, 9.0, 2.4)
    # 定向耦合器（四端口方块）
    dx, dy, dw, dh = 3.0, 1.2, 3.0, 2.0
    _dut_box(ax, dx, dy, dw, dh, "定向\n耦合器")
    tl = (dx, dy + dh * 0.7)        # 端口1 输入(左上)
    bl = (dx, dy + dh * 0.3)        # 端口4 隔离(左下)
    tr = (dx + dw, dy + dh * 0.7)   # 端口2 耦合(右上)
    br = (dx + dw, dy + dh * 0.3)   # 端口3 直通(右下)
    ax.text(dx - 0.1, tl[1], "1", ha="right", va="center", fontsize=9, color=GREY)
    ax.text(dx - 0.1, bl[1], "4", ha="right", va="center", fontsize=9, color=GREY)
    ax.text(dx + dw + 0.1, tr[1], "2", ha="left", va="center", fontsize=9, color=GREY)
    ax.text(dx + dw + 0.1, br[1], "3", ha="left", va="center", fontsize=9, color=GREY)
    # VNA端口1 -> 端口1输入
    ax.plot([p1[0], p1[0], tl[0]], [p1[1], tl[1], tl[1]], color="black", lw=1.8)
    # VNA端口2 -> 端口2耦合(待测端)
    ax.plot([p2[0], p2[0], tr[0]], [p2[1], tr[1], tr[1]], color="black", lw=1.8)
    # 其余端口接 50Ω
    _load(ax, br[0] + 1.2, br[1])
    ax.plot([br[0], br[0] + 0.65], [br[1], br[1]], color="black", lw=1.6)
    _load(ax, bl[0] - 1.2, bl[1])
    ax.plot([bl[0] - 0.65, bl[0]], [bl[1], bl[1]], color="black", lw=1.6)
    ax.set_title("装置图二　定向耦合器测量连接（待测端测 $S_{21}$，余端接 50 Ω）", fontsize=11.5)
    plt.tight_layout()
    save(fig, "fig_setup_coupler.png")


def draw_setup_divider():
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7.5)
    ax.axis("off")
    p1, p2 = _vna_box(ax, 1.0, 4.8, 9.0, 2.4)
    # 功分器（三端口）
    dx, dy, dw, dh = 3.2, 1.2, 3.0, 2.0
    _dut_box(ax, dx, dy, dw, dh, "功率\n分配器")
    inp = (dx, dy + dh / 2)            # 端口1 输入(左)
    o2 = (dx + dw, dy + dh * 0.72)     # 端口2 输出(右上)
    o3 = (dx + dw, dy + dh * 0.28)     # 端口3 输出(右下)
    ax.text(dx - 0.1, inp[1], "1", ha="right", va="center", fontsize=9, color=GREY)
    ax.text(dx + dw + 0.1, o2[1], "2", ha="left", va="center", fontsize=9, color=GREY)
    ax.text(dx + dw + 0.1, o3[1], "3", ha="left", va="center", fontsize=9, color=GREY)
    # VNA端口1 -> 输入
    ax.plot([p1[0], p1[0], inp[0]], [p1[1], inp[1], inp[1]], color="black", lw=1.8)
    # VNA端口2 -> 端口2(待测支路)
    ax.plot([p2[0], p2[0], o2[0]], [p2[1], o2[1], o2[1]], color="black", lw=1.8)
    # 端口3 接 50Ω
    _load(ax, o3[0] + 1.2, o3[1])
    ax.plot([o3[0], o3[0] + 0.65], [o3[1], o3[1]], color="black", lw=1.6)
    ax.set_title("装置图三　功率分配器测量连接（测 $S_{21}$，未测支路接 50 Ω）", fontsize=11.5)
    plt.tight_layout()
    save(fig, "fig_setup_divider.png")


def main():
    draw_q_halfpower()
    draw_coupler_ports()
    draw_wilkinson()
    draw_setup_resonator()
    draw_setup_coupler()
    draw_setup_divider()
    print("ALL figures done ->", OUT)


if __name__ == "__main__":
    main()
