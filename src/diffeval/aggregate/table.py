"""Aggregate mean and sample std across seeds."""

from diffeval.aggregate.names import names
from diffeval.aggregate.row import row


def aggregate(per_seed: list[dict]) -> dict:
    return {name: row(per_seed, name) for name in names(per_seed)}
