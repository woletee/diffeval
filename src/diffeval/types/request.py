"""One image a backend is asked to generate."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class GenerationRequest:
    prompt_id: str
    prompt: str
    seed: int
    width: int
    height: int
    negative_prompt: str | None = None
    meta: dict | None = field(default=None, hash=False)
