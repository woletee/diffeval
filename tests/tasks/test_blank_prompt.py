"""A prompt of only whitespace raises SuiteError."""

from pathlib import Path

import pytest

from diffeval.tasks.errors import SuiteError
from diffeval.tasks.load_path import load_path

_YAML = "name: demo\nseeds: [0]\nprompts:\n- {id: a, prompt: \"   \"}\n"


def test_blank_prompt(tmp_path: Path):
    path = tmp_path / "suite.yaml"
    path.write_text(_YAML, encoding="utf-8")
    with pytest.raises(SuiteError):
        load_path(path)
