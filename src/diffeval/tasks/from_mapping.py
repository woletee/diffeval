"""Build a Suite from a mapping."""

from pathlib import Path

from diffeval.tasks.build_suite import build_suite
from diffeval.tasks.fields_metrics import metrics
from diffeval.tasks.fields_paths import paths
from diffeval.tasks.fields_prompts import prompts
from diffeval.tasks.fields_seeds import seeds
from diffeval.tasks.fields_size import width_and_height
from diffeval.tasks.fields_text import name_and_description


def from_mapping(data: dict, source: str, base: Path):
    fields = {"source": source}
    fields.update(name_and_description(data))
    fields.update(width_and_height(data))
    fields.update(seeds(data))
    fields.update(prompts(data))
    fields.update(metrics(data))
    fields.update(paths(data, base))
    return build_suite(fields)
