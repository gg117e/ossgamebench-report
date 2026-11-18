"""Validate and materialize explicit provisional README annotations, not infer labels.

The input decisions are LLM-authored annotation data. All resulting counts remain
provisional until scope and test-path annotations have been independently validated.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import pandas as pd


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def labels_for(cards, decisions, additions):
    chosen = {}
    for source in (decisions, additions):
        for scope in ("game", "engine_tool", "mixed"):
            for index in source[scope]:
                if index in chosen:
                    raise ValueError(f"Index assigned more than once: {index}")
                chosen[index] = scope
    quotes = {**decisions["evidence_overrides"], **additions["evidence_overrides"]}
    external = additions["external_evidence"]
    if any(index < 0 or index >= len(cards) for index in chosen):
        raise ValueError("Annotation index outside the source cards")
    labels = []
    for index, card in enumerate(cards):
        ext = external.get(str(index))
        scope = ext["scope"] if ext else chosen.get(index, "unknown")
        quote = ext["quote"] if ext else quotes.get(str(index), card["review_line"][:120])
        if scope == "unknown":
            quote = ""
        if quote and not ext and quote not in card["readme"]:
            raise ValueError(f"Evidence is not verbatim in source README: {index} {quote!r}")
        if len(quote.split()) > 22:
            end = 0
            import re
            words = list(re.finditer(r"\S+", quote))
            end = words[21].end()
            quote = quote[:end]
        labels.append({"project_key": card["project_key"], "scope": scope,
                       "evidence_quote": quote, "evidence_source": "external_current_page" if ext else "dataset_project_readme",
                       "evidence_url": ext["url"] if ext else "", "confidence": "medium" if scope != "unknown" else "low",
                       "review_status": "llm_provisional_not_human_validated", "annotator": "Codex",
                       "model_id": "not_exposed_in_session", "review_date_jst": "2026-11-12",
                       "source_index": index, "source_readme_sha256": hashlib.sha256(card["readme"].encode()).hexdigest(),
                       "rationale": ext["note"] if ext else {
                           "game": "Specific playable game, game rules service, or target-game reimplementation/complete gameplay variant.",
                           "engine_tool": "Reusable engine/library, creator, operations/companion tool or non-game software artifact.",
                           "mixed": "Game/tool combination, partial modification, runtime component, or boundary requiring independent review.",
                           "unknown": "Insufficient evidence in the inspected dataset README; held out of game-only cohort."
                       }[scope]})
    return labels


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cohort_dir", type=Path)
    parser.add_argument("cards_path", type=Path)
    parser.add_argument("annotation_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    if args.output_dir.exists():
        parser.error("Use a new output directory to preserve existing versions")
    cards = [json.loads(line) for line in args.cards_path.read_text(encoding="utf-8").splitlines()]
    source_paths = [args.annotation_dir / "decisions.json", args.annotation_dir / "review_additions.json"]
    labels = labels_for(cards, *(json.loads(p.read_text(encoding="utf-8")) for p in source_paths))
    label_frame = pd.DataFrame(labels)
    if label_frame.project_key.duplicated().any():
        raise ValueError("Duplicate project labels")
    cohort = pd.read_parquet(args.cohort_dir / "cohort.parquet")
    joined = cohort.merge(label_frame, left_on="pk", right_on="project_key", how="left", validate="many_to_one")
    if joined.scope.isna().any():
        raise ValueError("Projects are missing annotations")
    summary = joined.groupby("scope").agg(projects=("pk", "nunique"), candidate_issues=("issue_number", "size"),
                                           test_candidate_issues=("test_candidate_change", "sum"))
    summary["test_candidate_rate"] = summary.test_candidate_issues / summary.candidate_issues
    games = joined[joined.scope.eq("game")].copy()
    args.output_dir.mkdir(parents=True)
    games.to_parquet(args.output_dir / "game_cohort.parquet", index=False, compression="zstd")
    joined.drop(columns=["body", "title"]).to_parquet(args.output_dir / "scoped_cohort_index.parquet", index=False)
    with (args.annotation_dir / "labels.jsonl").open("w", encoding="utf-8") as output:
        for row in labels:
            output.write(json.dumps(row, ensure_ascii=False) + "\n")
    project_counts = joined.groupby(["pk", "scope"]).agg(
        candidate_issues=("issue_number", "size"), test_candidate_issues=("test_candidate_change", "sum")).reset_index()
    project_counts.to_json(args.annotation_dir / "project_counts.json", orient="records", force_ascii=False, indent=2)
    result = {"status": "provisional_scope_not_human_validated", "scope_counts": summary.reset_index().to_dict("records"),
              "game_issues_dataset_readme_evidence": int((games.evidence_source == "dataset_project_readme").sum()),
              "game_issues_external_evidence": int((games.evidence_source == "external_current_page").sum()),
              "sources": {str(p): sha256(p) for p in [args.cards_path, *source_paths]},
              "game_cohort": str((args.output_dir / "game_cohort.parquet").resolve())}
    (args.annotation_dir / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
