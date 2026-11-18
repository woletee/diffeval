"""diffeval-coco30k-images: write the 30k COCO reference PNGs for fid and kid (about 5 GB).

Needs the benchmarks extra: pip install "diffeval[benchmarks]".
"""

import argparse
import importlib.util
from pathlib import Path

from diffeval.bench.coco30k_export import coco30k_export


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="diffeval-coco30k-images")
    parser.add_argument("--out", required=True, type=Path)
    out = parser.parse_args(argv).out
    if any(importlib.util.find_spec(name) is None for name in ("pyarrow", "huggingface_hub")):
        print('install the benchmarks extra: pip install "diffeval[benchmarks]"')
        return 2
    print(f"wrote {coco30k_export(out)} images to {out}")
    return 0
