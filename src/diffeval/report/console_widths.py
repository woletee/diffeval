"""Column widths for the text table."""


def widths(rows: list[list[str]]) -> list[int]:
    return [max(len(row[index]) for row in rows) for index in range(len(rows[0]))]
