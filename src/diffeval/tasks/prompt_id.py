"""Prompt ids that are safe filenames."""

import re

from diffeval.tasks.errors import SuiteError

_ID = re.compile(r"[A-Za-z0-9_-]+")


def check_id(value: str) -> str:
    if not isinstance(value, str) or _ID.fullmatch(value) is None:
        raise SuiteError(f"bad prompt id {value!r}")
    return value
