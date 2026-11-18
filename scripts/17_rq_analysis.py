"""Main analysis: test-candidate changes in final fix diffs by bug symptom (RQ2),
with report reproduction material by symptom as an auxiliary analysis (RQ1).

Population: game-scope bug issues whose merged linked PRs all have a final
(landing) diff (11_final_pr_diff.py), i.e. 10,082 issues.
Symptoms come from the frozen keyword rules (symptom_rules.py). Rare categories
whose rule accuracy could not be checked (save_load, network, performance,
tooling_other) are merged into "other" for inference and also listed raw.

Usage:
    python -I scripts/17_rq_analysis.py <interim_dir> <out_dir> [--boot 2000]
"""
import argparse
import json
from pathlib import Path
import re
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import symptom_rules as R  # noqa: E402

TEST_RE = re.compile(
    r"(^|/)(tests?|__tests__|spec|specs|testing|unittests?|playmodetests?|editmodetests?)(/|$)|"
    r"(^|/)test_[^/]*$|_tests?\.[a-z]+$|tests?\.(cs|java|kt|scala|cpp|cc|h|hpp|ts|js|py|rs|go|gd|lua)$|"
    r"\.(spec|test)\.[jt]sx?$", re.I)
MAIN = ["gameplay", "ui", "crash_hang", "visual", "audio", "other"]
MERGE = {"save_load": "other", "network": "other", "performance": "other", "tooling_other": "other"}
EVIDENCE = {  # crude, unvalidated text rules (auxiliary analysis only)
    "image": r"!\[[^\]]*\]\([^)]+\)|<img\s|user-images\.githubusercontent|github\.com/user-attachments/assets|\.(?:png|jpe?g|gif)\b",
    "video": r"\.(?:mp4|webm|mov)\b|youtu\.?be|streamable\.com|\.gifv\b",
    "save_data": r"\.(?:sav|savc|sav\w*|broguesave)\b|github\.com/[^\s/]+/[^\s/]+/files/\S+\.zip|gist\.github\.com",
    "log_trace": r"```[\s\S]*?(?:exception|error|traceback|stack|at [\w.$<>]+\(|panicked|assert)[\s\S]*?```|stack ?trace|traceback",
    "steps": r"(?:steps to reproduce|to reproduce|reproduction)[^\n]*\n+\s*(?:1[.)]|-|\*)\s*\S{3,}",
    "game_link": r"18xx\.games/game/\d+|lichess\.org/\w{8}|zero-k\.info/Battles",
}
EVID_RE = {k: re.compile(v, re.I) for k, v in EVIDENCE.items()}


def boot_rate(df, col, groups, reps, seed):
    """Project-cluster bootstrap CI for the share of True in df[col] within each group."""
    rng = np.random.default_rng(seed)
    projects = df.pk.unique()
    by_proj = {p: g for p, g in df.groupby("pk")}
    out = {g: [] for g in groups}
    for _ in range(reps):
        sample = pd.concat([by_proj[p] for p in rng.choice(projects, len(projects), replace=True)])
        rates = sample.groupby("symptom")[col].mean()
        for g in groups:
            if g in rates:
                out[g].append(rates[g])
    return {g: (float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))) if v else (None, None)
            for g, v in out.items()}


def table(df, col, reps, seed):
    ci = boot_rate(df, col, MAIN, reps, seed)
    rows = []
    for g in MAIN + ["all"]:
        s = df if g == "all" else df[df.symptom.eq(g)]
        lo, hi = ci.get(g, (None, None)) if g != "all" else boot_all(df, col, reps, seed)
        rows.append(dict(symptom=g, issues=len(s), projects=s.pk.nunique(), with_test=int(s[col].sum()),
                         rate=s[col].mean(), ci_low=lo, ci_high=hi,
                         top_project_share=(s.pk.value_counts().iloc[0] / len(s)) if len(s) else None,
                         projects_with_any=int(s.groupby("pk")[col].any().sum())))
    return pd.DataFrame(rows)


