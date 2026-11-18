"""Identical embeddings score 0, and a missing reference skips."""

from diffeval.metrics.cmmd.metric import Cmmd
from diffeval.metrics.cmmd.mmd import mmd
from diffeval.metrics.count_warning import count_warning
from diffeval.types.context import EvalContext


def test_identical_embeddings_score_zero():
    rows = [[1.0, 2.0], [3.0, 4.0]]
    assert mmd(rows, rows) == 0.0


def test_skips_without_reference(tmp_path):
    context = EvalContext(tmp_path, None, "cpu", 0, None, None, 1)
    result = Cmmd().compute([], context)
    text = " ".join(str(item) for item in result.protocol.values())
    assert result.status == "skipped" and result.value is None and "336" in text and "L2-normalized" in text and "not L2" not in text and "center square crop" in text


def test_small_set_warns():
    text = count_warning(4)
    assert text is not None and "COCO" in text and "30000" in text
