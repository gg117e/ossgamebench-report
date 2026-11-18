"""Robustness checks requested by the methods review (2026-11-18).

Usage:
    python -I scripts/27_robustness.py <interim_dir> <game_type_labels.csv> <out_dir> [--reps 1000]

Changes compared with scripts 17, 20 and 26:
  * the size control counts only NON-test files of the final diff (the old control
    log(1 + all files) contains the outcome itself);
  * every GEE fit records its working correlation, the estimated correlation and
    whether it converged (maxiter=500); no silent fallback;
  * RQ2 is reported over a grid of specifications instead of one model;
  * the project-level RQ2 model is repeated for projects with >= 10 and >= 20 fixes and
    as a binomial model of project rates;
  * rates by symptom are split by the rule source (title / body / no keyword);
  * rates without very large diffs (> 100 files);
  * test rates of issues excluded at step 5 (no unique landing diff).
Outputs (out_dir must not exist): *.csv and summary.json.
"""
import argparse
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.tools.sm_exceptions import ConvergenceWarning

SYM = "C(symptom, Treatment('gameplay'))"
SYMPTOMS = ["ui", "crash_hang", "visual", "audio", "other"]


def load(interim, labels):
    a = pd.read_parquet(interim / "final_diff_v1" / "analysis_table.parquet")
    f = pd.read_parquet(interim / "final_diff_v1" / "issue_final_diff.parquet",
                        columns=["pk", "issue_number", "n_test_final_paths"])
    d = a.merge(f, on=["pk", "issue_number"], how="left", validate="one_to_one")
    assert d.n_test_final_paths.notna().all()
    lab = pd.read_csv(labels)[["pk", "game_type", "web"]]
    d = d.merge(lab, on="pk", how="left", validate="many_to_one")
    d["y"] = d.test_final.astype(int)
    d["n_nontest"] = d.n_final_paths - d.n_test_final_paths
    d["log_nontest"] = np.log1p(d.n_nontest)
    d["log_paths"] = np.log1p(d.n_final_paths)
    d["year_c"] = d.year - 2020
    d["discrete"] = d.game_type.eq("discrete").astype(int)
    d["web_i"] = d.web.astype(bool).astype(int)
    d["log_proj"] = np.log(d.pk.map(d.groupby("pk").size()))
    return d


def gee(formula, data, cov, term):
    cs = sm.cov_struct.Exchangeable() if cov == "exchangeable" else sm.cov_struct.Independence()
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        m = smf.gee(formula, groups="pk", data=data, family=sm.families.Binomial(), cov_struct=cs).fit(maxiter=500)
    conv = not any(issubclass(x.category, ConvergenceWarning) for x in w)
    ci = m.conf_int()
    rows = []
    for t in ([term] if isinstance(term, str) else term):
        rows.append({"term": t, "odds_ratio": float(np.exp(m.params[t])), "ci_low": float(np.exp(ci.loc[t, 0])),
                     "ci_high": float(np.exp(ci.loc[t, 1])), "p_value": float(m.pvalues[t]), "cov_struct": cov,
                     "converged": conv,
                     "dep_param": float(np.atleast_1d(m.cov_struct.dep_params)[0]) if cov == "exchangeable" else 0.0})
    return rows


def fe_logit(d, cols):
    v = d.groupby("pk").y.agg(["min", "max"])
    di = d[d.pk.isin(v.index[(v["min"] == 0) & (v["max"] == 1)])].copy()
    for s in SYMPTOMS:
        di[f"s_{s}"] = (di.symptom == s).astype(float)
    names = [f"s_{s}" for s in SYMPTOMS] + cols
    X = pd.concat([di[names].astype(float), pd.get_dummies(di.pk, dtype=float)], axis=1)
    r = sm.GLM(di.y.values, X.values, family=sm.families.Binomial()).fit(
        cov_type="cluster", cov_kwds={"groups": pd.factorize(di.pk)[0]})
    ci = np.asarray(r.conf_int())
    return [{"term": n.replace("s_", "symptom="), "odds_ratio": float(np.exp(r.params[i])),
             "ci_low": float(np.exp(ci[i, 0])), "ci_high": float(np.exp(ci[i, 1])), "p_value": float(r.pvalues[i])}
            for i, n in enumerate(names)], di


