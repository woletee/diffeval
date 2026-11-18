"""geneval2 is skipped without the extra, and errors on prompts without questions."""

import json

from diffeval.cli.main import main
from diffeval.metrics.geneval2 import judge_load


def _run(suite, out):
    assert main(["run", "--backend", "dummy", "--suite", str(suite), "--output", str(out)]) == 0
    return json.loads((out / "results.json").read_text())["per_seed"][0]["metrics"][0]


def test_skipped_and_error(g2_suite, tmp_path, monkeypatch):
    monkeypatch.setattr(judge_load, "load_judge", lambda model_id: None)
    skipped = _run(g2_suite, tmp_path / "a")
    assert skipped["status"] == "skipped" and "diffeval[geneval2]" in skipped["error"]
    monkeypatch.setattr(judge_load, "load_judge", lambda model_id: ("processor", "model"))
    g2_suite.write_text(g2_suite.read_text().split("prompts:")[0] + "prompts:\n- {id: a, prompt: a cat}\n")
    error = _run(g2_suite, tmp_path / "b")
    assert error["status"] == "error" and "diffeval-geneval2" in error["error"]
