"""Generate, save, and score one seed."""

from pathlib import Path

from diffeval.runner.generate_save import generate_save
from diffeval.runner.requests import requests_for
from diffeval.runner.safe_metric import safe_metric
from diffeval.types.context import EvalContext


def _public(sample) -> dict:
    return {"prompt_id": sample.prompt_id, "prompt": sample.prompt, "seed": sample.seed, "width": sample.width, "height": sample.height, "path": sample.path, "negative_prompt": sample.negative_prompt}


def one_seed(backend, suite, seed, picked, metrics, output_dir, device):
    folder = Path(output_dir) / "images" / f"seed_{seed}"
    samples = generate_save(backend, requests_for(suite, seed, picked["width"], picked["height"]), folder, output_dir)
    context = EvalContext(folder, suite.reference_dir, device, seed, suite.clean_fid_stats, suite.cmmd_ref_embed, backend.describe()["batch_size"])
    scored = [safe_metric(metrics[name], samples, context) for name in picked["metrics"]]
    return {"seed": seed, "samples": [_public(item) for item in samples], "metrics": scored}
