"""Unregister removes a name."""

import pytest

from diffeval.registry.lookup import get
from diffeval.registry.names import names
from diffeval.registry.register import register
from diffeval.registry.tables import TASKS
from diffeval.registry.unregister import unregister


def test_unregister_removes_name():
    class Gone:
        pass

    register(TASKS, "gone")(Gone)
    unregister(TASKS, "gone")
    assert "gone" not in names(TASKS)
    with pytest.raises(KeyError):
        get(TASKS, "gone", "task")
