"""Per-prompt means and the 100x benchmark total."""

import pytest

from diffeval.metrics.geneval2.means import geometric
from diffeval.metrics.geneval2.total import total

_LISTS = [[0.25, 1.0], [0.5, 0.5, 0.5]]


def test_means_and_total():
    assert geometric([0.25, 1.0]) == pytest.approx(0.5) and geometric([0.0, 0.9]) == 0.0
    assert total(_LISTS, "soft_tifa_gm") == pytest.approx(50.0)
    assert total(_LISTS, "soft_tifa_am") == pytest.approx(100 * (0.625 + 0.5) / 2)
    assert total([[1, 0]], "tifa") == pytest.approx(50.0)


def test_bad_input():
    for lists, method in (([[0.5]], "soft_tifa"), ([], "soft_tifa_gm"), ([[]], "soft_tifa_am")):
        with pytest.raises(ValueError):
            total(lists, method)
