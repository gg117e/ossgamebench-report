"""Check linkage provenance, exclusions and denominators on synthetic relations."""
import importlib.util
from pathlib import Path
import unittest
import pandas as pd

spec = importlib.util.spec_from_file_location("cohort", Path(__file__).with_name("07_build_fix_cohort.py"))
cohort = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cohort)


def fixtures():
    issues = pd.DataFrame([dict(project="Synthetic/Game", number=n, title=f"Example {n}", body="",
                                labels=["enhancement"] if n == 7 else ["bug", "duplicate"] if n == 8 else ["bug"],
                                state="CLOSED", created_at="2024-01-01", closed_at="2024-02-01")
                           for n in range(1, 10)])
    prs = pd.DataFrame([dict(project="synthetic/game", number=n, state="CLOSED" if n == 13 else "MERGED",
                             title=f"PR {n}", body="", created_at="2024-01-02", merged_at="2024-02-01")
                        for n in range(10, 16)])
    ip = pd.DataFrame([dict(project="SYNTHETIC/GAME", issue_number=i, pr_number=p)
                       for i, p in [(1, 10), (1, 10), (1, 15), (2, 11), (3, 12), (5, 13), (6, 14), (9, 10)]])
    pc = pd.DataFrame([dict(project="synthetic/game", pr_number=p, commit_sha=s)
                       for p, s in [(10, "a" * 40), (12, "e" * 40), (14, "f" * 40), (15, "d" * 40)]])
    cm = pd.DataFrame([dict(project_key="synthetic/game", sha=s * 40, message=m, files=fs,
                            created_at="2024-01-10", source_file="synthetic__game.parquet")
                       for s, m, fs in [("a", "Direct A", ["src/a.cpp", "tests/a.cpp"]),
                                        ("b", "Empty change (#11)", []),
                                        ("c", "Unrelated change\nReferences (#12)", ["src/c.cpp"]),
                                        ("d", "Direct D", ["src/a.cpp"])]] )
    projects = pd.DataFrame([dict(project="synthetic/game", topics="game", readme_content="Synthetic game")])
    return issues, prs, ip, pc, cm, projects, set()


class CohortTests(unittest.TestCase):
    def test_denominators_missing_files_and_repeated_links(self):
        tables, metrics = cohort.build(*fixtures())
        self.assertEqual(metrics["eligible_bug_issues"], 7)
        self.assertEqual(metrics["included_issues"], 3)
        self.assertEqual(metrics["issues_with_observed_commit"], 4)
        self.assertEqual(metrics["duplicate_bug_link_rows_removed"], 1)
        self.assertEqual(metrics["test_candidate_issues"], 2)
        bugs = tables["bug_issues"].set_index("issue_number")
        self.assertEqual(bugs.loc[2, "selection_status"], "observed_commit_no_paths")
        self.assertEqual(bugs.loc[4, "selection_status"], "no_linked_pr")
        self.assertEqual(bugs.loc[5, "selection_status"], "no_merged_linked_pr")
        self.assertEqual(bugs.loc[6, "selection_status"], "no_observed_commit")
        self.assertEqual(bugs.loc[1, "n_paths"], 2)  # Same path in two commits is not counted twice.

    def test_broad_references_are_not_silently_treated_as_strict(self):
        tables, metrics = cohort.build(*fixtures())
        self.assertEqual(metrics["strict_marker_included_issues"], 2)
        row = tables["pr_commit_refs"].query("pr_number == 12 and commit_observed").iloc[0]
        self.assertEqual(row.route, "B")
        self.assertFalse(row.strict_message_marker)
        self.assertEqual(metrics["unobserved_pr_commit_refs"], 2)

    def test_shared_prs_and_multiple_prs_are_flagged(self):
        tables, metrics = cohort.build(*fixtures())
        self.assertEqual(metrics["shared_prs"], 1)
        self.assertEqual(metrics["issues_sharing_a_merged_pr"], 2)
        self.assertEqual(metrics["issues_with_multiple_merged_prs"], 1)

    def test_no_message_references_still_allows_direct_links(self):
        data = list(fixtures())
        data[4] = data[4].copy()
        data[4]["message"] = "No references"
        tables, metrics = cohort.build(*data)
        self.assertEqual(metrics["included_issues"], 2)
        self.assertEqual(set(tables["pr_commit_refs"].route), {"A"})

    def test_duplicate_commit_keys_are_rejected(self):
        data = list(fixtures())
        extra = data[4].iloc[[0]].copy()
        extra["message"] = "Conflicting metadata"
        data[4] = pd.concat([data[4], extra], ignore_index=True)
        with self.assertRaises(ValueError):
            cohort.build(*data)

    def test_identical_split_file_commits_are_deduplicated_with_sources(self):
        data = list(fixtures())
        extra = data[4].iloc[[0]].copy()
        extra["source_file"] = "synthetic__game__2.parquet"
        data[4] = pd.concat([data[4], extra], ignore_index=True)
        tables, metrics = cohort.build(*data)
        self.assertEqual(metrics["included_issues"], 3)
        self.assertEqual(metrics["duplicate_commit_rows_removed"], 1)
        row = tables["pr_commit_refs"].query("pr_number == 10").iloc[0]
        self.assertEqual(len(row.source_files), 2)


if __name__ == "__main__":
    unittest.main()
