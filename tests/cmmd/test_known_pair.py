"""The pair 0 and 10 matches the official diagonal-included RBF."""

import math

from diffeval.metrics.cmmd.mmd import mmd


def test_known_pair():
    value = mmd([[0.0]], [[10.0]])
    assert abs(value - 1000 * (2 - 2 * math.exp(-0.5))) < 1e-8