def boot_all(df, col, reps, seed):
    rng = np.random.default_rng(seed + 1)
    agg = df.groupby("pk")[col].agg(["sum", "size"])
    vals = []
    for _ in range(reps):
        idx = rng.integers(0, len(agg), len(agg))
        s = agg.iloc[idx]
        vals.append(s["sum"].sum() / s["size"].sum())
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def gee(df):
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    d = df.copy()
    d["y"] = d.test_final.astype(int)
    d["log_paths"] = np.log1p(d.n_final_paths)
    d["year_c"] = d.year - 2020
    model = smf.gee("y ~ C(symptom, Treatment('gameplay')) + log_paths + year_c", groups="pk", data=d,
                    family=sm.families.Binomial(), cov_struct=sm.cov_struct.Exchangeable())
    res = model.fit()
    ci = res.conf_int()
    out = pd.DataFrame({"odds_ratio": np.exp(res.params), "ci_low": np.exp(ci[0]), "ci_high": np.exp(ci[1]),
                        "p_value": res.pvalues})
    out.index = [i.replace("C(symptom, Treatment('gameplay'))[T.", "symptom=").rstrip("]") for i in out.index]
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("interim_dir", type=Path)
    ap.add_argument("out_dir", type=Path)
    ap.add_argument("--boot", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=20261113)
    args = ap.parse_args()
    I = args.interim_dir
    fin = pd.read_parquet(I / "final_diff_v1" / "issue_final_diff.parquet")
    games = pd.read_parquet(I / "game_scope_v1" / "game_cohort.parquet",
                            columns=["pk", "issue_number", "title", "body", "created_at", "max_issues_per_merged_pr"])
    df = fin[fin.scope.eq("game") & fin.final_status.eq("all_landing")].merge(games, on=["pk", "issue_number"],
                                                                              validate="one_to_one")
    df["test_final"] = df.test_final.astype(bool)
    pred = [R.classify(t, b) for t, b in zip(df.title.fillna(""), df.body.fillna(""))]
    df["symptom_raw"] = [p for p, _ in pred]
    df["rule_source"] = [s for _, s in pred]
    df["symptom"] = df.symptom_raw.map(lambda s: MERGE.get(s, s))
    df["year"] = pd.to_datetime(df.created_at, utc=True, errors="coerce").dt.year
    body = df.body.fillna("")
    for k, rx in EVID_RE.items():
        df["ev_" + k] = body.map(lambda b: bool(rx.search(b)))
    # projects with any test-candidate change anywhere in their recorded history
    cm = pd.read_parquet(I / "commits_slim.parquet", columns=["project_key", "files"])
    cm = cm[cm.project_key.isin(set(df.pk))]
    hist = cm.groupby("project_key").files.apply(lambda s: any(TEST_RE.search(p) for fs in s for p in fs))
    df["project_has_tests"] = df.pk.map(hist).fillna(False).astype(bool)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    res = {"population": {"issues": len(df), "projects": int(df.pk.nunique()),
                          "projects_with_test_history": int(df.groupby("pk").project_has_tests.first().sum()),
                          "issues_in_projects_with_test_history": int(df.project_has_tests.sum())},
           "symptom_raw_counts": df.symptom_raw.value_counts().to_dict(),
           "rule_source": df.rule_source.value_counts().to_dict()}
    main_t = table(df, "test_final", args.boot, args.seed)
    main_t.to_csv(args.out_dir / "rq2_test_rate_by_symptom.csv", index=False)
    sub = df[df.project_has_tests]
    t_hist = table(sub, "test_final", args.boot, args.seed)
    t_hist.to_csv(args.out_dir / "rq2_test_rate_by_symptom_projects_with_tests.csv", index=False)
    # sensitivity analyses
    top = df.pk.value_counts().index[:3].tolist()
    sens = {}
    for name, d in [("main", df), ("projects_with_test_history", sub),
                    ("without_top3_projects", df[~df.pk.isin(top)]),
                    ("single_issue_prs_only", df[df.max_issues_per_merged_pr.le(1)]),
                    ("rule_hit_only_no_fallback", df[df.rule_source.ne("fallback")])]:
        sens[name] = {"issues": len(d), "projects": int(d.pk.nunique()),
                      **{g: round(float(d[d.symptom.eq(g)].test_final.mean()), 4) if (d.symptom == g).any() else None
                         for g in MAIN},
                      "all": round(float(d.test_final.mean()), 4)}
    res["top3_projects"] = top
    res["sensitivity_rates"] = sens
    # per-project view
    pp = df.groupby("pk").agg(n=("test_final", "size"), rate=("test_final", "mean"))
    res["per_project"] = {"projects": len(pp), "projects_with_any_test_fix": int((pp.rate > 0).sum()),
                          "median_rate": float(pp.rate.median()),
                          "median_rate_projects_ge20": float(pp[pp.n >= 20].rate.median()),
                          "projects_ge20": int((pp.n >= 20).sum()),
                          "share_of_test_fixes_from_top5_projects": float(
                              df[df.test_final].pk.value_counts().iloc[:5].sum() / df.test_final.sum())}
    pp.sort_values("n", ascending=False).to_csv(args.out_dir / "rq2_per_project.csv")
    g_all = gee(df)
    g_all.to_csv(args.out_dir / "rq2_gee_all.csv")
    g_hist = gee(sub)
    g_hist.to_csv(args.out_dir / "rq2_gee_projects_with_tests.csv")
    # auxiliary RQ1: report material by symptom (same population)
    ev_cols = ["ev_" + k for k in EVIDENCE]
    ev = df.groupby("symptom")[ev_cols].mean().reindex(MAIN)
    ev.loc["all"] = df[ev_cols].mean()
    ev.to_csv(args.out_dir / "rq1_report_material_by_symptom.csv")
    # does report material relate to test change? (descriptive)
    res["test_rate_by_material"] = {k: {"with": round(float(df[df["ev_" + k]].test_final.mean()), 4),
                                        "without": round(float(df[~df["ev_" + k]].test_final.mean()), 4),
                                        "n_with": int(df["ev_" + k].sum())} for k in EVIDENCE}
    df[["pk", "issue_number", "symptom_raw", "symptom", "rule_source", "test_final", "n_final_paths", "year",
        "project_has_tests"] + ev_cols].to_parquet(I / "final_diff_v1" / "analysis_table.parquet", index=False)
    (args.out_dir / "summary.json").write_text(json.dumps(res, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    pd.set_option("display.width", 200)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    print(main_t.round(4).to_string(index=False))
    print(t_hist.round(4).to_string(index=False))
    print(g_all.round(3).to_string())
    print(g_hist.round(3).to_string())
    print(ev.round(3).to_string())


if __name__ == "__main__":
    main()
