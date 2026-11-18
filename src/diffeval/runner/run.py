"""Run one evaluation and write results.json."""

from pathlib import Path

from diffeval.aggregate.table import aggregate
from diffeval.registry.lookup import get
from diffeval.registry.tables import BACKENDS
from diffeval.runner.metric_device import metric_device
from diffeval.runner.options import chosen
from diffeval.runner.payload import payload
from diffeval.runner.seeds import score_seeds
from diffeval.runner.write_reports import write_reports


def run_evaluation(options):
    picked = chosen(options)
    backend = get(BACKENDS, options.backend, "backend").from_config(options.backend_config)
    backend.prepare()
    device = metric_device(options.backend_config.get("device"))
    out = Path(options.output_dir)
    per_seed = score_seeds(backend, options.suite, picked, out, device)
    body = payload(options, backend, device, picked["seeds"], per_seed, aggregate(per_seed))
    write_reports(body, out)
    return body
