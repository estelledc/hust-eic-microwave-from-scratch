"""Numerical cross-check for 《微波技术基础》第二次与第三次作业标准解答.md"""
import numpy as np


def zin(zl, z0, bl):
    t = np.tan(bl)
    den = z0 + 1j * zl * t
    if abs(den) < 1e-9:
        return np.inf + 0j
    return z0 * (zl + 1j * z0 * t) / den


def z_at_d(zl, z0, d_lam):
    return zin(zl, z0, 2 * np.pi * d_lam)


def y_at_d(zl, z0, d_lam):
    return 1 / z_at_d(zl, z0, d_lam)


def assert_close(name, got, expect, rtol=1e-3, atol=1e-2):
    if isinstance(expect, complex):
        ok = abs(got - expect) <= atol + rtol * max(abs(expect), 1)
    else:
        ok = abs(got - expect) <= atol + rtol * max(abs(expect), 1)
    print(f"{'OK' if ok else 'FAIL'} {name}: got {got}, expect ~{expect}")
    return ok


ok_all = True

print("=== Lec06-2 ===")
Zl, Zc = -75j, 50
bl_inf = np.pi - np.arctan(2 / 3)
bl_sh = np.arctan(1.5)
ok_all &= assert_close(
    "l/lam Zin=inf", bl_inf / (2 * np.pi), 0.406, atol=0.002
)
ok_all &= assert_close(
    "l/lam Zin=0", bl_sh / (2 * np.pi), 0.156, atol=0.002
)
z_inf = zin(Zl, Zc, bl_inf - 1e-6)
ok_all &= abs(z_inf) > 1e4
print("  |Zin| at near-pole", abs(z_inf))
z_sh = zin(Zl, Zc, bl_sh)
ok_all &= assert_close("Zin short", z_sh, 0j, atol=1e-6)

print("=== Lec06-3 barZ ===")
refs = [
    ((0.5, 45), 1.38 + 1.30j),
    ((0.35, 30), 1.70 + 0.68j),
]
for (mag, ang), zexp in refs:
    G = mag * np.exp(1j * np.deg2rad(ang))
    zb = (1 + G) / (1 - G)
    ok_all &= assert_close(f"barZ |G|={mag} ang={ang}", zb, zexp, atol=0.02)

print("=== Lec06-5 ZL ===")
Zc = 50
rho = 2
g = (rho - 1) / (rho + 1)
zmin = 0.1
GL = -g * np.exp(1j * 4 * np.pi * zmin)
ZL = Zc * (1 + GL) / (1 - GL)
ok_all &= assert_close("ZL Lec06-5", ZL, 33.74 - 24.07j, atol=0.05)

print("=== Lec07-1 Gamma ===")
ZL, Zc = 100 + 75j, 50
G = (ZL - Zc) / (ZL + Zc)
ok_all &= assert_close("Re(G)", G.real, 0.467, atol=0.002)
ok_all &= assert_close("Im(G)", G.imag, 0.267, atol=0.002)
ok_all &= assert_close("|G|", abs(G), 0.538, atol=0.002)

print("=== Lec07-2 rho ===")
ZL = 100 - 50j
G = (ZL - Zc) / (ZL + Zc)
rho = (1 + abs(G)) / (1 - abs(G))
ok_all &= assert_close("rho", rho, 2.618, atol=0.01)

print("=== Lec07-3 Zin ===")
ZL = 50 - 100j
Zin = zin(ZL, Zc, 0.4 * np.pi)
ok_all &= assert_close("Zin re", Zin.real, 8.63, atol=0.05)
ok_all &= assert_close("Zin im", Zin.imag, 3.82, atol=0.05)

print("=== Lec07-4 l ===")
zlbar = (80 + 100j) / 100
zinbar = (90 - 109j) / 100
t = (zinbar - zlbar) / (1j * (1 - zinbar * zlbar))
llam = np.arctan(t) / (2 * np.pi)
ok_all &= assert_close("l/lam", float(np.real(llam)), 0.191, atol=0.002)
ok_all &= assert_close("l_m", float(np.real(llam)) * 10, 1.91, atol=0.02)

print("=== Lec07-5 ZL ===")
g = 1 / 3
GL = -g * np.exp(1j * 0.8 * np.pi)
ZL = 50 * (1 + GL) / (1 - GL)
ok_all &= assert_close("ZL re", ZL.real, 77.73, atol=0.05)
ok_all &= assert_close("ZL im", ZL.imag, -34.27, atol=0.05)

print("=== Lec08-2 ===")
Zc = 600
ZL = 22 - 66j
lam = 3e8 / 200e6
L = 32
beta = 2 * np.pi / lam
GL = (ZL - Zc) / (ZL + Zc)
rho = (1 + abs(GL)) / (1 - abs(GL))
Zin = zin(ZL, Zc, beta * L)
ok_all &= assert_close("lam", lam, 1.5, atol=1e-6)
ok_all &= assert_close("|GL|", abs(GL), 0.930, atol=0.002)
ok_all &= assert_close("rho", rho, 27.6, atol=0.3)
ok_all &= assert_close("Zin re", Zin.real, 133.5, atol=1)
ok_all &= assert_close("Zin im", Zin.imag, -1354.9, atol=2)

