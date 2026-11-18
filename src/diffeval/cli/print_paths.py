"""Print the table and the written output paths."""

from diffeval.report.console import console


def print_paths(folder, stream, body=None) -> None:
    if body is not None:
        print(console(body), end="", file=stream)
    print(folder / "results.json", file=stream)
    print(folder / "report.md", file=stream)
    print(folder / "report.html", file=stream)
    print(folder / "images", file=stream)
