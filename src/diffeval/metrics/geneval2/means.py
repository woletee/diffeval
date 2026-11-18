"""Arithmetic and geometric means of one prompt's question scores."""

import math


def arithmetic(scores: list[float]) -> float:
    if not scores:
        raise ValueError("a prompt needs at least one question score")
    return sum(scores) / len(scores)


def geometric(scores: list[float]) -> float:
    if not scores:
        raise ValueError("a prompt needs at least one question score")
    if min(scores) <= 0:
        return 0.0
    return math.exp(sum(math.log(score) for score in scores) / len(scores))
