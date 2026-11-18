"""Compare the author's symptom labels with the Claude audit labels and the symptom rules.

The author labeled the first 19 issues of the 50-issue sample while consulting ChatGPT,
without seeing the Claude audit labels or the rule predictions
(validation/samples_game_v3/README.md). Only issues with a primary_category are used.

Usage:
    python -I scripts/28_compare_author_labels.py validation/samples_game_v3/human_answers.json \
        validation/samples_game_v3/audit_llm_labels.jsonl validation/samples_game_v3/human_blind.jsonl \
        validation/samples_game_v3/audit_llm_labels_sealed.json results/author_labels_v1

Checks the SHA-256 of the audit labels against the sealed record before comparing.
Writes summary.json and items.csv to the output directory (refuses to overwrite).
"""
from collections import Counter
import csv
import hashlib
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


def agreement(pairs):
    k = sum(a == b for a, b in pairs)
    n = len(pairs)
    # Exact (Clopper-Pearson) 95% interval for k/n, by bisection on the binomial CDF.
    def cdf(x, p):
        from math import comb
        return sum(comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(x + 1))

    def solve(f):
        lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if f(mid) else (lo, mid)
        return (lo + hi) / 2

    lower = 0.0 if k == 0 else solve(lambda p: 1 - cdf(k - 1, p) < 0.025)
    upper = 1.0 if k == n else solve(lambda p: cdf(k, p) > 0.025)
    return {"n": n, "agree": k, "accuracy": round(k / n, 3), "ci95": [round(lower, 3), round(upper, 3)],
            "kappa": round(kappa(pairs), 3)}


def main():
    human_p, audit_p, blind_p, seal_p, out = map(Path, sys.argv[1:6])
    if out.exists():
        sys.exit(f"{out} exists; use a new directory")
    seal = json.loads(seal_p.read_text(encoding="utf-8"))
    digest = hashlib.sha256(audit_p.read_bytes()).hexdigest()
    if digest != seal["sha256"]:
        sys.exit(f"SHA-256 mismatch: {digest} != {seal['sha256']}")

    human = [r for r in json.loads(human_p.read_text(encoding="utf-8")) if r.get("primary_category")]
    audit = {}
    for line in audit_p.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            audit[r["sample_id"]] = r
    issues = {}
    for line in blind_p.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            issues[r["sample_id"]] = r

    rows = []
    for h in human:
        sid = h["sample_id"]
        a = audit[sid]
        rule, src = R.classify(issues[sid]["title"], issues[sid]["body"])
        rows.append({"sample_id": sid, "title": issues[sid]["title"],
                     "author_bug": h["is_actual_bug"], "claude_bug": a["is_actual_bug"],
                     "author": h["primary_category"], "claude": a["primary_category"],
                     "rule": rule, "rule_source": src})

    summary = {
        "note": "Author labels were made while consulting ChatGPT, without seeing the Claude labels "
                "or the rule predictions. They are not independent of an LLM.",
        "audit_sha256": digest,
        "n_author_labels": len(rows),
        "author_vs_claude_category": agreement([(r["author"], r["claude"]) for r in rows]),
        "author_vs_claude_is_bug": agreement([(r["author_bug"], r["claude_bug"]) for r in rows]),
        "rule_vs_author": agreement([(r["author"], r["rule"]) for r in rows]),
        "rule_vs_claude_same_issues": agreement([(r["claude"], r["rule"]) for r in rows]),
        "author_categories": dict(Counter(r["author"] for r in rows)),
    }
    out.mkdir(parents=True)
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n",
                                      encoding="utf-8", newline="\n")
    with (out / "items.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(json.dumps(summary, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
