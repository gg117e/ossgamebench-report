"""Record the path-level validation of the test-candidate rule and a sensitivity check.

Judgements were made by Claude (claude-fable-5-2, 2026-11-15) from the file paths
of the final diffs in validation/test_path_rule_v1/sample.jsonl (50 flagged and 50
unflagged fixes) and from the probe hits among all unflagged fixes. Paths only:
file contents were not inspected here. Not human-validated.

Categories for flagged fixes:
  executable   at least one flagged path is a test source file
  support      only fixtures, mocks or test infrastructure (test-related, no test code)
  manual       manual test harness (not an automated test)
  not_test     the rule matched a non-test file (false positive)

Usage:
    python -I scripts/24_test_path_rule_validation.py <interim_dir> <validation_dir> <labels_csv> <out_json>
"""
import argparse
from collections import Counter
import json
from pathlib import Path

import pandas as pd

# flagged sample: exceptions to "executable" (index = order in sample.jsonl)
FLAGGED = {
    0: ("manual", "in-game test screen (Screens/Tests)"),
    2: ("support", "game-record fixture only"), 3: ("support", "mock header only"),
    4: ("not_test", "test card content (cards/Tests/placeholder.js)"),
    7: ("support", "fixtures only"), 17: ("support", "fixture only"), 24: ("support", "fixture only"),
    28: ("not_test", "in-game test commands (CommandsTest.ts)"),
    30: ("support", "fixture only"), 31: ("not_test", "image asset named test_crystal.png"),
    33: ("support", "mock header only"), 35: ("support", "CMake files for test assets"),
    36: ("support", "mock and fixture class"), 39: ("support", "test list (infrastructure)"),
    46: ("support", "fixture only"), 47: ("support", "fixture only"),
}
# unflagged sample: none of the 50 contains a test-related path (full path lists checked with the probe)
UNFLAGGED_MISSES = 0


def probe_category(pk, paths):
    if pk == "tobymao/18xx" and any("public/fixtures/" in p for p in paths):
        return "missed_fixture"          # game-record fixtures moved to public/fixtures
    if any("rectest" in p.lower() for p in paths):
        return "missed_record_replay"    # omf2097/openomf recorded-input tests
    if any(s in p for p in paths for s in ("test_fixtures/", "Content.IntegrationTests/", "zzre.core.tests/",
                                           "OpenRA.Test.nunit", "interface_mock/")):
        return "missed_other_test_related"
    if any(".github/workflows" in p and "test" in p for p in paths):
        return "ci_workflow_only"
    return "not_test"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for a in ("interim_dir", "validation_dir", "labels_csv", "out_json"):
        ap.add_argument(a, type=Path)
    args = ap.parse_args()
    sample = [json.loads(l) for l in (args.validation_dir / "sample.jsonl").read_text(encoding="utf-8").splitlines()]
    flagged = [s for s in sample if s["stratum"] == "flagged"]
    judged = []
    for i, s in enumerate(flagged):
        cat, why = FLAGGED.get(i, ("executable", ""))
        judged.append({"pk": s["pk"], "issue_number": s["issue_number"], "category": cat, "note": why})
    (args.validation_dir / "flagged_judgements.jsonl").write_text(
        "".join(json.dumps(j, ensure_ascii=False) + "\n" for j in judged), encoding="utf-8")
    fc = Counter(j["category"] for j in judged)
    hits = [json.loads(l) for l in (args.validation_dir / "unflagged_probe_hits.jsonl").read_text(encoding="utf-8").splitlines()]
    for h in hits:
        h["category"] = probe_category(h["pk"], h["probe_paths"])
    pc = Counter(h["category"] for h in hits)
    missed = {(h["pk"], h["issue_number"]) for h in hits if h["category"].startswith("missed")}

    # sensitivity: flip the known misses to "with test" and recompute the headline rates
    a = pd.read_parquet(args.interim_dir / "final_diff_v1" / "analysis_table.parquet")
    lab = pd.read_csv(args.labels_csv)[["pk", "game_type"]]
    a = a.merge(lab, on="pk")
    a["test_ext"] = a.test_final.astype(bool) | [(p, n) in missed for p, n in zip(a.pk, a.issue_number)]
    def r(d, c):
        return round(float(d[c].mean()), 4)
    sens = {"all": {"rule": r(a, "test_final"), "with_known_misses": r(a, "test_ext")}}
    for g in ("discrete", "continuous"):
        d = a[a.game_type == g]
        sens[g] = {"rule": r(d, "test_final"), "with_known_misses": r(d, "test_ext")}
    for s in ("gameplay", "ui", "crash_hang", "visual", "audio", "other"):
        d = a[a.symptom == s]
        sens[s] = {"rule": r(d, "test_final"), "with_known_misses": r(d, "test_ext")}
    n_f = len(flagged)
    out = {
        "annotator": "Claude", "model_id": "claude-fable-5-2", "date_jst": "2026-11-15",
        "basis": "file paths of final diffs only; not human-validated",
        "flagged_sample": {"n": n_f, **dict(fc),
                           "precision_test_related": round((fc["executable"] + fc["support"]) / n_f, 3),
                           "share_with_executable_test_file": round(fc["executable"] / n_f, 3)},
        "unflagged_sample": {"n": len(sample) - n_f, "misses": UNFLAGGED_MISSES,
                             "upper_95_miss_rate_rule_of_three": round(3 / (len(sample) - n_f), 3)},
        "probe_all_unflagged": {"unflagged_fixes": int((~a.test_final.astype(bool)).sum()),
                                "with_probe_substring": len(hits), **dict(pc),
                                "known_missed_fixes": len(missed)},
        "sensitivity_rates": sens,
        "note": "The probe only finds misses whose paths contain test/spec/mock/fixture; other misses stay unknown.",
    }
    args.out_json.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
