# Reproduction Instructions

These steps reproduce every number, table and figure in the report (`report/report.tex`).

## Environment

- Python 3.13 or 3.14; install dependencies with `pip install -r requirements.txt` (pandas, pyarrow, statsmodels, matplotlib, pypdf, …).
- About 70 GB of free disk space (ZIP 62 GB + derived tables), or 150 GB if all commit files are extracted.
- Run every script from the repository root with `python -I`. Keep the data directory outside the repository and outside synced folders.
- Optional: the GitHub CLI `gh` (authenticated) for the two checks against GitHub (steps 6 and 9). Their responses are not required for the main analysis.

Below, `RAW` is the raw-data directory and `INT` the directory for derived tables, for example

```
RAW=C:/Users/<user>/ossgamebench-data/raw
INT=C:/Users/<user>/ossgamebench-data/interim
```

## Steps

| # | Command | Purpose | Main output |
|---|---|---|---|
| 1 | `python -I scripts/00_download_data.py $RAW --source zenodo` | Download `OSSGameBench.zip`; verifies size and MD5 `40fd064b56ec327b6284039b18b19ea1` | `$RAW/OSSGameBench.zip` |
| 2 | `python -I scripts/01_extract_tables.py $RAW` | Extract the eight relational tables | `$RAW/tables/` |
| 3 | `python -I scripts/02b_build_commit_table.py $RAW $INT --from-zip` | Commit table without patches (reads the ZIP member by member) | `$INT/commits_slim.parquet` |
| 4 | `python -I scripts/07_build_fix_cohort.py $RAW $INT $INT/cohort_v1 <new_report_dir>` | Bug issues, issue–PR–commit–path links (Table 1, steps 2–3) | `$INT/cohort_v1/`, `project_scope_cards.jsonl` |
| 5 | `python -I scripts/08_prepare_scope_cards.py <new_report_dir>/project_scope_cards.jsonl results/cohort_v1/scope_review_cards.jsonl` then `python -I scripts/08_apply_project_scope.py $INT/cohort_v1 results/cohort_v1/scope_review_cards.jsonl validation/project_scope_v1 $INT/game_scope_v1` | Apply the stored game/tool labels (Table 1, step 4) | `$INT/game_scope_v1/` |
| 6 | `python -I scripts/11_final_pr_diff.py $INT/cohort_v1 $INT/game_scope_v1/scoped_cohort_index.parquet $INT/final_diff_v1 results/final_diff_v1` | Landing commit per pull request; outcome measure (Sections 3.2–3.3, Table 1 step 5) | `$INT/final_diff_v1/`, `results/final_diff_v1/summary.json` |
| 6b | `python -I scripts/12_check_final_diff_github.py $INT/final_diff_v1 $INT/game_scope_v1/scoped_cohort_index.parquet $INT/final_diff_v1/github_cache results/final_diff_v1` | Optional (network): compare 74 landing diffs with GitHub | `results/final_diff_v1/github_check_*.json` |
| 7 | `python -I scripts/17_rq_analysis.py $INT results/rq_analysis_v1` | Symptoms, shares, bootstrap intervals, sensitivity (Table 6; sensitivity in Section 5.2) | `results/rq_analysis_v1/`, `$INT/final_diff_v1/analysis_table.parquet` |
| 8 | `python -I scripts/18_figures.py results/rq_analysis_v1` | Supplementary figures (not used in the report) | `results/rq_analysis_v1/fig_*.png` |
| 9 | `python -I scripts/09_extract_test_cases.py $RAW $INT/cohort_v1 $INT/game_scope_v1/game_cohort.parquet validation/samples_game_v2/issues_llm.jsonl data/commit_files_manifest.csv $INT/test_cases_final_v1 --final-dir $INT/final_diff_v1` | Select 30 pull requests and extract their test patches (RQ3) | `$INT/test_cases_final_v1/cases.jsonl` |
| 9b | `python -I scripts/13_check_patch_direction.py $INT/test_cases_final_v1/cases.jsonl <cache_dir> results/test_cases_final_v1/patch_direction.json` and `python -I scripts/13b_check_patch_direction_random.py $RAW data/commit_files_manifest.csv <cache_dir> results/test_cases_final_v1/patch_direction_random.json` | Optional (network): patch direction against GitHub (Section 3.2) | `results/test_cases_final_v1/patch_direction*.json` |
| 10 | `python -I scripts/14_write_case_annotations.py $INT/test_cases_final_v1/cases.jsonl validation/test_cases_final_v1/annotations.jsonl results/test_cases_final_v1/case_summary.json` | Stored content-analysis labels (Tables 10–11) | `validation/test_cases_final_v1/annotations.jsonl` |
| 11 | `python -I scripts/19_game_type_labels.py validation/game_type_v1/labels.csv` | Stored game-type labels (Section 3.5) | `validation/game_type_v1/labels.csv` |
| 12 | `python -I scripts/20_game_type_analysis.py $INT validation/game_type_v1/labels.csv results/game_type_v1` and `python -I scripts/21_game_type_figure.py results/game_type_v1` | RQ2 rates (Table 8, Figure 1). The output directory must not exist | `results/game_type_v1/` |
| 13 | `python -I scripts/22_bug_type_distribution.py $INT validation/project_scope_v1/labels.jsonl validation/samples_game_v3/development_labels.jsonl results/bug_types_v1` | Symptom distribution and bug-identification precision (Tables 2 and 5) | `results/bug_types_v1/` |
| 14 | `python -I scripts/23_sample_test_path_validation.py $INT validation/test_path_rule_v1` then `python -I scripts/24_test_path_rule_validation.py $INT validation/test_path_rule_v1 validation/game_type_v1/labels.csv validation/test_path_rule_v1/summary.json` | Validation of the test-path rule (Section 3.3, Table 2) | `validation/test_path_rule_v1/` |
| 15 | `python -I scripts/16_evaluate_symptom_rules.py validation/samples_game_v3/issues_llm.jsonl validation/samples_game_v3/development_labels.jsonl <audit_labels.jsonl> results/rq_analysis_v1/symptom_rule_evaluation.json <details.json>` | Agreement of the symptom rules (Table 4) | `results/rq_analysis_v1/symptom_rule_evaluation.json` |
| 16 | `python -I scripts/26_within_project.py $INT results/within_project_v1` | Within-project (project fixed effects) comparison, McFadden R² (Section 5.2, Table 7; after step 7) | `results/within_project_v1/` |
| 17 | `python -I scripts/27_robustness.py $INT validation/game_type_v1/labels.csv results/robustness_v1` | Primary RQ1 odds ratios with the non-test size control, within-project table, RQ2 specification grid and project-level models, rule-source split, large diffs, step-5 exclusions (after step 7) | `results/robustness_v1/` |

