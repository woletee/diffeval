"""Finite value and status rules for a metric result."""

import math


def check(status: str, value: float | None, error: str | None) -> None:
    if status == "ok":
        finite = isinstance(value, (int, float)) and not isinstance(value, bool)
        if finite and math.isfinite(value) and error is None:
            return
    elif status in ("skipped", "error") and value is None and error:
        return
    raise ValueError(f"bad metric result status {status!r}")
