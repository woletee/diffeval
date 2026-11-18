"""CI JSON records versions, a null GPU, and dummy attention."""

from diffeval.metrics.ok import ok
from diffeval.registry.register import register
from diffeval.registry.tables import METRICS
from diffeval.registry.unregister import unregister
from diffeval.runner.options import RunOptions
from diffeval.runner.run import run_evaluation
from diffeval.tasks.load_path import load_path


def test_versions_gpu_attention(tmp_path):
    (tmp_path / "s.yaml").write_text("name: demo\nseeds: [0]\nmetrics: [seed_metric]\nprompts:\n- {id: red_cube, prompt: red}\n")
    metric = type("S", (), {"name": "seed_metric", "compute": lambda self, samples, context: ok("seed_metric", 1, True, {}), "higher_is_better": True, "protocol": {}})
    register(METRICS, "seed_metric")(metric)
    try:
        body = run_evaluation(RunOptions(load_path(tmp_path / "s.yaml"), "dummy", {}, tmp_path / "out"))
    finally:
        unregister(METRICS, "seed_metric")
    versions = body["versions"]
    present = ("torch", "diffusers", "transformers", "clean-fid", "numpy", "pillow", "pyyaml", "accelerate", "python")
    assert versions["diffeval"] and versions["torch"] is None and all(key in versions for key in present)
    assert body["system"]["gpu"] is None and body["system"]["torch_attention"] is None
    assert body["backend"]["attention_backend"] == "none"
