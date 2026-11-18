"""Synthetic checks for 11_final_pr_diff.py (landing-commit selection and issue status)."""
import importlib.util
from pathlib import Path
import unittest

import pandas as pd

spec = importlib.util.spec_from_file_location("final_diff", Path(__file__).with_name("11_final_pr_diff.py"))
fd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fd)
PK = "synthetic/game"


def ref(pr, sha, message, via_pr_commit, via_message):
    return dict(pk=PK, pr_number=pr, sha=sha * 40, message=message, via_pr_commit=via_pr_commit,
                via_message=via_message, commit_observed=True)


def fixtures():
    refs = pd.DataFrame([
        # PR 10: own commit + in-branch merge carrying tests + GitHub merge commit (final diff, no test)
        ref(10, "a", "Fix z-index", True, False),
        ref(10, "b", "Merge branch 'master' into fix", True, False),
        ref(10, "c", "Merge pull request #10 from someone/fix\n\nFix z-index", False, True),
        # PR 11: squash commit with a test
        ref(11, "d", "Fix save crash (#11)", False, True),
        # PR 12: two landing candidates with different paths -> ambiguous
        ref(12, "e", "Fix A (#12)", False, True),
        ref(12, "f", "Merge pull request #12 from x/y", False, True),
        # PR 13: no landing commit; revert mentioning the PR is not a landing commit
        ref(13, "g", "Work in progress", True, False),
        ref(13, "h", "Revert \"Fix B (#13)\"", False, True),
        # PR 14: cherry-pick with identical paths -> equivalent
        ref(14, "i", "Fix C (#14)", False, True),
        ref(14, "j", "Fix C (#14)", False, True),
    ])
    paths = {"a": ["src/ui.cpp"], "b": ["src/net.cpp", "tests/net_test.cpp"], "c": ["src/ui.cpp"],
             "d": ["src/save.cpp", "tests/save_test.cpp"], "e": ["src/a.cpp"], "f": ["src/a.cpp", "src/b.cpp"],
             "g": ["src/b.cpp", "tests/b_test.cpp"], "h": ["src/b.cpp"], "i": ["src/c.cpp"], "j": ["src/c.cpp"]}
    cpaths = pd.DataFrame([dict(pk=PK, sha=s * 40, path=p) for s, ps in paths.items() for p in ps])
    bip = pd.DataFrame([dict(pk=PK, issue_number=i, pr_number=p, merged=True)
                        for i, p in [(1, 10), (2, 11), (3, 12), (4, 13), (5, 14), (6, 10), (6, 13)]])
    scoped = pd.DataFrame([dict(pk=PK, issue_number=i, scope="game", test_candidate_change=t, n_paths=1, n_merged_prs=1)
                           for i, t in [(1, True), (2, True), (3, False), (4, True), (5, False), (6, True)]])
    return refs, cpaths, bip, scoped


class FinalDiffTests(unittest.TestCase):
    def setUp(self):
        self.pr, self.issue = fd.build(*fixtures())
        self.pr = self.pr.set_index("pr_number")
        self.issue = self.issue.set_index("issue_number")

    def test_in_branch_merge_is_excluded_from_final_diff(self):
        row = self.pr.loc[10]
        self.assertEqual(row.pr_status, "landing_unique")
        self.assertEqual(row.landing_kind, "gh_merge")
        self.assertFalse(row.test_final)
        self.assertTrue(row.test_union)
        self.assertFalse(row.test_fallback)

    def test_squash_ambiguous_equivalent_and_revert(self):
        self.assertTrue(self.pr.loc[11].test_final)
        self.assertEqual(self.pr.loc[12].pr_status, "landing_ambiguous")
        self.assertEqual(self.pr.loc[13].pr_status, "no_landing")
        self.assertTrue(self.pr.loc[13].test_fallback)
        self.assertEqual(self.pr.loc[14].pr_status, "landing_equivalent")

    def test_issue_status_requires_every_merged_pr(self):
        self.assertEqual(self.issue.loc[1].final_status, "all_landing")
        self.assertFalse(self.issue.loc[1].test_final)
        self.assertEqual(self.issue.loc[3].final_status, "none")
        self.assertEqual(self.issue.loc[6].final_status, "partial")
        self.assertTrue(pd.isna(self.issue.loc[6].test_final))
        m = fd.metrics(*fd.build(*fixtures()))
        self.assertEqual(m["by_scope"]["game"]["v1_true_final_false"], 1)


if __name__ == "__main__":
    unittest.main()
