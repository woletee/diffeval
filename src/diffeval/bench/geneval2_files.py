"""The GenEval 2 prompts and questions, from a pinned commit of facebookresearch/GenEval2."""

import json
from pathlib import Path

from diffeval.bench.fetch import fetch

COMMIT = "a6e82d2289e8d418f27f0adee77908b07060eea3"
DATA_URL = f"https://raw.githubusercontent.com/facebookresearch/GenEval2/{COMMIT}/geneval2_data.jsonl"
NOTICE = "GenEval 2 data is CC BY-NC 4.0 (facebookresearch/GenEval2): non-commercial use only. diffeval downloads it and does not ship it."


def geneval2_rows(out: Path, limit: int) -> list[dict]:
    with fetch(DATA_URL, out / "geneval2_data.jsonl").open(encoding="utf-8") as handle:
        rows = [json.loads(line) for line in handle if line.strip()]
    return rows[:limit]
