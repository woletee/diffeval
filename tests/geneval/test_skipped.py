"""geneval returns skipped with the six tag keys."""

from diffeval.cli.main import main
from diffeval.metrics.geneval.metric import Geneval
from diffeval.metrics.geneval.tags import TAGS


def test_compute_skips():
    result = Geneval().compute([], None)
    tags = result.details["by_tag"]
    assert result.status == "skipped" and result.value is None
    assert set(tags) == set(TAGS) and all(tags[name] is None for name in TAGS)


def test_list_includes_geneval(capsys):
    assert main(["list", "metrics"]) == 0
    text = capsys.readouterr().out
    assert "geneval" in text and "vbench" not in text
