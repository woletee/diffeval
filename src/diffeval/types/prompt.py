"""One prompt in a suite."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Prompt:
    id: str
    prompt: str
    negative_prompt: str | None = None
    meta: dict | None = field(default=None, hash=False)
