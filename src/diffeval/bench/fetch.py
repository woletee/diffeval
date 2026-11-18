"""Download a URL to a path once."""

import urllib.request
from pathlib import Path


def fetch(url: str, path: Path) -> Path:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        print(f"downloading {path.name}")
        urllib.request.urlretrieve(url, path)
    return path
