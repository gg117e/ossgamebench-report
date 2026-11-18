# 評価標本 v3（最終差分の対象、2026-11-13）

`scripts/10_prepare_grouped_holdout.py --final-dir` で作成。v2 の後継。

- 母集団：game のプロジェクトで、Issue のすべてのマージ済み PR に最終差分があるバグ Issue **10,082 件**（177 プロジェクト）。
- development 100 件：v2（v1）と同じ。手引きの試行に使い済み（Codex による開発用の判定 `development_labels.jsonl`）。うち 97 件が新しい母集団に入る。
- audit 100 件：母集団から、development と内容分析の 30 PR（`validation/test_cases_final_v1`）と Issue–PR の連結成分を共有しない Issue を無作為に抽出（シード 20261114、抽出枠 9,899 件）。
- 本人用 50 件：audit から無作為に選んだもの。`human_review.md`（タイトルと本文だけ。LLM の答えは含まない）を読み、`human_answers.json` に記入する。
- 手引き：[validation/codebook.md](../codebook.md) の v1-2026-11-13。

v2 の audit と本人用 50 件は、母集団を最終差分に絞ったので使わない（記入はされていない）。

## LLM による audit 100 件の判定（封印中、2026-11-13）

- Claude（claude-opus-5-5）が、タイトルと収録本文だけから手引き v1-2026-11-13 の 1 節・1b 節で 100 件を判定した。再現情報の 5 項目は未判定。
- 本人の 50 件を独立に保つため、判定結果と、それを書いたスクリプト（`15_write_audit_llm_labels.py`）は**リポジトリの外**の
  `C:/Users/<user>/ossgamebench-sealed/` に置き、SHA-256 だけを [audit_llm_labels_sealed.json](audit_llm_labels_sealed.json) に記録した。
- 本人の `human_answers.json` が完成したら、両方をリポジトリに移して commit し、一致率と κ を計算する。
- **注意**：この封印ファイルは元の Windows 端末にしかない。ほかの端末で続ける場合は、本人の判定が終わってから移す。

## 本人の判定（2026-11-18）

- `human_answers.json` に、50 件のうち**先頭 19 件**（並びは無作為）の判定を記入した。残り 31 件は空欄。ツールは `validation/label_tool.html`。
- **判定の方法**：本人が ChatGPT と相談しながら付けた。したがって LLM から独立した判定ではない。
  Claude の audit の判定（封印中）と、症状の規則の予測は見ていない。
- 使い方：規則の評価（規則 対 本人：15/19 一致、κ 0.64）と、Claude の判定との照合に使う。
  「人の判定と LLM の判定が一致する」根拠には使わない。
- 2026-11-18 の commit メッセージにある "blind" は、Claude の判定と規則の予測を見ていないという意味に限る。

## 封印の解除と照合（2026-11-18）

- 本人の判定を 19 件で終えることにしたので、Claude の判定を `audit_llm_labels.jsonl` としてリポジトリに入れた。SHA-256 は封印時の記録（`3b7434ba…`）と一致。
- `scripts/28_compare_author_labels.py` の結果（[results/author_labels_v1](../../results/author_labels_v1/summary.json)）：
  本人 対 Claude は 18/19 一致（κ 0.91、95% 区間 0.74–1.00）、「本当のバグか」は 19/19。
  規則 対 本人 15/19（κ 0.64）、同じ 19 件で規則 対 Claude 16/19（κ 0.72）。
- 唯一の不一致は ihhub/fheroes2#4838（移動のたびに経路が変わる）：本人 visual、Claude gameplay。
- 本人は ChatGPT と相談したので、これは「LLM から独立した人の判定」との一致ではない。
