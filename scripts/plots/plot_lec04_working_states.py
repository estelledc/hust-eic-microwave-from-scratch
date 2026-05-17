"""Lec04-1 辅助图：行波、纯驻波、行驻波沿线电压幅值包络示意（归一化）。"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parents[2] / "assets" / "images"
OUT.mkdir(parents=True, exist_ok=True)


def main():
    z = np.linspace(0, 2, 800)  # 2 个波长示意
    beta = 2 * np.pi

    # 行波：|cos(bz - wt)| 包络为常数 — 画 |U| = 常数
    traveling = np.ones_like(z)

    # 纯驻波 |sin(bz)|（短路端 z=0 为波节）
    standing = np.abs(np.sin(beta * z))

    # 行驻波 |1 + Gamma e^{-2j b z}|，|Gamma|=0.5
    Gamma = 0.5 * np.exp(1j * 0.7)
    mixed = np.abs(1 + Gamma * np.exp(-2j * beta * z))

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(z, traveling, label="Traveling: $|U|$ const.", lw=2)
    ax.plot(z, standing / standing.max(), label="Pure standing: $\\propto|\\sin\\beta z|$", lw=2)
    ax.plot(z, mixed / mixed.max(), label="Mixed: $|1+\\Gamma e^{-2j\\beta z}|$", lw=2)
    ax.set_xlabel(r"$z/\lambda$")
    ax.set_ylabel(r"normalized $|U|$")
    ax.set_title("Lec04 Q1 sketch: three regimes along line")
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()
    out_path = OUT / "lec04_working_states_envelope.png"
    fig.savefig(out_path, dpi=160)
    plt.close(fig)
    print("saved", out_path)


if __name__ == "__main__":
    main()
