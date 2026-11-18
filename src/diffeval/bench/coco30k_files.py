"""The captions and reference embeddings cmmd-pytorch publishes for COCO-30k."""

import csv
from pathlib import Path

from diffeval.bench.fetch import fetch

CSV_URL = "https://huggingface.co/datasets/sayakpaul/sample-datasets/raw/main/coco_30k_randomly_sampled_2014_val.csv"
EMB_URL = "https://huggingface.co/datasets/sayakpaul/coco-30-val-2014/resolve/main/ref_embs_coco_30k.npy"
EMB_NAME = "ref_embs_coco_30k.npy"


def coco30k_captions(out: Path, limit: int) -> list[str]:
    fetch(EMB_URL, out / EMB_NAME)
    with fetch(CSV_URL, out / "captions.csv").open(encoding="utf-8") as handle:
        return [row["caption"].strip() for row in csv.DictReader(handle)][:limit]