ds = np.linspace(1e-6, 0.15, 300000)
best = (1e9, 0.0)
for d in ds:
    z = z_at_d(ZL, Zc, d / lam)
    e = abs(z.imag)
    if e < best[0]:
        best = (e, d)
d0 = best[1]
z0 = z_at_d(ZL, Zc, d0 / lam)
Z0T = np.sqrt(Zc * z0.real)
ok_all &= assert_close("d_m", d0, 0.0262, atol=0.0005)
ok_all &= assert_close("R", z0.real, 21.74, atol=0.05)
ok_all &= assert_close("Z0T", Z0T, 114.2, atol=0.2)

print("=== Lec08-3 ===")
Zc = 100
Zp = 50 + 50j
Ytot = 1 / Zc + 1 / Zp
Zpar = 1 / Ytot
Zin = zin(Zpar, Zc, np.pi / 4)
ok_all &= assert_close("Zpar re", Zpar.real, 40, atol=0.01)
ok_all &= assert_close("Zpar im", Zpar.imag, 20, atol=0.01)
ok_all &= assert_close("Zin", Zin, 100 + 100j, atol=0.5)

print("=== Lec08-4 stub match ===")
Zc = 50
ZL = 100 - 50j
d = 0.125
Yd = y_at_d(ZL, Zc, d)
Yc = 1 / Zc
ok_all &= assert_close("Re(Y)/Yc at d", Yd.real / Yc, 1.0, atol=0.02)
# Im(Y_line) - Yc/tan(beta l) = 0 => tan(beta l) = Yc/Im(Y_line)
B_line = Yd.imag
tan_l = Yc / B_line
bl = np.arctan(tan_l)
if bl < 0:
    bl += np.pi
l_lam = bl / (2 * np.pi)
ok_all &= assert_close("l/lam from Y", l_lam, 0.125, atol=0.02)
print("  Im(Yd)*Zc", Yd.imag * Zc, "l/lam", l_lam)

print("=== Lec08-5 (numeric search) ===")
Zc = 100
YL = 0.0425 + 0.0175j
ZL = 1 / YL
Yc = 1 / Zc

cands5 = []
for d in np.linspace(0.001, 0.499, 8000):
    Y = y_at_d(ZL, Zc, d)
    if abs(Y.real - Yc) > 0.002:
        continue
    if abs(Y.imag) < 1e-9:
        continue
    tanb = Yc / Y.imag
    for k in range(-2, 4):
        bl = np.arctan(tanb) + k * np.pi
        if bl <= 0 or bl >= np.pi:
            continue
        l = bl / (2 * np.pi)
        if l > 0.5:
            continue
        Ys = -1j * Yc / np.tan(bl)
        err = abs(Y + Ys - Yc)
        if err < 1e-5:
            cands5.append((d, l, err))
# 多解：取距负载最近的一组（与文档「常用解」一致）
cands5.sort(key=lambda x: x[0])
best5 = (cands5[0][2], cands5[0][0], cands5[0][1]) if cands5 else (1e9, 0, 0)
print("  shortest-d solution (err, d, l)", best5)
ok_all &= assert_close("Lec08-5 d/lam", best5[1], 0.0806, atol=0.003)
ok_all &= assert_close("Lec08-5 l/lam", best5[2], 0.419, atol=0.01)

print("=== Lec08-6 double stub ===")
Z0 = 100
ZL = 50 + 100j
zL = ZL / Z0
# after lambda/4 from load: z' = 1/zL
zp = 1 / zL
yp = 1 / zp
print("  after lam/4 zbar", zp, "ybar", yp)


def y_transform(y_in, d_lam):
    """Move from load toward generator by d_lam on Z0 line; admittance."""
    z = 1 / y_in
    z2 = zin(z * Z0, Z0, 2 * np.pi * d_lam) / Z0
    return 1 / z2


def double_stub_err(l1, l2):
    """l1 at first stub (after quarter wave), l2 at second after lambda/8."""
    y1 = yp
    # parallel short stub l1: Y -> Y + j B_stub
    bl1 = 2 * np.pi * l1
    y_after1 = y1 - 1j / np.tan(bl1)
    y2 = y_transform(y_after1, 1 / 8)
    bl2 = 2 * np.pi * l2
    y_final = y2 - 1j / np.tan(bl2)
    return abs(y_final - 1.0)


best6 = (1e9, 0.0, 0.0)
for l1 in np.linspace(0.001, 0.25, 400):
    for l2 in np.linspace(0.001, 0.25, 400):
        e = double_stub_err(l1, l2)
        if e < best6[0]:
            best6 = (e, l1, l2)
print("  coarse grid best", best6)
# refine
l1c, l2c = best6[1], best6[2]
for _ in range(3):
    for dl1 in np.linspace(-0.02, 0.02, 81):
        for dl2 in np.linspace(-0.02, 0.02, 81):
            e = double_stub_err(l1c + dl1, l2c + dl2)
            if e < best6[0]:
                best6 = (e, l1c + dl1, l2c + dl2)
    l1c, l2c = best6[1], best6[2]
