"""geometric matches scipy.stats.gmean, which the reference uses."""

import random

import pytest


def test_matches_scipy():
    gmean = pytest.importorskip("scipy.stats").gmean
    from diffeval.metrics.geneval2.means import geometric

    rng = random.Random(0)
    for _ in range(200):
        scores = [rng.random() for _ in range(rng.randint(1, 12))]
        assert geometric(scores) == pytest.approx(float(gmean(scores)), rel=1e-12)
    assert geometric([0.0, 0.5]) == float(gmean([0.0, 0.5]))
