"""A loaded prompt and seed suite."""

from dataclasses import dataclass
from pathlib import Path

from diffeval.types.prompt import Prompt


@dataclass(frozen=True)
class Suite:
    name: str
    description: str
    prompts: tuple[Prompt, ...]
    seeds: tuple[int, ...]
    width: int
    height: int
    metrics: tuple[str, ...]
    reference_dir: Path | None
    clean_fid_stats: dict | None
    cmmd_ref_embed: Path | None
    source: str
