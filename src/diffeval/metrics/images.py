"""List image files in a directory."""

from pathlib import Path

_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}


def list_images(folder) -> list[Path]:
    root = Path(folder)
    if not root.is_dir():
        return []
    return sorted(path for path in root.iterdir() if path.suffix.lower() in _SUFFIXES)
