"""One Markdown table row."""

from diffeval.report.direction import direction
from diffeval.report.number import number


def markdown_row(name: str, row: dict) -> str:
    seeds = ", ".join(number(item) for item in row["per_seed"])
    cells = (name, row["status"], number(row["mean"]), number(row["std"]), seeds, direction(row.get("higher_is_better")))
    return "| " + " | ".join(cells) + " |"
