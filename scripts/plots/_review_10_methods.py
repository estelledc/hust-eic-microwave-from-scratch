# -*- coding: utf-8 -*-
"""
《第二次作业》多方法交叉审查（10 类独立/半独立核验）。
运行: python scripts/plots/_review_10_methods.py
"""
from __future__ import annotations

import numpy as np

np.random.seed(0)

PASS = []
FAIL = []


def ok(name: str, cond: bool, detail: str = "") -> None:
    msg = f"[{'PASS' if cond else 'FAIL'}] {name}"
    if detail:
        msg += f" | {detail}"
    print(msg)
    (PASS if cond else FAIL).append(name)


def zin_tan(zl: complex, z0: float, bl: float) -> complex:
    t = np.tan(bl)
    return z0 * (zl + 1j * z0 * t) / (z0 + 1j * zl * t)


def zin_abcd(zl: complex, z0: float, bl: float) -> complex:
    """无耗线 ABCD：端口1向负载，端口2 接 ZL。Zin = V1/I1。"""
    c, s = np.cos(bl), np.sin(bl)
    a, b_, c_, d = c, 1j * z0 * s, 1j * s / z0, c
    return (a * zl + b_) / (c_ * zl + d)


def gamma_from_z(zl: complex, z0: float) -> complex:
    return (zl - z0) / (zl + z0)


def z_from_gamma(g: complex, z0: float) -> complex:
    return z0 * (1 + g) / (1 - g)


def rho_from_gamma(g: complex) -> float:
    return (1 + abs(g)) / (1 - abs(g))


# ---------- 方法1：无耗线 Zin —— tan 式 vs ABCD ----------
def pass1():
    cases = [
        (50 - 100j, 50, 0.4 * np.pi),
        (22 - 66j, 600, 2 * np.pi * 32 / 1.5),
        (40 + 20j, 100, np.pi / 4),
    ]
    for zl, z0, bl in cases:
        z1 = zin_tan(zl, z0, bl)
        z2 = zin_abcd(zl, z0, bl)
        ok(
            f"Pass1 ABCD==tan Z0={z0}",
            abs(z1 - z2) < 1e-6 * max(1, abs(z1)),
            f"diff={abs(z1-z2):.3e}",
        )


# ---------- 方法2：Lec06-2 —— 分子/分母零点直接代入 ----------
def pass2():
    zc, zl = 50, -75j
    bl0 = np.arctan(1.5)
    num = zl + 1j * zc * np.tan(bl0)
    ok("Pass2 Lec06-2 short num~0", abs(num) < 1e-9, str(num))
    bl_inf = np.pi - np.arctan(2 / 3)
    den = zc + 1j * zl * np.tan(bl_inf)
    ok("Pass2 Lec06-2 open den~0", abs(den) < 1e-9, str(den))
    ok(
        "Pass2 Lec06-2 l/lam",
        abs(bl_inf / (2 * np.pi) - 0.406) < 0.002
        and abs(bl0 / (2 * np.pi) - 0.156) < 0.002,
        f"open={bl_inf/(2*np.pi):.6f} short={bl0/(2*np.pi):.6f}",
    )


# ---------- 方法3：Lec06-3 —— Zbar→Gamma 回代 ----------
def pass3():
    for mag, ang, zbar_exp in [
        (0.5, 45, 1.38 + 1.30j),
        (0.35, 30, 1.70 + 0.68j),
    ]:
        g = mag * np.exp(1j * np.deg2rad(ang))
        zbar = (1 + g) / (1 - g)
        g2 = (zbar - 1) / (zbar + 1)
        ok(
            f"Pass3 roundtrip Γ mag={mag}",
            abs(g - g2) < 1e-6 and abs(zbar - zbar_exp) < 0.03,
            f"zbar={zbar}",
        )


# ---------- 方法4：Lec06-5 —— ZL→ρ 与第一波节位置 ----------
def pass4():
    zc = 50
    zl = 33.743593663936494 - 24.06904847797699j
    g0 = gamma_from_z(zl, zc)
    rho = rho_from_gamma(g0)
    ok("Pass4 Lec06-5 rho==2", abs(rho - 2) < 1e-6, f"rho={rho}")
    zmin = 0.1
    gz = g0 * np.exp(-1j * 4 * np.pi * zmin)
    ok(
        "Pass4 Lec06-5 Vmin phase",
        abs(gz + abs(g0)) < 1e-5,
        f"Gamma(zmin)={gz}",
    )


# ---------- 方法5：Lec07-5 —— 同上 ----------
def pass5():
    zc = 50
    zl = 77.73181617212909 - 34.26721138491528j
    g0 = gamma_from_z(zl, zc)
    rho = rho_from_gamma(g0)
    ok("Pass5 Lec07-5 rho==2", abs(rho - 2) < 1e-6, f"rho={rho}")
    zmin = 0.2
    gz = g0 * np.exp(-1j * 4 * np.pi * zmin)
    ok(
        "Pass5 Lec07-5 Vmin phase",
        abs(gz + abs(g0)) < 1e-5,
        f"Gamma(zmin)={gz}",
    )


