"""Write the LLM content analysis of the 30 final-diff PR cases (09 --final-dir output).

The labels below were assigned by Claude (model claude-opus-5-5, 2026-11-13) after
reading the PR title/body, the linked issue title/body and the test-candidate
patches of the landing commit, inverted to the usual parent->child direction
(the dataset stores patches child->parent; see results/test_cases_final_v1).
They are not human-validated.

Usage:
    python -I scripts/14_write_case_annotations.py <cases_jsonl> <out_jsonl> <summary_json>
"""
import argparse
from collections import Counter
import json
from pathlib import Path

# case: (symptom, contexts, relation, test_roles, change_kind, input_state, actions, oracle,
#        report_material_to_test, confidence, rationale)
A = {
    1: ("gameplay", [], "related_area", ["fixture"], "added", "Recorded full 18SJ game (JSON action log, v0.92)",
        "Replay all actions with strict validation", "Replay completes; validation passes (implicit: no exception)",
        "none_observed", "medium",
        "Fix found while replaying fixtures strictly; the new game record may cover the KHJ merger but the PR does not say so."),
    2: ("ui", [], "direct_regression", ["executable_test"], "added",
        "Spectator view; game fixture with chosen hands/points loaded via cy.loadGameFixture",
        "Opponent plays one-offs; cannot-counter dialog appears; opponent resolves",
        "DOM: dialog visible, then .v-overlay must not exist", "screenshot_in_issue_not_used_as_oracle", "high",
        "E2E test reproduces the leftover-scrim scenario; the oracle is DOM state, not the screenshot."),
    3: ("ui", [], "direct_regression", ["executable_test"], "added",
        "Board FEN positions (incl. crazyhouse pocket) and legal destinations",
        "Type move strings in mixed case (e.g. Q@C3, C8=N)", "inputToMove returns the expected move/drop object",
        "code_link_in_issue", "high", "Unit test enumerates the case variants named in the issue."),
    4: ("gameplay", [], "related_area", ["executable_test"], "modified", "RNA sequences and structures",
        "Score structures with ContraFold/EternaFold",
        "Expected free energies updated; FE == sum(NNFE) consistency check disabled", "none_observed", "medium",
        "Expected values changed with the rounding fix; an added UndoBlock test file concerns other features."),
    5: ("gameplay", [], "direct_regression", ["executable_test"], "added",
        "Battlefield with Whipgrass Entangler, lands, other Clerics",
        "Activate ability (once/twice), attack, choose to pay", "Opponent life total and number of tapped lands",
        "none_observed", "high", "Card-scenario tests cover paying the cost once and repeated activations."),
    6: ("multiple", ["ui", "visual"], "adapt_existing", ["executable_test"], "modified",
        "All vending inventory prototypes", "Resolve each listed item prototype",
        "Unknown prototype raises (message text changed only)", "none_observed", "high",
        "Only an error message field changed; none of the three linked symptoms is tested."),
    7: ("tooling_other", [], "direct_regression", ["executable_test"], "added",
        "Test classes with PER_CLASS/PER_METHOD lifecycles and @In injection", "Run JUnit lifecycle hooks and tests",
        "Injected engine/context identical across hooks (one engine set)", "none_observed", "high",
        "Bug is in the project's own test environment (MTE); tests check engine reuse directly."),
    8: ("gameplay", [], "unrelated_new_test", ["executable_test"], "added",
        "Player lists with factions and connection flags", "Call getFactionsOf", "Deduplicated faction list",
        "none_observed", "high",
        "New unit test for a helper used in the refactor; mana renewal on new waves is not tested."),
    9: ("gameplay", ["ui"], "related_area", ["fixture", "executable_test"], "modified",
        "Recorded 1817 game 15528 (in progress)", "Replay fixture", "Final player values (game_spec) updated",
        "game_url_in_issue_is_other_game", "low",
        "Fixture re-exported and expected scores changed; unclear whether the bankruptcy case occurs in it."),
    10: ("gameplay", [], "related_area", ["executable_test", "infrastructure"], "added",
         "Custom cards with {X} costs and cost adjusters", "Announce X values in strict test mode",
         "X within min/max; test framework asserts X limits", "game_log_in_issue", "medium",
         "General X-limit tests and test-player checks; the reported card itself is not tested."),
    11: ("gameplay", [], "direct_regression", ["executable_test"], "added",
         "Creatures put into graveyards from battlefield, hand, library, exile",
         "Cast Myojin, move creatures, remove counter", "Each returned creature is on the battlefield (permanent counts)",
         "none_observed", "high", "Test covers the non-battlefield zones named in the issue."),
    12: ("crash_hang", [], "direct_regression", ["executable_test"], "modified",
         "Point sets incl. duplicate/near-duplicate coordinates", "Compute parameterized index for route drawing",
         "Index has one value per point and is strictly increasing", "stack_trace_locates_function", "high",
         "Regression test cites the issue; the stack trace named the failing method."),
    13: ("ui", [], "direct_regression", ["executable_test"], "added",
         "DB with 3 users and generated ranked matches per month", "Request monthly ranking",
         "Ranking entries and values equal expected", "screenshot_in_issue_not_used", "medium",
         "Tests the ranking that replaced placeholder data; the symptom was a wrong scoreboard."),
    14: ("crash_hang", [], "direct_regression", ["fixture", "executable_test"], "added",
         "Recorded 18MEX game 17849 (the game linked in the issue)",
         "Replay all actions including bankruptcy; render endgame page",
         "Replay completes; final player values; page title shows Game Over - Bankruptcy",
         "game_record_from_issue_url", "high", "The game named in the bug report became the regression fixture."),
    15: ("gameplay", [], "direct_regression", ["executable_test"], "added",
         "Server map with a human buckled to a chair, items in hands", "Apply lethal damage",
         "Items are dropped (hands empty)", "none_observed_empty_body", "high",
         "Integration test reproduces the PR-title scenario; the issue body is empty."),
    16: ("gameplay", [], "direct_regression", ["executable_test"], "added",
         "Players in lobby with antag preference on/off", "Run antag selection for Traitor/NukeOps rules",
         "Only opted-in, eligible players are selected", "none_observed", "high",
         "New test for lobby eligibility; the NukeOps test now opts in explicitly."),
    17: ("multiple", ["ui", "tooling"], "adapt_existing", ["executable_test"], "modified",
         "Random-map template and options", "Generate random map", "(unchanged) map generation succeeds",
         "none_observed", "high", "Test updated to a renamed API; the team bugs are not tested."),
    18: ("gameplay", [], "direct_regression", ["executable_test"], "added",
         "Multistrand sequences (oligo with '&' cut point)", "Multifold and score structures; build layout score tree",
         "Expected structure string, energies and per-node scores", "puzzle_link_in_issue", "medium",
         "Tests cover energy placement with cut points described in the PR."),
    19: ("save_load", [], "adapt_existing", ["executable_test"], "modified", "Store with answers",
         "Start game, set guesses", "correctGuesses equals empty Set", "none_observed", "high",
         "Tests adapted from array to Set; multi-tab storage behaviour is not tested."),
    20: ("crash_hang", ["tooling"], "direct_regression", ["executable_test"], "modified",
         "Two YAML trees with additions and removals (-Key)", "Merge YAML",
         "Merged tree contains/omits the expected keys", "yaml_snippet_in_issue", "medium",
         "Rewritten merge tests cover the removal semantics behind the crashes."),
    21: ("tooling_other", [], "test_suite_bug", ["infrastructure", "executable_test"], "modified", "E2E specs",
         "Refresh opponent socket before suites", "(test setup no longer fails)", "none_observed", "high",
         "The bug was flaky CI tests; the change is test setup."),
    22: ("unknown", [], "adapt_existing", ["infrastructure"], "modified", "Generated vanilla card file may be absent",
         "Skip deckcode tests if the file is missing", "n/a", "none_observed_empty_body", "high",
         "Only adds a skip condition; the reported deck-creator behaviour is not tested."),
    23: ("gameplay", [], "direct_regression", ["executable_test"], "added",
         "Field row [null, carrotPlot, null] (target not first in row)", "findInField with predicate",
         "Returns the plot / null when absent", "none_observed", "high",
         "Input encodes the exact condition from the PR (scarecrow not first in its row)."),
    24: ("crash_hang", ["save_load"], "adapt_existing", ["infrastructure"], "modified", "Mock spell interface",
         "n/a", "n/a", "none_observed", "high", "Mock gains a method for an API change; the crash is not tested."),
    25: ("crash_hang", ["save_load"], "direct_regression", ["executable_test"], "modified",
         "Legacy saved game configs (single and multiplayer) with enum fields as raw values", "migrate_game_config",
         "Fields are proper enum members (assertIs)", "cause_described_in_issue", "high",
         "Save-migration test strengthened for the loaded single-player config."),
    26: ("gameplay", [], "adapt_existing", ["infrastructure"], "modified", "Mock callback", "n/a", "n/a",
         "none_observed", "high", "Mock signature follows an API change; movement points not tested."),
    27: ("visual", [], "adapt_existing", ["fixture"], "modified", "Minimal test data gemrb.ini", "n/a", "n/a",
         "screenshots_in_issue_not_used", "high", "Adds the new flag to test config only; highlighting not tested."),
    28: ("ui", [], "adapt_existing", ["executable_test"], "modified", "Replay/game summary data",
         "Build summary; call socket handlers", "Updated data shapes and handler names", "none_observed", "high",
         "Tests follow a refactor; the issue is a feature checklist (is_actual_bug doubtful)."),
    29: ("ui", [], "adapt_existing", ["executable_test"], "modified", "Keyboard move controller mocks",
         "Type 'clock'", "speakClock called once", "none_observed", "high",
         "Test adapted to an API change; the blindfold preview bug is not tested."),
    30: ("gameplay", [], "adapt_existing", ["executable_test"], "modified", "Mocked game properties for battle steps",
         "Compute battle steps", "(unchanged) step lists; new option stubbed false", "none_observed", "medium",
         "Added lines only stub the new option in existing tests; no test with the option enabled."),
}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("cases_jsonl", type=Path)
    ap.add_argument("out_jsonl", type=Path)
    ap.add_argument("summary_json", type=Path)
    args = ap.parse_args()
    cases = [json.loads(l) for l in args.cases_jsonl.read_text(encoding="utf-8").splitlines()]
    if len(cases) != len(A):
        raise ValueError("Annotations do not match the case file")
    rows = []
    for i, c in enumerate(cases, 1):
        s, ctx, rel, roles, kind, inp, act, orc, mat, conf, rat = A[i]
        rows.append(dict(case=i, project_key=c["project_key"], pr_number=c["pr_number"], pr_url=c["pr_url"],
                         issue_numbers=c["issue_numbers"], test_paths=[x["path"] for x in c["test_candidate_changes"]],
                         primary_category=s, secondary_contexts=ctx, relation_to_bug=rel, test_roles=roles,
                         change_kind=kind, input_state=inp, actions=act, oracle=orc,
                         report_material_to_test=mat, confidence=conf, rationale=rat,
                         annotator="Claude", model_id="claude-opus-5-5", date_jst="2026-11-13",
                         status="llm_annotation_not_human_validated"))
    args.out_jsonl.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    direct = [r for r in rows if r["relation_to_bug"] == "direct_regression"]
    summary = {"cases": len(rows), "projects": len({r["project_key"] for r in rows}),
               "relation_to_bug": Counter(r["relation_to_bug"] for r in rows),
               "primary_category_all": Counter(r["primary_category"] for r in rows),
               "primary_category_direct": Counter(r["primary_category"] for r in direct),
               "change_kind_direct": Counter(r["change_kind"] for r in direct),
               "fixture_role_any": sum("fixture" in r["test_roles"] for r in rows),
               "report_material_to_test": Counter(r["report_material_to_test"] for r in rows),
               "note": "Diversity sample (project cap 3), not a prevalence estimate. LLM labels, not human-validated."}
    args.summary_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
