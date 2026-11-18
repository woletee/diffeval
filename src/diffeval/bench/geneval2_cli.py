"""diffeval-geneval2: write <out>/suite.yaml with the GenEval 2 prompts and their questions."""

import argparse
from pathlib import Path

import yaml

from diffeval.bench.geneval2_files import NOTICE, geneval2_rows
from diffeval.bench.geneval2_suite import geneval2_suite


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="diffeval-geneval2", epilog=NOTICE)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--limit", type=int, default=800, help="first N prompts (default all 800)")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--size", type=int, default=512, help="image width and height")
    args = parser.parse_args(argv)
    print(NOTICE)
    suite = geneval2_suite(geneval2_rows(args.out, args.limit), args.seed, args.size)
    (args.out / "suite.yaml").write_text(yaml.safe_dump(suite, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"wrote {args.out / 'suite.yaml'} with {len(suite['prompts'])} prompts")
    return 0
