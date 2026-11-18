"""load_judge returns None when transformers is missing, so the metric can skip."""

import sys

from diffeval.metrics.geneval2 import judge_load


def test_missing_transformers(monkeypatch):
    monkeypatch.setitem(sys.modules, "transformers", None)
    monkeypatch.setattr(judge_load, "_CACHE", {})
    assert judge_load.load_judge("some/model") is None
    assert judge_load.MODEL == "Qwen/Qwen3-VL-8B-Instruct"
