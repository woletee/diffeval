"""Build a skipped MetricResult."""

from diffeval.types.result import MetricResult
from diffeval.types.result_rules import check


def skipped(name: str, error: str, higher_is_better, protocol: dict, details: dict | None = None):
    check("skipped", None, error)
    body = {} if details is None else details
    return MetricResult(name, None, "skipped", error, higher_is_better, body, dict(protocol))
