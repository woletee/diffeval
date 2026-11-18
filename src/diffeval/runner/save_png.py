"""Write one uint8 RGB PNG."""

from pathlib import Path


def save_png(image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(path, format="PNG")
