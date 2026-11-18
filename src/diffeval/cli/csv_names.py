"""Parse a comma-separated list of names."""


def csv_names(text: str) -> tuple[str, ...]:
    parts = tuple(item.strip() for item in text.split(",") if item.strip())
    if not parts:
        raise ValueError("expected at least one name")
    return parts
