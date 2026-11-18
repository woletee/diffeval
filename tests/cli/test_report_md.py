"""The run command prints the table and writes report.md."""

from diffeval.cli.main import main
from diffeval.metrics.ok import ok
from diffeval.registry.register import register
from diffeval.registry.tables import METRICS
from diffeval.registry.unregister import unregister


def test_prints_table_and_writes_markdown(tmp_path, capsys):
    suite = tmp_path / "s.yaml"
    suite.write_text("name: demo\nseeds: [1]\nwidth: 8\nheight: 8\nmetrics: [seed_metric]\nprompts:\n- {id: red_cube, prompt: red}\n")
    metric = {"name": "seed_metric", "compute": lambda self, samples, context: ok("seed_metric", 1, True, {}), "higher_is_better": True, "protocol": {}}
    register(METRICS, "seed_metric")(type("S", (), metric))
    out = tmp_path / "out"
    try:
        code = main(["run", "--suite", str(suite), "--backend", "dummy", "--output", str(out)])
    finally:
        unregister(METRICS, "seed_metric")
    text = (out / "report.md").read_text()
    captured = capsys.readouterr().out
    assert code == 0 and "| seed_metric | ok | 1 |" in text and "higher" in text
    assert "seed_metric" in captured and "report.md" in captured
