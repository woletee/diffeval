"""The table row shows the means and the published CMMD for a known model."""

import json

from diffeval.bench.table_cli import main


def test_row(tmp_path, capsys):
    body = {"backend": {"name": "diffusers", "pipeline": "stabilityai/sdxl-turbo", "steps": 1, "guidance": 0.0, "device": "cuda"}}
    body["suite"] = {"width": 512, "height": 512, "prompts": [{}, {}]}
    body["aggregate"] = {"cmmd": {"mean": 0.55, "std": None}, "clip_score": {"mean": 0.8, "std": 0.01}}
    (tmp_path / "r.json").write_text(json.dumps(body), encoding="utf-8")
    assert main([str(tmp_path / "r.json")]) == 0
    row = capsys.readouterr().out.splitlines()[-1]
    assert "stabilityai/sdxl-turbo" in row and "0.8 +/- 0.01" in row and "| 0.55 |" in row and row.endswith("| 0.548 |")
