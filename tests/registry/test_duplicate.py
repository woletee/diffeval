"""A second object on the same name raises."""

import pytest

from diffeval.registry.register import register
from diffeval.registry.tables import METRICS
from diffeval.registry.unregister import unregister


def test_duplicate_registration():
    class First:
        pass

    class Second:
        pass

    register(METRICS, "dup")(First)
    try:
        with pytest.raises(ValueError):
            register(METRICS, "dup")(Second)
    finally:
        unregister(METRICS, "dup")
