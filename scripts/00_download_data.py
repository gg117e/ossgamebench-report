"""Download OSSGameBench.zip and verify it against the MD5 published on Zenodo.

Usage:
    python -I scripts/00_download_data.py <raw_dir> [--source zenodo|zenodo] [--connections 4]

The archive is the same file in both places (65,816,061,871 bytes):
  - Zenodo record 17553539 (published 2025-11-10), which lists its MD5
  - the Dropbox folder given in the assignment (much faster in our tests:
    ~22 MB/s vs ~0.4 MB/s from Zenodo)
The download resumes from <raw_dir>/OSSGameBench.zip.part if interrupted.
"""
import argparse, concurrent.futures, hashlib, json, os, sys, time, urllib.request

EXPECTED_SIZE = 65_816_061_871
EXPECTED_MD5 = "40fd064b56ec327b6284039b18b19ea1"  # from Zenodo API, record 17553539
SOURCES = {
    "zenodo": "https://zenodo.org/records/17553539/files/OSSGameBench.zip?download=1",
}
CHUNK = 8 << 20
RANGE_SIZE = 64 << 20


def md5_of(path, md5):
    with open(path, "rb") as f:
        while b := f.read(CHUNK):
            md5.update(b)


def save_state(path, state):
    with open(path + ".tmp", "w", encoding="utf-8") as handle:
        json.dump(state, handle)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(path + ".tmp", path)


def parallel_download(url, part, connections):
    """Resume disjoint HTTP ranges; only fsynced ranges enter the atomic checkpoint."""
    state_path = part + ".json"
    size = os.path.getsize(part) if os.path.exists(part) else 0
    if size > EXPECTED_SIZE:
        raise ValueError("Partial file exceeds expected size")
    if os.path.exists(state_path):
        with open(state_path, encoding="utf-8") as handle:
            state = json.load(handle)
        if state["expected_size"] != EXPECTED_SIZE or state["expected_md5"] != EXPECTED_MD5:
            raise ValueError("Checkpoint belongs to another archive")
    else:
        state = {"expected_size": EXPECTED_SIZE, "expected_md5": EXPECTED_MD5,
                 "prefix_size": size, "range_size": RANGE_SIZE, "completed": []}
        # Commit the checkpoint BEFORE random writes can extend the file length.
        save_state(state_path, state)
    prefix, block_size = state["prefix_size"], state["range_size"]
    if not (0 <= prefix <= EXPECTED_SIZE and block_size > 0):
        raise ValueError("Invalid checkpoint bounds")
    ranges = [(start, min(start + block_size, EXPECTED_SIZE) - 1)
              for start in range(prefix, EXPECTED_SIZE, block_size)]
    complete = set(state["completed"])
    if any(not isinstance(i, int) or i < 0 or i >= len(ranges) for i in complete):
        raise ValueError("Invalid checkpoint range index")
    if size < prefix or any(size <= ranges[i][1] for i in complete):
        raise ValueError("Partial file is shorter than checkpoint")
    if not os.path.exists(part):
        with open(part, "xb"):
            pass

    def fetch(index):
        start, end = ranges[index]
        for attempt in range(1, 7):
            try:
                request = urllib.request.Request(url, headers={"Range": f"bytes={start}-{end}"})
                with urllib.request.urlopen(request, timeout=60) as response:
                    expected_range = f"bytes {start}-{end}/{EXPECTED_SIZE}"
                    if response.status != 206 or response.headers.get("Content-Range") != expected_range:
                        raise ValueError("Server did not honour the exact requested byte range")
                    remaining = end - start + 1
                    with open(part, "r+b", buffering=0) as out:
                        out.seek(start)
                        while remaining:
                            block = response.read(min(CHUNK, remaining))
                            if not block:
                                raise IOError("Incomplete HTTP range")
                            out.write(block)
                            remaining -= len(block)
                        out.flush()
                        os.fsync(out.fileno())
                return index
            except Exception:
                if attempt == 6:
                    raise
                time.sleep(min(attempt * 2, 10))

    done = prefix + sum(ranges[i][1] - ranges[i][0] + 1 for i in complete)
    print(f"parallel download: {connections} connections; {done:,} bytes checkpointed", flush=True)
    last = time.monotonic()
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=connections)
    futures = [pool.submit(fetch, i) for i in range(len(ranges)) if i not in complete]
    try:
        for future in concurrent.futures.as_completed(futures):
            index = future.result()
            complete.add(index)
            done += ranges[index][1] - ranges[index][0] + 1
            state["completed"] = sorted(complete)
            save_state(state_path, state)
            if time.monotonic() - last > 30 or done == EXPECTED_SIZE:
                last = time.monotonic()
                print(f"{done/1e9:7.2f} / {EXPECTED_SIZE/1e9:.2f} GB ({100*done/EXPECTED_SIZE:5.1f}%)", flush=True)
    finally:
        pool.shutdown(wait=True, cancel_futures=True)


