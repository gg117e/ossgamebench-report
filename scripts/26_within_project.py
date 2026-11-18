"""Within-project comparison of symptoms and project/symptom variance decomposition.

Usage:
    python -I scripts/26_within_project.py <interim_dir> <out_dir> [--reps 1000] [--seed 20261118]

Inputs: <interim_dir>/final_diff_v1/analysis_table.parquet (written by script 17).
Outputs (out_dir must not exist):
  conditional_logit.csv   odds ratios vs gameplay, conditional on project
                          (project fixed effects), Wald and project-bootstrap CIs
  deviance.csv            log-likelihood / McFadden R^2 of project-only, symptom-only,
                          additive and saturated models
  within_project_rates.csv  per-project rates by symptom for projects with >= 1 test change
  summary.json

Note: the class "gameplay" is the fallback of the keyword rules (issues that match no
symptom keyword).  A within-project comparison removes differences in the mix of
projects across symptom classes, which is the main way the fallback could create a
spurious difference.
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

SYMPTOMS = ["gameplay", "ui", "crash_hang", "visual", "audio", "other"]


def prep(df):
    d = df.copy()
    d["y"] = d.test_final.astype(int)
    d["log_paths"] = np.log1p(d.n_final_paths.astype(float))
    d["year_c"] = d.year - 2020
    for s in SYMPTOMS[1:]:
        d[f"s_{s}"] = (d.symptom == s).astype(int)
    return d


def informative(d):
    """Projects with both outcomes; others drop out of the conditional likelihood."""
    v = d.groupby("pk").y.agg(["min", "max"])
    keep = v.index[(v["min"] == 0) & (v["max"] == 1)]
    return d[d.pk.isin(keep)]


class _Res:
    def __init__(self, params, ci, pvalues):
        self.params, self._ci, self.pvalues = params, ci, pvalues

    def conf_int(self):
        return self._ci


def clogit(d, cols, robust=True):
    """Logistic regression with project fixed effects on informative projects.

    statsmodels' ConditionalLogit recurses once per fix and fails for projects with
    >1,000 fixes; with large groups the unconditional fixed-effects estimate is close
    to the conditional one.  Standard errors are clustered by project.
    """
    import statsmodels.api as sm
    d = informative(d)
    fe = pd.get_dummies(d.pk, dtype=float)
    X = pd.concat([d[cols].astype(float), fe], axis=1)
    model = sm.GLM(d.y.values, X.values, family=sm.families.Binomial())
    if robust:
        codes = pd.factorize(d.pk)[0]
        r = model.fit(cov_type="cluster", cov_kwds={"groups": codes})
    else:
        r = model.fit()
    k = len(cols)
    return _Res(np.asarray(r.params)[:k], np.asarray(r.conf_int())[:k], np.asarray(r.pvalues)[:k]), d


def bernoulli_ll(y, p):
    p = np.clip(p, 1e-12, 1 - 1e-12)
    return float(np.sum(y * np.log(p) + (1 - y) * np.log(1 - p)))


def group_mean_ll(d, keys):
    p = d.groupby(keys).y.transform("mean").values
    y = d.y.values
    exact = (p == 0) | (p == 1)          # contribute log(1) = 0 at the limit
    return bernoulli_ll(y[~exact], p[~exact])


def additive_ll(d):
    """Project fixed effects + symptom: fit on informative projects, others contribute 0."""
    import statsmodels.api as sm
    di = informative(d)
    X = pd.get_dummies(di[["pk"]], drop_first=False, dtype=float)
    X = pd.concat([X, di[[f"s_{s}" for s in SYMPTOMS[1:]]].astype(float)], axis=1)
    res = sm.GLM(di.y.values, X.values, family=sm.families.Binomial()).fit()
    return bernoulli_ll(di.y.values, res.fittedvalues)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("interim_dir")
    ap.add_argument("out_dir")
    ap.add_argument("--reps", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=20261118)
    a = ap.parse_args()
    out = Path(a.out_dir)
    if out.exists():
        sys.exit(f"{out} exists")
    df = pd.read_parquet(Path(a.interim_dir) / "final_diff_v1" / "analysis_table.parquet")
    d = prep(df)
    cols = [f"s_{s}" for s in SYMPTOMS[1:]] + ["log_paths", "year_c"]

    # 1. conditional logit (project fixed effects)
    res, di = clogit(d, cols)
    params, ci = res.params, res.conf_int()
    rng = np.random.default_rng(a.seed)
    projects = di.pk.unique()
    boot = []
    for _ in range(a.reps):
        pick = rng.choice(projects, size=len(projects), replace=True)
        parts = []
        for i, pk in enumerate(pick):
            part = di[di.pk == pk].copy()
            part["pk"] = f"{pk}#{i}"
            parts.append(part)
        b = pd.concat(parts)
        try:
            r, _ = clogit(b, cols, robust=False)
            boot.append(r.params)
        except Exception:
            continue
    boot = np.array(boot)
    rows = []
    for j, c in enumerate(cols):
        rows.append({
            "term": c.replace("s_", "symptom="), "odds_ratio": float(np.exp(params[j])),
            "wald_ci_low": float(np.exp(ci[j, 0])), "wald_ci_high": float(np.exp(ci[j, 1])),
            "p_value": float(res.pvalues[j]),
            "boot_ci_low": float(np.exp(np.percentile(boot[:, j], 2.5))),
            "boot_ci_high": float(np.exp(np.percentile(boot[:, j], 97.5))),
        })
    out.mkdir(parents=True)
    cl = pd.DataFrame(rows)
    cl.to_csv(out / "conditional_logit.csv", index=False)

    # 2. deviance decomposition on all fixes
    ll0 = bernoulli_ll(d.y.values, np.full(len(d), d.y.mean()))
    lls = {
        "null": ll0,
        "symptom_only": group_mean_ll(d, ["symptom"]),
        "project_only": group_mean_ll(d, ["pk"]),
        "project_plus_symptom": additive_ll(d),
        "project_x_symptom": group_mean_ll(d, ["pk", "symptom"]),
    }
    dev = pd.DataFrame([{"model": k, "log_likelihood": v, "mcfadden_r2": 1 - v / ll0} for k, v in lls.items()])
    dev.to_csv(out / "deviance.csv", index=False)

    # 3. per-project rates in projects with any test change
    tp = d[d.pk.isin(d.groupby("pk").y.max().loc[lambda s: s == 1].index)]
    rates = tp.pivot_table(index="pk", columns="symptom", values="y", aggfunc=["mean", "size"])
    rates.to_csv(out / "within_project_rates.csv")
    # share of projects (>= 20 fixes, >= 5 gameplay and >= 5 non-gameplay fixes) where gameplay rate > rest
    cmp_rows = []
    for pk, g in tp.groupby("pk"):
        gp, rest = g[g.symptom == "gameplay"], g[g.symptom != "gameplay"]
        if len(g) >= 20 and len(gp) >= 5 and len(rest) >= 5:
            cmp_rows.append({"pk": pk, "n": len(g), "gameplay": gp.y.mean(), "rest": rest.y.mean()})
    cmp = pd.DataFrame(cmp_rows)
    higher = int((cmp.gameplay > cmp.rest).sum())
    equal = int((cmp.gameplay == cmp.rest).sum())

    summary = {
        "n_fixes": int(len(d)), "n_projects": int(d.pk.nunique()),
        "informative_projects": int(di.pk.nunique()), "informative_fixes": int(len(di)),
        "bootstrap_reps_ok": int(len(boot)), "seed": a.seed,
        "conditional_logit": cl.set_index("term").round(4).to_dict(orient="index"),
        "mcfadden_r2": {k: round(1 - v / ll0, 4) for k, v in lls.items()},
        "gameplay_vs_rest_projects": {"n_projects": int(len(cmp)), "gameplay_higher": higher,
                                      "equal": equal, "gameplay_lower": int(len(cmp)) - higher - equal},
        "gameplay_is_fallback_class": bool((df[df.symptom == "gameplay"].rule_source == "fallback").all()),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
