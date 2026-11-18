"""Arithmetic mean of successful values."""


def mean(values: list[float]):
    if not values:
        return None
    return sum(values) / len(values)
