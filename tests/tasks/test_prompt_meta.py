"""A prompt's meta mapping loads from YAML and reaches the sample."""

from pathlib import Path

import diffeval
from diffeval.registry.tables import BACKENDS
from diffeval.runner.requests import requests_for
from diffeval.tasks.load_path import load_path

_YAML = "name: demo\nseeds: [0]\nprompts:\n- {id: a, prompt: a cat, meta: {skills: [object], vqa_list: [['Is there a cat?', 'yes']]}}\n- {id: b, prompt: a dog}\n"
_META = {"skills": ["object"], "vqa_list": [["Is there a cat?", "yes"]]}


def test_meta_reaches_sample(tmp_path: Path):
    path = tmp_path / "suite.yaml"
    path.write_text(_YAML, encoding="utf-8")
    suite = load_path(path)
    assert (suite.prompts[0].meta, suite.prompts[1].meta) == (_META, None)
    samples = BACKENDS["dummy"].from_config({}).generate(requests_for(suite, 0, 8, 8))
    assert (samples[0].meta, samples[1].meta) == (_META, None)
