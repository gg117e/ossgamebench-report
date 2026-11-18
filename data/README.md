# データの取得記録

取得日：2026-11-06（JST）

2026-11-12にこの端末でもDropboxから再取得し、同じサイズ・MD5を確認した。
省容量での入力表作成と再現確認は [LOCAL_SETUP.md](LOCAL_SETUP.md)、[準備結果](../results/local_setup_2026-11-12/README.md) を参照。
以下は元端末での取得記録。

## どのデータを使ったか

OSSGameBench の Zenodo レコードには 3 つの版があり、データ本体が入っているのは 1 つだけである。

| Zenodo レコード | 公開日 | 中身 | リポジトリ数 |
|---|---|---|---|
| 17525962 | 2025-11-04 | online-appendix.pdf のみ | - |
| **17553539** | **2025-11-10** | **OSSGameBench.zip（データ本体）**、data_collection.zip、analysis.zip、README.md、online-appendix.pdf | **970** |
| 18359123（最新） | 2026-01-23 | analysis.zip、Scripts.zip、README.md、online-appendix.pdf（**データなし**） | 論文では 950 |

課題に示された Dropbox フォルダの `OSSGameBench.zip` は、Zenodo 17553539 の `OSSGameBench.zip` と同じファイルである
（サイズが 65,816,061,871 バイトで一致し、ダウンロード後に Zenodo が公開している MD5 と一致することを確認した。下の表を参照）。

ダウンロード元：Dropbox（Zenodo からは約 0.4 MB/s しか出ず、全体で約 2 日かかるため。Dropbox は約 8〜22 MB/s）。

### 970 件と 950 件の関係

最新版（18359123）の `analysis.zip` 内の `analysis/analysis-2.ipynb` に、重複とされた 20 リポジトリの一覧
`duplicated_repos_v1` がある（[duplicated_repos_v1.txt](duplicated_repos_v1.txt) に写した）。

- この 20 件はダウンロードしたデータにすべて含まれている（project.parquet は 970 行）。
- この 20 件を除くと Issue は **319,709 件となり、論文の数値と完全に一致**する。
  → 論文の「950 件」は、このデータから 20 件を除いたものと判断できる。
- ただし、PR とコメントの件数は 20 件を除いても論文と一致しない（下表）。論文は v3 のスクリプト
  （`get_remaining_comments.py`、`pr_cross_repo_fix.py`）で追加収集したデータを使っている可能性があるが、
  そのデータは公開されていない。**レポートでは「Zenodo 17553539 の 970 件から重複 20 件を除いた 950 件」と明記する。**

| 表 | 全行数（970 件） | 重複 20 件を除く | 論文の値 |
|---|---:|---:|---:|
| issue | 326,182 | 319,709 | 319,709 |
| pr | 396,048 | 388,445 | 374,538 |
| issue_comment | 853,302 | 833,476 | 846,911 |
| pr_comment | 689,749 | 665,812 | 1,114,748 |

## ファイルと検証

