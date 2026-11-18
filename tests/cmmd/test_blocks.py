"""Blocked MMD equals the one-shot formula."""

import numpy as np

from diffeval.metrics.cmmd import mmd as module


def _direct(x, y):
    k = lambda a, b: np.exp(-((a[:, None, :] - b[None, :, :]) ** 2).sum(-1) / 200).mean()
    return 1000 * (k(x, x) + k(y, y) - 2 * k(x, y))


def test_blocks(monkeypatch):
    rng = np.random.default_rng(0)
    x, y = rng.normal(size=(7, 3)), rng.normal(size=(5, 3)) + 1
    monkeypatch.setattr(module, "BLOCK", 2)
    assert abs(module.mmd(x, y) - _direct(x, y)) < 1e-9
