"""Figure for RQ2b: test-change rate by symptom, discrete vs continuous games.

Usage:
    python -I scripts/21_game_type_figure.py <game_type_dir>
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

BLUE, ORANGE, INK, INK2, GRID, SURFACE = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#e1e0d9", "#fcfcfb"
LABEL = {"all": "All", "gameplay": "Gameplay / rules", "ui": "UI", "crash_hang": "Crash / hang",
         "visual": "Visual", "audio": "Audio", "other": "Other"}
ORDER = ["all", "gameplay", "ui", "crash_hang", "visual", "audio", "other"]
SERIES = [("discrete", "Discrete (turn/move-based)", BLUE, "o", -0.17),
          ("continuous", "Continuous (real-time)", ORANGE, "s", 0.17)]


def main():
    d = Path(sys.argv[1])
    cross = pd.read_csv(d / "rate_by_game_type_and_symptom.csv")
    tot = pd.read_csv(d / "rate_by_game_type.csv").assign(symptom="all")
    t = pd.concat([tot, cross], ignore_index=True)
    # Sized for one column of the two-column report (about 3.4 in), so that
    # the fonts appear at their nominal size instead of being scaled down.
    plt.rcParams.update({"font.size": 8, "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
                         "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK})
    fig, ax = plt.subplots(figsize=(3.4, 3.4))
    for gt, name, color, marker, off in SERIES:
        s = t[t.game_type.eq(gt)].set_index("symptom")
        for i, sym in enumerate(ORDER):
            if sym not in s.index:
                continue
            r = s.loc[sym]
            y = len(ORDER) - 1 - i + off
            ax.plot([r.ci_low * 100, r.ci_high * 100], [y, y], color=color, linewidth=1.6, solid_capstyle="round")
            ax.scatter(r.rate * 100, y, s=26, marker=marker, color=color, edgecolor=SURFACE, linewidth=0.8,
                       zorder=3, label=name if sym == "all" else None)
            ax.text(r.ci_high * 100 + 0.5, y, f"{r.rate * 100:.1f}%", va="center", fontsize=7, color=INK2)
    ax.set_yticks(range(len(ORDER)), [LABEL[s] for s in reversed(ORDER)])
    ax.set_ylim(-0.6, len(ORDER) - 0.4)
    ax.set_xlabel("Test-changing fixes (%), 95% CI")
    ax.set_xlim(0, 28.5)
    ax.set_xticks([0, 5, 10, 15, 20, 25])
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.grid(axis="x", color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0)
    ax.legend(loc="lower center", bbox_to_anchor=(0.42, 1.0), ncol=1, frameon=False, fontsize=7.5,
              handletextpad=0.3, borderaxespad=0.2)
    fig.tight_layout(pad=0.3)
    fig.savefig(d / "fig_game_type_by_symptom.png", dpi=300)
    print("figure written")


if __name__ == "__main__":
    main()
