"""Write report.md and report.html."""

from pathlib import Path

from diffeval.report.html_page import html_page
from diffeval.report.markdown import markdown
from diffeval.runner.write_json import write_json


def write_reports(body: dict, output_dir) -> None:
    write_json(body, output_dir)
    folder = Path(output_dir)
    (folder / "report.md").write_text(markdown(body), encoding="utf-8")
    (folder / "report.html").write_text(html_page(body), encoding="utf-8")
