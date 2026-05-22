"""
Smith chart assets/images for 《微波技术基础》第二次作业标准解答.md 圆图解法配图.
Run: python scripts/plots/plot_smith_charts.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from smith_chart_utils import (
    arc_constant_gamma_magnitude,
    circle_constant_r,
    circle_constant_x,
    circle_g1_in_gamma_plane,
    gamma_from_ybar,
    gamma_from_zbar,
    setup_smith_axes,
)

OUT = Path(__file__).resolve().parents[2] / "assets" / "images"
OUT.mkdir(parents=True, exist_ok=True)
DPI = 170


def save(fig, name: str) -> None:
    p = OUT / name
    fig.savefig(p, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print("saved", p)


def lec07_q0_anatomy():
    """
    Two panels: (left) only one r-circle + one x-arc to explain gray families;
    (right) lite gray grid + thick r=2, x=1.5 + example load + |Gamma| circle.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 5.15))
    th = np.linspace(0, 2 * np.pi, 400)

    # --- Left: minimal teaching chart (no gray soup) ---
    ax1.plot(np.cos(th), np.sin(th), color="k", lw=1.0)
    u, v = circle_constant_r(1.0)
    ax1.plot(u, v, color="#E4572E", lw=2.5, label=r"equal $r$ circle ($r=1$)")
    u, v = circle_constant_x(1.0)
    ax1.plot(u, v, color="#2E8B57", lw=2.5, label=r"equal $x$ arc ($x=+1$)")
    g1 = gamma_from_zbar(1.0 + 1.0j)
    ax1.plot(g1.real, g1.imag, "o", color="C0", ms=11, zorder=6)
    ax1.annotate(
        r"intersection $=$ $\bar Z=1+\mathrm{j}1$",
        xy=(g1.real, g1.imag),
        xytext=(g1.real - 0.52, g1.imag + 0.22),
        fontsize=9,
        arrowprops=dict(arrowstyle="-", color="C0", lw=0.8),
    )
    ax1.set_aspect("equal")
    ax1.set_xlim(-1.08, 1.08)
    ax1.set_ylim(-1.08, 1.08)
    ax1.set_xticks([-1, -0.5, 0, 0.5, 1])
    ax1.set_yticks([-1, -0.5, 0, 0.5, 1])
    ax1.set_xlabel(r"$\mathrm{Re}\{\Gamma\}$", fontsize=10)
    ax1.set_ylabel(r"$\mathrm{Im}\{\Gamma\}$", fontsize=10)
    ax1.set_title(r"Gray curves = many $r$ circles + many $x$ arcs (two families)", fontsize=10)
    ax1.legend(loc="lower left", fontsize=7.5)

    # --- Right: lite grid + highlight Lec07 Q1 ---
    setup_smith_axes(ax2, r"Find $\bar Z$: one $r$ circle + one $x$ arc (Q1 example)", grid="lite")
    u, v = circle_constant_r(2.0)
    ax2.plot(u, v, color="#E4572E", lw=2.8, zorder=4, label=r"your $r=2$")
    u, v = circle_constant_x(1.5)
    ax2.plot(u, v, color="#2E8B57", lw=2.8, zorder=4, label=r"your $x=+1.5$")
    z_ex = 2.0 + 1.5j
    g_ex = gamma_from_zbar(z_ex)
    ax2.plot(g_ex.real, g_ex.imag, "o", color="C0", ms=10, zorder=6, label=r"$\bar Z_L$")
    mag = abs(g_ex)
    ax2.plot(mag * np.cos(th), mag * np.sin(th), "b--", lw=1.5, zorder=3, label=r"$|\Gamma|$ circle")
    ax2.plot(0, 0, "k+", ms=12, mew=2, zorder=7)
    ax2.legend(loc="lower left", fontsize=7.5)
    ax2.text(-0.98, -0.92, r"faint gray $=$ other $r,x$ (ignore until needed)", fontsize=7.5, color="0.35")

    fig.suptitle(r"Lec07 primer: what the pale gray lines are", fontsize=11, y=1.02)
    save(fig, "smith_lec07_q0_anatomy.webp")


