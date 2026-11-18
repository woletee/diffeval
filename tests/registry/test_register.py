"""Register then get returns the same object."""

from diffeval.registry.lookup import get
from diffeval.registry.register import register
from diffeval.registry.tables import TASKS
from diffeval.registry.unregister import unregister


def test_register_then_get():
    class Alpha:
        pass

    register(TASKS, "alpha")(Alpha)
    try:
        assert get(TASKS, "alpha", "task") is Alpha
    finally:
        unregister(TASKS, "alpha")
