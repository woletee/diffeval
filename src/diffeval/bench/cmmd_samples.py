"""The six cmmd-pytorch sample PNGs (Apache-2.0) behind its 7.696 check."""

from pathlib import Path

from diffeval.bench.fetch import fetch

BASE = "https://raw.githubusercontent.com/sayakpaul/cmmd-pytorch/main"
FILES = {"reference_images": "glowing_512_1", "generated_images": "glowing_512_2"}


def cmmd_samples(root: Path) -> tuple[Path, Path]:
    for folder, stem in FILES.items():
        for suffix in ("", "_copy", "_copy_2"):
            fetch(f"{BASE}/{folder}/{stem}{suffix}.png", root / folder / f"{stem}{suffix}.png")
    return root / "reference_images", root / "generated_images"
