"""Check patch direction on random ordinary commits (not only PR landing commits).

Picks random small per-project commit files from the ZIP (fixed seed), then random
commits with a text patch, and compares '+'/'-' line counts with GitHub's
additions/deletions for the same file (`gh api repos/{o}/{r}/commits/{sha}`).

Usage:
    python -I scripts/13b_check_patch_direction_random.py <raw_dir> <zip_manifest> <cache_dir> <report_json>
"""
import argparse
import csv
import importlib.util
import json
from pathlib import Path
import random
import shutil
import sys
import tempfile
import zipfile

import pyarrow.parquet as pq

spec = importlib.util.spec_from_file_location("direction", Path(__file__).with_name("13_check_patch_direction.py"))
direction = importlib.util.module_from_spec(spec)
spec.loader.exec_module(direction)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("raw_dir", type=Path)
    ap.add_argument("zip_manifest", type=Path)
    ap.add_argument("cache_dir", type=Path)
    ap.add_argument("report_json", type=Path)
    ap.add_argument("--projects", type=int, default=15)
    ap.add_argument("--per-project", type=int, default=2)
    ap.add_argument("--max-bytes", type=int, default=60_000_000)
    ap.add_argument("--seed", type=int, default=20261113)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    with args.zip_manifest.open(encoding="utf-8") as handle:
        members = sorted((r for r in csv.DictReader(handle) if int(r["size"]) <= args.max_bytes),
                         key=lambda r: r["zip_member"])
    chosen = rng.sample(members, args.projects)
    args.cache_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    with zipfile.ZipFile(args.raw_dir / "OSSGameBench.zip") as archive:
        for member in chosen:
            with tempfile.TemporaryFile() as tmp:
                with archive.open(member["zip_member"]) as src:
                    shutil.copyfileobj(src, tmp, 8 << 20)
                tmp.seek(0)
                table = pq.read_table(tmp, columns=["repo", "sha", "diff"]).to_pylist()
            order = list(range(len(table)))
            rng.shuffle(order)
            taken = 0
            for i in order:
                row = table[i]
                diffs = row["diff"]
                if isinstance(diffs, str):
                    diffs = json.loads(diffs)
                text = [d for d in (diffs or []) if d.get("patch") and not d["patch"].startswith("Binary files")]
                text = [d for d in text if direction.counts(d["patch"])[0] != direction.counts(d["patch"])[1]]
                if not text:
                    continue
                d = rng.choice(text)
                repo, sha = row["repo"], row["sha"][:40]
                gh = direction.commit_files(repo, sha, args.cache_dir / f"{repo.replace('/', '__')}__{sha}.json")
                plus, minus = direction.counts(d["patch"])
                rec = dict(repo=repo, sha=sha, path=d["file"], data_plus=plus, data_minus=minus, gh_found=False)
                f = (gh or {}).get(d["file"])
                if f is not None:
                    rec.update(gh_found=True, gh_additions=f["additions"], gh_deletions=f["deletions"],
                               direction="same" if (plus, minus) == (f["additions"], f["deletions"]) else
                               "reversed" if (plus, minus) == (f["deletions"], f["additions"]) else "other")
                rows.append(rec)
                print(repo, sha[:10], d["file"][-40:], rec.get("direction"), flush=True)
                taken += 1
                if taken == args.per_project:
                    break
    summary = {}
    for r in rows:
        k = r.get("direction", "not_found_on_github")
        summary[k] = summary.get(k, 0) + 1
    args.report_json.write_text(json.dumps({"seed": args.seed, "summary": summary, "rows": rows},
                                           ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
