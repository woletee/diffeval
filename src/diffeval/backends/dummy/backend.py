"""Bind and register the dummy backend."""

from diffeval.backends.dummy.describe import describe as describe_config
from diffeval.backends.dummy.from_config import from_config as read_config
from diffeval.backends.dummy.generate import generate as render_batch
from diffeval.backends.noop_prepare import prepare as noop
from diffeval.registry.register import register
from diffeval.registry.tables import BACKENDS


@register(BACKENDS, "dummy")
class DummyBackend:
    description = "Deterministic RGB images for CPU tests."

    def __init__(self, config: dict):
        self.config = config

    def prepare(self) -> None:
        noop()

    def generate(self, requests):
        return render_batch(requests, self.config["batch_size"])

    def describe(self) -> dict:
        return describe_config(self.config)

    @staticmethod
    def from_config(config: dict):
        return DummyBackend(read_config(config))
