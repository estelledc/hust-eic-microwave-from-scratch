"""
Lec06 作业第1题：主线 AB 与两支线（各 λ/4）上 |V|、|I| 幅值分布。
归一化：Eg=1, Zc=1，则匹配主线上 |V|=0.5，|I|=0.5。
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parents[2] / "assets" / "images"
OUT.mkdir(parents=True, exist_ok=True)

# 归一化
Eg = 1.0
Zc = 1.0
R1 = 2 * Zc / 3
R2 = Zc / 3


def gamma_load(R):
    return (R - Zc) / (R + Zc)


def v_mag_from_load(d_lam, gam, uplus_mag):
    """d_lam: 距负载的电长度 d/lambda; gam: 负载反射系数; |U+| 常数"""
    beta_d = 2 * np.pi * d_lam
    return uplus_mag * np.abs(1 + gam * np.exp(-2j * beta_d))


def i_mag_from_load(d_lam, gam, uplus_mag):
    beta_d = 2 * np.pi * d_lam
    return (uplus_mag / Zc) * np.abs(1 - gam * np.exp(-2j * beta_d))


def main():
    g1 = gamma_load(R1)
    g2 = gamma_load(R2)
    # 在距负载 d=λ/4（即支点 B）处 |V|=Eg/2
    fac1 = np.abs(1 + g1 * np.exp(-2j * np.pi))  # = |1 - g1|
    fac2 = np.abs(1 + g2 * np.exp(-2j * np.pi))  # = |1 - g2|
    u1 = (Eg / 2) / fac1
    u2 = (Eg / 2) / fac2

    d = np.linspace(0, 0.25, 400)  # 从负载到 B
    V1 = v_mag_from_load(d, g1, u1)
    I1 = i_mag_from_load(d, g1, u1)
    V2 = v_mag_from_load(d, g2, u2)
    I2 = i_mag_from_load(d, g2, u2)

    # 主线 AB：匹配，常数
    z_ab = np.linspace(0, 1, 200)  # 用任意归一化长度表示“有限长线段”，幅值常数
    Vab = np.full_like(z_ab, Eg / 2)
    Iab = np.full_like(z_ab, (Eg / 2) / Zc)

    fig, axes = plt.subplots(2, 1, figsize=(9, 7), sharex=False)

    ax = axes[0]
    ax.plot(z_ab, Vab, "b-", lw=2, label=r"Main $AB$: $|V|$")
    ax.plot(0.25 + d, V1, "r-", lw=2, label=r"Branch to $R_1$: $|V|$")
    ax.plot(0.25 + d, V2, "g--", lw=2, label=r"Branch to $R_2$: $|V|$")
    ax.axvline(0.25, color="k", ls=":", lw=1, alpha=0.6)
    ax.text(0.25, Eg / 2 * 1.05, r"$B$", ha="center")
    ax.set_ylabel(r"$|V|/E_g$")
    ax.set_title(r"Lec06 Q1: $|V|$ (normalized $E_g=1,\,Z_c=1$)")
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 0.5)
    ax.set_xticks([0, 0.125, 0.25, 0.375, 0.5])
    ax.set_xticklabels([r"$A$", "", r"$B$", "", r"load"])

    ax = axes[1]
    ax.plot(z_ab, Iab / (Eg / Zc), "b-", lw=2, label=r"Main $AB$: $|I|/(E_g/Z_c)$")
    ax.plot(0.25 + d, I1 / (Eg / Zc), "r-", lw=2, label=r"Branch $R_1$: $|I|/(E_g/Z_c)$")
    ax.plot(0.25 + d, I2 / (Eg / Zc), "g--", lw=2, label=r"Branch $R_2$: $|I|/(E_g/Z_c)$")
    ax.axvline(0.25, color="k", ls=":", lw=1, alpha=0.6)
    ax.set_ylabel(r"$|I|/(E_g/Z_c)$")
    ax.set_title(r"Lec06 Q1: $|I|$ (same normalization)")
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 0.5)
    ax.set_xticks([0, 0.125, 0.25, 0.375, 0.5])
    ax.set_xticklabels([r"$A$", "", r"$B$", "", r"load"])

    plt.tight_layout()
    out_path = OUT / "lec06_q1_voltage_current.webp"
    fig.savefig(out_path, dpi=160)
    plt.close(fig)
    print("saved", out_path)


if __name__ == "__main__":
    main()