def lec07_q1():
    fig, ax = plt.subplots(figsize=(5.2, 5.0))
    setup_smith_axes(ax, r"Lec07 Q1: impedance Smith, $\bar Z_L=2+\mathrm{j}1.5$", grid="lite")
    z = 2.0 + 1.5j
    g = gamma_from_zbar(z)
    ax.plot(g.real, g.imag, "o", color="C0", ms=10, zorder=5)
    ax.annotate(
        r"$\bar Z_L$",
        xy=(g.real, g.imag),
        xytext=(g.real + 0.12, g.imag + 0.1),
        fontsize=10,
        arrowprops=dict(arrowstyle="-", color="C0", lw=0.8),
    )
    ax.text(-0.95, 0.82, r"$\Gamma\approx$" + f"{g.real:.3f}{g.imag:+.3f}j", fontsize=9)
    save(fig, "smith_lec07_q1.webp")


def lec07_q2():
    fig, ax = plt.subplots(figsize=(5.2, 5.0))
    setup_smith_axes(ax, r"Lec07 Q2: $\bar Z_L=2-\mathrm{j}$, constant $|\Gamma|$ and $\rho$", grid="lite")
    z = 2.0 - 1.0j
    g = gamma_from_zbar(z)
    mag = abs(g)
    th = np.linspace(0, 2 * np.pi, 300)
    ax.plot(mag * np.cos(th), mag * np.sin(th), "--", color="C1", lw=1.2)
    ax.plot(g.real, g.imag, "o", color="C0", ms=10, zorder=5)
    ax.annotate(r"$\bar Z_L$", xy=(g.real, g.imag), xytext=(g.real + 0.15, g.imag - 0.12), fontsize=10)
    rho = (1 + mag) / (1 - mag)
    ax.text(-0.95, 0.82, rf"$|\Gamma|\approx{mag:.3f}$", fontsize=9)
    ax.text(-0.95, 0.68, rf"$\rho\approx{rho:.2f}$", fontsize=9)
    save(fig, "smith_lec07_q2.webp")


def lec07_q3():
    fig, ax = plt.subplots(figsize=(5.2, 5.0))
    setup_smith_axes(ax, r"Lec07 Q3: toward generator $0.2\lambda$ (clockwise on chart)", grid="lite")
    zl = 1.0 - 2.0j
    gl = gamma_from_zbar(zl)
    ua, va = arc_constant_gamma_magnitude(gl, 0.2)
    ax.plot(ua, va, "-", color="C2", lw=2.2)
    ax.plot(gl.real, gl.imag, "o", color="C0", ms=9, zorder=5, label=r"$\bar Z_L$")
    gin = gl * np.exp(-1j * 4 * np.pi * 0.2)
    ax.plot(gin.real, gin.imag, "s", color="C3", ms=8, zorder=5, label=r"$\bar Z_{\mathrm{in}}$")
    ax.legend(loc="lower left", fontsize=9)
    ax.text(-0.98, -0.95, r"$\Gamma(z)=\Gamma_L\mathrm{e}^{-\mathrm{j}4\pi z/\lambda}$", fontsize=8)
    save(fig, "smith_lec07_q3.webp")


