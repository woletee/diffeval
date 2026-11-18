"""Minimum-variance RBF MMD, sigma 10, scale 1000, in row blocks."""

import numpy as np

_SIGMA = 10
_SCALE = 1000
BLOCK = 2048


def _kernel(x, y, x_sq, y_sq, gamma):
    total = 0.0
    for start in range(0, len(x), BLOCK):
        dist = -2 * (x[start:start + BLOCK] @ y.T) + x_sq[start:start + BLOCK, None] + y_sq[None, :]
        total += np.exp(-gamma * dist).sum()
    return total / (len(x) * len(y))


def mmd(x, y) -> float:
    x, y = np.asarray(x, dtype=np.float64), np.asarray(y, dtype=np.float64)
    gamma = 1 / (2 * _SIGMA**2)
    x_sq, y_sq = np.sum(x * x, axis=1), np.sum(y * y, axis=1)
    cross = _kernel(x, y, x_sq, y_sq, gamma)
    return float(_SCALE * (_kernel(x, x, x_sq, x_sq, gamma) + _kernel(y, y, y_sq, y_sq, gamma) - 2 * cross))
