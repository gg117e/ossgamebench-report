"""Build one slim commit table (no diffs) from per-project commit files or the ZIP.

Usage:
    python -I scripts/02b_build_commit_table.py <raw_dir> <interim_dir>
    python -I scripts/02b_build_commit_table.py <raw_dir> <interim_dir> --from-zip

The ZIP mode decompresses one member to a temporary file at a time, verifies its
CRC, reads only metadata columns, and discards the temporary member. The original
ZIP retains all diffs without requiring a second full copy of the commit data.

Reads <raw_dir>/commits/*.parquet (columns other than `diff`) and writes
<interim_dir>/commits_slim.parquet with:
    project_key   lower-cased owner/repo (tables differ in letter case, so joins use this)
    repo          owner/repo as stored in the commit file
    sha           first 40 characters of the stored sha
    sha_ref       the rest of the stored sha (e.g. 'remotes/origin/HEAD~3', added by the collector)
    contributor, contributor_email   git author name/e-mail (not GitHub logins)
    created_at    commit time converted to UTC
    message       commit message
    files         list of changed paths (36 files store this as a JSON string; normalised here)
    n_files       number of changed paths
Also prints per-file row counts so that incomplete projects can be spotted.
"""
import argparse, json, os, shutil, sys, tempfile, zipfile
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

COLS = ["repo", "sha", "contributor", "contributor_email", "created_at", "message", "files"]
SCHEMA = pa.schema([
    ("project_key", pa.string()), ("repo", pa.string()), ("sha", pa.string()), ("sha_ref", pa.string()),
    ("contributor", pa.string()), ("contributor_email", pa.string()),
    ("created_at", pa.timestamp("s", tz="UTC")), ("message", pa.string()),
    ("files", pa.list_(pa.string())), ("n_files", pa.int32()), ("source_file", pa.string()),
])


def normalize_files(x):
    """Same rule as the dataset's online appendix: JSON string -> list; non-JSON string -> [x]."""
    if x is None:
        return []
    if isinstance(x, str):
        try:
            v = json.loads(x)
            return [str(p) for p in v] if isinstance(v, list) else [x]
        except json.JSONDecodeError:
            return [x]
    return [str(p) for p in x]


def commit_sources(raw_dir, interim_dir, from_zip):
    if from_zip:
        prefix = "OSSGameBench/commits/commits|"
        with zipfile.ZipFile(os.path.join(raw_dir, "OSSGameBench.zip")) as archive:
            members = sorted((i for i in archive.infolist()
                              if i.filename.startswith(prefix) and i.filename.endswith(".parquet")),
                             key=lambda i: i.filename)
            if not members:
                raise ValueError("No commit parquet members in archive")
            for info in members:
                fn = info.filename[len(prefix):].replace("|", "__")
                with tempfile.TemporaryFile(dir=interim_dir) as extracted:
                    with archive.open(info) as source:
                        shutil.copyfileobj(source, extracted, 8 << 20)
                    extracted.seek(0)
                    yield fn, pq.read_table(extracted, columns=COLS).to_pandas()
    else:
        src = os.path.join(raw_dir, "commits")
        files = sorted(fn for fn in os.listdir(src) if fn.endswith(".parquet"))
        if not files:
            raise ValueError("No extracted commit parquet files")
        for fn in files:
            yield fn, pq.read_table(os.path.join(src, fn), columns=COLS).to_pandas()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw_dir")
    parser.add_argument("interim_dir")
    parser.add_argument("--from-zip", action="store_true")
    args = parser.parse_args()
    raw_dir, interim_dir = args.raw_dir, args.interim_dir
    os.makedirs(interim_dir, exist_ok=True)
    out = os.path.join(interim_dir, "commits_slim.parquet")
    stats = []
    with pq.ParquetWriter(out + ".tmp", SCHEMA, compression="zstd") as writer:
        for fn, df in commit_sources(raw_dir, interim_dir, args.from_zip):
            sha = df["sha"].fillna("")
            df["sha_ref"] = sha.str[40:].str.strip()
            df["sha"] = sha.str[:40]
            df["created_at"] = pd.to_datetime(df["created_at"], utc=True, errors="coerce", format="ISO8601")
            df["files"] = df["files"].map(normalize_files)
            df["n_files"] = df["files"].map(len).astype("int32")
            df["project_key"] = df["repo"].str.lower()
            df["source_file"] = fn
            writer.write_table(pa.Table.from_pandas(df[SCHEMA.names], schema=SCHEMA, preserve_index=False))
            stats.append({"source_file": fn, "rows": len(df), "repos": df["repo"].nunique(),
                          "bad_sha": int((~df["sha"].str.fullmatch(r"[0-9a-f]{40}")).sum()),
                          "bad_date": int(df["created_at"].isna().sum()),
                          "dup_sha": int(df["sha"].duplicated().sum())})
            if len(stats) % 25 == 0:
                print(f"processed {len(stats)} commit files", flush=True)
    os.replace(out + ".tmp", out)
    s = pd.DataFrame(stats)
    s.to_csv(os.path.join(interim_dir, "commits_slim_filestats.csv"), index=False)
    print(f"files {len(s)}, rows {s.rows.sum():,}, files with >1 repo value {int((s.repos > 1).sum())}")
    print(f"bad sha {s.bad_sha.sum():,}, unparsable dates {s.bad_date.sum():,}, duplicate sha within file {s.dup_sha.sum():,}")
    print("written:", out)


if __name__ == "__main__":
    main()
