"""Figures for the RQ2 analysis (outputs of 17_rq_analysis.py).

Usage:
    python -I scripts/18_figures.py <analysis_dir>
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker  # noqa: E402
import pandas as pd  # noqa: E402

SERIES, INK, INK2, GRID, SURFACE = "#2a78d6", "#0b0b0b", "#52514e", "#e1e0d9", "#fcfcfb"
LABEL = {"gameplay": "Gameplay / rules", "ui": "UI", "crash_hang": "Crash / hang", "visual": "Visual",
         "audio": "Audio", "other": "Other (save, network,\nperformance, tooling)", "all": "All"}
plt.rcParams.update({"font.size": 10, "axes.edgecolor": GRID, "axes.labelcolor": INK2, "xtick.color": INK2,
                     "ytick.color": INK, "figure.facecolor": SURFACE, "axes.facecolor": SURFACE})


def style(ax):
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0)


def rate_plot(t, path, title):
    t = t.iloc[::-1].reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    for i, r in t.iterrows():
        ax.plot([r.ci_low * 100, r.ci_high * 100], [i, i], color=SERIES, linewidth=2, solid_capstyle="round")
        ax.scatter(r.rate * 100, i, s=64, color=SERIES, edgecolor=SURFACE, linewidth=2, zorder=3)
        ax.text(r.ci_high * 100 + 0.3, i, f"{r.rate * 100:.1f}%  ({r.with_test}/{r.issues:,}, {r.projects} proj.)",
                va="center", color=INK2, fontsize=8.5)
    ax.set_yticks(range(len(t)), [LABEL[s] for s in t.symptom])
    ax.set_xlabel("Fixes whose final diff changes a test-candidate file (%)\n"
                  "with 95% project-cluster bootstrap CI")
    ax.set_xlim(0, max(t.ci_high) * 100 + 7)
    ax.set_title(title, loc="left", color=INK, fontsize=11)
    style(ax)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def or_plot(g, path, title):
    g = g[g.index.str.startswith("symptom=")].copy()
    g.index = [LABEL[i.split("=")[1]] for i in g.index]
    g = g.sort_values("odds_ratio")
    fig, ax = plt.subplots(figsize=(7.2, 2.9))
    for i, (name, r) in enumerate(g.iterrows()):
        ax.plot([r.ci_low, r.ci_high], [i, i], color=SERIES, linewidth=2, solid_capstyle="round")
        ax.scatter(r.odds_ratio, i, s=64, color=SERIES, edgecolor=SURFACE, linewidth=2, zorder=3)
        ax.text(1.12, i, f"{r.odds_ratio:.2f} [{r.ci_low:.2f}, {r.ci_high:.2f}]", va="center",
                color=INK2, fontsize=8.5)
    ax.axvline(1, color=INK2, linewidth=1, linestyle=(0, (3, 3)))
    ax.set_xscale("log")
    ax.set_xticks([0.25, 0.5, 1], ["0.25", "0.5", "1"])
    ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    ax.set_xlim(0.2, 2.0)
    ax.set_yticks(range(len(g)), g.index)
    ax.set_xlabel("Odds ratio vs. gameplay/rules (log scale)\n"
                  "GEE with project clusters, adjusted for log #changed paths and year")
    ax.set_title(title, loc="left", color=INK, fontsize=11)
    style(ax)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def concentration_plot(pp, path, title):
    s = pp.sort_values("with_test", ascending=False).with_test
    cum = s.cumsum() / s.sum() * 100
    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    ax.plot(range(1, len(cum) + 1), cum.values, color=SERIES, linewidth=2)
    k = int((s > 0).sum())
    ax.axvline(k, color=INK2, linewidth=1, linestyle=(0, (3, 3)))
    ax.text(k + 2, 40, f"{k} of {len(s)} projects have\nany fix with a test change", color=INK2, fontsize=8.5)
    ax.text(6, cum.iloc[4] - 8, f"top 5 projects: {cum.iloc[4]:.0f}%", color=INK2, fontsize=8.5)
    ax.scatter(5, cum.iloc[4], s=40, color=SERIES, zorder=3)
    ax.set_xlabel("Projects, ranked by number of fixes with a test change")
    ax.set_ylabel("Cumulative share (%)")
    ax.set_ylim(0, 102)
    ax.set_title(title, loc="left", color=INK, fontsize=11)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def main():
    d = Path(sys.argv[1])
    t = pd.read_csv(d / "rq2_test_rate_by_symptom.csv")
    rate_plot(t, d / "fig_rq2_test_rate_by_symptom.png",
              "Test-file changes in game bug fixes, by symptom")
    g = pd.read_csv(d / "rq2_gee_all.csv", index_col=0)
    or_plot(g, d / "fig_rq2_gee_odds_ratios.png", "Odds of a test change relative to gameplay/rules fixes")
    pp = pd.read_csv(d / "rq2_per_project.csv", index_col=0)
    pp["with_test"] = (pp.n * pp.rate).round().astype(int)
    concentration_plot(pp, d / "fig_rq2_project_concentration.png",
                       "Fixes with a test change are concentrated in few projects")
    print("figures written")


if __name__ == "__main__":
    main()
