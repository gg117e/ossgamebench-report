"""Exercise ranged resume and ZIP-based metadata extraction on synthetic inputs."""
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
import zipfile

HERE = Path(__file__).resolve().parent


def load_script(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


download = load_script("download", "00_download_data.py")


class DownloadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = bytes(range(256)) * 8192
        payload = cls.payload

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                start, end = map(int, self.headers["Range"].removeprefix("bytes=").split("-"))
                body = payload[start:end + 1]
                self.send_response(206)
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Content-Range", f"bytes {start}-{end}/{len(payload)}")
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *args):
                pass

        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f"http://127.0.0.1:{cls.server.server_port}/archive"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def test_resume_prefix_and_noncontiguous_completed_ranges(self):
        with tempfile.TemporaryDirectory() as tmp, patch.multiple(
                download, EXPECTED_SIZE=len(self.payload),
                EXPECTED_MD5=hashlib.md5(self.payload).hexdigest(), RANGE_SIZE=256 * 1024):
            part = Path(tmp) / "archive.part"
            prefix = 100
            part.write_bytes(self.payload[:prefix])
            # Emulate a previous parallel process with range 2 checkpointed and holes elsewhere.
            block_size = 256 * 1024
            start = prefix + 2 * block_size
            with part.open("r+b") as handle:
                handle.seek(start)
                handle.write(self.payload[start:start + block_size])
            download.save_state(str(part) + ".json", {
                "expected_size": len(self.payload), "expected_md5": download.EXPECTED_MD5,
                "prefix_size": prefix, "range_size": block_size, "completed": [2]})
            download.parallel_download(self.url, str(part), 4)
            self.assertEqual(part.read_bytes(), self.payload)
            # Re-running a completed checkpoint does not mistake holes for a valid prefix.
            download.parallel_download(self.url, str(part), 4)
            digest = hashlib.md5(part.read_bytes()).hexdigest()
            final = Path(tmp) / "archive.zip"
            download.verify_and_finalize(str(part), str(final), digest)
            self.assertEqual(final.read_bytes(), self.payload)
            self.assertFalse(Path(str(part) + ".json").exists())

    def test_mismatched_checkpoint_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            part = Path(tmp) / "archive.part"
            part.write_bytes(b"")
            download.save_state(str(part) + ".json", {"expected_size": 1, "expected_md5": "wrong"})
            with self.assertRaises(ValueError):
                download.parallel_download(self.url, str(part), 4)

    def test_sequential_prefix_can_switch_to_parallel(self):
        with tempfile.TemporaryDirectory() as tmp, patch.multiple(
                download, EXPECTED_SIZE=len(self.payload),
                EXPECTED_MD5=hashlib.md5(self.payload).hexdigest(), RANGE_SIZE=256 * 1024):
            part = Path(tmp) / "archive.part"
            part.write_bytes(self.payload[:100])
            download.parallel_download(self.url, str(part), 4)
            self.assertEqual(part.read_bytes(), self.payload)

    def test_ignored_range_never_enters_checkpoint(self):
        with tempfile.TemporaryDirectory() as tmp, patch.multiple(
                download, EXPECTED_SIZE=100, EXPECTED_MD5="synthetic", RANGE_SIZE=100), \
                patch.object(download.urllib.request, "urlopen") as request, \
                patch.object(download.time, "sleep"):
            response = request.return_value.__enter__.return_value
            response.status = 200
            response.headers = {}
            part = Path(tmp) / "archive.part"
            with self.assertRaises(ValueError):
                download.parallel_download(self.url, str(part), 2)
            state = json.loads(Path(str(part) + ".json").read_text())
            self.assertEqual(state["completed"], [])
            self.assertEqual(part.stat().st_size, 0)

    def test_bad_digest_does_not_finalize(self):
        with tempfile.TemporaryDirectory() as tmp:
            part, final = Path(tmp) / "archive.part", Path(tmp) / "archive.zip"
            part.write_bytes(b"bad")
            with self.assertRaises(SystemExit):
                download.verify_and_finalize(str(part), str(final), "wrong")
            self.assertTrue(part.exists())
            self.assertFalse(final.exists())


class ZipCommitTests(unittest.TestCase):
    def test_zip_and_extracted_modes_produce_same_metadata(self):
        import pandas as pd
        import pyarrow.parquet as pq

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw = root / "raw"
            extracted = raw / "commits"
            extracted.mkdir(parents=True)
            with zipfile.ZipFile(raw / "OSSGameBench.zip", "w", zipfile.ZIP_DEFLATED) as archive:
                for index, files in enumerate((["src/game.cpp", "tests/game.cpp"], '["audio/sound.ogg"]')):
                    data = dict(repo=["Synthetic/Game"], sha=[str(index) * 40 + " main"],
                                contributor=["Synthetic"], contributor_email=["example@example.invalid"],
                                created_at=["2025-01-01T00:00:00+09:00"], message=["Synthetic only"],
                                files=[files], diff=[["This diff must not appear in the slim table"]])
                    buffer = io.BytesIO()
                    pd.DataFrame(data).to_parquet(buffer, index=False)
                    name = f"synthetic__game__{index}.parquet"
                    (extracted / name).write_bytes(buffer.getvalue())
                    archive.writestr(f"OSSGameBench/commits/commits|synthetic|game|{index}.parquet",
                                     buffer.getvalue())
                archive.writestr("unrelated.txt", "ignored")
            paths = []
            for mode in ("extracted", "zip"):
                target = root / mode
                command = [sys.executable, "-I", str(HERE / "02b_build_commit_table.py"), str(raw), str(target)]
                if mode == "zip":
                    command.append("--from-zip")
                result = subprocess.run(command, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                paths.append(target / "commits_slim.parquet")
            left, right = (pq.read_table(path) for path in paths)
            self.assertTrue(left.equals(right))
            self.assertNotIn("diff", right.column_names)
            self.assertEqual(right.column("n_files").to_pylist(), [2, 1])
            self.assertEqual(right.column("sha_ref").to_pylist(), ["main", "main"])


if __name__ == "__main__":
    unittest.main()
