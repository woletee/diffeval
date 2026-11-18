"""One generated image and the request that produced it."""

from dataclasses import dataclass


@dataclass
class Sample:
    prompt_id: str
    prompt: str
    seed: int
    width: int
    height: int
    image: object | None
    path: str | None
    negative_prompt: str | None = None
    meta: dict | None = None
