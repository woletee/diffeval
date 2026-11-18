"""Reference inputs for one seed of a diffeval geneval2 run, and diffeval's own question scores."""

import json
from pathlib import Path


def _entry(run: Path, seed: int):
    body = json.loads((run / "results.json").read_text(encoding="utf-8"))
    entry = next((item for item in body["per_seed"] if item["seed"] == seed), None)
    metric = next((item for item in (entry or {}).get("metrics", []) if item["name"] == "geneval2"), None)
    if metric is None or metric["status"] != "ok":
        raise SystemExit(f"{run} has no ok geneval2 result for seed {seed}")
    return entry["samples"], metric["details"]["question_scores"]


def run_inputs(run: Path, seed: int, rows: list[dict], out: Path) -> list[list[float]]:
    samples, scores = _entry(run, seed)
    by_prompt = {row["prompt"]: row for row in rows}
    (out / "data.jsonl").write_text("".join(json.dumps(by_prompt[item["prompt"]]) + "\n" for item in samples), encoding="utf-8")
    images = {item["prompt"]: str((run / item["path"]).resolve()) for item in samples}
    (out / "images.json").write_text(json.dumps(images), encoding="utf-8")
    return [scores[item["prompt_id"]] for item in samples]
