"""TE10 rectangular waveguide: lambda_g/lambda0, vp/c, vg/c vs f/fc (air, lossless)."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
FIG = ROOT / "assets" / "images" / "lec_rect_wg_te10_dispersion.webp"


def main():
    r = np.linspace(1.001, 2.5, 500)  # f/fc
    lam0_over_lamg = np.sqrt(1 - 1 / r**2)
    vp_over_c = r * lam0_over_lamg  # = 1/sqrt(1-1/r^2)
    vg_over_c = 1 / vp_over_c

    fig, ax1 = plt.subplots(figsize=(7, 4))
    ax1.plot(r, 1 / lam0_over_lamg, label=r"$\lambda_g/\lambda_0$", color="C0")
    ax1.set_xlabel(r"$f/f_{c,\mathrm{TE10}}$")
    ax1.set_ylabel(r"$\lambda_g/\lambda_0$", color="C0")
    ax1.tick_params(axis="y", labelcolor="C0")
    ax1.grid(True, alpha=0.3)

    ax2 = ax1.twinx()
    ax2.plot(r, vp_over_c, label=r"$v_p/c$", color="C1", linestyle="--")
    ax2.plot(r, vg_over_c, label=r"$v_g/c$", color="C2", linestyle=":")
    ax2.set_ylabel(r"$v_p/c,\ v_g/c$", color="C1")
    ax2.tick_params(axis="y", labelcolor="C1")
    ax2.axhline(1.0, color="gray", linewidth=0.8, linestyle="-.")

    lines1, lab1 = ax1.get_legend_handles_labels()
    lines2, lab2 = ax2.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, lab1 + lab2, loc="upper right", fontsize=9)
    fig.suptitle("Air-filled rectangular WG, dominant TE10 (lossless schematic)")
    fig.tight_layout()
    FIG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG, dpi=160)
    plt.close(fig)
    print("wrote", FIG)


if __name__ == "__main__":
    main()
