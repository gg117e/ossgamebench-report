"""Create deterministic display excerpts for reading project purpose; no labels inferred."""
import argparse
import json
from pathlib import Path
import re


def prepare(rows):
    for index, row in enumerate(rows):
        row["index"] = index
        useful = []
        for number, line in enumerate(row["readme"].splitlines()[:300]):
            text = line.strip()
            if len(text) < 30 or text.startswith(("![", "[![", "<img", "<a ", "[build", "[Build", "[![", "| !")):
                continue
            if re.search(r"badge|shields\.io|travis-ci|ReadTheDocs|coverage|contributors|copyright|license|Licence", text, re.I):
                continue
            if re.search(r"\b(is (?:an?|the)|game|engine|framework|library|clone|remake|implementation|simulator|server|platform)\b", text, re.I):
                useful.append((number, text))
        row["review_line_no"] = useful[0][0] + 1 if useful else None
        row["review_line"] = useful[0][1] if useful else row["readme"][:220]
        row["scope"] = "unreviewed"
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_jsonl", type=Path)
    parser.add_argument("output_jsonl", type=Path)
    args = parser.parse_args()
    rows = [json.loads(line) for line in args.input_jsonl.read_text(encoding="utf-8").splitlines()]
    args.output_jsonl.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in prepare(rows)), encoding="utf-8")


if __name__ == "__main__":
    main()
