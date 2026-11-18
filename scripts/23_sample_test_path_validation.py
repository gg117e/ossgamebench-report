"""Draw the validation sample for the test-candidate path rule.

Population: the 10,082 analysed fixes (game scope, all merged PRs with a final diff).
Strata: 50 fixes flagged as test-changing and 50 not flagged (fixed seed). For each
fix the final-diff paths are listed; flagged paths are marked. Also runs a
population-wide probe: unflagged fixes whose paths contain test-like substrings
that the rule did not match (possible misses).

Usage:
    python -I scripts/23_sample_test_path_validation.py <interim_dir> <out_dir> [--n 50]
"""
import argparse
import json
from pathlib import Path
import random
import re

import pandas as pd

TEST_RE = re.compile(
    r"(^|/)(tests?|__tests__|spec|specs|testing|unittests?|playmodetests?|editmodetests?)(/|$)|"
    r"(^|/)test_[^/]*$|_tests?\.[a-z]+$|tests?\.(cs|java|kt|scala|cpp|cc|h|hpp|ts|js|py|rs|go|gd|lua)$|"
    r"\.(spec|test)\.[jt]sx?$", re.I)
PROBE = re.compile(r"test|spec(?!ial|ific|trum|tat|ies|ular|if)|mock|fixture|unittest", re.I)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("interim_dir", type=Path)
    ap.add_argument("out_dir", type=Path)
    ap.add_argument("--n", type=int, default=50)
    ap.add_argument("--seed", type=int, default=20261115)
    args = ap.parse_args()
    I = args.interim_dir
    a = pd.read_parquet(I / "final_diff_v1" / "analysis_table.parquet", columns=["pk", "issue_number", "test_final"])
    links = pd.read_parquet(I / "cohort_v1" / "bug_issue_pr.parquet")
    links = links[links.merged][["pk", "issue_number", "pr_number"]]
    prs = pd.read_parquet(I / "final_diff_v1" / "pr_final_diff.parquet", columns=["pk", "pr_number", "final_paths"])
    m = a.merge(links, on=["pk", "issue_number"]).merge(prs, on=["pk", "pr_number"])
    paths = m.groupby(["pk", "issue_number"]).agg(
        prs=("pr_number", lambda s: sorted(set(map(int, s)))),
        paths=("final_paths", lambda s: sorted({p for ps in s if ps is not None for p in ps})))
    a = a.merge(paths, on=["pk", "issue_number"])
    assert len(a) == 10082
    rng = random.Random(args.seed)
    rows = []
    for flag, name in [(True, "flagged"), (False, "unflagged")]:
        keys = sorted(zip(a[a.test_final == flag].pk, a[a.test_final == flag].issue_number))
        for pk, num in rng.sample(keys, args.n):
            r = a[(a.pk == pk) & (a.issue_number == num)].iloc[0]
            rows.append({"stratum": name, "pk": pk, "issue_number": int(num), "prs": list(r.prs),
                         "n_paths": len(r.paths),
                         "flagged_paths": [p for p in r.paths if TEST_RE.search(p)],
                         "other_paths": [p for p in r.paths if not TEST_RE.search(p)]})
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "sample.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows),
                                               encoding="utf-8")
    neg = a[~a.test_final]
    probe = neg[neg.paths.map(lambda ps: any(PROBE.search(p) for p in ps))]
    hits = [{"pk": r.pk, "issue_number": int(r.issue_number),
             "probe_paths": [p for p in r.paths if PROBE.search(p)][:8]} for r in probe.itertuples()]
    (args.out_dir / "unflagged_probe_hits.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in hits), encoding="utf-8")
    summary = {"seed": args.seed, "population": len(a), "flagged": int(a.test_final.sum()),
               "unflagged": int((~a.test_final).sum()), "sample_per_stratum": args.n,
               "unflagged_with_probe_substring": len(hits)}
    (args.out_dir / "sampling_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
