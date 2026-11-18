"""Write the COCO-30k reference images from the dataset's parquet shards."""

import io
from pathlib import Path

from PIL import Image


def coco30k_export(out: Path) -> int:
    import pyarrow.parquet as pq
    from huggingface_hub import snapshot_download
    out.mkdir(parents=True, exist_ok=True)
    root = Path(snapshot_download("sayakpaul/coco-30-val-2014", repo_type="dataset", allow_patterns=["data/*.parquet"]))
    count = 0
    for shard in sorted((root / "data").glob("*.parquet")):
        for row in pq.read_table(shard, columns=["image"]).column("image").to_pylist():
            Image.open(io.BytesIO(row["bytes"])).convert("RGB").save(out / f"ref_{count:05d}.png")
            count += 1
    return count
