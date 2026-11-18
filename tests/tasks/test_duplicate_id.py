"""Two prompts that share an id raise SuiteError."""

from pathlib import Path

import pytest

from diffeval.tasks.errors import SuiteError
from diffeval.tasks.load_path import load_path

_YAML = "name: demo\nseeds: [0, 1]\nprompts:\n- {id: same, prompt: one}\n- {id: same, prompt: two}\n"


def test_duplicate_id(tmp_path: Path):
    path = tmp_path / "suite.yaml"
    path.write_text(_YAML, encoding="utf-8")
    with pytest.raises(SuiteError):
        load_path(path)
