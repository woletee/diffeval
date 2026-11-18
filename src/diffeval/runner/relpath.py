"""Path relative to the output directory."""

from pathlib import Path


def relpath(path: Path, output_dir: Path) -> str:
    return Path(path).relative_to(output_dir).as_posix()
