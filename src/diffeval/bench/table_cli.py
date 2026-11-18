"""diffeval-table: print a Markdown table from results.json files."""

import argparse

from diffeval.bench.table_row import HEADER, table_row


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="diffeval-table")
    parser.add_argument("results", nargs="+")
    args = parser.parse_args(argv)
    print("| " + " | ".join(HEADER) + " |")
    print("|" + " --- |" * len(HEADER))
    for path in args.results:
        print(table_row(path))
    return 0
