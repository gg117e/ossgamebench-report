"""Measure test-candidate changes on the final (landed) diff of each merged PR.

Problem fixed here: the v1 cohort (07) takes the union of the paths of *all* commits
linked to a PR. Commits listed in `pr_commit` include in-branch merges such as
"Merge branch 'master' into feature", whose paths come from other work. Their test
files were then counted as part of the bug fix (e.g. lichess-org/lila#16700).

Measurement hierarchy per merged PR (no parent SHAs or merge_commit_sha exist in the
dataset, so landing commits are identified from commit messages):

1. landing_unique      exactly one observed commit whose first line is
                       "Merge pull request #N ..." or ends with "(#N)" (strict marker),
                       not a revert, with at least one path. Its paths = the final diff.
2. landing_equivalent  several such commits (e.g. cherry-picks) with identical path sets.
3. landing_ambiguous   several such commits with different path sets -> excluded from
                       the main measure.
4. no_landing          no such commit; the PR's final diff is unknown. A fallback using
                       the PR's own non-merge commits is stored for sensitivity only.

Issue level: `final_status` = all_landing if every merged linked PR has a landing diff,
partial if some do, none otherwise. The main measure uses all_landing issues only.

Usage:
    python -I scripts/11_final_pr_diff.py <cohort_dir> <scoped_index> <output_dir> <report_dir>
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
TEST_RE = re.compile(
    r"(^|/)(tests?|__tests__|spec|specs|testing|unittests?|playmodetests?|editmodetests?)(/|$)|"
    r"(^|/)test_[^/]*$|_tests?\.[a-z]+$|tests?\.(cs|java|kt|scala|cpp|cc|h|hpp|ts|js|py|rs|go|gd|lua)$|"
    r"\.(spec|test)\.[jt]sx?$", re.I)  # identical to 07 (pilot rule, unvalidated)
GH_MERGE = re.compile(r"^Merge pull request #(\d+)\b")
SQUASH = re.compile(r"\(#(\d+)\)\s*$")
BRANCH_MERGE = re.compile(r"^Merge (?:branch|remote-tracking branch|tag|commit) |^Merge \S.* into \S")
REVERT = re.compile(r"^Revert\b", re.I)


def first_line(message):
    lines = str(message or "").splitlines()
    return lines[0].strip() if lines else ""


def commit_kind(message, pr_number):
    line = first_line(message)
    if REVERT.match(line):
        return "revert"
    m = GH_MERGE.match(line)
    if m and int(m.group(1)) == pr_number:
        return "gh_merge"
    m = SQUASH.search(line)
    if m and int(m.group(1)) == pr_number:
        return "squash_like"
    if BRANCH_MERGE.match(line):
        return "branch_merge"
    return "other"


def build(refs, commit_paths, bug_issue_pr, scoped):
    refs = refs[refs.commit_observed].copy()
    refs["kind"] = [commit_kind(m, int(p)) for m, p in zip(refs.message, refs.pr_number)]
    paths = commit_paths.groupby(["pk", "sha"]).path.agg(lambda s: tuple(sorted(set(s)))).rename("paths")
    refs = refs.join(paths, on=["pk", "sha"])
    refs["paths"] = refs.paths.map(lambda x: x if isinstance(x, tuple) else ())

    rows = []
    for (pk, pr), g in refs.groupby(["pk", "pr_number"], sort=True):
        land = g[g.kind.isin(["gh_merge", "squash_like"]) & g.paths.map(len).gt(0)]
        variants = set(land.paths)
        own = g[g.via_pr_commit & ~g.kind.isin(["branch_merge", "revert"])]
        union_all = tuple(sorted({p for ps in g.paths for p in ps}))
        fallback = tuple(sorted({p for ps in own.paths for p in ps}))
        if len(variants) == 1:
            status = "landing_unique" if land.sha.nunique() == 1 else "landing_equivalent"
            final = next(iter(variants))
        elif len(variants) > 1:
            status, final = "landing_ambiguous", None
        else:
            status, final = "no_landing", None
        rows.append(dict(
            pk=pk, pr_number=int(pr), pr_status=status,
            landing_kind=",".join(sorted(set(land.kind))) if len(variants) else "",
            landing_shas=",".join(sorted(set(land.sha))),
            n_branch_merge_commits=int(g.kind.eq("branch_merge").sum()),
            final_paths=list(final) if final is not None else None,
            union_paths=list(union_all), fallback_paths=list(fallback),
            test_final=None if final is None else any(TEST_RE.search(p) for p in final),
            test_union=any(TEST_RE.search(p) for p in union_all),
            test_fallback=any(TEST_RE.search(p) for p in fallback) if fallback else None,
            n_final_paths=None if final is None else len(final), n_union_paths=len(union_all)))
    pr_table = pd.DataFrame(rows)

    merged = bug_issue_pr[bug_issue_pr.merged][["pk", "issue_number", "pr_number"]]
    cohort = scoped[["pk", "issue_number", "scope", "test_candidate_change", "n_paths", "n_merged_prs"]]
    links = cohort[["pk", "issue_number"]].merge(merged, on=["pk", "issue_number"])
    links = links.merge(pr_table, on=["pk", "pr_number"], how="left")
    links["pr_status"] = links.pr_status.fillna("no_observed_commit")

    def per_issue(g):
        ok = g.pr_status.isin(["landing_unique", "landing_equivalent"])
        final = sorted({p for ps in g.final_paths[ok] for p in ps}) if ok.any() else []
        fb_src = g.fallback_paths.dropna()
        fallback = sorted({p for ps in fb_src for p in ps})
        status = "all_landing" if ok.all() else "partial" if ok.any() else "none"
        return pd.Series(dict(
            final_status=status, n_merged_prs_linked=len(g), n_landing_prs=int(ok.sum()),
            n_final_paths=len(final) if status == "all_landing" else None,
            test_final=any(TEST_RE.search(p) for p in final) if status == "all_landing" else None,
            n_test_final_paths=sum(bool(TEST_RE.search(p)) for p in final) if status == "all_landing" else None,
            test_final_partial=any(TEST_RE.search(p) for p in final) if ok.any() else None,
            test_fallback=any(TEST_RE.search(p) for p in fallback) if fallback else None,
            any_branch_merge=bool(g.n_branch_merge_commits.fillna(0).gt(0).any())))

    issue = links.groupby(["pk", "issue_number"]).apply(per_issue, include_groups=False).reset_index()
    issue = cohort.merge(issue, on=["pk", "issue_number"], how="left", validate="one_to_one")
    issue["final_status"] = issue.final_status.fillna("none")
    return pr_table, issue


def rate(frame, column):
    s = frame[column].dropna().astype(bool)
    return dict(n=int(len(s)), with_test=int(s.sum()), rate=round(float(s.mean()), 4) if len(s) else None)


def metrics(pr_table, issue):
    out = {"pr_status": pr_table.pr_status.value_counts().to_dict(),
           "pr_landing_kind": pr_table.landing_kind.value_counts().to_dict(),
           "issue_final_status": issue.final_status.value_counts().to_dict(),
           "pr_level_by_scope": {}, "by_scope": {}}
    scope_of = issue[["pk", "scope"]].drop_duplicates()
    prs = pr_table.merge(scope_of, on="pk", how="left")
    for scope, g in [("all", prs)] + list(prs.groupby("scope")):
        landed = g[g.pr_status.isin(["landing_unique", "landing_equivalent"])]
        out["pr_level_by_scope"][scope] = {"merged_prs": int(len(g)),
                                           "final_rate_on_landed": rate(landed, "test_final"),
                                           "v1_union_rate_on_landed": rate(landed, "test_union")}
    for scope, g in [("all", issue)] + list(issue.groupby("scope")):
        a = g[g.final_status.eq("all_landing")]
        flips = pd.crosstab(a.test_candidate_change, a.test_final.astype(bool)) if len(a) else None
        out["by_scope"][scope] = {
            "issues": int(len(g)), "projects": int(g.pk.nunique()),
            "v1_union_rate_all_issues": rate(g, "test_candidate_change"),
            "v1_union_rate_on_all_landing": rate(a, "test_candidate_change"),
            "final_rate_on_all_landing": rate(a, "test_final"),
            "final_projects": int(a.pk.nunique()),
            "fallback_rate_on_none": rate(g[g.final_status.eq("none")], "test_fallback"),
            "v1_true_final_false": int(flips.loc[True, False]) if flips is not None and True in flips.index and False in flips.columns else 0,
            "v1_false_final_true": int(flips.loc[False, True]) if flips is not None and False in flips.index and True in flips.columns else 0,
        }
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("cohort_dir", type=Path)
    ap.add_argument("scoped_index", type=Path)
    ap.add_argument("output_dir", type=Path)
    ap.add_argument("report_dir", type=Path)
    args = ap.parse_args()
    if args.output_dir.exists():
        ap.error("output_dir exists; existing runs are preserved")
    inputs = [args.cohort_dir / f for f in ("pr_commit_refs.parquet", "commit_paths.parquet", "bug_issue_pr.parquet")]
    refs, cpaths, bip = (pd.read_parquet(p) for p in inputs)
    scoped = pd.read_parquet(args.scoped_index)
    pr_table, issue = build(refs, cpaths, bip, scoped)
    args.output_dir.mkdir(parents=True)
    args.report_dir.mkdir(parents=True, exist_ok=True)
    pr_table.to_parquet(args.output_dir / "pr_final_diff.parquet", index=False)
    issue.to_parquet(args.output_dir / "issue_final_diff.parquet", index=False)
    m = metrics(pr_table, issue)
    m["inputs_and_code"] = {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
                            for p in inputs + [args.scoped_index, Path(__file__)]}
    m["status"] = "final_diff_by_message_markers_not_yet_validated_against_github"
    (args.report_dir / "summary.json").write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in m.items() if k != "inputs_and_code"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
