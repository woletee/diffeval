"""Ids that differ only in case raise SuiteError."""

from pathlib import Path

import pytest

from diffeval.tasks.errors import SuiteError
from diffeval.tasks.load_path import load_path

_YAML = "name: demo\nseeds: [0]\nprompts:\n- {id: Cat, prompt: one}\n- {id: cat, prompt: two}\n"


def test_case_only_id(tmp_path: Path):
    path = tmp_path / "suite.yaml"
    path.write_text(_YAML, encoding="utf-8")
    with pytest.raises(SuiteError):
        load_path(path)
