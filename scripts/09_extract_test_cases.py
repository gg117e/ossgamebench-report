"""Prepare diverse PR cases and extract test-candidate patches from the source ZIP.

Audit-sample PRs are excluded to avoid exposing held-out issues while developing
the coding guide. This is a qualitative diversity sample, not a prevalence sample.

With --final-dir (output of 11_final_pr_diff.py), only PRs whose final (landing)
diff contains a test-candidate path are eligible, only game issues whose merged PRs
all have a final diff count, and patches come from the landing commit only. This
removes test files brought in by in-branch merges (v1 used every PR commit).
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import random
import shutil
import sys
import tempfile
import zipfile

import pandas as pd
import pyarrow.parquet as pq


def as_list(value):
    if value is None:
        return []
    if isinstance(value, str):
        parsed = json.loads(value)
        if not isinstance(parsed, list):
            raise ValueError("Expected a list in JSON-encoded diff")
        return parsed
    return list(value)


def candidate_patches(diffs, wanted_paths):
    results = []
    for entry in as_list(diffs):
        if not isinstance(entry, dict) or "file" not in entry:
            raise ValueError("Unknown diff schema; do not guess file-to-patch alignment")
        if entry["file"] in wanted_paths:
            results.append({"path": entry["file"], "change_type": entry.get("change_type"),
                            "patch": entry.get("patch"), "patch_completeness": "not_verified"})
    return results


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw_dir", type=Path)
    parser.add_argument("cohort_dir", type=Path)
    parser.add_argument("game_cohort", type=Path)
    parser.add_argument("sample_jsonl", type=Path)
    parser.add_argument("zip_manifest", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--n", type=int, default=30)
    parser.add_argument("--project-cap", type=int, default=3)
    parser.add_argument("--seed", type=int, default=20261112)
    parser.add_argument("--final-dir", type=Path, default=None)
    args = parser.parse_args()
    if args.output_dir.exists():
        parser.error("Choose a new output directory; existing case annotations are preserved")
    games = pd.read_parquet(args.game_cohort)
    ip = pd.read_parquet(args.cohort_dir / "bug_issue_pr.parquet")
    if args.final_dir is not None:
        final_issue = pd.read_parquet(args.final_dir / "issue_final_diff.parquet")
        games = games.merge(final_issue.loc[final_issue.final_status.eq("all_landing"), ["pk", "issue_number"]],
                            on=["pk", "issue_number"])
    ip = ip[ip.merged].merge(games[["pk", "issue_number"]], on=["pk", "issue_number"], validate="many_to_one")
    heldout = [json.loads(line) for line in args.sample_jsonl.read_text(encoding="utf-8").splitlines()]
    heldout_keys = {(r["project_key"], r["issue_number"]) for r in heldout if r["split"] == "audit"}
    excluded_prs = {(r.pk, r.pr_number) for r in ip.itertuples()
                    if (r.pk, r.issue_number) in heldout_keys}
    refs = pd.read_parquet(args.cohort_dir / "pr_commit_refs.parquet")
    refs = refs[refs.commit_observed].copy()
    paths = pd.read_parquet(args.cohort_dir / "commit_paths.parquet")
    if args.final_dir is not None:
        final_pr = pd.read_parquet(args.final_dir / "pr_final_diff.parquet")
        final_pr = final_pr[final_pr.pr_status.isin(["landing_unique", "landing_equivalent"])]
        landing = final_pr.assign(sha=final_pr.landing_shas.str.split(",")).explode("sha")[["pk", "pr_number", "sha"]]
        refs = refs.merge(landing, on=["pk", "pr_number", "sha"])
    positive = refs.merge(paths[paths.test_candidate], on=["pk", "sha"])
    eligible = ip[["pk", "pr_number"]].drop_duplicates().merge(
        positive[["pk", "pr_number"]].drop_duplicates(), on=["pk", "pr_number"])
    keys = sorted((r.pk, int(r.pr_number)) for r in eligible.itertuples()
                  if (r.pk, r.pr_number) not in excluded_prs)
    random.Random(args.seed).shuffle(keys)
    selected, per_project = [], {}
    for key in keys:
        if per_project.get(key[0], 0) < args.project_cap:
            selected.append(key)
            per_project[key[0]] = per_project.get(key[0], 0) + 1
        if len(selected) == args.n:
            break
    if len(selected) != args.n:
        raise ValueError("Insufficient eligible PRs under the project cap")
    selected_frame = pd.DataFrame(selected, columns=["pk", "pr_number"])
    wanted = positive.merge(selected_frame, on=["pk", "pr_number"])
    args.output_dir.mkdir(parents=True)
    wanted.drop(columns=["message"]).to_parquet(args.output_dir / "selected_test_paths.parquet", index=False)
    with args.zip_manifest.open(encoding="utf-8") as handle:
        member_for = {Path(row["local_file"]).name: row["zip_member"] for row in csv.DictReader(handle)}
    patches_by_commit = {}
    with zipfile.ZipFile(args.raw_dir / "OSSGameBench.zip") as archive:
        for index, (source_file, group) in enumerate(wanted.groupby("source_file"), 1):
            targets = group.groupby(["pk", "sha"]).path.agg(set).to_dict()
            remaining = set(targets)
            with tempfile.TemporaryFile(dir=args.output_dir) as temporary:
                with archive.open(member_for[source_file]) as source:
                    shutil.copyfileobj(source, temporary, 8 << 20)
                temporary.seek(0)
                for batch in pq.ParquetFile(temporary).iter_batches(batch_size=128, columns=["repo", "sha", "diff"]):
                    # Arrow selects rows before Python conversion of large nested patch arrays.
                    repo_values, sha_values = batch.column(0).to_pylist(), batch.column(1).to_pylist()
                    matches = [i for i, (repo, sha) in enumerate(zip(repo_values, sha_values))
                               if (repo.lower(), sha[:40]) in remaining]
                    for row_index in matches:
                        row = batch.slice(row_index, 1).to_pylist()[0]
                        key = (row["repo"].lower(), row["sha"][:40])
                        patches_by_commit[key] = candidate_patches(row["diff"], targets[key])
                        remaining.remove(key)
                if remaining:
                    raise ValueError(f"Selected commits missing in ZIP member: {remaining}")
            print(f"Read {index}/{wanted.source_file.nunique()} project files; CRC verified: {source_file}", flush=True)

    records = []
    for project, pr_number in selected:
        pr_links = ip[(ip.pk == project) & (ip.pr_number == pr_number)]
        commits = wanted[(wanted.pk == project) & (wanted.pr_number == pr_number)].sha.unique()
        changes = []
        seen_patches = set()
        for sha in commits:
            for record in patches_by_commit[(project, sha)]:
                identity = (record["path"], record["patch"])
                if identity in seen_patches:
                    continue
                seen_patches.add(identity)
                changes.append(dict(record, commit_sha=sha))
        first = pr_links.iloc[0]
        records.append({"project_key": project, "pr_number": pr_number,
                        "pr_url": f"https://github.com/{project}/pull/{pr_number}",
                        "pr_title": first.title, "pr_body": first.body,
                        "issue_numbers": sorted(map(int, pr_links.issue_number.unique())),
                        "test_candidate_changes": changes,
                        "status": "unreviewed_path_candidates_not_proven_regression_tests",
                        "test_roles": [], "input_state": "", "actions": "", "oracle": "", "rationale": ""})
    with (args.output_dir / "cases.jsonl").open("w", encoding="utf-8") as output:
        for record in records:
            output.write(json.dumps(record, ensure_ascii=False) + "\n")
    summary = {"status": "patches_extracted_not_semantically_classified", "prs": len(records),
               "projects": len(per_project), "test_candidate_patches": sum(len(r["test_candidate_changes"]) for r in records),
               "sampling": "shuffled eligible PRs, capped by project, excluding held-out issue PRs; qualitative only",
               "seed": args.seed, "project_cap": args.project_cap,
               "diff_source": "final_landing_commit" if args.final_dir is not None else "union_of_all_pr_commits_v1", "excluded_holdout_prs": len(excluded_prs),
               "missing_candidate_patches": int(len(wanted[["pk", "sha", "path"]].drop_duplicates()) -
                   sum(len(values) for values in patches_by_commit.values())),
               "source_sample_sha256": hashlib.sha256(args.sample_jsonl.read_bytes()).hexdigest()}
    (args.output_dir / "manifest.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
