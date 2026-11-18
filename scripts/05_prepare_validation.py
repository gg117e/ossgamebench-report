"""Prepare reproducible, unlabelled issue samples. Never produces gold labels.

Requires only raw/tables/issue.parquet, pandas and pyarrow.
See validation/README.md for the sampling design and annotation instructions.
"""
import argparse
import hashlib
import json
from pathlib import Path
import random
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import duplicated_projects, is_bug_label, is_nofix_label


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def select_samples(records, seed, sample_size, dev_size, human_size, seen_ids=None):
    """Sort before sampling so parquet row order cannot change membership."""
    ordered = sorted(records, key=lambda row: (row["project_key"], row["issue_number"]))
    if len({(r["project_key"], r["issue_number"]) for r in ordered}) != len(ordered):
        raise ValueError("Duplicate issue keys; audit inputs before sampling")
    if not (0 < dev_size < sample_size <= len(ordered)):
        raise ValueError("Need 0 < dev_size < sample_size <= eligible issue count")
    if not (0 < human_size <= sample_size - dev_size):
        raise ValueError("Human sample must fit in the held-out audit sample")
    if seen_ids:
        forced = [row for row in ordered if row["sample_id"] in seen_ids]
        if len(forced) > dev_size:
            raise ValueError("Previously seen cases exceed the development allocation")
        unseen = [row for row in ordered if row["sample_id"] not in seen_ids]
        rng = random.Random(seed)
        development = forced + rng.sample(unseen, dev_size - len(forced))
        dev_ids = {row["sample_id"] for row in development}
        audit = rng.sample([row for row in unseen if row["sample_id"] not in dev_ids], sample_size - dev_size)
        sample = development + audit
    else:
        sample = random.Random(seed).sample(ordered, sample_size)
    rows = [dict(row, split="development" if i < dev_size else "audit")
            for i, row in enumerate(sample)]
    human = random.Random(seed + 1).sample(rows[dev_size:], human_size)
    return rows, human


def annotation_fields():
    return {"is_actual_bug": "", "primary_category": "", "secondary_contexts": [],
            "image": "", "video": "", "save_data": "", "log_trace": "", "steps": "",
            "evidence_quotes": {}, "confidence": "", "rationale": "",
            "annotator": "", "model_id": "", "annotated_at": "", "status": "unlabelled"}


def write_jsonl(path, rows):
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw_dir", type=Path)
    parser.add_argument("output_dir", type=Path, help="New directory; existing directories are refused")
    parser.add_argument("--seed", type=int, default=20261112)
    parser.add_argument("--sample-size", type=int, default=200)
    parser.add_argument("--dev-size", type=int, default=100)
    parser.add_argument("--human-size", type=int, default=50)
    parser.add_argument("--cohort", type=Path, help="Optional parquet with unique pk/issue_number population keys")
    parser.add_argument("--seen-development", type=Path,
                        help="Old sample JSONL; its development cases must not enter the new audit")
    parser.add_argument("--expected-bugs", type=int, default=81620,
                        help="Fail if the population differs from the historical pilot")
    args = parser.parse_args()
    source = args.raw_dir / "tables" / "issue.parquet"
    if not source.is_file():
        parser.error(f"Missing input: {source}. Copy tables from the original machine first.")
    if args.output_dir.exists():
        parser.error("Output directory already exists; choose a new directory to protect annotations.")
    try:
        import pandas as pd
    except ImportError:
        parser.error("Install pandas and pyarrow in the selected Python environment.")
    columns = ["project", "number", "title", "body", "labels"]
    df = pd.read_parquet(source, columns=columns)
    df["project_key"] = df.project.str.lower()
    df = df[~df.project_key.isin(duplicated_projects())].copy()
    df = df[df.labels.map(lambda labels: any(is_bug_label(x) for x in labels)
                         and not any(is_nofix_label(x) for x in labels))].copy()
    all_bug_count = len(df)
    if args.cohort:
        keys = pd.read_parquet(args.cohort, columns=["pk", "issue_number"]).rename(
            columns={"pk": "project_key", "issue_number": "number"})
        if keys.duplicated(["project_key", "number"]).any():
            parser.error("Cohort contains duplicate issue keys")
        df = df.merge(keys, on=["project_key", "number"], validate="one_to_one")
        if len(df) != len(keys):
            parser.error("Some cohort keys are not in the eligible bug population")
    if len(df) != args.expected_bugs:
        parser.error(f"Eligible bugs: {len(df)}, expected {args.expected_bugs}. Audit inputs/rules.")
    records = []
    for row in df.itertuples(index=False):
        records.append({"sample_id": f"{row.project_key}#{row.number}",
                        "project_key": row.project_key, "project": row.project,
                        "issue_number": int(row.number), "title": row.title if pd.notna(row.title) else "",
                        "body": row.body if pd.notna(row.body) else ""})
    seen_ids = set()
    if args.seen_development:
        with args.seen_development.open(encoding="utf-8") as handle:
            for line in handle:
                old = json.loads(line)
                if old.get("split") == "development":
                    seen_ids.add(old["sample_id"])
    rows, human = select_samples(records, args.seed, args.sample_size, args.dev_size, args.human_size, seen_ids)
    forced_ids = sorted(seen_ids.intersection(row["sample_id"] for row in records))
    metadata = {
        "status": "samples_only_no_annotations", "codebook_version": "draft-2026-11-12",
        "seed": args.seed, "population": len(df), "sample_size": len(rows),
        "development_size": args.dev_size, "audit_size": len(rows) - args.dev_size,
        "human_size": len(human), "projects_in_sample": len({r["project_key"] for r in rows}),
        "design": "simple random sample without replacement; no project cap",
        "inclusion_probability": len(rows) / len(df),
        "source": str(source.resolve()), "source_sha256": sha256(source),
        "script_sha256": sha256(Path(__file__)),
        "common_sha256": sha256(Path(__file__).with_name("common.py")),
        "python_version": sys.version, "pandas_version": pd.__version__,
        "sample_ids": [r["sample_id"] for r in rows],
        "human_ids": [r["sample_id"] for r in human],
        "all_eligible_bug_count": all_bug_count,
        "cohort_path": str(args.cohort.resolve()) if args.cohort else None,
        "cohort_sha256": sha256(args.cohort) if args.cohort else None,
        "seen_development_path": str(args.seen_development.resolve()) if args.seen_development else None,
        "seen_development_sha256": sha256(args.seen_development) if args.seen_development else None,
        "forced_development_ids": forced_ids,
    }
    if args.seen_development:
        metadata["design"] = "Seen cases fixed in development; random development fill; audit SRS from remaining unseen population"
        metadata["inclusion_probability"] = None
        metadata["audit_sampling_frame_size"] = len(records) - args.dev_size
        metadata["audit_inclusion_probability_conditional_on_development"] = (len(rows) - args.dev_size) / (len(records) - args.dev_size)
    args.output_dir.mkdir(parents=True, exist_ok=False)
    write_jsonl(args.output_dir / "issues_llm.jsonl", [dict(r, **annotation_fields()) for r in rows])
    # Do not copy LLM predictions, split membership, or labels to the blind file.
    write_jsonl(args.output_dir / "human_blind.jsonl",
                [dict({k: v for k, v in r.items() if k != "split"}, **annotation_fields()) for r in human])
    (args.output_dir / "manifest.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared {len(rows)} issues and {len(human)} blind human rows in {args.output_dir}")
    print("No classifications have been performed. Keep audit labels sealed during rule development.")


if __name__ == "__main__":
    main()
