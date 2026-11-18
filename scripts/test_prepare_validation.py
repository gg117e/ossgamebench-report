"""Check sample isolation, determinism and input safeguards using synthetic data."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("prepare_validation", HERE / "05_prepare_validation.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SamplingTests(unittest.TestCase):
    def setUp(self):
        self.rows = [{"project_key": "synthetic/game", "issue_number": i,
                      "sample_id": f"synthetic/game#{i}", "title": "Synthetic", "body": ""}
                     for i in range(240)]

    def test_order_invariant_and_blind_sample_is_held_out(self):
        rows, human = module.select_samples(self.rows, 20261112, 200, 100, 50)
        reverse, _ = module.select_samples(list(reversed(self.rows)), 20261112, 200, 100, 50)
        self.assertEqual(rows, reverse)
        dev = {r["sample_id"] for r in rows if r["split"] == "development"}
        audit = {r["sample_id"] for r in rows if r["split"] == "audit"}
        human_ids = {r["sample_id"] for r in human}
        self.assertEqual((len(dev), len(audit), len(human_ids)), (100, 100, 50))
        self.assertFalse(dev & audit)
        self.assertTrue(human_ids <= audit)

    def test_duplicate_keys_are_rejected(self):
        with self.assertRaises(ValueError):
            module.select_samples(self.rows + [self.rows[0]], 1, 200, 100, 50)

    def test_seen_cases_are_fixed_in_development_not_audit(self):
        seen = {r["sample_id"] for r in self.rows[:30]}
        sample, human = module.select_samples(self.rows, 20261112, 200, 100, 50, seen)
        dev = {r["sample_id"] for r in sample if r["split"] == "development"}
        audit = {r["sample_id"] for r in sample if r["split"] == "audit"}
        self.assertTrue(seen <= dev)
        self.assertFalse(seen & audit)
        self.assertFalse(seen & {r["sample_id"] for r in human})

    def test_seen_cases_cannot_overflow_development(self):
        with self.assertRaises(ValueError):
            module.select_samples(self.rows, 1, 200, 100, 50, {r["sample_id"] for r in self.rows[:101]})

    def test_invalid_sizes_are_rejected(self):
        for sizes in [(250, 100, 50), (200, 200, 50), (200, 100, 101)]:
            with self.subTest(sizes=sizes), self.assertRaises(ValueError):
                module.select_samples(self.rows, 1, *sizes)

    def test_cli_filters_input_and_protects_output(self):
        import pandas as pd

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tables = root / "raw" / "tables"
            tables.mkdir(parents=True)
            records = [dict(project="Synthetic/Game", number=i, title="Synthetic example",
                            body=None if i == 0 else "Example only", labels=["bug"])
                       for i in range(240)]
            records += [dict(project="Synthetic/Game", number=1000, title="Duplicate report",
                             body="", labels=["bug", "duplicate"]),
                        dict(project="Synthetic/Game", number=1001, title="Feature request",
                             body="", labels=["enhancement"]),
                        dict(project=sorted(module.duplicated_projects())[0], number=1,
                             title="Excluded project", body="", labels=["bug"])]
            pd.DataFrame(records).to_parquet(tables / "issue.parquet", index=False)
            target = root / "samples"
            command = [sys.executable, "-I", str(HERE / "05_prepare_validation.py"),
                       str(root / "raw"), str(target), "--expected-bugs", "240"]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            manifest = json.loads((target / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["population"], 240)
            self.assertEqual(len(manifest["source_sha256"]), 64)
            blind_file = target / "human_blind.jsonl"
            original = blind_file.read_bytes()
            human = [json.loads(line) for line in original.decode("utf-8").splitlines()]
            self.assertEqual(len(human), 50)
            for row in human:
                self.assertNotIn("split", row)
                self.assertNotIn("labels", row)
                self.assertEqual(row["primary_category"], "")
                self.assertEqual(row["status"], "unlabelled")
            repeated = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(repeated.returncode, 0)
            self.assertEqual(blind_file.read_bytes(), original)

    def test_missing_input_fails_without_creating_samples(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "samples"
            result = subprocess.run([sys.executable, "-I", str(HERE / "05_prepare_validation.py"),
                                     str(Path(tmp) / "missing"), str(target)], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