print("  refined best", best6)
ok_all &= assert_close("Lec08-6 l1/lam", best6[1], 0.136, atol=0.02)
ok_all &= assert_close("Lec08-6 l2/lam", best6[2], 0.150, atol=0.02)

print("=== Lec13-3 (third homework) fc GHz ===")
c = 299792458.0
a, b = 10e-3, 6e-3


def fc_mn(m, n, a_, b_, eps_r=1.0):
    kc = np.sqrt((m * np.pi / a_) ** 2 + (n * np.pi / b_) ** 2)
    return c / np.sqrt(eps_r) * kc / (2 * np.pi)


ok_all &= assert_close("TE10 fc", fc_mn(1, 0, a, b) / 1e9, 14.99, atol=0.02)
ok_all &= assert_close("TE20 fc", fc_mn(2, 0, a, b) / 1e9, 29.98, atol=0.02)
ok_all &= assert_close("TE21 fc", fc_mn(2, 1, a, b) / 1e9, 39.02, atol=0.03)


def lam_c_mn(m, n, a_, b_):
    kc = np.sqrt((m * np.pi / a_) ** 2 + (n * np.pi / b_) ** 2)
    return 2 * np.pi / kc


def count_modes_rect(a_, b_, lam0):
    """Count distinct TE_mn and TM_mn modes that propagate (lam0 < lam_c)."""
    cnt = 0
    for m in range(0, 12):
        for n in range(0, 12):
            if m == 0 and n == 0:
                continue
            if m == 0 and n > 0:
                lc = lam_c_mn(m, n, a_, b_)
                if lam0 < lc - 1e-12:
                    cnt += 1
            elif n == 0 and m > 0:
                lc = lam_c_mn(m, n, a_, b_)
                if lam0 < lc - 1e-12:
                    cnt += 1
            elif m > 0 and n > 0:
                lc = lam_c_mn(m, n, a_, b_)
                if lam0 < lc - 1e-12:
                    cnt += 2
    return cnt


print("=== Lec13-4 mode count ===")
a, b = 22.86e-3, 10.16e-3
ok_all &= assert_close("P4 n_modes", count_modes_rect(a, b, 18e-3), 5, atol=0.1)

print("=== Lec13-6 lam_c mm ===")
ok_all &= assert_close("TE10 lc mm", lam_c_mn(1, 0, a, b) * 1000, 45.72, atol=0.02)
ok_all &= assert_close("TE11 lc mm", lam_c_mn(1, 1, a, b) * 1000, 18.57, atol=0.02)

print("=== Lec13-7 lambda_g ===")
ok_all &= assert_close("P7 lambda_g mm", 2 * 22.40, 44.80, atol=0.01)

print("=== Lec13-8 ybar + stub (TE10 equiv line) ===")
lam0 = 32e-3
fc10 = c / (2 * a)
f0 = c / lam0
lam_g = lam0 / np.sqrt(1 - (fc10 / f0) ** 2)
beta = 2 * np.pi / lam_g
rho = 3.0
gmag = (rho - 1) / (rho + 1)
zmin = 9e-3
ths = np.linspace(-np.pi, np.pi, 400001)
best = (1e9, 0.0)
for th in ths:
    gL = gmag * np.exp(1j * th)
    gz = gL * np.exp(-1j * 2 * beta * zmin)
    v = abs(1 + gz)
    if v < best[0]:
        best = (v, th)
theta = best[1]
gL = gmag * np.exp(1j * theta)
zbar_l = (1 + gL) / (1 - gL)
ybar_l = 1 / zbar_l
ok_all &= assert_close("P8 Re(ybar)", ybar_l.real, 0.3631, atol=0.002)
ok_all &= assert_close("P8 Im(ybar)", ybar_l.imag, 0.2803, atol=0.002)


def ybar_at_z(g_l, z_m):
    gz = g_l * np.exp(-1j * 2 * beta * z_m)
    zb = (1 + gz) / (1 - gz)
    return 1 / zb


d_best = None
for i in range(1, 300000):
    d = i * (lam_g / 2) / 300000
    yb = ybar_at_z(gL, d)
    if abs(yb.real - 1.0) < 1e-4 and d > 1e-6:
        d_best = d
        y_line = yb
        break
ok_all &= assert_close("P8 d_mm", d_best * 1000, 5.27, atol=0.03)
ok_all &= assert_close("P8 Bstub", (-y_line.imag), -1.155, atol=0.02)

print("=== Lec13-9 rho ===")
gL9 = ((0.5 - 1) / (0.5 + 1)) + 0j
rho9 = (1 + abs(gL9)) / (1 - abs(gL9))
ok_all &= assert_close("P9 rho", rho9, 2.0, atol=1e-6)

print("=== Lec13-10 mode count 6 GHz ===")
ok_all &= assert_close(
    "P10 n_modes",
    count_modes_rect(72.14e-3, 34.04e-3, c / 6e9),
    5,
    atol=0.1,
)

print("\n=== SUMMARY ===", "ALL OK" if ok_all else "SOME FAILURES")
