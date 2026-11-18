"""Default directory outputs/<utc>-<suite>-<backend>."""

from datetime import datetime, timezone
from pathlib import Path


def output_dir(explicit, suite_name: str, backend: str) -> Path:
    if explicit:
        return Path(explicit)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    label = f"{stamp}-{suite_name}-{backend}".replace(" ", "_").replace("/", "_")
    return Path("outputs") / label
