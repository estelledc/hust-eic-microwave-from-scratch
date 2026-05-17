"""
Schematic figures for 《微波技术基础》第二次作业标准解答.md
Run from repo root: python scripts/plots/plot_second_homework_schematics.py
Also runs plot_smith_charts.py to refresh Smith-chart figures for 圆图解法.
"""
from pathlib import Path
import runpy

import matplotlib.pyplot as plt
from matplotlib import patches
import numpy as np

OUT = Path(__file__).resolve().parents[2] / "assets" / "images"
OUT.mkdir(parents=True, exist_ok=True)
DPI = 160


def save(fig, name: str) -> None:
    p = OUT / name
    fig.savefig(p, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print("saved", p)


def draw_z_direction():
    fig, ax = plt.subplots(figsize=(8, 2.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 2)
    ax.axis("off")
    # transmission line as double line
    y0, y1 = 0.9, 1.1
    ax.plot([1, 9], [y0, y0], "k-", lw=2)
    ax.plot([1, 9], [y1, y1], "k-", lw=2)
    ax.text(1, 0.35, r"Load $z=0$", ha="center", fontsize=11)
    ax.text(9, 0.35, r"Generator", ha="center", fontsize=11)
    ax.annotate(
        "",
        xy=(8.2, 1.35),
        xytext=(2.2, 1.35),
        arrowprops=dict(arrowstyle="->", color="C0", lw=2),
    )
    ax.text(5.2, 1.55, r"$z$ (toward source)", ha="center", fontsize=11, color="C0")
    ax.text(
        5,
        2.0,
        r"$\Gamma(z)=\Gamma_L\,\mathrm{e}^{-\mathrm{j}2\beta z}$",
        ha="center",
        fontsize=10,
    )
    ax.set_title(r"Transmission line: $z$ measured from load toward source", fontsize=12)
    save(fig, "lec_symbol_z_direction.png")


def draw_lec06_q4_AB():
    fig, ax = plt.subplots(figsize=(9, 2.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 2.2)
    ax.axis("off")
    y0, y1 = 0.95, 1.15
    ax.plot([0.5, 9.5], [y0, y0], "k-", lw=2)
    ax.plot([0.5, 9.5], [y1, y1], "k-", lw=2)
    # load at left
    ax.plot([0.5, 0.5], [0.75, 1.35], "k-", lw=3)
    ax.text(0.5, 0.45, r"Load", ha="center", fontsize=10)
    xb, xa = 3.0, 6.5
    ax.axvline(xb, color="C1", ls="--", lw=1.2)
    ax.axvline(xa, color="C2", ls="--", lw=1.2)
    ax.text(xb, 1.55, r"$B$", ha="center", fontsize=12, color="C1", fontweight="bold")
    ax.text(xa, 1.55, r"$A$", ha="center", fontsize=12, color="C2", fontweight="bold")
    ax.annotate(
        "",
        xy=(xa - 0.05, 0.65),
        xytext=(xb + 0.05, 0.65),
        arrowprops=dict(arrowstyle="<->", color="k", lw=1.2),
    )
    ax.text((xb + xa) / 2, 0.4, r"$\lambda/4$", ha="center", fontsize=11)
    ax.annotate(
        "",
        xy=(0.6, 1.0),
        xytext=(xb - 0.15, 1.0),
        arrowprops=dict(arrowstyle="->", color="gray", lw=1),
    )
    ax.text(1.7, 0.85, r"toward load", fontsize=9, color="gray")
    ax.set_title(
        r"Lec06 Q4: $A$ and $B$ separated by $\lambda/4$ ($B$ closer to load than $A$)",
        fontsize=11,
    )
    save(fig, "lec06_q4_quarter_wave_AB.png")


def draw_parallel_stub():
    fig, ax = plt.subplots(figsize=(7, 3.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")
    # main line horizontal through junction at x=5
    ax.plot([1, 5], [3, 3], "k-", lw=2.5)
    ax.plot([5, 9], [3, 3], "k-", lw=2.5)
    ax.plot([5, 5], [3, 1.0], "k-", lw=2.5)
    ax.plot([5, 5], [1.0, 0.5], "k-", lw=4)  # stub thick at end (short)
    ax.text(1, 2.5, r"toward load", fontsize=9, color="gray")
    ax.text(7.5, 2.5, r"toward gen.", fontsize=9, color="gray")
    ax.text(5.7, 2.0, r"stub", fontsize=10)
    ax.text(5.15, 0.35, r"short", fontsize=9)
    ax.plot([4.7, 5.3], [3, 3], "C0", lw=5, alpha=0.35)
    ax.text(5, 3.55, r"junction", ha="center", fontsize=9, color="C0")
    ax.set_title(r"Lec08: parallel short-circuited stub (topology)", fontsize=12)
    save(fig, "lec08_parallel_stub_topology.png")


def draw_double_stub():
    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4)
    ax.axis("off")
    y = 2.2
    x0, x1, x2, x3 = 0.8, 3.2, 5.4, 9.5
    ax.plot([x0, x3], [y, y], "k-", lw=2.5)
    ax.plot([x0, x0], [y - 0.35, y + 0.35], "k-", lw=4)
    ax.text(x0, 1.5, r"$Z_L$", ha="center", fontsize=11)
    # stub 1 at x1
    ax.plot([x1, x1], [y, 0.9], "k-", lw=2.5)
    ax.plot([x1, x1], [0.9, 0.5], "k-", lw=4)
    ax.text(x1, 0.25, r"$l_1$", ha="center", fontsize=10)
    # stub 2 at x2
    ax.plot([x2, x2], [y, 0.9], "k-", lw=2.5)
    ax.plot([x2, x2], [0.9, 0.5], "k-", lw=4)
    ax.text(x2, 0.25, r"$l_2$", ha="center", fontsize=10)
    ax.annotate(
        "",
        xy=(x1 - 0.05, 1.05),
        xytext=(x0 + 0.1, 1.05),
        arrowprops=dict(arrowstyle="<->", color="C0", lw=1.2),
    )
    ax.text((x0 + x1) / 2, 0.85, r"$d_1$", ha="center", fontsize=10, color="C0")
    ax.annotate(
        "",
        xy=(x2 - 0.05, 1.05),
        xytext=(x1 + 0.05, 1.05),
        arrowprops=dict(arrowstyle="<->", color="C1", lw=1.2),
    )
    ax.text((x1 + x2) / 2, 0.85, r"$d_2$", ha="center", fontsize=10, color="C1")
    ax.text(10.2, y, r"$\to$ gen.", fontsize=10)
    ax.set_title(
        r"Lec08 Q6: double parallel stubs (spacing $d_1$, $d_2$ along main line)",
        fontsize=11,
    )
    save(fig, "lec08_double_stub_topology.png")


def draw_lec08_q7():
    fig, ax = plt.subplots(figsize=(10, 3.8))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4.5)
    ax.axis("off")
    y = 2.4
    xl, x1, x2, xr = 0.7, 3.0, 6.5, 10.0
    ax.plot([xl, xr], [y, y], "k-", lw=2.5)
    ax.plot([xl, xl], [y - 0.35, y + 0.35], "k-", lw=4)
    ax.text(xl, 1.5, r"$Z_L$", ha="center", fontsize=10)
    # parallel stub at x1
    ax.plot([x1, x1], [y, 1.0], "k-", lw=2)
    ax.plot([x1, x1], [1.0, 0.55], "k-", lw=4)
    ax.text(x1 - 0.35, 2.9, r"parallel", fontsize=8, color="C0")
    ax.text(x1, 0.25, r"$l_1$", ha="center", fontsize=9)
    # series stub at x2: show as series element in line (break + vertical stub symbol)
    ax.plot([x1 + 0.15, x2 - 0.35], [y, y], "k-", lw=2.5)
    ax.plot([x2 + 0.35, xr], [y, y], "k-", lw=2.5)
    # T for series short line going up-down at x2 (simplified: box)
    box = patches.Rectangle((x2 - 0.35, y - 0.25), 0.7, 0.5, fill=False, lw=2, edgecolor="C3")
    ax.add_patch(box)
    ax.plot([x2, x2], [y - 0.25, 0.9], "k-", lw=2)
    ax.plot([x2, x2], [0.9, 0.55], "k-", lw=4)
    ax.text(x2 + 0.55, y, r"series", fontsize=8, color="C3", va="center")
    ax.text(x2, 0.25, r"$l_2$", ha="center", fontsize=9)
    ax.text(
        5.5,
        4.0,
        r"(sketch; exact order per course slides)",
        ha="center",
        fontsize=9,
        style="italic",
    )
    ax.set_title(
        r"Lec08 Q7: parallel stub at $d_1$, series stub at $d_2$ (conceptual)",
        fontsize=11,
    )
    save(fig, "lec08_q7_topology_sketch.png")


def draw_lec07_gamma_rotation():
    """Constant |Γ| circle: toward generator rotates Γ clockwise by 2βl (Lec07 Smith idea)."""
    fig, ax = plt.subplots(figsize=(5.2, 5.0))
    mag = 0.48
    th = np.linspace(0, 2 * np.pi, 300)
    ax.plot(mag * np.cos(th), mag * np.sin(th), "k--", lw=1.2, label=r"$|\Gamma|=\mathrm{const}$")
    ax.axhline(0, color="gray", lw=0.5)
    ax.axvline(0, color="gray", lw=0.5)
    phi_l = np.deg2rad(55)
    dl = 0.8 * np.pi
    phi_in = phi_l - dl
    ax.plot(mag * np.cos(phi_l), mag * np.sin(phi_l), "o", color="C0", ms=9, label=r"$\Gamma_L$ at load")
    ax.plot(mag * np.cos(phi_in), mag * np.sin(phi_in), "s", color="C3", ms=8, label=r"$\Gamma$ after $l/\lambda$")
    arc = np.linspace(phi_in, phi_l, 80)
    ax.plot(mag * np.cos(arc), mag * np.sin(arc), "-", color="C2", lw=2.5)
    ax.annotate(
        r"toward gen." + "\n" + r"$2\beta l$",
        xy=(mag * np.cos((phi_l + phi_in) / 2) * 0.72, mag * np.sin((phi_l + phi_in) / 2) * 0.72),
        fontsize=9,
        ha="center",
    )
    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-1.05, 1.05)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$\mathrm{Re}\{\Gamma\}$", fontsize=11)
    ax.set_ylabel(r"$\mathrm{Im}\{\Gamma\}$", fontsize=11)
    ax.set_title(r"Lec07: rotate on $|\Gamma|$ circle (example $2\beta l=0.8\pi$)", fontsize=11)
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(True, alpha=0.25)
    save(fig, "lec07_gamma_rotation_smith_principle.png")


def draw_lec07_Zbar_q1():
    fig, ax = plt.subplots(figsize=(5.0, 4.5))
    ax.set_xlim(-0.2, 2.6)
    ax.set_ylim(-0.2, 2.0)
    ax.set_aspect("equal")
    ax.axhline(0, color="k", lw=0.6)
    ax.axvline(0, color="k", lw=0.6)
    ax.plot(2.0, 1.5, "o", color="C0", ms=12, zorder=5)
    ax.annotate(
        r"$\bar Z_L=2+\mathrm{j}1.5$",
        xy=(2.0, 1.5),
        xytext=(2.15, 1.65),
        fontsize=11,
        arrowprops=dict(arrowstyle="-", color="C0", lw=0.8),
    )
    ax.set_xlabel(r"$\mathrm{Re}\{\bar Z_L\}$", fontsize=11)
    ax.set_ylabel(r"$\mathrm{Im}\{\bar Z_L\}$", fontsize=11)
    ax.set_title(r"Lec07 Q1: normalized load in impedance plane", fontsize=11)
    ax.grid(True, alpha=0.3)
    save(fig, "lec07_Zbar_plane_q1.png")


def draw_lec07_same_mod_gamma():
    fig, ax = plt.subplots(figsize=(5.0, 4.8))
    mag = np.sqrt(0.2)
    a1, a2 = np.deg2rad(30), np.deg2rad(-110)
    ax.axhline(0, color="gray", lw=0.5)
    ax.axvline(0, color="gray", lw=0.5)
    th = np.linspace(0, 2 * np.pi, 200)
    ax.plot(mag * np.cos(th), mag * np.sin(th), "k:", lw=1)
    ax.plot([0, mag * np.cos(a1)], [0, mag * np.sin(a1)], "C0", lw=2)
    ax.plot([0, mag * np.cos(a2)], [0, mag * np.sin(a2)], "C1", lw=2)
    ax.plot(mag * np.cos(a1), mag * np.sin(a1), "o", color="C0", ms=9)
    ax.plot(mag * np.cos(a2), mag * np.sin(a2), "o", color="C1", ms=9)
    ax.text(0.15, 0.35, r"$|\Gamma|$ same", fontsize=11)
    ax.text(0.15, 0.22, r"$\Rightarrow$ $\rho$ same", fontsize=11)
    ax.set_xlim(-0.55, 0.55)
    ax.set_ylim(-0.55, 0.45)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$\mathrm{Re}\{\Gamma\}$", fontsize=11)
    ax.set_ylabel(r"$\mathrm{Im}\{\Gamma\}$", fontsize=11)
    ax.set_title(r"Lec07 Q2: $\rho$ depends only on $|\Gamma|$, not angle", fontsize=11)
    save(fig, "lec07_constant_mod_gamma_rho.png")


def draw_lec07_tline_Zin_segment():
    fig, ax = plt.subplots(figsize=(8.5, 2.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 2.5)
    ax.axis("off")
    y0, y1 = 1.0, 1.25
    ax.plot([1.2, 8.5], [y0, y0], "k-", lw=2.2)
    ax.plot([1.2, 8.5], [y1, y1], "k-", lw=2.2)
    ax.plot([1.2, 1.2], [0.75, 1.5], "k-", lw=3.5)
    ax.text(1.2, 0.45, r"$Z_L$", ha="center", fontsize=11)
    ax.text(8.5, 0.45, r"$Z_{\mathrm{in}}$", ha="center", fontsize=11)
    ax.plot([8.5, 8.5], [0.75, 1.5], "k-", lw=3.5)
    ax.annotate(
        "",
        xy=(8.45, 1.65),
        xytext=(1.25, 1.65),
        arrowprops=dict(arrowstyle="<->", color="C0", lw=1.5),
    )
    ax.text(4.85, 1.88, r"electrical length $l$  (e.g. $l/\lambda=0.2$)", ha="center", fontsize=10, color="C0")
    ax.annotate(
        "",
        xy=(2.5, 1.0),
        xytext=(1.4, 1.0),
        arrowprops=dict(arrowstyle="->", color="gray", lw=1),
    )
    ax.text(2.0, 0.82, r"$z=0$", fontsize=9, color="gray")
    ax.set_title(
        r"Lec07 Q3/Q4: $Z_{\mathrm{in}}$ at distance $l$ from load ($z$ toward source)",
        fontsize=11,
    )
    save(fig, "lec07_tline_ZL_l_Zin.png")


def draw_lec07_vmin_q5():
    z_lam = np.linspace(0, 0.75, 600)
    rho = 2.0
    g = (rho - 1) / (rho + 1)
    zmin = 0.2
    Gamma_L = -g * np.exp(1j * 4 * np.pi * zmin)
    v = np.abs(1 + Gamma_L * np.exp(-1j * 4 * np.pi * z_lam))
    v = v / np.max(v)
    fig, ax = plt.subplots(figsize=(8, 2.8))
    ax.plot(z_lam, v, "b-", lw=2)
    ax.axvline(zmin, color="C1", ls="--", lw=1.5)
    ax.scatter([zmin], [np.interp(zmin, z_lam, v)], color="C1", s=40, zorder=5)
    ax.text(zmin, -0.12, r"$z_{\min}=0.2\lambda$", ha="center", fontsize=10, color="C1")
    ax.set_xlabel(r"$z/\lambda$ (from load toward source)", fontsize=10)
    ax.set_ylabel(r"$|V|$ (normalized)", fontsize=10)
    ax.set_xlim(0, 0.65)
    ax.set_ylim(-0.05, 1.1)
    ax.grid(True, alpha=0.3)
    ax.set_title(r"Lec07 Q5: first $V_{\min}$ at $0.2\lambda$ from load ($\rho=2$)", fontsize=11)
    save(fig, "lec07_vmin_first_null_02lambda.png")


def draw_vmin_first_null():
    fig, ax = plt.subplots(figsize=(8, 2.8))
    z_lam = np.linspace(0, 0.65, 600)
    rho = 2.0
    g = (rho - 1) / (rho + 1)
    zmin = 0.1
    # $\Gamma(z)=\Gamma_L e^{-\mathrm{j}2\beta z}$, $z=z_{\min}$ 处第一波节：$\Gamma(z_{\min})=-|\Gamma|$
    Gamma_L = -g * np.exp(1j * 4 * np.pi * zmin)
    v = np.abs(1 + Gamma_L * np.exp(-1j * 4 * np.pi * z_lam))
    v = v / np.max(v)
    ax.plot(z_lam, v, "b-", lw=2)
    ax.axvline(zmin, color="C1", ls="--", lw=1.5)
    ax.scatter([zmin], [np.interp(zmin, z_lam, v)], color="C1", s=40, zorder=5)
    ax.text(zmin, -0.12, r"$z_{\min}$ (1st $V_{\min}$)", ha="center", fontsize=10, color="C1")
    ax.set_xlabel(r"$z/\lambda$ (from load toward source)", fontsize=10)
    ax.set_ylabel(r"$|V|$ (normalized)", fontsize=10)
    ax.set_xlim(0, 0.6)
    ax.set_ylim(-0.05, 1.1)
    ax.grid(True, alpha=0.3)
    ax.set_title(
        r"Example: $\rho=2$, first $V_{\min}$ at $z_{\min}=0.1\lambda$ (Lec06-5 type)",
        fontsize=11,
    )
    save(fig, "lec_vmin_first_null.png")


def main():
    draw_z_direction()
    draw_lec06_q4_AB()
    draw_parallel_stub()
    draw_double_stub()
    draw_lec08_q7()
    draw_vmin_first_null()
    draw_lec07_gamma_rotation()
    draw_lec07_Zbar_q1()
    draw_lec07_same_mod_gamma()
    draw_lec07_tline_Zin_segment()
    draw_lec07_vmin_q5()
    smith_script = Path(__file__).resolve().parent / "plot_smith_charts.py"
    if smith_script.is_file():
        print("running", smith_script.name)
        runpy.run_path(str(smith_script), run_name="__main__")


if __name__ == "__main__":
    main()
