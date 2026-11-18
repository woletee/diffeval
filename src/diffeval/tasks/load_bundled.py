"""Load a suite YAML packaged with the tasks."""

from pathlib import Path

from diffeval.tasks.load_path import load_path


def load_bundled(name: str):
    return load_path(Path(__file__).parent / "suites" / name)
