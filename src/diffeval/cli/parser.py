"""argparse for run and list."""

import argparse

from diffeval.cli.run_parser_eval import add_eval_flags
from diffeval.cli.run_parser_model import add_model_flags


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="diffeval")
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run")
    add_model_flags(run)
    add_eval_flags(run)
    listed = commands.add_parser("list")
    listed.add_argument("kind", choices=("tasks", "metrics", "backends"))
    return parser