def lec07_q4():
    fig, ax = plt.subplots(figsize=(5.2, 5.0))
    setup_smith_axes(ax, r"Lec07 Q4: same $|\Gamma|$ circle, $\bar Z_L\to\bar Z_{\mathrm{in}}$", grid="lite")
    zl = 0.8 + 1.0j
    zin = 0.9 - 1.09j
    gl, gi = gamma_from_zbar(zl), gamma_from_zbar(zin)
    mag = abs(gl)
    th = np.linspace(0, 2 * np.pi, 300)
    ax.plot(mag * np.cos(th), mag * np.sin(th), ":", color="0.5", lw=1)
    ax.plot(gl.real, gl.imag, "o", color="C0", ms=9, label=r"$\bar Z_L$")
    ax.plot(gi.real, gi.imag, "s", color="C3", ms=8, label=r"$\bar Z_{\mathrm{in}}$")
    ua, va = arc_constant_gamma_magnitude(gl, 0.191)
    ax.plot(ua, va, "-", color="C2", lw=2.0)
    ax.legend(loc="upper right", fontsize=9)
    ax.text(-0.98, -0.95, r"$\Delta(l/\lambda)\approx 0.191$", fontsize=8)
    save(fig, "smith_lec07_q4.webp")


def lec07_q5():
    fig, ax = plt.subplots(figsize=(5.2, 5.0))
    setup_smith_axes(ax, r"Lec07 Q5: $\rho=2$, first $V_{\min}$ toward load $0.2\lambda$ (CCW)", grid="lite")
    gmag = 1.0 / 3.0
    g_vmin = -gmag + 0j
    g_l = g_vmin * np.exp(1j * 4 * np.pi * 0.2)
    th = np.linspace(0, 2 * np.pi, 300)
    ax.plot(gmag * np.cos(th), gmag * np.sin(th), "--", color="0.55", lw=1)
    ax.plot(g_vmin.real, g_vmin.imag, "s", color="C1", ms=8, label=r"$\Gamma$ at $V_{\min}$")
    ax.plot(g_l.real, g_l.imag, "o", color="C0", ms=9, label=r"$\Gamma_L$")
    arc_b = np.linspace(np.angle(g_l), np.angle(g_vmin), 60)
    ax.plot(gmag * np.cos(arc_b), gmag * np.sin(arc_b), "-", color="C2", lw=2.0)
    ax.annotate(
        r"toward load $0.2\lambda$",
        xy=(0.15, -0.35),
        fontsize=9,
        color="C2",
    )
    ax.legend(loc="upper left", fontsize=8)
    save(fig, "smith_lec07_q5.webp")


def lec08_q0_g1():
    """Lec08 zero-base: g=1 locus in Gamma plane (Re Ybar = 1)."""
    fig, ax = plt.subplots(figsize=(5.8, 5.2))
    setup_smith_axes(ax, r"Lec08: $g=1$ ($\mathrm{Re}\,\bar Y=1$) in $\Gamma$ plane", grid="lite")
    ug, vg = circle_g1_in_gamma_plane()
    ax.plot(ug, vg, color="#E4572E", lw=2.6, label=r"$g=1$ locus")
    ax.plot(0, 0, "k+", ms=11, mew=2, zorder=6)
    ax.text(-0.98, 0.82, r"$\bar Y=1$ : on $g{=}1$ and $b{=}0$", fontsize=8)
    ax.legend(loc="lower left", fontsize=8)
    ax.text(-0.98, -0.92, r"rotate $\bar Y_L$ CW to meet orange", fontsize=7.5, color="0.35")
    save(fig, "smith_lec08_q0_g1_explained.webp")


def lec08_q1_stub_concept():
    fig, ax = plt.subplots(figsize=(5.4, 5.0))
    setup_smith_axes(ax, r"Lec08 Q1: shunt stub — $g=1$ circle and rotation toward gen.")
    ug, vg = circle_g1_in_gamma_plane()
    ax.plot(ug, vg, "-", color="C1", lw=1.8, label=r"$g=1$ ($\mathrm{Re}\,\bar Y=1$)")
    y0 = 0.4 + 0.2j
    g0 = gamma_from_ybar(y0)
    ua, va = arc_constant_gamma_magnitude(g0, 0.125)
    ax.plot(ua, va, "-", color="C2", lw=2.0)
    ax.plot(g0.real, g0.imag, "o", color="C0", ms=9, label=r"$\bar Y_L$ (e.g. $Z_L=100-\mathrm{j}50\,\Omega$)")
    g1 = g0 * np.exp(-1j * 4 * np.pi * 0.125)
    ax.plot(g1.real, g1.imag, "s", color="C3", ms=8, label=r"intersect $g=1$ (find $d$)")
    ax.legend(loc="lower left", fontsize=7.5)
    ax.text(-0.98, -0.92, r"short stub: cancel $b$ on outer chart", fontsize=8)
    save(fig, "smith_lec08_q1_stub_concept.webp")


