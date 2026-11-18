"""A prompt meta that is not a mapping raises SuiteError."""

from pathlib import Path

import pytest

from diffeval.tasks.errors import SuiteError
from diffeval.tasks.load_path import load_path

_YAML = "name: demo\nseeds: [0]\nprompts:\n- {id: a, prompt: a cat, meta: [1, 2]}\n"


def test_meta_must_be_mapping(tmp_path: Path):
    path = tmp_path / "suite.yaml"
    path.write_text(_YAML, encoding="utf-8")
    with pytest.raises(SuiteError):
        load_path(path)
