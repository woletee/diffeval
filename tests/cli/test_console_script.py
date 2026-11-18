"""The console script writes results.json and honors --seeds."""

import json

from diffeval.cli.main import main
from diffeval.metrics.ok import ok
from diffeval.registry.register import register
from diffeval.registry.tables import METRICS
from diffeval.registry.unregister import unregister


def test_console_script(tmp_path, capsys):
    suite = tmp_path / "s.yaml"
    suite.write_text("name: demo\nseeds: [0, 1]\nwidth: 8\nheight: 8\nmetrics: [seed_metric]\nprompts:\n- {id: red_cube, prompt: red}\n")
    metric = {"name": "seed_metric", "compute": lambda self, samples, context: ok("seed_metric", 1, True, {}), "higher_is_better": True, "protocol": {}}
    register(METRICS, "seed_metric")(type("SeedMetric", (), metric))
    out = tmp_path / "out"
    try:
        code = main(["run", "--suite", str(suite), "--backend", "dummy", "--output", str(out), "--seeds", "4"])
    finally:
        unregister(METRICS, "seed_metric")
    body = json.loads((out / "results.json").read_text())
    png = out / "images" / "seed_4" / "red_cube.png"
    assert code == 0 and body["seeds"] == [4] and png.is_file() and not (out / "images" / "seed_0").exists()
    assert "results.json" in capsys.readouterr().out