def verify_and_finalize(part, final, digest):
    size = os.path.getsize(part)
    print(f"size {size:,} (expected {EXPECTED_SIZE:,})", flush=True)
    print(f"md5  {digest} (expected {EXPECTED_MD5})", flush=True)
    if size != EXPECTED_SIZE or digest != EXPECTED_MD5:
        sys.exit("VERIFICATION FAILED - keep the .part file and investigate")
    os.replace(part, final)
    state_path = part + ".json"
    if os.path.exists(state_path):
        os.remove(state_path)
    print("OK:", final, flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("raw_dir")
    ap.add_argument("--source", choices=SOURCES, default="zenodo")
    ap.add_argument("--connections", type=int, choices=range(1, 9), default=1)
    a = ap.parse_args()
    os.makedirs(a.raw_dir, exist_ok=True)
    final = os.path.join(a.raw_dir, "OSSGameBench.zip")
    part = final + ".part"
    if os.path.exists(final):
        digest = hashlib.md5()
        print("verifying existing archive:", final, flush=True)
        md5_of(final, digest)
        if os.path.getsize(final) != EXPECTED_SIZE or digest.hexdigest() != EXPECTED_MD5:
            sys.exit("Existing archive failed verification")
        print("OK:", final, flush=True)
        return

    if a.connections > 1:
        parallel_download(SOURCES[a.source], part, a.connections)
        print("download finished; verifying MD5 ...", flush=True)
        md5 = hashlib.md5()
        md5_of(part, md5)
        verify_and_finalize(part, final, md5.hexdigest())
        return
    if os.path.exists(part + ".json"):
        sys.exit("Parallel checkpoint found; resume with --connections 2 (or more)")

    md5 = hashlib.md5()
    done = os.path.getsize(part) if os.path.exists(part) else 0
    if done:
        print(f"resuming at {done:,} bytes; re-hashing existing part ...", flush=True)
        md5_of(part, md5)

    retries = 0
    while done < EXPECTED_SIZE:
        req = urllib.request.Request(SOURCES[a.source], headers={"Range": f"bytes={done}-"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r, open(part, "ab") as out:
                if r.status != 206:
                    sys.exit(f"server did not honour Range request (HTTP {r.status})")
                last = 0
                while b := r.read(CHUNK):
                    out.write(b); md5.update(b); done += len(b)
                    if time.time() - last > 30:
                        last = time.time()
                        print(f"{done/1e9:7.2f} / {EXPECTED_SIZE/1e9:.2f} GB "
                              f"({100*done/EXPECTED_SIZE:5.1f}%)", flush=True)
            retries = 0
        except Exception as e:  # network hiccup: resume from current offset
            retries += 1
            if retries > 20:
                raise
            print(f"error: {e!r}; retry {retries} in 10 s", flush=True)
            time.sleep(10)

    verify_and_finalize(part, final, md5.hexdigest())


if __name__ == "__main__":
    main()
