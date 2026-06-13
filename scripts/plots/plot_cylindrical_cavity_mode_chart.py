"""
Cylindrical cavity mode chart schematic for exam review.
Run: python scripts/plots/plot_cylindrical_cavity_mode_chart.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parents[2] / "assets" / "images"
OUT.mkdir(parents=True, exist_ok=True)
DPI = 170


def mode_curve(d_over_l_sq: np.ndarray, slope: float, intercept: float) -> np.ndarray:
    """Schematic (fD)^2 * 1e-20 vs (D/l)^2 — linear family for teaching."""
    return slope * d_over_l_sq + intercept


def main() -> None:
    x = np.linspace(0.5, 6.0, 200)

    # Schematic slopes (not exact textbook values; shape-only for exam reading)
    curves = [
        ("TM010", 0.8, 1.0, "#1f77b4", "-"),
        ("TM110", 2.5, 2.0, "#ff7f0e", "-"),
        ("TM111 (work)", 3.2, 3.5, "#d62728", "-", 3.0),
        ("TM112", 3.2, 5.5, "#ff9896", "--"),
        ("TE111", 4.0, 1.5, "#2ca02c", "-"),
        ("TE011", 4.0, 4.0, "#9467bd", "-"),
        ("TM011", 4.0, 4.0, "#8c564b", ":"),
        ("TE112", 5.5, 2.0, "#17becf", "-"),
        ("TM210", 5.5, 4.5, "#bcbd22", "-"),
    ]

    fig, ax = plt.subplots(figsize=(8.5, 5.5))

    for item in curves:
        name, slope, intercept, color, ls = item[:5]
        lw = 2.8 if "work" in name else 1.6
        y = mode_curve(x, slope, intercept)
        ax.plot(x, y, color=color, ls=ls, lw=lw, label=name)

    # Work point
    x0 = 3.0
    y0 = mode_curve(np.array([x0]), 3.2, 3.5)[0]
    ax.plot(x0, y0, "o", color="#d62728", ms=10, zorder=5)
    ax.axvline(x0, color="0.75", ls=":", lw=1)

    # Annotation boxes for interference types
    ax.annotate(
        "self: TM110, TM112",
        xy=(2.2, mode_curve(np.array([2.2]), 2.5, 2.0)[0]),
        xytext=(0.8, 8),
        fontsize=8,
        arrowprops=dict(arrowstyle="->", color="#ff7f0e", lw=1),
    )
    ax.annotate(
        "cross: TE112 x TM210",
        xy=(4.8, mode_curve(np.array([4.8]), 5.5, 4.0)[0]),
        xytext=(3.5, 18),
        fontsize=8,
        arrowprops=dict(arrowstyle="->", color="#17becf", lw=1),
    )
    ax.annotate(
        "degenerate: TE011 = TM011",
        xy=(4.0, mode_curve(np.array([4.0]), 4.0, 4.0)[0]),
        xytext=(4.2, 11),
        fontsize=8,
        arrowprops=dict(arrowstyle="->", color="#9467bd", lw=1),
    )

    ax.set_xlabel(r"$(D/l)^2$", fontsize=11)
    ax.set_ylabel(r"$(fD)^2 \times 10^{-20}$", fontsize=11)
    ax.set_title("Cylindrical cavity mode chart (schematic for exam reading)", fontsize=11)
    ax.set_xlim(0.5, 6.0)
    ax.set_ylim(0, 22)
    ax.grid(True, alpha=0.25)
    ax.legend(loc="upper left", fontsize=7, ncol=2)

    fig.text(
        0.5,
        0.01,
        "Schematic only — classify interference types; verify frequencies with cavity formulas.",
        ha="center",
        fontsize=8,
        color="0.4",
    )

    out_path = OUT / "gpt-cylindrical-cavity-mode-chart.webp"
    fig.savefig(out_path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print("saved", out_path)


if __name__ == "__main__":
    main()
