"""List tasks, metrics, or backends."""

import sys

from diffeval.cli.print_registered import print_registered
from diffeval.registry.tables import BACKENDS, METRICS, TASKS

_TABLES = {"tasks": TASKS, "metrics": METRICS, "backends": BACKENDS}


def command_list(args, stream=None) -> int:
    print_registered(_TABLES[args.kind], stream or sys.stdout)
    return 0