The odds ratios in the report (Tables 6, 7 and 9) come from step 17. Script 20's GEE models are superseded by the specification grid of step 17: script 20 suppresses convergence warnings and falls back silently to an independence structure, and its full exchangeable model does not converge under the default iteration limit.

Scripts 07, 09, 10, 11, 20, 26 and 27 refuse to overwrite an existing output directory; use a new directory or remove the old one.

## Notes

- **Seeds.** 20261112 (case selection), 20261113 (bootstrap in 17, GitHub samples), 20261114 (audit sample, bootstrap in 20), 20261115 (test-path sample). They are defaults in the scripts.
- **Stored labels.** Classifications made by LLMs or by the author are data, not computed: `validation/project_scope_v1/` (game/tool), `validation/game_type_v1/labels.csv`, `validation/samples_game_v3/` (symptom samples), `validation/test_cases_final_v1/annotations.jsonl`, `validation/test_path_rule_v1/`. The scripts 14, 19 and 24 only write these stored labels to files.
- **Audit labels (step 15).** The LLM labels of the audit sample were kept outside the repository while the author labeled. They are now `validation/samples_game_v3/audit_llm_labels.jsonl`; their SHA-256 matches the value recorded before the author labeled (`validation/samples_game_v3/audit_llm_labels_sealed.json`). Per-category results of the symptom rules are in `results/rq_analysis_v1/symptom_rule_evaluation_by_category.json` (written by script 16 as its last argument).
- **Author's labels.** `validation/samples_game_v3/human_answers.json` holds the author's labels of 19 issues (made while consulting ChatGPT; see the README there). `python -I scripts/28_compare_author_labels.py validation/samples_game_v3/human_answers.json validation/samples_game_v3/audit_llm_labels.jsonl validation/samples_game_v3/human_blind.jsonl validation/samples_game_v3/audit_llm_labels_sealed.json results/author_labels_v1` checks the SHA-256 and compares the author's labels with the Claude labels and the rules.
- **Samples.** `validation/samples_game_v3/` was created with `scripts/10_prepare_grouped_holdout.py … --final-dir $INT/final_diff_v1` (seed 20261114). It does not need to be regenerated.
- **Tests of the scripts.** `python -I scripts/test_fix_cohort.py`, `test_final_pr_diff.py`, `test_mining_annotations.py`, `test_prepare_validation.py`, `test_data_preparation.py` run on synthetic data.
- **Expected checkpoints.** Step 4 prints 81,620 eligible bug issues and 13,883 included issues; step 6 reports 10,082 game issues with status `all_landing` and 626 with a test change; step 7 reproduces the shares in Table 6.

## Building the PDF

The submitted PDF is `report/report.pdf`, built from `report/report.tex` (two columns, 7 A4 pages). `report/report_ja.pdf` is a Japanese translation with the same content, built from `report/report_ja.tex` with LuaLaTeX. With TeX Live:

```
cd report
pdflatex report.tex
pdflatex report.tex
lualatex report_ja.tex
lualatex report_ja.tex
```

The figure is read from `results/game_type_v1/`. If the repository path contains non-ASCII characters and the build fails, copy `report/` and `results/` to an ASCII path first.
