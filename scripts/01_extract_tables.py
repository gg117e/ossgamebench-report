"""Extract the relational tables (everything except commits/) from OSSGameBench.zip.

Usage:
    python -I scripts/01_extract_tables.py <raw_dir>

Reads <raw_dir>/OSSGameBench.zip and writes <raw_dir>/tables/*.parquet.
zipfile verifies each member's CRC-32 while reading, so a corrupted member raises an error.
The per-project commit files (commits/, ~81 GB uncompressed) are NOT extracted here; they are
processed one at a time by a later script because they do not fit on disk alongside the zip.
Note: commit file names contain '|', which Windows forbids; later scripts read them from the zip.
"""
import os, shutil, sys, zipfile


def main():
    raw_dir = sys.argv[1]
    zpath = os.path.join(raw_dir, "OSSGameBench.zip")
    out_dir = os.path.join(raw_dir, "tables")
    os.makedirs(out_dir, exist_ok=True)
    with zipfile.ZipFile(zpath) as z:
        for info in z.infolist():
            name = info.filename
            parts = name.split("/")
            # top-level tables only: OSSGameBench/<table>.parquet
            if len(parts) != 2 or parts[0] != "OSSGameBench" or not name.endswith(".parquet"):
                continue
            dest = os.path.join(out_dir, parts[1])
            with z.open(info) as src, open(dest, "wb") as dst:
                shutil.copyfileobj(src, dst, 8 << 20)  # CRC checked at end of stream
            print(f"{parts[1]:28s} {info.file_size:>13,} bytes  crc32={info.CRC:08x}")


if __name__ == "__main__":
    main()
