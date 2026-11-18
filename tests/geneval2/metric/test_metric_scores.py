"""geneval2 runs through diffeval run and reports Soft-TIFA GM, AM, and breakdowns."""

import json

import pytest

from diffeval.cli.main import main
from diffeval.metrics.geneval2 import judge_load, prompt_scores

_PROBS = {"How many toys": 0.25, "Are there any toys": 1.0, "Are there any cats": 0.81, "Is the cat red": 1.0}


def test_scores(g2_suite, tmp_path, monkeypatch):
    monkeypatch.setattr(judge_load, "load_judge", lambda model_id: ("processor", "model"))
    monkeypatch.setattr(prompt_scores, "ask", lambda p, m, image, text, answers: ("x", next(v for k, v in _PROBS.items() if text.startswith(k))))
    assert main(["run", "--backend", "dummy", "--suite", str(g2_suite), "--output", str(tmp_path / "out")]) == 0
    result = json.loads((tmp_path / "out" / "results.json").read_text())["per_seed"][0]["metrics"][0]
    assert result["status"] == "ok", result["error"]
    assert result["value"] == pytest.approx(70.0)
    details = result["details"]
    assert details["soft_tifa_am"] == pytest.approx(76.5) and details["question_scores"] == {"a": [0.25, 1.0], "b": [0.81, 1.0]}
    assert details["by_skill"] == pytest.approx({"object": 100 * 1.81 / 2, "attribute": 100.0, "count": 25.0})
    assert details["by_atom_count"] == pytest.approx({"3": 50.0, "4": 90.0})
