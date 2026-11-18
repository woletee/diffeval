"""One metric score for one seed."""

from dataclasses import dataclass


@dataclass
class MetricResult:
    name: str
    value: float | None
    status: str
    error: str | None
    higher_is_better: bool | None
    details: dict
    protocol: dict
