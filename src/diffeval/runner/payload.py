"""Assemble the results object."""

from datetime import datetime, timezone

from diffeval.system.describe import describe as system_info
from diffeval.system.versions import versions


def _text(path):
    return None if path is None else str(path)


def _protocols(per_seed):
    found = {}
    for seed in per_seed:
        for metric in seed["metrics"]:
            found.setdefault(metric["name"], metric.pop("protocol", {}))
    return found


def payload(options, backend, device, seeds, per_seed, aggregate) -> dict:
    suite = options.suite
    prompts = [{"id": item.id, "prompt": item.prompt, "negative_prompt": item.negative_prompt} for item in suite.prompts]
    info = {"name": suite.name, "description": suite.description, "source": suite.source, "width": options.width or suite.width, "height": options.height or suite.height, "prompts": prompts, "reference_dir": _text(suite.reference_dir), "clean_fid_stats": suite.clean_fid_stats, "cmmd_ref_embed": _text(suite.cmmd_ref_embed)}
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {"schema_version": 1, "created_at": stamp, "suite": info, "backend": backend.describe(), "metric_device": device, "seeds": list(seeds), "versions": versions(), "system": system_info(), "metric_protocols": _protocols(per_seed), "per_seed": per_seed, "aggregate": aggregate, "outputs": ["results.json", "report.md", "report.html"]}
