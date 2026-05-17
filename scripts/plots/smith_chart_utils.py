"""
Smith chart (impedance) in the reflection-coefficient plane Γ = U + jV.
Normalized z = r + jx:  Γ = (z - 1) / (z + 1).

Constant-r circles: center (r/(1+r), 0), radius 1/(1+r).
Constant-x circles: center (1, 1/x), radius 1/|x|  (x ≠ 0).
"""
from __future__ import annotations

import numpy as np


def gamma_from_zbar(z: complex) -> complex:
    """Normalized impedance z = Z/Zc -> Γ."""
    return (z - 1) / (z + 1)


def gamma_from_ybar(y: complex) -> complex:
    """Normalized admittance y = Y*Zc -> Γ (same chart as impedance with y labels)."""
    return (y - 1) / (y + 1)


def zbar_from_gamma(g: complex) -> complex:
    return (1 + g) / (1 - g)


def ybar_from_gamma(g: complex) -> complex:
    return (1 - g) / (1 + g)


def circle_constant_r(r: float, n: int = 400):
    """Arc of constant r inside |Γ|<=1."""
    if r < 0:
        return np.array([]), np.array([])
    cr = r / (1.0 + r)
    rr = 1.0 / (1.0 + r)
    th = np.linspace(0, 2 * np.pi, n)
    u = cr + rr * np.cos(th)
    v = rr * np.sin(th)
    m = u * u + v * v <= 1.0001
    return u[m], v[m]


def circle_constant_x(x: float, n: int = 600):
    """Arc of constant x inside |Γ|<=1."""
    if abs(x) < 1e-12:
        return np.array([]), np.array([])
    cx, cy = 1.0, 1.0 / x
    R = abs(1.0 / x)
    th = np.linspace(0, 2 * np.pi, n)
    u = cx + R * np.cos(th)
    v = cy + R * np.sin(th)
    m = u * u + v * v <= 1.0001
    return u[m], v[m]


def draw_impedance_smith_grid(ax, r_list=None, x_list=None, lw=0.35, color="0.65"):
    if r_list is None:
        r_list = [0.0, 0.2, 0.5, 1.0, 2.0, 5.0]
    if x_list is None:
        x_list = [-5.0, -2.0, -1.0, -0.5, 0.5, 1.0, 2.0, 5.0]
    _draw_smit_grid_impl(ax, r_list, x_list, lw, color)


def draw_impedance_smith_grid_lite(ax, lw=0.45, color="0.5"):
    """Fewer gray curves — easier for beginners (Lec07 figures)."""
    r_list = [0.2, 0.5, 1.0, 2.0, 5.0]
    x_list = [-2.0, -1.0, -0.5, 0.5, 1.0, 2.0]
    _draw_smit_grid_impl(ax, r_list, x_list, lw, color)


def _draw_smit_grid_impl(ax, r_list, x_list, lw, color):
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(np.cos(th), np.sin(th), color="k", lw=0.8)
    for r in r_list:
        if r <= 0:
            continue
        u, v = circle_constant_r(r)
        if len(u) > 2:
            ax.plot(u, v, color=color, lw=lw)
    for x in x_list:
        u, v = circle_constant_x(x)
        if len(u) > 2:
            ax.plot(u, v, color=color, lw=lw)
    ax.axhline(0, color="0.4", lw=0.25)
    ax.axvline(0, color="0.4", lw=0.25)
    ax.set_aspect("equal")
    ax.set_xlim(-1.08, 1.08)
    ax.set_ylim(-1.08, 1.08)
    ax.set_xticks([-1, -0.5, 0, 0.5, 1])
    ax.set_yticks([-1, -0.5, 0, 0.5, 1])


def setup_smith_axes(ax, title: str, *, grid: str = "full"):
    """
    grid: \"full\" = many r,x curves; \"lite\" = fewer gray curves (less clutter).
    """
    if grid == "lite":
        draw_impedance_smith_grid_lite(ax)
    else:
        draw_impedance_smith_grid(ax)
    ax.set_xlabel(r"$\mathrm{Re}\{\Gamma\}$", fontsize=10)
    ax.set_ylabel(r"$\mathrm{Im}\{\Gamma\}$", fontsize=10)
    ax.set_title(title, fontsize=11)


def arc_constant_gamma_magnitude(g0: complex, dlambda: float, n: int = 120):
    """
    Move toward generator: Γ' = Γ * exp(-j 4π d/λ)  (since 2βz = 4π z/λ).
    Returns arrays for arc from g0 to g1 in Γ plane (clockwise if dlambda>0).
    """
    mag = abs(g0)
    phi0 = np.angle(g0)
    phi1 = phi0 - 4 * np.pi * dlambda
    phis = np.linspace(phi0, phi1, n)
    return mag * np.cos(phis), mag * np.sin(phis)


def circle_g1_in_gamma_plane(n: int = 400):
    """Normalized admittance g=1: y=1+jb -> Γ = (y-1)/(y+1) = jb/(2+jb)."""
    b = np.linspace(-80, 80, n)
    y = 1.0 + 1j * b
    g = (y - 1.0) / (y + 1.0)
    m = np.abs(g) <= 1.001
    return g.real[m], g.imag[m]


