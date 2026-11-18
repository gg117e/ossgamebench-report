"""Build provenance-preserving bug/PR/commit/path tables for the mining study.

No bug-symptom or game/tool labels are inferred here. Test flags reproduce the
unvalidated pilot path rule and must not be interpreted as test execution.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import duplicated_projects, is_bug_label, is_nofix_label

TEST_RE = re.compile(
    r"(^|/)(tests?|__tests__|spec|specs|testing|unittests?|playmodetests?|editmodetests?)(/|$)|"
    r"(^|/)test_[^/]*$|_tests?\.[a-z]+$|tests?\.(cs|java|kt|scala|cpp|cc|h|hpp|ts|js|py|rs|go|gd|lua)$|"
    r"\.(spec|test)\.[jt]sx?$", re.I)
BROAD_REF = re.compile(r"\(#(\d+)\)|Merge pull request #(\d+)")
STRICT_REF = re.compile(r"^Merge pull request #(\d+)\b|\(#(\d+)\)\s*$")


def keyed(frame):
    frame = frame.copy()
    frame["pk"] = frame.project.str.lower()
    return frame


def build(issues, prs, issue_pr, pr_commit, commits, projects, duplicates):
    issues, prs, issue_pr, pr_commit, projects = map(keyed, (issues, prs, issue_pr, pr_commit, projects))
    issues = issues[~issues.pk.isin(duplicates)].copy()
    prs = prs[~prs.pk.isin(duplicates)].copy()
    projects = projects[~projects.pk.isin(duplicates)].copy()
    commits = commits[~commits.project_key.isin(duplicates)].rename(columns={"project_key": "pk"}).copy()
    duplicate_commits = commits[commits.duplicated(["pk", "sha"], keep=False)].copy()
    extra_sources = {}
    for key, group in duplicate_commits.groupby(["pk", "sha"]):
        signatures = {(str(row.created_at), None if pd.isna(row.message) else row.message,
                       tuple(map(str, row.files))) for row in group.itertuples()}
        if len(signatures) != 1:
            raise ValueError(f"Conflicting commit metadata for {key}; resolve before joining")
        extra_sources[key] = sorted(set(group.source_file))
    duplicate_commit_rows_removed = len(commits) - len(commits.drop_duplicates(["pk", "sha"]))
    commits = commits.drop_duplicates(["pk", "sha"]).copy()
    for name, frame, keys in [("issues", issues, ["pk", "number"]),
                              ("prs", prs, ["pk", "number"]),
                              ("commits", commits, ["pk", "sha"])]:
        if frame.duplicated(keys).any():
            raise ValueError(f"Conflicting duplicate keys in {name}; resolve before joining")

    issues["has_bug_label"] = issues.labels.map(lambda xs: any(is_bug_label(x) for x in xs))
    issues["has_nofix_label"] = issues.labels.map(lambda xs: any(is_nofix_label(x) for x in xs))
    issues["eligible_bug"] = issues.has_bug_label & ~issues.has_nofix_label
    selection = issues[["pk", "number", "has_bug_label", "has_nofix_label", "eligible_bug"]].rename(
        columns={"number": "issue_number"})
    bugs = issues[issues.eligible_bug].rename(columns={"number": "issue_number"}).copy()

    ip = issue_pr.merge(bugs[["pk", "issue_number"]], on=["pk", "issue_number"])
    duplicated_links = ip[ip.duplicated(["pk", "issue_number", "pr_number"], keep=False)].copy()
    ip = ip.groupby(["pk", "issue_number", "pr_number"]).size().rename("raw_link_rows").reset_index()
    pr_table = prs.rename(columns={"number": "pr_number", "state": "pr_state"})
    pr_fields = ["pk", "pr_number", "pr_state", "created_at", "merged_at", "title", "body"]
    ip = ip.merge(pr_table[pr_fields], on=["pk", "pr_number"], how="left", validate="many_to_one")
    ip["pr_present"] = ip.pr_state.notna()
    ip["merged"] = ip.pr_state.eq("MERGED")
    merged = ip[ip.merged][["pk", "issue_number", "pr_number"]].copy()
    referenced_prs = merged[["pk", "pr_number"]].drop_duplicates()

    direct = pr_commit.merge(referenced_prs, on=["pk", "pr_number"])[
        ["pk", "pr_number", "commit_sha"]].rename(columns={"commit_sha": "sha"})
    direct["via_pr_commit"] = True
    direct["via_message"] = False
    direct["strict_message_marker"] = False

    ref = commits.message.fillna("").str.extractall(BROAD_REF)
    ref["pr_number"] = ref[0].fillna(ref[1]).astype("int64")
    message = commits[["pk", "sha", "message"]].join(ref.pr_number.droplevel(1), how="inner")
    message = message.merge(referenced_prs, on=["pk", "pr_number"])
    message["strict_message_marker"] = message.apply(
        lambda row: any(int(a or b) == row.pr_number for a, b in STRICT_REF.findall(
            str(row.message).splitlines()[0] if str(row.message).splitlines() else "")), axis=1)
    message["via_pr_commit"] = False
    message["via_message"] = True
    refs = pd.concat([direct, message[direct.columns]], ignore_index=True).groupby(
        ["pk", "pr_number", "sha"], as_index=False).agg(
            via_pr_commit=("via_pr_commit", "any"), via_message=("via_message", "any"),
            strict_message_marker=("strict_message_marker", "any"))

    metadata = commits[["pk", "sha", "created_at", "message", "source_file"]].rename(
        columns={"created_at": "commit_created_at"})
    refs = refs.merge(metadata, on=["pk", "sha"], how="left", indicator=True, validate="many_to_one")
    refs["commit_observed"] = refs.pop("_merge").eq("both")
    refs["source_files"] = [extra_sources.get((p, s), [fn] if isinstance(fn, str) else [])
                            for p, s, fn in zip(refs.pk, refs.sha, refs.source_file)]
    refs["route"] = refs.apply(lambda r: "A+B" if r.via_pr_commit and r.via_message else
                              "A" if r.via_pr_commit else "B", axis=1)
    seen = refs[refs.commit_observed][["pk", "sha"]].drop_duplicates()
    cm = seen.merge(commits[["pk", "sha", "files"]], on=["pk", "sha"], validate="one_to_one")
    files = cm.explode("files").dropna(subset=["files"]).rename(columns={"files": "path"})
    files["path"] = files.path.astype(str)
    files = files.drop_duplicates(["pk", "sha", "path"])
    files["test_candidate"] = files.path.map(lambda p: bool(TEST_RE.search(p)))
    lengths = cm[["pk", "sha", "files"]].copy()
    lengths["n_paths"] = lengths.files.map(len)
    refs = refs.merge(lengths.drop(columns="files"), on=["pk", "sha"], how="left", validate="many_to_one")

    issue_commits = merged.merge(refs[["pk", "pr_number", "sha", "commit_observed", "via_pr_commit",
                                      "via_message", "strict_message_marker"]], on=["pk", "pr_number"])
    issue_files = issue_commits[issue_commits.commit_observed][["pk", "issue_number", "sha"]].drop_duplicates().merge(
        files, on=["pk", "sha"])
    issue_paths = issue_files[["pk", "issue_number", "path", "test_candidate"]].drop_duplicates()
    path_stats = issue_paths.groupby(["pk", "issue_number"]).agg(
        n_paths=("path", "size"), test_candidate_change=("test_candidate", "any"),
        n_test_candidate_paths=("test_candidate", "sum"))
    observed = issue_commits[issue_commits.commit_observed]
    obs_stats = observed.groupby(["pk", "issue_number"]).agg(
        n_observed_commits=("sha", "nunique"), direct_commit_observed=("via_pr_commit", "any"),
        message_commit_observed=("via_message", "any"))
    strict = observed[observed.via_pr_commit | observed.strict_message_marker][
        ["pk", "issue_number", "sha"]].drop_duplicates().merge(files, on=["pk", "sha"])
    strict_keys = set(zip(strict.pk, strict.issue_number))
    n_pr = merged.groupby(["pk", "issue_number"]).pr_number.nunique().rename("n_merged_prs")
    n_link = ip.groupby(["pk", "issue_number"]).pr_number.nunique().rename("n_linked_prs")
    shared = merged.groupby(["pk", "pr_number"]).issue_number.nunique().rename("n_eligible_bug_issues")
    linked_sharing = merged.join(shared, on=["pk", "pr_number"]).groupby(["pk", "issue_number"])[
        "n_eligible_bug_issues"].max().rename("max_issues_per_merged_pr")
    bugs = bugs.join(n_link, on=["pk", "issue_number"]).join(n_pr, on=["pk", "issue_number"])
    bugs = bugs.join(obs_stats, on=["pk", "issue_number"]).join(path_stats, on=["pk", "issue_number"])
    bugs = bugs.join(linked_sharing, on=["pk", "issue_number"])
    integer_columns = ["n_linked_prs", "n_merged_prs", "n_observed_commits", "n_paths", "n_test_candidate_paths",
                       "max_issues_per_merged_pr"]
    bugs[integer_columns] = bugs[integer_columns].fillna(0).astype("int64")
    for column in ["test_candidate_change", "direct_commit_observed", "message_commit_observed"]:
        bugs[column] = bugs[column].eq(True)
    bugs["included"] = bugs.n_paths.gt(0)
    bugs["strict_included"] = [(p, n) in strict_keys for p, n in zip(bugs.pk, bugs.issue_number)]
    bugs["selection_status"] = "included"
    bugs.loc[~bugs.included, "selection_status"] = "observed_commit_no_paths"
    bugs.loc[bugs.n_observed_commits.eq(0), "selection_status"] = "no_observed_commit"
    bugs.loc[bugs.n_merged_prs.eq(0), "selection_status"] = "no_merged_linked_pr"
    bugs.loc[bugs.n_linked_prs.eq(0), "selection_status"] = "no_linked_pr"
    cohort = bugs[bugs.included].copy()
    projects = projects.merge(cohort.groupby("pk").agg(
        candidate_issues=("issue_number", "size"), test_candidate_issues=("test_candidate_change", "sum")),
        on="pk", how="inner")
    metrics = {
        "issues_after_project_filter": len(issues), "eligible_bug_issues": len(bugs),
        "included_issues": len(cohort), "included_projects": cohort.pk.nunique(),
        "issues_with_observed_commit": int(bugs.n_observed_commits.gt(0).sum()),
        "test_candidate_issues": int(cohort.test_candidate_change.sum()),
        "strict_marker_included_issues": int(bugs.strict_included.sum()),
        "selection_status": {str(k): int(v) for k, v in bugs.selection_status.value_counts().items()},
        "duplicate_bug_link_rows_removed": int((ip.raw_link_rows - 1).sum()),
        "duplicate_commit_rows_removed": duplicate_commit_rows_removed,
        "merged_prs": len(referenced_prs), "shared_prs": int(shared.gt(1).sum()),
        "issues_with_multiple_merged_prs": int(cohort.n_merged_prs.gt(1).sum()),
        "issues_sharing_a_merged_pr": int(cohort.max_issues_per_merged_pr.gt(1).sum()),
        "pr_commit_refs": len(refs), "unobserved_pr_commit_refs": int((~refs.commit_observed).sum()),
    }
    tables = {"issue_selection": selection, "bug_issues": bugs, "bug_issue_pr": ip,
              "pr_commit_refs": refs, "issue_pr_commit": issue_commits, "commit_paths": files,
              "issue_paths": issue_paths, "cohort": cohort, "project_candidates": projects,
              "duplicate_bug_links": duplicated_links, "duplicate_commits": duplicate_commits}
    return tables, metrics


def file_hash(path):
    h = hashlib.sha256()
    with path.open("rb") as source:
        for data in iter(lambda: source.read(8 << 20), b""):
            h.update(data)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw_dir", type=Path)
    parser.add_argument("interim_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("report_dir", type=Path)
    parser.add_argument("--expected-bugs", type=int, default=81620)
    parser.add_argument("--expected-included", type=int, default=13883)
    args = parser.parse_args()
    if args.output_dir.exists() or args.report_dir.exists():
        parser.error("Use new output and report directories; existing runs are preserved")
    names = ["issue", "pr", "issue_pr", "pr_commit", "project"]
    paths = [args.raw_dir / "tables" / f"{name}.parquet" for name in names]
    frames = [pd.read_parquet(path) for path in paths]
    commit_path = args.interim_dir / "commits_slim.parquet"
    cm = pd.read_parquet(commit_path, columns=["project_key", "sha", "created_at", "message", "files", "source_file"])
    tables, metrics = build(*frames[:4], cm, frames[4], duplicated_projects())
    if metrics["eligible_bug_issues"] != args.expected_bugs or metrics["included_issues"] != args.expected_included:
        raise ValueError(f"Cohort differs from expected baseline: {metrics}")
    args.output_dir.mkdir(parents=True)
    args.report_dir.mkdir(parents=True)
    for name, frame in tables.items():
        frame.to_parquet(args.output_dir / f"{name}.parquet", index=False, compression="zstd")
    empty = tables["bug_issues"].query("selection_status == 'observed_commit_no_paths'")
    empty[["pk", "issue_number", "title", "n_observed_commits"]].to_json(
        args.report_dir / "observed_commit_no_paths.json", orient="records", force_ascii=False, indent=2)
    source_manifest = {str(path.resolve()): {"bytes": path.stat().st_size, "sha256": file_hash(path)}
                       for path in paths + [commit_path, Path(__file__), Path(__file__).with_name("common.py")]}
    summary = {"status": "candidate_cohort_built_not_semantically_validated", "metrics": metrics,
               "tables_dir": str(args.output_dir.resolve()), "inputs_and_code": source_manifest,
               "test_rule": "pilot_path_rule_unvalidated", "broad_message_pattern": BROAD_REF.pattern,
               "strict_first_line_pattern": STRICT_REF.pattern}
    (args.report_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    cards = []
    for row in tables["project_candidates"].sort_values(["candidate_issues", "pk"], ascending=[False, True]).to_dict("records"):
        cards.append({"project_key": row["pk"], "project": row["project"], "candidate_issues": int(row["candidate_issues"]),
                      "test_candidate_issues": int(row["test_candidate_issues"]), "topics": row["topics"],
                      "readme": row["readme_content"] if isinstance(row["readme_content"], str) else "",
                      "scope": "unreviewed", "evidence": "", "rationale": "", "confidence": ""})
    with (args.report_dir / "project_scope_cards.jsonl").open("w", encoding="utf-8") as output:
        for row in cards:
            output.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(json.dumps(metrics, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
