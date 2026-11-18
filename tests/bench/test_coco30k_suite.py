"""The COCO-30k suite mapping loads as a diffeval suite."""

import yaml

from diffeval.bench.coco30k_suite import coco30k_suite
from diffeval.tasks.load_path import load_path


def test_suite_loads(tmp_path):
    data = coco30k_suite(["a dog", "a cat"], 2024, tmp_path / "refs")
    (tmp_path / "suite.yaml").write_text(yaml.safe_dump(data), encoding="utf-8")
    suite = load_path(tmp_path / "suite.yaml")
    assert suite.name == "coco30k-2" and suite.seeds == (2024,) and [p.id for p in suite.prompts] == ["c00000", "c00001"]
    assert suite.metrics == ("clip_score", "cmmd", "fid", "kid") and suite.cmmd_ref_embed == tmp_path / "ref_embs_coco_30k.npy"