保存場所：`C:\Users\<user>\ossgamebench-data\raw\`（OneDrive の同期対象外。65 GB を同期させないため）

| ファイル | サイズ（バイト） | MD5（Zenodo 公開値） | 検証 |
|---|---:|---|---|
| OSSGameBench.zip | 65,816,061,871 | 40fd064b56ec327b6284039b18b19ea1 | 一致（2026-11-06 19:52 JST 完了） |
| zenodo_17553539/online-appendix.pdf | 518,058 | df9e54b39d113bb34f9cb567a16ea154 | 一致 |
| zenodo_17553539/README.md | 1,450 | 649fb3bb313fac0942f2bf1ec214d31b | 一致 |
| zenodo_17553539/data_collection.zip | 19,762 | 644c1a31fde456399392f60334ab8fc7 | 一致 |
| zenodo_17553539/analysis.zip | 447,243 | bbbe6dcadca54ebe0c3cd5f8a1215687 | 一致 |
| zenodo_18359123/online-appendix.pdf | - | 32a59ec2aa401110bbe9bc7eb889e7cd | 一致 |
| zenodo_18359123/README.md | - | 6332caf247ab130bfb39a1b66a751b97 | 一致 |
| zenodo_18359123/analysis.zip | - | 8c6155a7603b391ded1991caf69ed6b6 | 一致 |
| zenodo_18359123/Scripts.zip | - | b416d06113d02a7abdccb636508c0c9d | 一致 |

## zip の中身

988 エントリ。圧縮後 65.82 GB、展開後 82.13 GB。

| パス | 展開後サイズ | 行数 | 列 |
|---|---:|---:|---|
| OSSGameBench/project.parquet | 3.1 MB | 970 | project, is_fork, languages(JSON 文字列), topics(`;` 区切り), created_at, size, readme_content |
| OSSGameBench/issue.parquet | 142 MB | 326,182 | project, number, contributor, title, body, labels(list), state(OPEN/CLOSED), created_at, closed_at |
| OSSGameBench/issue_comment.parquet | 150 MB | 853,302 | project, issue_number, contributor, body（**created_at なし**） |
| OSSGameBench/pr.parquet | 136 MB | 396,048 | project, number, contributor, title, body, labels, state(OPEN/CLOSED/MERGED), created_at, closed_at, merged_at |
| OSSGameBench/pr_comment.parquet | 155 MB | 689,749 | project, pr_number, contributor, body（**created_at、type、path、line なし**） |
| OSSGameBench/issue_pr.parquet | 0.5 MB | 78,060 | project, issue_number, pr_number（多対多） |
| OSSGameBench/pr_commit.parquet | 59 MB | 1,565,625 | project, pr_number, commit_sha |
| OSSGameBench/commit_metadata.parquet | 0.05 MB | 970 | project, file_location |
| OSSGameBench/commits/commits\|owner\|repo.parquet | 計 81.5 GB | 973 ファイル | repo, sha, contributor, contributor_email, created_at, message, files(list), diff(list) |

取り出した表の MD5（`tables/`）。Range リクエストで先に取り出した分と、ダウンロードした zip から取り出した分で一致した。

| 表 | MD5 |
|---|---|
| commit_metadata.parquet | 42b7eeeb30b94570e70b565b9ed5a78f |
| issue.parquet | 9b533413d7d93c17d1ef8e07edfc1ebe |
| issue_comment.parquet | 8d639bcce6cb2e193b65bd061735dc35 |
| issue_pr.parquet | 79248f8bafcbe682f508cae13728d197 |
| pr.parquet | 076397d1eb1a950f8cee2c8385d8c581 |
| pr_comment.parquet | 06a9d2a0788f7f9882338b51b481bb83 |
| pr_commit.parquet | eff25dc714f221b1e4fc54b7325195a3 |
| project.parquet | 065d33fc304d0f1ed7fdba0687c660de |

注意点：

- コミットのファイルは 973 個 = commit_metadata の 969 件 + `4ian/gdevelop` の分割 4 ファイル
  （commit_metadata は分割前の名前 `commits|4ian|gdevelop.parquet` を指しており、その名前のファイルは zip にない）。
- コミットの created_at はタイムゾーン付きのローカル時刻（例 `2025-08-12 17:50:49+02:00`）で、Issue（`...Z`、UTC）と形式が違う。比較する前に UTC にそろえる。
- コミットの sha に枝の名前が付いている例がある（例 `bae6005f... main`）。pr_commit の commit_sha と結合する前に、先頭 40 文字に切り詰める必要があるかもしれない。
- `Patryk27/kartoffels` のコミットは 1 行しかない。収集が欠けているプロジェクトがある可能性があるので、プロジェクトごとのコミット数を確認する。
- 最大のコミットファイルは 8.56 GB（gdevelop の 1 つ目）。1 ファイルずつ読み、diff の列は読まない。

- 日時は ISO 8601 の文字列（例 `2012-12-09T02:39:04Z`、UTC）。Issue の created_at の最大は 2025-10-12T12:12:48Z で、
  **収集時点はおおむね 2025-10-12** と推定できる（未クローズの Issue はこの時点で打ち切り）。
- コミットのファイル名には `|` が含まれ、Windows ではそのまま展開できない。`01b_extract_commits.py` で
  `|` を `__` に置き換えて `raw/commits/` に展開した（例 `commits|4ian|gdevelop|1.parquet` → `4ian__gdevelop__1.parquet`）。
  元の名前との対応、サイズ、CRC-32 は [commit_files_manifest.csv](commit_files_manifest.csv)。
  2026-11-06 に 973 ファイル、計 81,480,567,887 バイトを展開し、全ファイルで CRC-32 とサイズが一致した。
- `4ian/gdevelop` のコミットは 4 ファイルに分割されている（付録より）。
- 付録には「コミットのデータは 300 GB 超」とあるが、zip 内の展開後サイズは 81.5 GB。

## 再現手順

```bash
python -I scripts/00_download_data.py C:/Users/<user>/ossgamebench-data/raw --source zenodo
python -I scripts/01_extract_tables.py C:/Users/<user>/ossgamebench-data/raw
python -I scripts/01b_extract_commits.py C:/Users/<user>/ossgamebench-data/raw data/commit_files_manifest.csv
python -I scripts/02_inspect_files.py C:/Users/<user>/ossgamebench-data/raw > data/inspect_output.txt
python -I scripts/02b_build_commit_table.py C:/Users/<user>/ossgamebench-data/raw C:/Users/<user>/ossgamebench-data/interim
python -I scripts/03_pilot_stats.py C:/Users/<user>/ossgamebench-data/raw C:/Users/<user>/ossgamebench-data/interim > results/pilot_stats.txt
```

`02b` は diff を除いた軽いコミット表 `interim/commits_slim.parquet`（2,796,851 行、311 MB）を作る。
sha は先頭 40 文字（残りの参照名は sha_ref 列）、日時は UTC に変換。全行で sha の形式と日時の変換に問題はなかった。