def lec08_q2_quarter_wave():
    fig, ax = plt.subplots(figsize=(5.2, 5.0))
    setup_smith_axes(ax, r"Lec08 Q2: to positive real axis ($\lambda/4$ transformer point)")
    zc = 600.0
    zl = 22 - 66j
    zb = zl / zc
    gl = gamma_from_zbar(zb)
    dlam = 0.0262 / 1.5
    ua, va = arc_constant_gamma_magnitude(gl, dlam)
    ax.plot(ua, va, "-", color="C2", lw=2.2)
    ax.plot(gl.real, gl.imag, "o", color="C0", ms=9, label=r"$\bar Z_L$")
    g1 = gl * np.exp(-1j * 4 * np.pi * dlam)
    ax.plot(g1.real, g1.imag, "s", color="C3", ms=8, label=r"$\bar Z(d)\approx R$")
    ax.plot([g1.real, 0], [0, 0], ":", color="0.4", lw=0.8)
    ax.legend(loc="upper left", fontsize=8)
    ax.text(-0.98, -0.92, rf"$d/\lambda\approx{dlam:.4f}$", fontsize=8)
    save(fig, "smith_lec08_q2_quarter_wave.webp")


def lec08_q3_parallel_mid():
    fig, ax = plt.subplots(figsize=(5.2, 5.0))
    setup_smith_axes(ax, r"Lec08 Q3: after shunt, $\bar Z_{\mathrm{tot}}$ then $+\lambda/8$ toward gen.")
    zt = 0.4 + 0.2j
    g0 = gamma_from_zbar(zt)
    ua, va = arc_constant_gamma_magnitude(g0, 1.0 / 8.0)
    ax.plot(ua, va, "-", color="C2", lw=2.2)
    ax.plot(g0.real, g0.imag, "o", color="C0", ms=9, label=r"$\bar Z_{\mathrm{tot}}$")
    g1 = g0 * np.exp(-1j * 4 * np.pi * (1.0 / 8.0))
    ax.plot(g1.real, g1.imag, "s", color="C3", ms=8, label=r"$\bar Z_{\mathrm{in}}$")
    ax.legend(loc="lower left", fontsize=9)
    save(fig, "smith_lec08_q3_parallel_mid.webp")


def lec08_q4_single_stub():
    fig, ax = plt.subplots(figsize=(5.4, 5.0))
    setup_smith_axes(ax, r"Lec08 Q4: single stub, $\bar Y_L\to g=1$ (e.g. $d/\lambda\approx 0.125$)")
    ug, vg = circle_g1_in_gamma_plane()
    ax.plot(ug, vg, "-", color="C1", lw=1.6, alpha=0.9)
    yl = 1.0 / (2.0 - 1.0j)
    g0 = gamma_from_ybar(yl)
    ua, va = arc_constant_gamma_magnitude(g0, 0.125)
    ax.plot(ua, va, "-", color="C2", lw=2.2)
    ax.plot(g0.real, g0.imag, "o", color="C0", ms=9, label=r"$\bar Y_L$")
    g1 = g0 * np.exp(-1j * 4 * np.pi * 0.125)
    ax.plot(g1.real, g1.imag, "s", color="C3", ms=8, label=r"on $g=1$ (find $d,l$)")
    ax.legend(loc="lower left", fontsize=8)
    save(fig, "smith_lec08_q4_single_stub.webp")


