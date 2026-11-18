"""Drop one registry entry."""


def unregister(table: dict, name: str) -> None:
    table.pop(name, None)
