"""Plain text table of aggregate scores."""

from diffeval.report.console_widths import widths
from diffeval.report.direction import direction
from diffeval.report.number import number


def _cells(name, row) -> list[str]:
    seeds = ",".join(number(item) for item in row["per_seed"])
    return [name, row["status"], number(row["mean"]), number(row["std"]), seeds, direction(row.get("higher_is_better"))]


def console(body: dict) -> str:
    header = ["metric", "status", "mean", "std", "per-seed", "direction"]
    rows = [header, *[_cells(name, row) for name, row in body["aggregate"].items()]]
    size = widths(rows)
    lines = ["  ".join(cell.ljust(size[i]) for i, cell in enumerate(row)) for row in rows]
    return "\n".join(lines) + "\n"
