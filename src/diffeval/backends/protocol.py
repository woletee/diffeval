"""Backend contract."""

from typing import Protocol

from diffeval.types.request import GenerationRequest
from diffeval.types.sample import Sample


class Backend(Protocol):
    description: str

    def from_config(self, config: dict) -> "Backend": ...
    def prepare(self) -> None: ...
    def generate(self, requests: list[GenerationRequest]) -> list[Sample]: ...
    def describe(self) -> dict: ...
