"""Check the direction of the dataset's per-file patches against GitHub.

For every extracted test-candidate patch (09 output), count '+' and '-' lines in
the dataset patch and compare them with GitHub's `additions`/`deletions` and
`status` for the same file in the same commit (`gh api repos/{o}/{r}/commits/{sha}`).
Read-only; only repository names and commit SHAs are sent.

Usage:
    python -I scripts/13_check_patch_direction.py <cases_jsonl> <cache_dir> <report_json>
"""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys


def counts(patch):
    plus = minus = 0
    for line in (patch or "").splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            plus += 1
        elif line.startswith("-") and not line.startswith("---"):
            minus += 1
    return plus, minus


def commit_files(repo, sha, cache):
    if not cache.exists():
        out = subprocess.run(["gh", "api", "--paginate", "--slurp", f"repos/{repo}/commits/{sha}"],
                             capture_output=True, text=True, encoding="utf-8")
        body = json.loads(out.stdout) if out.returncode == 0 else None
        cache.write_text(json.dumps({"ok": out.returncode == 0, "body": body}), encoding="utf-8")
    data = json.loads(cache.read_text(encoding="utf-8"))
    if not data["ok"]:
        return None
    return {f["filename"]: f for page in data["body"] for f in page.get("files", [])}


HUNK = re.compile(r"^@@ -(\d+(?:,\d+)?) \+(\d+(?:,\d+)?) @@")


def invert_patch(patch):
    """Turn a dataset patch (child -> parent) into the usual parent -> child direction."""
    out = []
    for line in (patch or "").splitlines():
        m = HUNK.match(line)
        if m:
            out.append(f"@@ -{m.group(2)} +{m.group(1)} @@" + line[m.end():])
        elif line.startswith("+"):
            out.append("-" + line[1:])
        elif line.startswith("-"):
            out.append("+" + line[1:])
        else:
            out.append(line)
    return "\n".join(out)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("cases_jsonl", type=Path)
    ap.add_argument("cache_dir", type=Path)
    ap.add_argument("report_json", type=Path)
    args = ap.parse_args()
    args.cache_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for line in args.cases_jsonl.read_text(encoding="utf-8").splitlines():
        case = json.loads(line)
        for ch in case["test_candidate_changes"]:
            sha = ch["commit_sha"]
            gh = commit_files(case["project_key"], sha, args.cache_dir / f"{case['project_key'].replace('/', '__')}__{sha}.json")
            plus, minus = counts(ch["patch"])
            row = dict(project_key=case["project_key"], pr_number=case["pr_number"], sha=sha, path=ch["path"],
                       data_plus=plus, data_minus=minus, gh_found=False)
            f = (gh or {}).get(ch["path"])
            if f is not None:
                row.update(gh_found=True, gh_status=f["status"], gh_additions=f["additions"], gh_deletions=f["deletions"])
                same = (plus, minus) == (f["additions"], f["deletions"])
                swapped = (plus, minus) == (f["deletions"], f["additions"])
                row["direction"] = ("symmetric" if same and swapped else "same" if same else
                                    "reversed" if swapped else "other")
            rows.append(row)
            print(row["project_key"], row["pr_number"], row["path"][-50:], row.get("gh_status"), row.get("direction"), flush=True)
    summary = {}
    for r in rows:
        summary[r.get("direction", "not_found_on_github")] = summary.get(r.get("direction", "not_found_on_github"), 0) + 1
    args.report_json.parent.mkdir(parents=True, exist_ok=True)
    args.report_json.write_text(json.dumps({"summary": summary, "rows": rows}, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8")
    print(json.dumps(summary))


if __name__ == "__main__":
    main()

