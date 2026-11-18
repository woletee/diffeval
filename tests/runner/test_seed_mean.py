"""Seed values 2 and 4, plus an error metric."""

from diffeval.metrics.ok import ok
from diffeval.registry.register import register
from diffeval.registry.tables import METRICS
from diffeval.registry.unregister import unregister
from diffeval.runner.options import RunOptions
from diffeval.runner.run import run_evaluation
from diffeval.tasks.load_path import load_path


def test_seed_mean(tmp_path):
    (tmp_path / "s.yaml").write_text("name: demo\nseeds: [2, 4]\nwidth: 8\nheight: 8\nmetrics: [seed_metric, boom]\nprompts:\n- {id: red_cube, prompt: red}\n- {id: blue_sphere, prompt: blue}\n")
    specs = (("seed_metric", lambda self, samples, context: ok("seed_metric", context.seed, True, {})), ("boom", lambda *_a: (_ for _ in ()).throw(RuntimeError("boom"))))
    for name, fn in specs:
        register(METRICS, name)(type(name, (), {"name": name, "compute": fn, "higher_is_better": True, "protocol": {}}))
    try:
        body = run_evaluation(RunOptions(load_path(tmp_path / "s.yaml"), "dummy", {}, tmp_path / "out"))
    finally:
        unregister(METRICS, "seed_metric"), unregister(METRICS, "boom")
    score = body["aggregate"]["seed_metric"]
    out = tmp_path / "out"
    pngs = all((out / f"images/seed_{seed}/{pid}.png").is_file() for seed in (2, 4) for pid in ("red_cube", "blue_sphere"))
    assert score["mean"] == 3 and abs(score["std"] ** 2 - 2) < 1e-9 and score["per_seed"] == [2, 4] and body["aggregate"]["boom"]["status"] == "error" and pngs and (out / "results.json").is_file() and body["per_seed"][0]["samples"][0]["path"] == "images/seed_2/red_cube.png"
