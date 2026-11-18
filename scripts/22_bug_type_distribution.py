"""Distribution of bug symptoms (RQ1, first part) and bug-identification precision.

Applies the frozen symptom rules (symptom_rules.py) to
  (a) the analysis population: game-scope bug issues with final fix diffs (10,082), and
  (b) all eligible bug issues in the same 181 game projects, linked to a fix or not,
so the bias of the linked subset can be shown. Also records how often the label-based
bug identification was judged a real bug in the development sample.

Usage:
    python -I scripts/22_bug_type_distribution.py <interim_dir> <scope_labels_jsonl> <dev_labels_jsonl> <out_dir>
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import symptom_rules as R  # noqa: E402

ORDER = ["gameplay", "ui", "crash_hang", "visual", "tooling_other", "audio", "network", "save_load", "performance"]


def dist(series):
    c = series.value_counts()
    return pd.DataFrame({"issues": c, "share": c / c.sum()}).reindex(ORDER).fillna(0)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("interim_dir", type=Path)
    ap.add_argument("scope_labels_jsonl", type=Path)
    ap.add_argument("dev_labels_jsonl", type=Path)
    ap.add_argument("out_dir", type=Path)
    args = ap.parse_args()
    scope = [json.loads(l) for l in args.scope_labels_jsonl.read_text(encoding="utf-8").splitlines()]
    games = {s["project_key"] for s in scope if s["scope"] == "game"}
    bugs = pd.read_parquet(args.interim_dir / "cohort_v1" / "bug_issues.parquet",
                           columns=["pk", "issue_number", "title", "body", "selection_status", "state"])
    bugs = bugs[bugs.pk.isin(games)].copy()
    bugs["symptom"] = [R.classify(t, b)[0] for t, b in zip(bugs.title.fillna(""), bugs.body.fillna(""))]
    fin = pd.read_parquet(args.interim_dir / "final_diff_v1" / "issue_final_diff.parquet",
                          columns=["pk", "issue_number", "scope", "final_status"])
    analysed = fin[fin.scope.eq("game") & fin.final_status.eq("all_landing")][["pk", "issue_number"]]
    analysed["in_analysis"] = True
    bugs = bugs.merge(analysed, on=["pk", "issue_number"], how="left")
    bugs["in_analysis"] = bugs.in_analysis.eq(True)

    d_all = dist(bugs.symptom)
    d_in = dist(bugs[bugs.in_analysis].symptom)
    d_out = dist(bugs[~bugs.in_analysis].symptom)
    table = pd.concat({"all_game_bugs": d_all, "analysed_with_fix": d_in, "not_analysed": d_out}, axis=1)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    table.to_csv(args.out_dir / "symptom_distribution.csv")
    share_analysed = bugs.groupby("symptom").in_analysis.mean().reindex(ORDER)
    share_analysed.to_csv(args.out_dir / "share_traceable_to_fix_by_symptom.csv")

    dev = [json.loads(l) for l in args.dev_labels_jsonl.read_text(encoding="utf-8").splitlines()]
    bug_id = Counter(r["is_actual_bug"] for r in dev)
    summary = {
        "game_projects": len(games),
        "game_bug_issues": len(bugs), "game_bug_projects": int(bugs.pk.nunique()),
        "analysed": int(bugs.in_analysis.sum()),
        "share_analysed": round(float(bugs.in_analysis.mean()), 4),
        "selection_status_game_bugs": bugs.selection_status.value_counts().to_dict(),
        "bug_identification_development_sample": {"n": len(dev), **dict(bug_id),
                                                  "annotator": "Codex (LLM), development sample of samples_game_v3"},
        "note": "Symptoms from frozen keyword rules (audit accuracy 0.71, kappa 0.59 against LLM labels).",
    }
    (args.out_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
                                               encoding="utf-8")
    pd.set_option("display.width", 200)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(table.round(4).to_string())
    print(share_analysed.round(4).to_string())


if __name__ == "__main__":
    main()
