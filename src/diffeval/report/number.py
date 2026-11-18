"""Format a float, or n/a when the value is missing."""


def number(value) -> str:
    if value is None:
        return "n/a"
    return f"{float(value):.6g}"
