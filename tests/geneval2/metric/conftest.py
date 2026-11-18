"""A two-prompt suite with GenEval 2 questions in meta."""

from pathlib import Path

import pytest


@pytest.fixture
def g2_suite(tmp_path):
    path = tmp_path / "suite.yaml"
    path.write_text((Path(__file__).parent / "g2_suite.yaml").read_text(encoding="utf-8"), encoding="utf-8")
    return path
