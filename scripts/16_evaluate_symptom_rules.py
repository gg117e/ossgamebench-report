"""Evaluate the frozen symptom rules (symptom_rules.py) against LLM reference labels.

Development labels (Codex) were used to write the rules; the audit labels (Claude,
sealed until the first author's blind labels are done) are used once for evaluation.
Writes overall metrics to <public_json> and per-category details to <sealed_json>
(keep the latter outside the repository until the human labels are complete).

Usage:
    python -I scripts/16_evaluate_symptom_rules.py <issues_llm_jsonl> <dev_labels_jsonl> <audit_labels_jsonl> <public_json> <sealed_json>
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import symptom_rules as R  # noqa: E402


def kappa(pairs):
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n ** 2
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def evaluate(labels, issues):
    pairs = []
    for lab in labels:
        r = issues[lab["sample_id"]]
        pred, src = R.classify(r["title"], r["body"])
        pairs.append((lab["primary_category"], pred, src, lab["is_actual_bug"]))
    allp = [(g, p) for g, p, _, _ in pairs]
    bugs = [(g, p) for g, p, _, b in pairs if b == "yes" and g not in ("unknown", "multiple")]
    cats = sorted({g for g, _ in allp} | {p for _, p in allp})
    per = {}
    for c in cats:
        tp = sum(g == c and p == c for g, p in allp)
        per[c] = {"reference_n": sum(g == c for g, _ in allp), "predicted_n": sum(p == c for _, p in allp),
                  "precision": round(tp / max(1, sum(p == c for _, p in allp)), 3),
                  "recall": round(tp / max(1, sum(g == c for g, _ in allp)), 3)}
    f1 = [2 * v["precision"] * v["recall"] / (v["precision"] + v["recall"]) if v["precision"] + v["recall"] else 0
          for c, v in per.items() if v["reference_n"]]
    overall = {"n": len(allp), "accuracy": round(sum(g == p for g, p in allp) / len(allp), 3),
               "kappa": round(kappa(allp), 3), "macro_f1_reference_categories": round(sum(f1) / len(f1), 3),
               "n_actual_bug_known_category": len(bugs),
               "accuracy_actual_bug_known_category": round(sum(g == p for g, p in bugs) / len(bugs), 3),
               "kappa_actual_bug_known_category": round(kappa(bugs), 3),
               "source_of_prediction": dict(Counter(s for _, _, s, _ in pairs))}
    return overall, per, Counter((g, p) for g, p in allp)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for a in ("issues_llm_jsonl", "dev_labels_jsonl", "audit_labels_jsonl", "public_json", "sealed_json"):
        ap.add_argument(a, type=Path)
    args = ap.parse_args()
    read = lambda p: [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines()]
    issues = {r["sample_id"]: r for r in read(args.issues_llm_jsonl)}
    dev_o, dev_p, _ = evaluate(read(args.dev_labels_jsonl), issues)
    aud_o, aud_p, aud_c = evaluate(read(args.audit_labels_jsonl), issues)
    public = {"rules": "scripts/symptom_rules.py (frozen after development)", "fallback": "gameplay",
              "development_codex_labels": dev_o, "audit_claude_labels": aud_o,
              "note": "Reference labels are LLM labels, not human ground truth. Per-category audit details are "
                      "sealed until the first author's blind labels are complete."}
    args.public_json.write_text(json.dumps(public, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    sealed = {"audit_per_category": aud_p, "development_per_category": dev_p,
              "audit_confusion": {f"{g} -> {p}": n for (g, p), n in sorted(aud_c.items())}}
    args.sealed_json.write_text(json.dumps(sealed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(public, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
