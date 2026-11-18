"""A dummy core run writes JSON, HTML, and eight images."""

import json

from diffeval.cli.main import main
from diffeval.registry.tables import METRICS


def test_dummy_json_html(tmp_path):
    out = tmp_path / "out"
    code = main(["run", "--backend", "dummy", "--suite", "core", "--output", str(out)])
    body = json.loads((out / "results.json").read_text())
    html = (out / "report.html").read_text()
    paths = [sample["path"] for seed in body["per_seed"] for sample in seed["samples"]]
    wanted = {"clip_score", "cmmd", "fid", "kid"}
    rows = body["aggregate"]
    assert code == 0 and body["seeds"] == [0, 1] and len(paths) == 8 and html.count("<img ") == 8
    assert all((out / path).is_file() and f'src="{path}"' in html for path in paths)
    assert (not wanted <= set(METRICS)) or wanted <= set(rows)
    assert all(rows[name]["status"] in {"skipped", "ok"} for name in wanted if name in rows)
