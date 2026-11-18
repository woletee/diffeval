"""Dispatch diffeval commands and return an exit code."""

from diffeval.cli.command_list import command_list
from diffeval.cli.command_run import command_run
from diffeval.cli.parser import build_parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "list":
        return command_list(args)
    return command_run(args)
