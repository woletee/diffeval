"""Load a suite from a filesystem YAML path."""

from pathlib import Path

from diffeval.tasks.from_mapping import from_mapping
from diffeval.tasks.read_yaml import read_yaml
from diffeval.types.suite import Suite


def load_path(path) -> Suite:
    file = Path(path)
    return from_mapping(read_yaml(file), str(file), file.parent)
