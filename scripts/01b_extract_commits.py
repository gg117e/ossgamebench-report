"""Extract the per-project commit files from OSSGameBench.zip (about 81.5 GB uncompressed).

Usage:
    python -I scripts/01b_extract_commits.py <raw_dir> <manifest_csv>

Writes <raw_dir>/commits/<name>.parquet and a manifest CSV mapping each zip member to its new file.
Zip member names look like 'OSSGameBench/commits/commits|owner|repo.parquet'. Windows forbids '|',
so the file is saved as 'owner__repo.parquet' (gdevelop's split files become 'owner__repo__1.parquet').
GitHub user names cannot contain '_', so the first '__' always separates owner from repo.
zipfile verifies each member's CRC-32. Files already extracted with the right size are skipped,
so the script can be re-run after an interruption.
"""
import csv, os, shutil, sys, time, zipfile

PREFIX = "OSSGameBench/commits/commits|"


def local_name(member):
    return member[len(PREFIX):].replace("|", "__")


def main():
    raw_dir, manifest = sys.argv[1], sys.argv[2]
    out_dir = os.path.join(raw_dir, "commits")
    os.makedirs(out_dir, exist_ok=True)
    rows, t0 = [], time.time()
    with zipfile.ZipFile(os.path.join(raw_dir, "OSSGameBench.zip")) as z:
        members = [i for i in z.infolist() if i.filename.startswith(PREFIX) and i.filename.endswith(".parquet")]
        total = sum(i.file_size for i in members)
        done = 0
        for n, info in enumerate(members, 1):
            name = local_name(info.filename)
            dest = os.path.join(out_dir, name)
            if not (os.path.exists(dest) and os.path.getsize(dest) == info.file_size):
                tmp = dest + ".tmp"
                with z.open(info) as src, open(tmp, "wb") as dst:
                    shutil.copyfileobj(src, dst, 16 << 20)  # raises BadZipFile on CRC mismatch
                os.replace(tmp, dest)
            done += info.file_size
            rows.append({"zip_member": info.filename, "local_file": "commits/" + name,
                         "size": info.file_size, "crc32": f"{info.CRC:08x}"})
            if n % 50 == 0 or n == len(members):
                print(f"{n}/{len(members)} files, {done/1e9:.1f}/{total/1e9:.1f} GB, "
                      f"{time.time()-t0:.0f} s", flush=True)
    with open(manifest, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["zip_member", "local_file", "size", "crc32"])
        w.writeheader(); w.writerows(rows)
    print("manifest:", manifest)


if __name__ == "__main__":
    main()
