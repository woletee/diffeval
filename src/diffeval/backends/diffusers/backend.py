"""Bind and register the diffusers backend."""

from diffeval.backends.diffusers.describe import describe as describe_state
from diffeval.backends.diffusers.from_config import from_config as read_config
from diffeval.backends.diffusers.generate import generate as render
from diffeval.registry.register import register
from diffeval.registry.tables import BACKENDS


@register(BACKENDS, "diffusers")
class DiffusersBackend:
    description = "Diffusers AutoPipelineForText2Image."

    def __init__(self, config: dict):
        self.config, self.state = config, {}

    def prepare(self) -> None:
        from diffeval.backends.diffusers.load_pipe import prepare_pipe
        self.state = prepare_pipe(self.config)

    def generate(self, requests):
        return render(self.state["pipe"], requests, self.config["batch_size"], self.state["sampling"]["steps"], self.state["sampling"]["guidance"])

    def describe(self) -> dict:
        return describe_state(self.config, self.state)

    @staticmethod
    def from_config(config: dict):
        return DiffusersBackend(read_config(config))
