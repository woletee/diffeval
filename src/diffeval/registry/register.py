"""Register one object under one name."""


def register(table: dict, name: str):
    def decorator(obj):
        if name in table and table[name] is not obj:
            raise ValueError(f"{name} is already registered")
        table[name] = obj
        return obj

    return decorator
