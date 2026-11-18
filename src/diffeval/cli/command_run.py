"""Resolve a suite, run it, and print output paths."""

import sys

from diffeval.cli.config import backend_config, backend_name
from diffeval.cli.output_dir import output_dir
from diffeval.cli.print_paths import print_paths
from diffeval.runner.options import RunOptions
from diffeval.runner.run import run_evaluation
from diffeval.tasks.resolve import resolve


def command_run(args, stream=None) -> int:
    out = stream or sys.stdout
    try:
        suite = resolve(args.suite)
        name = backend_name(args)
        folder = output_dir(args.output, suite.name, name)
        options = RunOptions(suite, name, backend_config(args), folder, args.seeds, args.metrics, args.width, args.height)
        body = run_evaluation(options)
    except Exception as exc:
        print(exc, file=out)
        return 2
    print_paths(folder, out, body)
    return 2 if args.strict and any(row["status"] != "ok" for row in body["aggregate"].values()) else 0
