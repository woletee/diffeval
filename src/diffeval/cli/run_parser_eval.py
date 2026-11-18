"""Evaluation flags for diffeval run."""

from diffeval.cli.csv_ints import csv_ints
from diffeval.cli.csv_names import csv_names
from diffeval.cli.positive_int import positive_int


def add_eval_flags(parser) -> None:
    parser.add_argument("--suite", required=True)
    parser.add_argument("--seeds", type=csv_ints, default=None)
    parser.add_argument("--metrics", type=csv_names, default=None)
    parser.add_argument("--width", type=positive_int, default=None)
    parser.add_argument("--height", type=positive_int, default=None)
    parser.add_argument("--output", default=None)
    parser.add_argument("--strict", action="store_true")
