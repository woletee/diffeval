"""diffeval-check-geneval2 feeds the reference the run's prompts and images and compares scores."""

import json
import sys

import pytest

from diffeval.bench import geneval2_check_cli, geneval2_ref

_WRITE = "import json, sys; json.dump([[0.5, float(sys.argv[2])]], open(sys.argv[1], 'w'))"


@pytest.mark.parametrize(("reference", "code"), [("0.25004", 0), ("0.3", 1)])
def test_check(g2_run, g2_rows, monkeypatch, reference, code):
    monkeypatch.setattr(geneval2_check_cli, "geneval2_rows", lambda out, limit: g2_rows)
    monkeypatch.setattr(geneval2_ref, "reference_command", lambda out, data, images, scores: [sys.executable, "-c", _WRITE, str(scores), reference])
    assert geneval2_check_cli.main(["--run", str(g2_run)]) == code
    out = g2_run / "geneval2-check"
    assert json.loads((out / "data.jsonl").read_text()) == g2_rows[1]
    assert json.loads((out / "images.json").read_text()) == {"a cat": str((g2_run / "images/seed_0/g00000.png").resolve())}
