"""Write results.json."""

import json
from pathlib import Path


def write_json(body: dict, output_dir: Path) -> Path:
    path = Path(output_dir) / "results.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
    return path