def fe_boot(di, cols, reps, seed):
    rng = np.random.default_rng(seed)
    pks = di.pk.unique()
    groups = {pk: g for pk, g in di.groupby("pk")}
    out = []
    for _ in range(reps):
        parts = []
        for i, pk in enumerate(rng.choice(pks, len(pks), replace=True)):
            parts.append(groups[pk].assign(pk=f"{pk}#{i}"))
        b = pd.concat(parts)
        names = [f"s_{s}" for s in SYMPTOMS] + cols
        X = pd.concat([b[names].astype(float), pd.get_dummies(b.pk, dtype=float)], axis=1)
        try:
            r = sm.GLM(b.y.values, X.values, family=sm.families.Binomial()).fit()
            out.append(np.asarray(r.params)[:len(names)])
        except Exception:
            continue
    return np.array(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("interim_dir", type=Path)
    ap.add_argument("labels")
    ap.add_argument("out_dir", type=Path)
    ap.add_argument("--reps", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=20261118)
    a = ap.parse_args()
    if a.out_dir.exists():
        sys.exit(f"{a.out_dir} exists")
    d = load(a.interim_dir, a.labels)
    a.out_dir.mkdir(parents=True)
    summary = {"n_fixes": int(len(d))}
    sym_terms = [f"{SYM}[T.{s}]" for s in SYMPTOMS]

    # A. RQ1 GEE with non-test size control
    rows = []
    for ctrl in ["log_nontest", "log_paths"]:
        for cov in ["exchangeable", "independence"]:
            for r in gee(f"y ~ {SYM} + {ctrl} + year_c", d, cov, sym_terms + [ctrl, "year_c"]):
                rows.append({"size_control": ctrl, **r})
    rq1 = pd.DataFrame(rows)
    rq1["term"] = rq1.term.str.replace(f"{SYM}[T.", "symptom=", regex=False).str.rstrip("]")
    rq1.to_csv(a.out_dir / "rq1_gee.csv", index=False)

    # B. within-project (fixed effects) with non-test size control + bootstrap
    fe, di = fe_logit(d, ["log_nontest", "year_c"])
    boot = fe_boot(di, ["log_nontest", "year_c"], a.reps, a.seed)
    for i, r in enumerate(fe):
        r["boot_ci_low"] = float(np.exp(np.percentile(boot[:, i], 2.5)))
        r["boot_ci_high"] = float(np.exp(np.percentile(boot[:, i], 97.5)))
    fe_df = pd.DataFrame(fe)
    fe_df.to_csv(a.out_dir / "within_project_nontest.csv", index=False)
    summary["within_project"] = {"projects": int(di.pk.nunique()), "fixes": int(len(di)), "boot_reps_ok": int(len(boot))}
    summary["audio_test_changing"] = d[(d.symptom == "audio") & (d.y == 1)].pk.value_counts().to_dict()

    # C. RQ2 specification grid
    g = d[d.game_type.isin(["discrete", "continuous"])]
    specs = {
        "type_only": "y ~ discrete",
        "type_symptom": f"y ~ discrete + {SYM}",
        "type_web": "y ~ discrete + web_i",
        "full_nontest": f"y ~ discrete + {SYM} + web_i + log_nontest + year_c + log_proj",
        "full_allpaths": f"y ~ discrete + {SYM} + web_i + log_paths + year_c + log_proj",
        "full_nontest_no_size": f"y ~ discrete + {SYM} + web_i + log_nontest + year_c",
        "full_no_paths": f"y ~ discrete + {SYM} + web_i + year_c + log_proj",
    }
    rows = []
    for name, f in specs.items():
        for cov in ["independence", "exchangeable"]:
            for r in gee(f, g, cov, ["discrete"] + (["web_i"] if "web_i" in f else [])):
                rows.append({"spec": name, **r})
    top5 = g[g.y == 1].pk.value_counts().index[:5]
    for name, sub in [("nonweb_only", g[g.web_i == 0]), ("without_top5", g[~g.pk.isin(top5)]),
                      ("projects_with_tests", g[g.project_has_tests])]:
        f = specs["full_nontest"].replace(" + web_i", "") if name == "nonweb_only" else specs["full_nontest"]
        for cov in ["independence", "exchangeable"]:
            for r in gee(f, sub, cov, "discrete"):
                rows.append({"spec": "full_nontest/" + name, **r})
    rq2 = pd.DataFrame(rows)
    rq2.to_csv(a.out_dir / "rq2_spec_grid.csv", index=False)

    # D. project level
    p = g.groupby("pk").agg(k=("y", "sum"), n=("y", "size"), discrete=("discrete", "first"), web=("web_i", "first"))
    p["any"] = (p.k > 0).astype(int)
    p["log_n"] = np.log(p.n)
    rows = []
    for mn in [1, 10, 20]:
        s = p[p.n >= mn]
        m = smf.logit("any ~ discrete + web + log_n", data=s).fit(disp=0)
        ci = m.conf_int().loc["discrete"]
        rows.append({"model": f"any_test_logit_min{mn}", "projects": len(s), "odds_ratio": float(np.exp(m.params["discrete"])),
                     "ci_low": float(np.exp(ci[0])), "ci_high": float(np.exp(ci[1])), "p_value": float(m.pvalues["discrete"]),
                     "discrete_share_any": float(s[s.discrete == 1]["any"].mean()),
                     "continuous_share_any": float(s[s.discrete == 0]["any"].mean())})
    m = smf.glm("k + nk ~ discrete + web + log_n", data=p.assign(nk=p.n - p.k), family=sm.families.Binomial()).fit(cov_type="HC0")
    ci = m.conf_int().loc["discrete"]
    rows.append({"model": "project_rate_binomial_HC0", "projects": len(p), "odds_ratio": float(np.exp(m.params["discrete"])),
                 "ci_low": float(np.exp(ci[0])), "ci_high": float(np.exp(ci[1])), "p_value": float(m.pvalues["discrete"])})
    pl = pd.DataFrame(rows)
    pl.to_csv(a.out_dir / "rq2_project_level.csv", index=False)

    # E. rule source split
    rs = d.groupby(["symptom", "rule_source"]).y.agg(fixes="size", test="sum", rate="mean").reset_index()
    rs.to_csv(a.out_dir / "rate_by_rule_source.csv", index=False)

    # F. without very large diffs
    big = d[d.n_final_paths <= 100].groupby("symptom").y.agg(fixes="size", rate="mean").reset_index()
    big.to_csv(a.out_dir / "rate_without_large_diffs.csv", index=False)
    summary["share_test_fixes_from_diffs_over_50"] = float(d[d.n_final_paths > 50].y.sum() / d.y.sum())
    summary["rate_without_large_diffs_all"] = float(d[d.n_final_paths <= 100].y.mean())

    # G. step-5 exclusions (game projects with a merged PR but no unique landing diff for every PR)
    f = pd.read_parquet(a.interim_dir / "final_diff_v1" / "issue_final_diff.parquet")
    f = f[f.scope == "game"]
    inc, exc = f[f.final_status == "all_landing"], f[f.final_status != "all_landing"]
    summary["step5"] = {
        "included": int(len(inc)), "excluded": int(len(exc)),
        "union_rate_included": float(inc.test_candidate_change.mean()),
        "union_rate_excluded": float(exc.test_candidate_change.mean()),
        "top_projects_excluded": exc.pk.value_counts().head(3).to_dict(),
    }

    summary["files"] = sorted(p.name for p in a.out_dir.iterdir())
    (a.out_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    pd.set_option("display.width", 220)
    print(rq1.round(3).to_string())
    print(fe_df.round(3).to_string())
    print(rq2.round(3).to_string())
    print(pl.round(3).to_string())
    print(rs.round(4).to_string())
    print(big.round(4).to_string())
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
