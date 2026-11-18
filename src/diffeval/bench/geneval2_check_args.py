"""Arguments for diffeval-check-geneval2."""

import argparse
from pathlib import Path


def check_args(argv):
    parser = argparse.ArgumentParser(prog="diffeval-check-geneval2", description="Rescore a geneval2 run with the reference evaluation.py and compare.")
    parser.add_argument("--run", required=True, type=Path, help="a diffeval output folder with an ok geneval2 result")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--tolerance", type=float, default=1e-4, help="largest allowed difference per question")
    return parser.parse_args(argv)
