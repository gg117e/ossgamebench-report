"""RQ2b: do test-candidate changes in fixes differ between discrete (turn/move-based)
and continuous (real-time) games?

Inputs: the analysis table written by 17_rq_analysis.py and the provisional labels
from 19_game_type_labels.py. Mixed-type projects (2) are reported but left out of
the comparisons.

Usage:
    python -I scripts/20_game_type_analysis.py <interim_dir> <labels_csv> <out_dir> [--boot 2000]
"""
import argparse
import json
from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

warnings.filterwarnings("ignore")


def cluster_ci(df, col, reps, seed):
    rng = np.random.default_rng(seed)
    agg = df.groupby("pk")[col].agg(["sum", "size"])
    vals = []
    for _ in range(reps):
        s = agg.iloc[rng.integers(0, len(agg), len(agg))]
        vals.append(s["sum"].sum() / s["size"].sum())
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def rates(df, by, reps, seed):
    rows = []
    for key, g in df.groupby(by):
        lo, hi = cluster_ci(g, "test_final", reps, seed)
        rows.append({**dict(zip(by if isinstance(by, list) else [by], key if isinstance(key, tuple) else [key])),
                     "issues": len(g), "projects": g.pk.nunique(), "with_test": int(g.test_final.sum()),
                     "rate": g.test_final.mean(), "ci_low": lo, "ci_high": hi})
    return pd.DataFrame(rows)


def gee(df, formula):
    """Exchangeable working correlation; falls back to independence (still cluster-robust
    standard errors) when the exchangeable fit does not converge to finite estimates."""
    out = None
    for cov in (sm.cov_struct.Exchangeable(), sm.cov_struct.Independence()):
        m = smf.gee(formula, groups="pk", data=df, family=sm.families.Binomial(), cov_struct=cov).fit()
        ci = m.conf_int()
        out = pd.DataFrame({"odds_ratio": np.exp(m.params), "ci_low": np.exp(ci[0]), "ci_high": np.exp(ci[1]),
                            "p_value": m.pvalues, "cov_struct": type(cov).__name__})
        if np.isfinite(out[["odds_ratio", "ci_low", "ci_high"]].to_numpy()).all():
            break
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("interim_dir", type=Path)
    ap.add_argument("labels_csv", type=Path)
    ap.add_argument("out_dir", type=Path)
    ap.add_argument("--boot", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=20261114)
    args = ap.parse_args()
    a = pd.read_parquet(args.interim_dir / "final_diff_v1" / "analysis_table.parquet")
    lab = pd.read_csv(args.labels_csv)
    df = a.merge(lab[["pk", "game_type", "web", "idle"]], on="pk", how="left", validate="many_to_one")
    if df.game_type.isna().any():
        raise ValueError("Unlabelled projects in the analysis table")
    df["test_final"] = df.test_final.astype(bool)
    df["y"] = df.test_final.astype(int)
    df["discrete"] = df.game_type.eq("discrete").astype(int)
    df["web_i"] = df.web.astype(int)
    df["log_paths"] = np.log1p(df.n_final_paths)
    df["year_c"] = df.year - 2020
    size = df.groupby("pk").size()
    df["log_proj_issues"] = np.log(df.pk.map(size))
    main = df[df.game_type.ne("mixed")].copy()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    res = {"labels": lab.game_type.value_counts().to_dict(), "web_projects": int(lab.web.sum()),
           "issues_by_type": df.game_type.value_counts().to_dict()}
    t_type = rates(main, "game_type", args.boot, args.seed)
    t_type.to_csv(args.out_dir / "rate_by_game_type.csv", index=False)
    t_cross = rates(main, ["game_type", "symptom"], args.boot, args.seed)
    t_cross.to_csv(args.out_dir / "rate_by_game_type_and_symptom.csv", index=False)
    t_web = rates(main, ["game_type", "web"], args.boot, args.seed)
    t_web.to_csv(args.out_dir / "rate_by_game_type_and_web.csv", index=False)

    # project level: does the project have any fix with a test change / any test history?
    proj = main.groupby("pk").agg(game_type=("game_type", "first"), web=("web_i", "first"),
                                  n=("y", "size"), any_test_fix=("y", "max"),
                                  test_history=("project_has_tests", "first"), rate=("y", "mean"))
    proj["discrete"] = proj.game_type.eq("discrete").astype(int)
    proj["log_n"] = np.log(proj.n)
    pt = proj.groupby("game_type").agg(projects=("n", "size"), with_any_test_fix=("any_test_fix", "sum"),
                                       with_test_history=("test_history", "sum"),
                                       median_rate=("rate", "median"),
                                       median_rate_ge20=("rate", lambda s: s[proj.loc[s.index, "n"] >= 20].median()))
    pt.to_csv(args.out_dir / "project_level_by_game_type.csv")
    logit = smf.logit("any_test_fix ~ discrete + web + log_n", data=proj).fit(disp=0)
    ci = logit.conf_int()
    res["project_logit_any_test_fix"] = {k: {"odds_ratio": round(float(np.exp(logit.params[k])), 3),
                                             "ci": [round(float(np.exp(ci.loc[k, 0])), 3), round(float(np.exp(ci.loc[k, 1])), 3)],
                                             "p": round(float(logit.pvalues[k]), 4)} for k in logit.params.index}

    models = {
        "type_only": "y ~ discrete",
        "type_symptom": "y ~ discrete + C(symptom, Treatment('gameplay'))",
        "full": "y ~ discrete + C(symptom, Treatment('gameplay')) + web_i + log_paths + year_c + log_proj_issues",
    }
    gee_out = {}
    for name, f in models.items():
        g = gee(main, f)
        g.to_csv(args.out_dir / f"gee_{name}.csv")
        gee_out[name] = {k: [round(float(v), 3) for v in g.loc[k, ["odds_ratio", "ci_low", "ci_high", "p_value"]]]
                         for k in g.index if k in ("discrete", "web_i")}
    res["gee"] = gee_out
    # sensitivity on the full model's discrete OR
    top5 = main[main.test_final].pk.value_counts().index[:5].tolist()
    sens = {}
    for name, d in [("without_top5_test_projects", main[~main.pk.isin(top5)]),
                    ("native_only", main[main.web_i.eq(0)]),
                    ("web_only", main[main.web_i.eq(1)]),
                    ("without_idle", main[~main.idle.astype(bool)]),
                    ("projects_with_test_history", main[main.project_has_tests])]:
        try:
            g = gee(d, models["full"].replace(" + web_i", "") if name in ("native_only", "web_only") else models["full"])
            sens[name] = {"issues": len(d), "projects": int(d.pk.nunique()),
                          "rate_discrete": round(float(d[d.discrete.eq(1)].y.mean()), 4),
                          "rate_continuous": round(float(d[d.discrete.eq(0)].y.mean()), 4),
                          "or_discrete": [round(float(v), 3) for v in g.loc["discrete", ["odds_ratio", "ci_low", "ci_high", "p_value"]]]}
        except Exception as e:  # small subsets may not converge
            sens[name] = {"error": str(e)[:200]}
    res["top5_test_projects"] = top5
    res["sensitivity"] = sens
    (args.out_dir / "summary.json").write_text(json.dumps(res, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    pd.set_option("display.width", 200)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    print(t_type.round(4).to_string(index=False))
    print(pt.round(4).to_string())
    print(t_cross.pivot(index="symptom", columns="game_type", values="rate").round(4).to_string())
    print(t_cross.pivot(index="symptom", columns="game_type", values="issues").to_string())
    print(t_web.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
