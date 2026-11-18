"""A relative reference_dir resolves next to the suite file."""

from pathlib import Path

from diffeval.tasks.load_path import load_path

_YAML = "name: demo\nseeds: [0, 1]\nwidth: 64\nheight: 32\nreference_dir: refs\nprompts:\n- {id: red_cube, prompt: a red cube}\n"


def test_relative_reference(tmp_path: Path):
    path = tmp_path / "suite.yaml"
    path.write_text(_YAML, encoding="utf-8")
    suite = load_path(path)
    assert suite.reference_dir == path.parent / "refs"
    assert (suite.width, suite.height, suite.seeds) == (64, 32, (0, 1))
