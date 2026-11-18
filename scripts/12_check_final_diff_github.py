"""Check landing-commit paths (11) against the file list GitHub reports for each PR.

Read-only calls to the public GitHub REST API through the authenticated `gh` CLI
(`pulls/{n}` and `pulls/{n}/files`). Only repository names and PR numbers are sent.

Strata (fixed seed):
  gh_merge     landing commit "Merge pull request #N"     (random, game scope)
  squash_like  landing commit "... (#N)"                   (random, game scope)
  flipped      v1 union had a test candidate, final diff has none (random, all scopes)

Usage:
    python -I scripts/12_check_final_diff_github.py <final_dir> <scoped_index> <cache_dir> <report_dir> [--n 25]
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
spec_path = Path(__file__).with_name("11_final_pr_diff.py")
import importlib.util
spec = importlib.util.spec_from_file_location("final_diff", spec_path)
final_diff = importlib.util.module_from_spec(spec)
spec.loader.exec_module(final_diff)
TEST_RE = final_diff.TEST_RE


def gh_json(endpoint, cache):
    if cache.exists():
        return json.loads(cache.read_text(encoding="utf-8"))
    out = subprocess.run(["gh", "api", "--paginate", "--slurp", endpoint] if endpoint.endswith("/files")
                         else ["gh", "api", endpoint], capture_output=True, text=True, encoding="utf-8")
    data = {"ok": out.returncode == 0, "body": json.loads(out.stdout) if out.returncode == 0 else out.stderr[-500:]}
    cache.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return data


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("final_dir", type=Path)
    ap.add_argument("scoped_index", type=Path)
    ap.add_argument("cache_dir", type=Path)
    ap.add_argument("report_dir", type=Path)
    ap.add_argument("--n", type=int, default=25)
    ap.add_argument("--seed", type=int, default=20261113)
    args = ap.parse_args()
    pr = pd.read_parquet(args.final_dir / "pr_final_diff.parquet")
    scope = pd.read_parquet(args.scoped_index, columns=["pk", "scope"]).drop_duplicates()
    pr = pr.merge(scope, on="pk", how="left")
    landed = pr[pr.pr_status.eq("landing_unique")]
    game = landed[landed.scope.eq("game")]
    strata = {
        "gh_merge": game[game.landing_kind.eq("gh_merge")].sample(args.n, random_state=args.seed),
        "squash_like": game[game.landing_kind.eq("squash_like")].sample(args.n, random_state=args.seed),
        "flipped": landed[landed.test_union & ~landed.test_final.astype(bool)].sample(args.n, random_state=args.seed),
    }
    args.cache_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for stratum, frame in strata.items():
        for r in frame.itertuples():
            base = f"repos/{r.pk}/pulls/{r.pr_number}"
            tag = f"{r.pk.replace('/', '__')}__{r.pr_number}"
            meta = gh_json(base, args.cache_dir / f"{tag}.json")
            files = gh_json(base + "/files", args.cache_dir / f"{tag}.files.json")
            row = dict(stratum=stratum, pk=r.pk, pr_number=int(r.pr_number), scope=r.scope,
                       landing_kind=r.landing_kind, landing_sha=r.landing_shas,
                       n_final_paths=int(r.n_final_paths), n_union_paths=int(r.n_union_paths),
                       test_final=bool(r.test_final), test_union=bool(r.test_union), api_ok=meta["ok"] and files["ok"])
            if row["api_ok"]:
                gh_paths = {f["filename"] for page in files["body"] for f in page}
                ours = set(r.final_paths)
                row.update(gh_changed_files=meta["body"]["changed_files"], gh_listed=len(gh_paths),
                           gh_merge_commit_sha=meta["body"].get("merge_commit_sha"),
                           sha_matches=meta["body"].get("merge_commit_sha") == r.landing_shas,
                           same_paths=gh_paths == ours,
                           jaccard=round(len(gh_paths & ours) / max(1, len(gh_paths | ours)), 3),
                           gh_test=any(TEST_RE.search(p) for p in gh_paths),
                           only_ours=sorted(ours - gh_paths)[:5], only_gh=sorted(gh_paths - ours)[:5])
                row["test_flag_agrees"] = row["gh_test"] == row["test_final"]
            rows.append(row)
            print(stratum, r.pk, r.pr_number, row.get("same_paths"), row.get("test_flag_agrees"), flush=True)
    df = pd.DataFrame(rows)
    args.report_dir.mkdir(parents=True, exist_ok=True)
    df.to_json(args.report_dir / "github_check_rows.json", orient="records", force_ascii=False, indent=1)
    ok = df[df.api_ok]
    summary = {"seed": args.seed, "n_per_stratum": args.n, "api_failures": int((~df.api_ok).sum()), "strata": {}}
    for stratum, g in ok.groupby("stratum"):
        summary["strata"][stratum] = {
            "checked": int(len(g)), "same_paths": int(g.same_paths.sum()),
            "jaccard_median": float(g.jaccard.median()), "jaccard_min": float(g.jaccard.min()),
            "merge_commit_sha_matches": int(g.sha_matches.sum()),
            "test_flag_agrees": int(g.test_flag_agrees.sum()),
            "gh_has_test": int(g.gh_test.sum())}
    (args.report_dir / "github_check_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
