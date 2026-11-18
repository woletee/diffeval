"""Metric contract."""

from typing import Protocol

from diffeval.types.context import EvalContext
from diffeval.types.result import MetricResult
from diffeval.types.sample import Sample


class Metric(Protocol):
    name: str
    description: str
    higher_is_better: bool | None
    requires_references: bool
    protocol: dict

    def compute(self, samples: list[Sample], context: EvalContext) -> MetricResult: ...
