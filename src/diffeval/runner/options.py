"""Options for one evaluation run."""

from dataclasses import dataclass
from pathlib import Path

from diffeval.types.suite import Suite


@dataclass(frozen=True)
class RunOptions:
    suite: Suite
    backend: str
    backend_config: dict
    output_dir: Path
    seeds: tuple[int, ...] | None = None
    metrics: tuple[str, ...] | None = None
    width: int | None = None
    height: int | None = None


def chosen(options) -> dict:
    suite = options.suite
    return {"seeds": options.seeds or suite.seeds, "metrics": options.metrics or suite.metrics, "width": options.width or suite.width, "height": options.height or suite.height}
