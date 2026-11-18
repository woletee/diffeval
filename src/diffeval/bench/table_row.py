"""One Markdown row from one results.json."""

import json
from pathlib import Path

from diffeval.bench.published import PUBLISHED_CMMD

METRICS = ("clip_score", "cmmd", "fid", "kid")
HEADER = ["model", "steps", "guidance", "size", "device", "images", *METRICS, "published CMMD (30k)"]


def _cell(row) -> str:
    if row is None or row.get("mean") is None:
        return "-"
    return f"{row['mean']:.4g}" if row.get("std") is None else f"{row['mean']:.4g} +/- {row['std']:.2g}"


def table_row(path) -> str:
    body = json.loads(Path(path).read_text(encoding="utf-8"))
    backend, suite, agg = body["backend"], body["suite"], body["aggregate"]
    model = backend.get("pipeline") or backend["name"]
    cells = [model, str(backend.get("steps")), str(backend.get("guidance")), f"{suite['width']}x{suite['height']}", str(backend.get("device")), str(len(suite["prompts"]))]
    published = PUBLISHED_CMMD.get(model)
    return "| " + " | ".join(cells + [_cell(agg.get(name)) for name in METRICS] + ["-" if published is None else str(published)]) + " |"