# ---------- 方法6：Lec07-4 —— 由 barZ 反解 t 再代回（题给数含舍入时 t 可带微小虚部） ----------
def pass6():
    z0 = 100
    zl = 80 + 100j
    zin_doc = 90 - 109j
    zin_b = zin_doc / z0
    zl_b = zl / z0
    t = (zin_b - zl_b) / (1j * (1 - zin_b * zl_b))
    bl = np.arctan(t)
    z_calc = zin_tan(zl, z0, bl)
    ok(
        "Pass6 Lec07-4 Zin closure",
        abs(z_calc - zin_doc) < 1e-6,
        f"tan解闭合 Zin={z_calc}; Re(l/lam)={float(np.real(bl/(2*np.pi))):.4f}",
    )


# ---------- 方法7：Lec08-3 —— 分段：并联用导纳，线用阻抗 ----------
def pass7():
    zc = 100
    zp = 50 + 50j
    y_par = 1 / zc + 1 / zp
    z_par = 1 / y_par
    zin = zin_tan(z_par, zc, np.pi / 4)
    ok(
        "Pass7 Lec08-3 Zin",
        abs(zin - (100 + 100j)) < 0.5,
        str(zin),
    )


# ---------- 方法8：Lec08-4 —— 并联匹配方程直接验 ----------
def pass8():
    zc = 50
    zl = 100 - 50j
    d, l = 0.125, 0.125
    zd = zin_tan(zl, zc, 2 * np.pi * d)
    yd = 1 / zd
    yc = 1 / zc
    ys = -1j * yc / np.tan(2 * np.pi * l)
    ok(
        "Pass8 Lec08-4 Ysum==Yc",
        abs(yd + ys - yc) < 1e-6,
        f"Ytot={yd+ys}",
    )


# ---------- 方法9：Lec06-4 —— 随机 Zbar 恒等式 ----------
def pass9():
    z0 = 50.0
    for _ in range(200):
        zr = np.random.uniform(0.2, 5)
        zi = np.random.uniform(-5, 5)
        zb = zr + 1j * zi
        zl = zb * z0
        z_b = zl
        z_a = z0**2 / z_b
        yb = (1 / z_b) * z0
        za_bar = z_a / z0
        ok_one = abs(za_bar - yb) < 1e-9
        if not ok_one:
            ok("Pass9 Lec06-4 random", False, f"za_bar={za_bar} yb={yb}")
            return
    ok("Pass9 Lec06-4 random (200)", True, "barZ_A==barY_B")


# ---------- 方法10：Lec08-6 双支节 —— 密网格 + 残差 ----------
def pass10():
    z0 = 100.0
    zl = 50 + 100j
    zbar_l = zl / z0
    y_after_q = 1 / (1 / zbar_l)

    def y_from_zbar_move(y_in: complex, d_lam: float) -> complex:
        z = 1 / y_in
        z_phys = z * z0
        bl = 2 * np.pi * d_lam
        z2 = zin_tan(z_phys, z0, bl)
        return z0 / z2

    def residual(l1: float, l2: float) -> float:
        y1 = y_after_q
        y_a = y1 - 1j / np.tan(2 * np.pi * l1)
        y2 = y_from_zbar_move(y_a, 1 / 8)
        y_f = y2 - 1j / np.tan(2 * np.pi * l2)
        return abs(y_f - 1.0)

    best = 1e9
    best_l1 = best_l2 = 0.0
    for l1 in np.linspace(0.001, 0.249, 1200):
        for l2 in np.linspace(0.001, 0.249, 1200):
            r = residual(l1, l2)
            if r < best:
                best, best_l1, best_l2 = r, l1, l2
    ok(
        "Pass10 Lec08-6 residual",
        best < 0.02,
        f"min|y-1|={best:.4e} at l1={best_l1:.4f} l2={best_l2:.4f}",
    )
    ok(
        "Pass10 Lec08-6 near doc",
        abs(best_l1 - 0.136) < 0.02 and abs(best_l2 - 0.150) < 0.02,
        "",
    )


# ---------- 附加：Lec06-1 并联与 Γ ----------
def bonus_lec06_1():
    zc = 1.0
    r1, r2 = 2 / 3, 1 / 3
    zb1 = zc**2 / r1
    zb2 = zc**2 / r2
    zb = 1 / (1 / zb1 + 1 / zb2)
    g1 = (r1 - zc) / (r1 + zc)
    g2 = (r2 - zc) / (r2 + zc)
    ok("Bonus Lec06-1 Z_B==Zc", abs(zb - zc) < 1e-12, f"Z_B={zb}")
    ok("Bonus Lec06-1 G1", abs(g1 + 0.2) < 1e-12, str(g1))
    ok("Bonus Lec06-1 G2", abs(g2 + 0.5) < 1e-12, str(g2))


if __name__ == "__main__":
    print("=== 10+ 种方法交叉审查 ===\n")
    pass1()
    pass2()
    pass3()
    pass4()
    pass5()
    pass6()
    pass7()
    pass8()
    pass9()
    pass10()
    bonus_lec06_1()
    print(f"\n--- 汇总: PASS={len(PASS)} FAIL={len(FAIL)} ---")
    if FAIL:
        print("失败项:", FAIL)
        raise SystemExit(1)
    print("全部通过。")
