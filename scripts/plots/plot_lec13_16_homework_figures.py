# -*- coding: utf-8 -*-
"""Generate assets/images/lec13_16_q01..q12_*.webp for 第三次作业 Lec13-16 分题."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
FIG = ROOT / "assets" / "images"

# Physical constants
C0 = 299_792_458.0
# BJ-100 / WR-90 (m)
A_BJ = 22.86e-3
B_BJ = 10.16e-3


def _set_cn_font() -> None:
    plt.rcParams["font.sans-serif"] = [
        "Microsoft YaHei",
        "SimHei",
        "Noto Sans CJK SC",
        "Arial Unicode MS",
        "DejaVu Sans",
    ]
    plt.rcParams["axes.unicode_minus"] = False


def kc_mn(a: float, b: float, m: int, n: int) -> float:
    return np.sqrt((m * np.pi / a) ** 2 + (n * np.pi / b) ** 2)


def lam_c_mn(a: float, b: float, m: int, n: int) -> float:
    k = kc_mn(a, b, m, n)
    return 2 * np.pi / k


def f_c_mn(a: float, b: float, m: int, n: int) -> float:
    return C0 * kc_mn(a, b, m, n) / (2 * np.pi)


def fig_q01() -> Path:
    """Schematic: single-mode (TE10 only) window on lambda0 (BJ-100 example)."""
    a, b = A_BJ, B_BJ
    lc10 = lam_c_mn(a, b, 1, 0)
    lc20 = lam_c_mn(a, b, 2, 0)
    lc01 = lam_c_mn(a, b, 0, 1)
    lc11 = lam_c_mn(a, b, 1, 1)
    lo = max(lc20, lc01, lc11)
    hi = lc10
    x0, x1 = 0, 55e-3
    fig, ax = plt.subplots(figsize=(7.5, 2.2))
    ax.hlines(0, x0, x1, color="k", linewidth=0.5)
    ax.fill_betweenx([-0.15, 0.15], lo, hi, color="C0", alpha=0.35, label="仅 TE10 开区间(示意,BJ-100)")
    for x, lab, c in [
        (lc10, r"$\lambda_{c,10}$", "C1"),
        (lo, r"max lower", "C2"),
    ]:
        ax.axvline(x * 1e3, color=c, linestyle="--", alpha=0.7)
    ax.set_xlim(x0 * 1e3, x1 * 1e3)
    ax.set_ylim(-0.22, 0.22)
    ax.set_xlabel("lambda0 (mm)")
    ax.set_yticks([])
    ax.set_title("题1: 主模能传 且 竞争模全截止 -> lambda0 落在阴影区(例: BJ-100)", fontsize=10)
    ax.legend(loc="upper right", fontsize=7)
    path = FIG / "lec13_16_q01_single_mode_window.webp"
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def fig_q02() -> Path:
    """TE10 dispersion + 10 GHz marker (BJ-100)."""
    a = A_BJ
    fc = C0 / (2 * a)
    f = 10e9
    r0 = f / fc
    r = np.linspace(1.001, 2.5, 500)
    lam0_over_lamg = np.sqrt(1 - 1 / r**2)
    vp_over_c = r * lam0_over_lamg
    vg_over_c = 1 / vp_over_c
    fig, ax1 = plt.subplots(figsize=(7, 4))
    ax1.plot(r, 1 / lam0_over_lamg, color="C0", label=r"$\lambda_g/\lambda_0$")
    ax1.set_xlabel(r"$f/f_{c,\mathrm{TE10}}$")
    ax1.set_ylabel(r"$\lambda_g/\lambda_0$", color="C0")
    ax1.axvline(r0, color="red", lw=1.2, label=f"10 GHz, r={r0:.2f}")
    ax1.grid(True, alpha=0.3)
    ax2 = ax1.twinx()
    ax2.plot(r, vp_over_c, color="C1", linestyle="--", label=r"$v_p/c$")
    ax2.plot(r, vg_over_c, color="C2", linestyle=":", label=r"$v_g/c$")
    ax2.set_ylabel(r"$v_p/c,\ v_g/c$")
    lines1, l1 = ax1.get_legend_handles_labels()
    lines2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, l1 + l2, loc="upper right", fontsize=8)
    fig.suptitle("题2: TE10 色散(空气无耗) 与 10 GHz 工作点", fontsize=10)
    path = FIG / "lec13_16_q02_te10_dispersion.webp"
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def fig_q03() -> Path:
    a, b = 10e-3, 6e-3
    names = [r"TE$_{10}$", r"TE$_{20}$", r"TE$_{21}$"]
    fcs = [f_c_mn(a, b, 1, 0), f_c_mn(a, b, 2, 0), f_c_mn(a, b, 2, 1)]
    fcs_ghz = [f / 1e9 for f in fcs]
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.bar(names, fcs_ghz, color=["C0", "C1", "C2"])
    ax.set_ylabel("f_c (GHz)")
    ax.set_title("题3: 10x6 mm^2 截止频率(空气)", fontsize=10)
    for i, v in enumerate(fcs_ghz):
        ax.text(i, v + 0.8, f"{v:.2f}", ha="center", fontsize=8)
    path = FIG / "lec13_16_q03_fc_bar.webp"
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def fig_q04() -> Path:
    a, b = A_BJ, B_BJ
    lam0 = 18e-3
    modes = [("TE10", lam_c_mn(a, b, 1, 0)), ("TE20", lam_c_mn(a, b, 2, 0)), ("TE01", lam_c_mn(a, b, 0, 1)), ("TE11", lam_c_mn(a, b, 1, 1))]
    x = [m[1] * 1e3 for m in modes]
    labels = [m[0] for m in modes]
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.barh(labels, x, color="C0", alpha=0.7)
    ax.axvline(lam0 * 1e3, color="red", lw=2, label="lambda0=18 mm")
    ax.set_xlabel("lambda_c (mm)")
    ax.set_title("题4: 各模 lambda_c 与 18mm 比较(均>18 则可导行)", fontsize=10)
    ax.legend()
    path = FIG / "lec13_16_q04_modes_on_axis.webp"
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def fig_q05() -> Path:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.2))
    a1, b1 = A_BJ, B_BJ
    lc1 = lam_c_mn(a1, b1, 1, 0)
    a2, b2 = 72.14e-3, 34.04e-3
    lc2 = lam_c_mn(a2, b2, 1, 0)
    for ax, Lc, title in [(ax1, lc1 * 1e3, "(1) BJ-100"), (ax2, lc2 * 1e3, "(2) 大截面")]:
        ax.barh([r"TE$_{10}$ $ \lambda_c$"], [Lc], color="C0", height=0.35)
        for lam_cm, name in [
            (10, "10 cm"),
            (8, "8 cm"),
            (3.2, "3.2 cm"),
            (2, "2 cm"),
        ]:
            ax.axvline(lam_cm, color="gray", alpha=0.4, ls="--")
        ax.set_xlabel("wavelength (cm) ~ compare with lambda0")
        ax.set_title(title, fontsize=9)
    fig.suptitle("题5: 工作波长 与 主模 截止尺度 对照(示意)", fontsize=10)
    path = FIG / "lec13_16_q05_two_wgs.webp"
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def fig_q06() -> Path:
    a, b = A_BJ, B_BJ
    lc10 = lam_c_mn(a, b, 1, 0)
    lc20 = lam_c_mn(a, b, 2, 0)
    lo, hi = lc20, lc10
    fig, ax = plt.subplots(figsize=(7.5, 2.2))
    ax.hlines(0, 0, 50, color="k", linewidth=0.5)
    ax.fill_betweenx([-0.12, 0.12], lo * 1e3, hi * 1e3, color="C0", alpha=0.4)
    ax.set_xlim(0, 50)
    ax.set_ylim(-0.18, 0.18)
    ax.set_xlabel("lambda0 (mm)")
    ax.set_yticks([])
    ax.set_title("题6: BJ-100 只传 TE10 的 波长 窗(22.86..45.72 mm, 开区间 按课程)", fontsize=10)
    path = FIG / "lec13_16_q06_single_mode_bj100.webp"
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def fig_q07() -> Path:
    d_node = 22.4e-3
    lam_g = 2 * d_node
    z = np.linspace(0, 1.2 * lam_g, 500)
    beta = 2 * np.pi / lam_g
    env = np.abs(np.cos(beta * z))
    fig, ax = plt.subplots(figsize=(7, 2.8))
    ax.plot(z * 1e3, env, "C0", lw=1.5, label="|E| 驻波包络(示意)")
    for k in range(3):
        zn = (k + 0.5) * (lam_g / 2)
        if zn <= z[-1]:
            ax.axvline(zn * 1e3, color="C3", ls="--", alpha=0.6)
    ax.set_xlabel("z (mm)")
    ax.set_ylabel("幅值(归一)")
    ax.set_title("题7: 相邻 波节 距 = lambda_g/2  ->  lambda_g = 2*22.4 mm", fontsize=10)
    path = FIG / "lec13_16_q07_standing_wave.webp"
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def fig_q08() -> Path:
    fig, ax = plt.subplots(figsize=(6.5, 2.0))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 1.4)
    ax.axis("off")
    ax.text(0.2, 0.9, "Load", ha="left", fontsize=9)
    ax.text(3.0, 0.9, "---- 等效 无耗 线 (TE10, beta) ---->", fontsize=9, color="C0")
    ax.text(2.0, 0.45, "Screw: shunt b", ha="center", fontsize=8, color="C1", bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.4))
    ax.annotate(
        "",
        xy=(1.0, 0.85),
        xytext=(3.0, 0.85),
        arrowprops=dict(arrowstyle="->", color="C0", lw=1.5),
    )
    ax.annotate(
        "",
        xy=(6.0, 0.85),
        xytext=(9.0, 0.85),
        arrowprops=dict(arrowstyle="->", color="C0", lw=1.5),
    )
    ax.text(8.2, 0.9, "向源", fontsize=9)
    ax.text(0.2, 0.15, "题8: 驻波+第一波节+并联 螺钉 调匹配(示意, z 以课程/导读为准)", fontsize=8, wrap=True)
    path = FIG / "lec13_16_q08_stub_match.webp"
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def fig_q09() -> Path:
    fig, ax = plt.subplots(figsize=(4.5, 3.2))
    ax.bar([r"$\rho$", r"$|\Gamma_L|$"], [2, 1 / 3], color=["C0", "C1"], width=0.5)
    ax.set_ylabel("无量纲")
    ax.set_title("题9: 归一化 Z_L=0.5  ->  |Gamma| 与 驻波比", fontsize=10)
    ax.set_ylim(0, 2.3)
    for i, v in enumerate([2, 1 / 3]):
        ax.text(i, v + 0.05, f"{v:.3f}" if i else f"{v:.1f}", ha="center", fontsize=9)
    path = FIG / "lec13_16_q09_gamma_rho.webp"
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def fig_q10() -> Path:
    a, b = 72.14e-3, 34.04e-3
    f = 6e9
    lam0 = C0 / f
    spec = [("TE10", lam_c_mn(a, b, 1, 0)), ("TE20", lam_c_mn(a, b, 2, 0)), ("TE01", lam_c_mn(a, b, 0, 1)), ("TE11", lam_c_mn(a, b, 1, 1)), ("TM11", lam_c_mn(a, b, 1, 1))]
    names = [s[0] for s in spec]
    lcs = [s[1] * 1e3 for s in spec]
    fig, ax = plt.subplots(figsize=(6.5, 3.5))
    y = range(len(names))
    ax.barh(y, lcs, color="C0", alpha=0.75)
    ax.set_yticks(y)
    ax.set_yticklabels(names)
    ax.axvline(lam0 * 1e3, color="red", lw=1.5, label=f"lambda0 @6 GHz = {lam0*1e3:.1f} mm")
    ax.set_xlabel("lambda_c (mm)")
    ax.set_title("题10: 大波导+6 GHz  可导行( lambda_c>lambda0 )的模(示意5个)", fontsize=9)
    ax.legend()
    path = FIG / "lec13_16_q10_modes_enum.webp"
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def fig_q11() -> Path:
    fig, ax = plt.subplots(figsize=(8, 2.0))
    ax.hlines(0, 0, 50, color="k", lw=0.5)
    ax.fill_betweenx([-0.1, 0.1], 22.86, 45.72, color="C0", alpha=0.4, label="严格单模(题6 同)")
    ax.fill_betweenx([-0.18, -0.08], 0, 46, color="C2", alpha=0.2, label="题设宽区间含多模 子区")
    ax.set_xlim(0, 50)
    ax.set_ylim(-0.25, 0.2)
    ax.set_xlabel("lambda0 (mm)")
    ax.set_yticks([])
    ax.legend(loc="upper right", fontsize=7)
    ax.set_title("题11: 宽 口语 区间 不能 代替 严格 开区间(示意 BJ-100)", fontsize=9)
    path = FIG / "lec13_16_q11_interval_compare.webp"
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def fig_q12() -> Path:
    a, b = A_BJ * 1e3, B_BJ * 1e3
    fig, ax = plt.subplots(figsize=(3.5, 2.0))
    rect = plt.Rectangle((0, 0), a, b, fill=False, ec="C0", lw=2)
    ax.add_patch(rect)
    ax.set_xlim(-1, a + 1)
    ax.set_ylim(-0.2, b + 0.2)
    ax.set_aspect("equal")
    ax.set_xlabel("a (mm)")
    ax.set_ylabel("b (mm)")
    ax.set_title("题12: TE10 管壁 附近 E 大 -> P_max 受 E_br 与 a,b(示意,见教材 公式)", fontsize=8)
    path = FIG / "lec13_16_q12_breakdown_hint.webp"
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def main() -> None:
    _set_cn_font()
    FIG.mkdir(parents=True, exist_ok=True)
    out = [
        fig_q01(),
        fig_q02(),
        fig_q03(),
        fig_q04(),
        fig_q05(),
        fig_q06(),
        fig_q07(),
        fig_q08(),
        fig_q09(),
        fig_q10(),
        fig_q11(),
        fig_q12(),
    ]
    for p in out:
        print("wrote", p)


if __name__ == "__main__":
    main()
