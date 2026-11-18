"""Keep reviewed development cases, then sample audit from disjoint Issue-PR components.

The audit sampling frame also excludes selected qualitative PR cases. Human
packets contain source text and blank fields only, never the LLM answers.

With --final-dir, the audit is drawn only from issues whose merged PRs all have a
final (landing) diff (11_final_pr_diff.py); components still span the whole game
cohort so that no audit issue shares a PR with development or qualitative cases.
"""
import argparse
import hashlib
import html
import importlib.util
import json
from pathlib import Path
import random
import re
import sys

import pandas as pd


def components(keys, links):
    parent = {key: key for key in keys}

    def root(key):
        while parent[key] != key:
            parent[key] = parent[parent[key]]
            key = parent[key]
        return key

    for _, group in links.groupby(["pk", "pr_number"], sort=True):
        members = sorted(set(zip(group.pk, group.issue_number)).intersection(parent))
        if not members:
            continue
        first = members[0]
        for member in members[1:]:
            a, b = root(first), root(member)
            parent[max(a, b)] = min(a, b)
    return {key: root(key) for key in parent}


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def write_jsonl(path, rows):
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cohort_dir", type=Path)
    parser.add_argument("game_cohort", type=Path)
    parser.add_argument("previous_samples", type=Path)
    parser.add_argument("qualitative_cases", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--seed", type=int, default=20261114)
    parser.add_argument("--final-dir", type=Path, default=None)
    args = parser.parse_args()
    if args.output_dir.exists():
        parser.error("Choose a new output directory to preserve annotation versions")
    cohort = pd.read_parquet(args.game_cohort)
    links = pd.read_parquet(args.cohort_dir / "bug_issue_pr.parquet")
    links = links[links.merged].merge(cohort[["pk", "issue_number"]], on=["pk", "issue_number"])
    keys = set(zip(cohort.pk, cohort.issue_number))
    group = components(keys, links)
    old = read_jsonl(args.previous_samples / "issues_llm.jsonl")
    development = [row for row in old if row["split"] == "development"]
    dev_keys = {(row["project_key"], row["issue_number"]) for row in development}
    if len(dev_keys) != 100 or not dev_keys <= keys:
        raise ValueError("Expected exactly 100 preserved development issues from this cohort")
    cases = read_jsonl(args.qualitative_cases / "cases.jsonl")
    case_prs = {(row["project_key"], row["pr_number"]) for row in cases}
    case_keys = {(row.pk, row.issue_number) for row in links.itertuples()
                 if (row.pk, row.pr_number) in case_prs}
    blocked_groups = {group[key] for key in dev_keys | case_keys}
    population = keys
    if args.final_dir is not None:
        final_issue = pd.read_parquet(args.final_dir / "issue_final_diff.parquet")
        final_issue = final_issue[final_issue.final_status.eq("all_landing")]
        population = keys & set(zip(final_issue.pk, final_issue.issue_number))
    audit_frame = sorted(key for key in population if group[key] not in blocked_groups)
    audit_keys = random.Random(args.seed).sample(audit_frame, 100)
    assert not {group[key] for key in audit_keys} & blocked_groups
    spec = importlib.util.spec_from_file_location("sampling", Path(__file__).with_name("05_prepare_validation.py"))
    sampling = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sampling)
    by_key = cohort.set_index(["pk", "issue_number"])
    audit = []
    for project, number in audit_keys:
        row = by_key.loc[(project, number)]
        audit.append(dict(sample_id=f"{project}#{number}", project_key=project, project=row.project,
                          issue_number=int(number), title=row.title if pd.notna(row.title) else "",
                          body=row.body if pd.notna(row.body) else "", split="audit", **sampling.annotation_fields()))
    human = random.Random(args.seed + 1).sample(audit, 50)
    args.output_dir.mkdir(parents=True)
    write_jsonl(args.output_dir / "issues_llm.jsonl", development + audit)
    write_jsonl(args.output_dir / "human_blind.jsonl", [{k: v for k, v in row.items() if k != "split"} for row in human])
    old_labels = read_jsonl(args.previous_samples / "development_labels.jsonl")
    if {row["sample_id"] for row in old_labels} != {row["sample_id"] for row in development}:
        raise ValueError("Development annotation IDs do not match preserved source cases")
    write_jsonl(args.output_dir / "development_labels.jsonl", old_labels)
    answers = [{"sample_id": row["sample_id"], "is_actual_bug": "", "primary_category": "",
                "issue_domain": "", "confidence": "", "rationale": ""} for row in human]
    (args.output_dir / "human_answers.json").write_text(json.dumps(answers, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    packet = ["# 独立判定用50件（LLMの回答は含まない）", "",
              "判定手引き `validation/codebook.md` を読み、各報告のタイトルと収録本文だけで判断する。",
              "`human_answers.json` の is_actual_bug、primary_category、issue_domain、confidence、rationale を記入する。",
              "development_labels.jsonl は回答が終わるまで開かない。画像・動画の中身や現在のGitHub本文では補完しない。",
              "判断できないときは unknown とし、理由を残す。画像等の5項目は今回は記入不要。", ""]
    for index, row in enumerate(human, 1):
        runs = [len(match) for match in re.findall(r"`{3,}", row["body"])]
        fence = "`" * max(4, max(runs, default=3) + 1)
        packet += [f"## {index}. {html.escape(row['title'])}", "", row["sample_id"], "",
                   fence + "text", row["body"], fence, ""]
    (args.output_dir / "human_review.md").write_text("\n".join(packet), encoding="utf-8")
    manifest = {"status": "group_disjoint_audit_prepared_human_answers_blank", "scope_status": "LLM_provisional_game_scope",
                "population": len(population), "game_cohort_issues": len(keys),
                "population_definition": "game scope, all merged PRs with final landing diff" if args.final_dir is not None else "game scope",
                "development_in_population": len(dev_keys & population), "development_size": 100, "audit_size": 100, "human_size": 50,
                "seed": args.seed, "design": "Development fixed; audit SRS of issues from remaining disjoint Issue-PR components",
                "audit_sampling_frame_size": len(audit_frame), "audit_inclusion_probability": 100 / len(audit_frame),
                "held_out_from_audit_due_to_development_or_qualitative_cases": len(population) - len(audit_frame),
                "issue_pr_components": len(set(group.values())), "shared_development_audit_components": 0,
                "development_ids": [row["sample_id"] for row in development],
                "audit_ids": [row["sample_id"] for row in audit], "human_ids": [row["sample_id"] for row in human],
                "sources": {str(path): file_hash(path) for path in [args.game_cohort,
                    args.previous_samples / "issues_llm.jsonl", args.previous_samples / "development_labels.jsonl",
                    args.qualitative_cases / "cases.jsonl", Path(__file__)]}}
    (args.output_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in manifest.items() if not key.endswith("_ids") and key != "sources"}, indent=2))


if __name__ == "__main__":
    main()
