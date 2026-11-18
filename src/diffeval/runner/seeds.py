"""Score every seed."""

from diffeval.metrics.skipped import skipped
from diffeval.registry.lookup import get
from diffeval.registry.tables import METRICS
from diffeval.runner.one_seed import one_seed

_PENDING = {"clip_score", "cmmd", "fid", "kid"}


def _metric(name):
    try:
        return get(METRICS, name, "metric")()
    except KeyError:
        if name not in _PENDING:
            raise
        compute = lambda self, samples, context: skipped(name, "metric is not installed", None, {})
        return type("Missing", (), {"name": name, "compute": compute, "higher_is_better": None, "protocol": {}})()


def score_seeds(backend, suite, picked, output_dir, device):
    metrics = {name: _metric(name) for name in picked["metrics"]}
    return [one_seed(backend, suite, seed, picked, metrics, output_dir, device) for seed in picked["seeds"]]
