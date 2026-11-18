"""Unknown names raise KeyError listing known keys."""

import pytest

from diffeval.registry.lookup import get
from diffeval.registry.register import register
from diffeval.registry.tables import BACKENDS
from diffeval.registry.unregister import unregister


def test_missing_name_lists_known():
    class Known:
        pass

    register(BACKENDS, "known")(Known)
    try:
        with pytest.raises(KeyError, match="known") as caught:
            get(BACKENDS, "missing", "backend")
        assert "backend" in str(caught.value)
        assert "Known:" in str(caught.value)
    finally:
        unregister(BACKENDS, "known")
