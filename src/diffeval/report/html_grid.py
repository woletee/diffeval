"""Image grids grouped by prompt."""

from html import escape

from diffeval.report.html_figure import html_figure


def _samples(body, prompt_id):
    return [sample for seed in body["per_seed"] for sample in seed["samples"] if sample["prompt_id"] == prompt_id]


def html_grid(body: dict) -> str:
    blocks = []
    for prompt in body["suite"]["prompts"]:
        figures = "".join(html_figure(sample) for sample in _samples(body, prompt["id"]))
        heading = escape(prompt["id"])
        text = escape(prompt["prompt"])
        blocks.append(f'<section><h2>{heading}</h2><p>{text}</p>{figures}</section>')
    return "\n".join(blocks)
