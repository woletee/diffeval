"""Look up a registered object by name."""


def get(table: dict, name: str, kind: str):
    try:
        return table[name]
    except KeyError:
        known = ", ".join(sorted(table)) or "(none)"
        raise KeyError(f"Unknown {kind} {name!r}. Known: {known}") from None
