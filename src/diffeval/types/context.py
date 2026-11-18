"""Inputs a metric sees for one seed."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EvalContext:
    generated_dir: Path
    reference_dir: Path | None
    device: str
    seed: int
    clean_fid_stats: dict | None
    cmmd_ref_embed: Path | None
    batch_size: int
