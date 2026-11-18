"""A diffeval output folder holding one ok geneval2 seed."""

import json

import pytest

_SAMPLES = [{"prompt_id": "g00000", "prompt": "a cat", "path": "images/seed_0/g00000.png"}]
_METRIC = {"name": "geneval2", "status": "ok", "details": {"question_scores": {"g00000": [0.5, 0.25]}}}
_ROWS = [{"prompt": "a dog", "vqa_list": []}, {"prompt": "a cat", "vqa_list": [["Is there a cat?", "Yes"]], "skills": ["object"]}]


@pytest.fixture
def g2_run(tmp_path):
    run = tmp_path / "run"
    run.mkdir()
    body = {"per_seed": [{"seed": 0, "samples": _SAMPLES, "metrics": [_METRIC]}]}
    (run / "results.json").write_text(json.dumps(body), encoding="utf-8")
    return run


@pytest.fixture
def g2_rows():
    return _ROWS
