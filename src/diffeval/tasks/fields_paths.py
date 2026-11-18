"""reference_dir, cmmd_ref_embed, and clean_fid_stats."""

from pathlib import Path

from diffeval.tasks.errors import SuiteError


def _path(base: Path, value):
    if value is None:
        return None
    if not isinstance(value, str) or not value:
        raise SuiteError("path fields must be strings")
    path = Path(value)
    return path if path.is_absolute() else base / path


def paths(data: dict, base: Path) -> dict:
    stats = data.get("clean_fid_stats")
    if stats is not None and not isinstance(stats, dict):
        raise SuiteError("clean_fid_stats must be a mapping")
    return {
        "reference_dir": _path(base, data.get("reference_dir")),
        "cmmd_ref_embed": _path(base, data.get("cmmd_ref_embed")),
        "clean_fid_stats": stats,
    }
