"""Print registry names and descriptions."""


def print_registered(table: dict, stream) -> None:
    for name in sorted(table):
        print(f"{name}\t{getattr(table[name], 'description', '')}", file=stream)
