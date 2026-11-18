"""CLIPScore clips negative cosines and skips without the extra."""

import json

from diffeval.cli.main import main
from diffeval.metrics.clip.formula import clip_score


def test_formula_clips_negative_cosine():
    assert clip_score([1, 0, -1], 2.5) == 2.5 / 3


def test_core_skips_without_metrics_extra(tmp_path):
    out = tmp_path / "out"
    code = main(["run", "--backend", "dummy", "--suite", "core", "--output", str(out)])
    body = json.loads((out / "results.json").read_text())
    protocol = body["metric_protocols"]["clip_score"]
    assert code == 0 and body["aggregate"]["clip_score"]["status"] == "skipped" and (out / "report.html").is_file()
    assert protocol["model"] == "openai/clip-vit-base-patch32" and protocol["weight"] == 2.5 and "no prefix" in protocol["text"]
    assert "224" in protocol["crop"] and "Hessel" in protocol["paper"] and "2021" in protocol["paper"]
