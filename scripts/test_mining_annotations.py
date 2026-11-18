"""Guard evidence alignment and avoid inferring patch identity from list positions."""
import importlib.util
from pathlib import Path
import unittest


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scope = load("scope", "08_apply_project_scope.py")
patches = load("patches", "09_extract_test_cases.py")
holdout = load("holdout", "10_prepare_grouped_holdout.py")


class AnnotationTests(unittest.TestCase):
    def inputs(self):
        card = {"project_key": "synthetic/game", "readme": "A playable game.", "review_line": "A playable game."}
        decisions = {"game": [0], "engine_tool": [], "mixed": [], "evidence_overrides": {}}
        additions = {"game": [], "engine_tool": [], "mixed": [], "evidence_overrides": {}, "external_evidence": {}}
        return [card], decisions, additions

    def test_evidence_must_be_in_the_readme(self):
        cards, decisions, additions = self.inputs()
        decisions["evidence_overrides"] = {"0": "Invented claim"}
        with self.assertRaises(ValueError):
            scope.labels_for(cards, decisions, additions)

    def test_labels_are_explicitly_provisional(self):
        row = scope.labels_for(*self.inputs())[0]
        self.assertEqual(row["review_status"], "llm_provisional_not_human_validated")
        self.assertEqual(row["project_key"], "synthetic/game")

    def test_duplicate_annotations_fail(self):
        cards, decisions, additions = self.inputs()
        additions["engine_tool"] = [0]
        with self.assertRaises(ValueError):
            scope.labels_for(cards, decisions, additions)

    def test_patch_mapping_uses_file_keys_not_position(self):
        entries = [{"file": "src/game.cpp", "patch": "code"},
                   {"file": "tests/game.cpp", "patch": "test", "change_type": None}]
        result = patches.candidate_patches(entries, {"tests/game.cpp"})
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["patch"], "test")
        self.assertIsNone(result[0]["change_type"])
        self.assertEqual(result[0]["patch_completeness"], "not_verified")

    def test_unknown_patch_schema_is_not_guessed(self):
        with self.assertRaises(ValueError):
            patches.candidate_patches(["unkeyed patch"], {"tests/game.cpp"})

    def test_shared_pr_components_include_transitive_links(self):
        import pandas as pd
        keys = {("game", n) for n in range(1, 5)}
        links = pd.DataFrame([{"pk": "game", "issue_number": n, "pr_number": p}
                              for n, p in [(1, 10), (2, 10), (2, 20), (3, 20), (4, 30)]])
        group = holdout.components(keys, links)
        self.assertEqual(group[("game", 1)], group[("game", 3)])
        self.assertNotEqual(group[("game", 1)], group[("game", 4)])


if __name__ == "__main__":
    unittest.main()
