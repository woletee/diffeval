"""Build an ok MetricResult."""

from diffeval.types.result import MetricResult
from diffeval.types.result_rules import check


def ok(name: str, value: float, higher_is_better, protocol: dict, details: dict | None = None):
    check("ok", value, None)
    return MetricResult(name, value, "ok", None, higher_is_better, details or {}, dict(protocol))
