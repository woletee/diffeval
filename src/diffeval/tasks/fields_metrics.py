"""Metric name list."""

from diffeval.tasks.errors import SuiteError

_DEFAULT = ("clip_score", "cmmd", "fid", "kid")


def metrics(data: dict) -> dict:
    raw = data.get("metrics", list(_DEFAULT))
    if not isinstance(raw, list) or not raw:
        raise SuiteError("metrics must be a non-empty list")
    if any(not isinstance(item, str) or not item for item in raw):
        raise SuiteError("metric names must be non-empty strings")
    return {"metrics": tuple(raw)}
