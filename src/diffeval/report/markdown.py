"""Markdown report for one run."""

from diffeval.report.markdown_row import markdown_row


def markdown(body: dict) -> str:
    header = "| metric | status | mean | std | per-seed | direction |"
    rule = "| --- | --- | --- | --- | --- | --- |"
    rows = [markdown_row(name, row) for name, row in body["aggregate"].items()]
    title = f"# {body['suite']['name']}"
    return "\n".join([title, "", header, rule, *rows, ""]) + "\n"
