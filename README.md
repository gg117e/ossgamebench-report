# Which Game Bugs Get Tested?

Replication package for the course report *"Which Game Bugs Get Tested? Bug Symptoms, Game Types, and Test Changes in 10,000 Open-Source Game Bug Fixes"* (AdSE report assignment, Option B).

The study links bug reports of open-source games in **OSSGameBench** to the final diff of the merged pull requests that fixed them and measures whether the fix changes a test file, by bug symptom and by game type.

## Contents

| Path | Content |
|---|---|
| `report/report.tex`, `report/report.pdf` | The report (LaTeX source and PDF) |
| `report/report_ja.tex`, `report/report_ja.pdf` | Japanese translation of the report, same content |
| `report/REPRODUCE.md` | Step-by-step reproduction instructions, with commands, outputs and seeds |
| `scripts/` | All analysis code (numbered in order of use) and tests on synthetic data |
| `validation/` | Stored classifications with annotator, model and reason; codebook; samples; labelling tool |
| `results/` | Result tables, figures and summaries produced by the scripts |
| `data/` | Notes on the data, list of duplicated repositories, manifest of commit files |

## Data

The data are not included. Download `OSSGameBench.zip` from Zenodo record 17553539 (https://doi.org/10.5281/zenodo.17553539, 65,816,061,871 bytes, MD5 `40fd064b56ec327b6284039b18b19ea1`); `scripts/00_download_data.py --source zenodo` does this and verifies the checksum.

Dataset paper: F. Marsad and N. Weeraddana. *OSSGameBench: A Large-Scale Dataset of Development Activities in Open-Source Video Games.* MSR '26. https://doi.org/10.1145/3793302.3793313

## Reproduction

See [report/REPRODUCE.md](report/REPRODUCE.md). In short: Python 3.13+, `pip install -r requirements.txt`, about 70 GB of disk space, and run the numbered steps from the repository root with `python -I`.

## Notes

- Classifications made by LLMs or by the author are stored as data in `validation/`; the scripts do not call any LLM.
- The samples in `validation/` contain titles and bodies of public GitHub issues taken from the dataset.
- Some result notes (`results/*/README.md`, `validation/README.md`, `data/README.md`) are working notes written in Japanese. The report and the reproduction instructions are in English; a Japanese translation of the report is included.
- Local paths in logs and manifests were replaced by `<repo>` and `C:/Users/<user>`.
- Two observations about the dataset that matter for reuse are documented in `results/final_diff_v1/README.md` and `results/test_cases_final_v1/README.md`: commits of a pull request include merges of other work, and the per-file patches are stored in reverse direction.