def lec08_q5_single_stub():
    fig, ax = plt.subplots(figsize=(5.4, 5.0))
    setup_smith_axes(ax, r"Lec08 Q5: $\bar Y_L=4.25+\mathrm{j}1.75$ toward $g=1$")
    ug, vg = circle_g1_in_gamma_plane()
    ax.plot(ug, vg, "-", color="C1", lw=1.6, alpha=0.9)
    yl = 4.25 + 1.75j
    g0 = gamma_from_ybar(yl)
    dlam = 0.0806
    ua, va = arc_constant_gamma_magnitude(g0, dlam)
    ax.plot(ua, va, "-", color="C2", lw=2.2)
    ax.plot(g0.real, g0.imag, "o", color="C0", ms=9, label=r"$\bar Y_L$")
    g1 = g0 * np.exp(-1j * 4 * np.pi * dlam)
    ax.plot(g1.real, g1.imag, "s", color="C3", ms=8, label=r"nearest $g=1$")
    ax.legend(loc="lower left", fontsize=7.5)
    ax.text(-0.98, -0.92, rf"$d/\lambda\approx{dlam}$", fontsize=8)
    save(fig, "smith_lec08_q5_single_stub.webp")


def lec08_q6_double_stub():
    fig, ax = plt.subplots(figsize=(5.4, 5.0))
    setup_smith_axes(ax, r"Lec08 Q6: double stub, after $\lambda/4$: $\bar Y\approx 0.5+\mathrm{j}1$")
    y = 0.5 + 1.0j
    g = gamma_from_ybar(y)
    ax.plot(g.real, g.imag, "o", color="C0", ms=10, zorder=5)
    ax.annotate(
        r"junction-1 $\bar Y$",
        xy=(g.real, g.imag),
        xytext=(g.real - 0.35, g.imag + 0.2),
        fontsize=9,
        arrowprops=dict(arrowstyle="-", color="C0", lw=0.7),
    )
    ug, vg = circle_g1_in_gamma_plane()
    ax.plot(ug, vg, ":", color="C1", lw=1.2, alpha=0.7)
    ax.text(-0.98, -0.92, r"then textbook steps for $l_1,l_2$", fontsize=8)
    save(fig, "smith_lec08_q6_double_stub.webp")


def lec08_q7_hybrid():
    fig, ax = plt.subplots(figsize=(5.2, 5.0))
    setup_smith_axes(ax, r"Lec08 Q7: $\bar Z_L=1+\mathrm{j}2$ (shunt: $Y$, series: $Z$)")
    zl = 1.0 + 2.0j
    g = gamma_from_zbar(zl)
    ax.plot(g.real, g.imag, "o", color="C0", ms=10, zorder=5)
    ax.annotate(r"$\bar Z_L$", xy=(g.real, g.imag), xytext=(g.real + 0.1, g.imag + 0.15), fontsize=10)
    ax.text(-0.98, 0.75, r"$d_1$: shunt stub (admittance)", fontsize=8)
    ax.text(-0.98, 0.58, r"$d_2$: series $\bar Z_s$ (impedance)", fontsize=8)
    ax.text(-0.98, -0.92, r"(topology per slides)", fontsize=8, style="italic")
    save(fig, "smith_lec08_q7_hybrid.webp")


def main():
    lec07_q0_anatomy()
    lec07_q1()
    lec07_q2()
    lec07_q3()
    lec07_q4()
    lec07_q5()
    lec08_q0_g1()
    lec08_q1_stub_concept()
    lec08_q2_quarter_wave()
    lec08_q3_parallel_mid()
    lec08_q4_single_stub()
    lec08_q5_single_stub()
    lec08_q6_double_stub()
    lec08_q7_hybrid()


if __name__ == "__main__":
    main()
