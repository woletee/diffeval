"""Read a YAML file to a mapping."""

from pathlib import Path

import yaml

from diffeval.tasks.errors import SuiteError


def read_yaml(path: Path) -> dict:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SuiteError(f"{path} must be a mapping")
    return data
