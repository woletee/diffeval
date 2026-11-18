"""diffeval-coco30k: write <out>/suite.yaml for the cmmd-pytorch COCO-30k protocol."""

import argparse
from pathlib import Path

import yaml

from diffeval.bench.coco30k_files import coco30k_captions
from diffeval.bench.coco30k_suite import coco30k_suite


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="diffeval-coco30k")
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--limit", type=int, default=30000, help="first N captions (default all 30000)")
    parser.add_argument("--seed", type=int, default=2024, help="cmmd-pytorch uses 2024")
    parser.add_argument("--reference-images", type=Path, default=None, help="COCO image folder; adds fid and kid")
    args = parser.parse_args(argv)
    refs = None if args.reference_images is None else args.reference_images.resolve()
    suite = coco30k_suite(coco30k_captions(args.out, args.limit), args.seed, refs)
    (args.out / "suite.yaml").write_text(yaml.safe_dump(suite, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"wrote {args.out / 'suite.yaml'} with {len(suite['prompts'])} prompts and metrics {suite['metrics']}")
    return 0
