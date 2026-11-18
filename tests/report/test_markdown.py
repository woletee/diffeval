"""Markdown rows include mean, std, direction, and n/a."""

from diffeval.report.markdown import markdown


def test_markdown_rows_and_null_mean():
    score = {"status": "ok", "mean": 3, "std": 2 ** 0.5, "per_seed": [2, 4], "higher_is_better": True}
    missing = {"status": "skipped", "mean": None, "std": None, "per_seed": [None], "higher_is_better": False}
    text = markdown({"suite": {"name": "demo"}, "aggregate": {"score": score, "missing": missing}})
    assert "| score | ok | 3 | 1.41421 | 2, 4 | higher |" in text
    assert "| missing | skipped | n/a | n/a | n/a | lower |" in text
