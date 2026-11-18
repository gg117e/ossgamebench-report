"""Print the schema, row count and first rows of each extracted table, plus the commit-file listing.

Usage:
    python -I scripts/02_inspect_files.py <raw_dir> > data/inspect_output.txt
"""
import os, sys, zipfile
import pyarrow.parquet as pq
import pandas as pd

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 50)
pd.set_option("display.max_colwidth", 60)


def main():
    sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to cp932
    raw_dir = sys.argv[1]
    tdir = os.path.join(raw_dir, "tables")
    for fn in sorted(os.listdir(tdir)):
        if not fn.endswith(".parquet"):
            continue
        pf = pq.ParquetFile(os.path.join(tdir, fn))
        print("=" * 100)
        print(f"{fn}: {pf.metadata.num_rows:,} rows, {pf.metadata.num_row_groups} row groups")
        print(pf.schema_arrow)
        head = pf.read_row_group(0).slice(0, 3).to_pandas()
        for c in head.columns:  # long text columns would flood the output
            if head[c].dtype == object:
                head[c] = head[c].map(lambda v: (str(v)[:57] + "...") if len(str(v)) > 60 else v)
        print(head.to_string())

    print("=" * 100)
    zpath = os.path.join(raw_dir, "OSSGameBench.zip")
    if not os.path.exists(zpath):
        print("OSSGameBench.zip not present; skipping commit-file listing")
        return
    with zipfile.ZipFile(zpath) as z:
        commits = [i for i in z.infolist()
                   if i.filename.startswith("OSSGameBench/commits/") and i.filename.endswith(".parquet")]
    sizes = sorted(i.file_size for i in commits)
    print(f"commit files: {len(commits)}; total uncompressed {sum(sizes)/1e9:.1f} GB; "
          f"median {sizes[len(sizes)//2]/1e6:.1f} MB; largest {sizes[-1]/1e9:.2f} GB")
    for i in sorted(commits, key=lambda i: -i.file_size)[:10]:
        print(f"  {i.file_size/1e9:6.2f} GB  {i.filename}")


if __name__ == "__main__":
    main()
