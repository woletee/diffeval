"""Resolve a suite from a path or a registered name."""

from pathlib import Path

from diffeval.registry.lookup import get
from diffeval.registry.tables import TASKS
from diffeval.tasks.errors import SuiteError
from diffeval.tasks.load_path import load_path


def resolve(source: str):
    path = Path(source)
    if path.suffix in {".yaml", ".yml"}:
        return load_path(path)
    try:
        return get(TASKS, source, "task").load()
    except KeyError as exc:
        raise SuiteError(str(exc)) from None
