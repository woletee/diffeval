"""Parse a comma-separated list of distinct seeds."""

from argparse import ArgumentTypeError


def csv_ints(text: str) -> tuple[int, ...]:
    parts = [item.strip() for item in text.split(",") if item.strip()]
    if not parts or any(not item.lstrip("-").isdigit() for item in parts):
        raise ArgumentTypeError(f"expected integers, got {text!r}")
    seeds = tuple(int(item) for item in parts)
    if len(set(seeds)) != len(seeds):
        raise ArgumentTypeError(f"seeds must not repeat, got {text!r}")
    return seeds
