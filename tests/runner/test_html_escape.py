"""HTML escapes prompts and points each image at its PNG."""

from diffeval.metrics.ok import ok
from diffeval.registry.register import register
from diffeval.registry.tables import METRICS
from diffeval.registry.unregister import unregister
from diffeval.runner.options import RunOptions
from diffeval.runner.run import run_evaluation
from diffeval.tasks.load_path import load_path


def test_html_escapes_prompt(tmp_path):
    (tmp_path / "s.yaml").write_text('name: demo\nseeds: [1, 2]\nwidth: 8\nheight: 8\nmetrics: [seed_metric]\nprompts:\n- {id: red_cube, prompt: "red <script>alert(1)</script>"}\n- {id: blue_sphere, prompt: blue}\n')
    metric = {"name": "seed_metric", "compute": lambda self, samples, context: ok("seed_metric", 1, True, {}), "higher_is_better": True, "protocol": {}}
    register(METRICS, "seed_metric")(type("S", (), metric))
    try:
        body = run_evaluation(RunOptions(load_path(tmp_path / "s.yaml"), "dummy", {}, tmp_path / "out"))
    finally:
        unregister(METRICS, "seed_metric")
    html = (tmp_path / "out" / "report.html").read_text()
    paths = [sample["path"] for seed in body["per_seed"] for sample in seed["samples"]]
    note = "Metric numbers have to be checked against the published reference before they are compared to a paper."
    assert "&lt;script&gt;" in html and "<script>" not in html and html.count("<img ") == len(paths) == 4 and note in html
    assert all(f'src="{path}"' in html and (tmp_path / "out" / path).is_file() for path in paths) and "smoke suite" in html and "http" not in html
