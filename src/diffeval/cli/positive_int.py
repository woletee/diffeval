"""Parse a positive int for --width and --height."""

from argparse import ArgumentTypeError


def positive_int(text: str) -> int:
    try:
        value = int(text)
    except ValueError:
        raise ArgumentTypeError(f"expected a positive integer, got {text!r}") from None
    if value < 1:
        raise ArgumentTypeError(f"expected a positive integer, got {text!r}")
    return value
