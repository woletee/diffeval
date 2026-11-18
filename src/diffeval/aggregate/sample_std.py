"""Sample standard deviation, null below two values."""

import statistics


def sample_std(values: list[float]):
    if len(values) < 2:
        return None
    return statistics.stdev(values)
