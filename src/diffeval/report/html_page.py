"""Fill the static HTML template."""

from html import escape
from pathlib import Path

from diffeval.report.html_grid import html_grid
from diffeval.report.html_row import html_row


def html_page(body: dict) -> str:
    rows = "\n".join(html_row(name, row) for name, row in body["aggregate"].items())
    template = (Path(__file__).parent / "templates" / "page.html").read_text(encoding="utf-8")
    text = template.replace("{{TITLE}}", escape(str(body["suite"]["name"])))
    text = text.replace("{{ROWS}}", rows)
    return text.replace("{{GRID}}", html_grid(body))
