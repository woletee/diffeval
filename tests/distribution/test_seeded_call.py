"""Same seed, same NumPy draw, and a short folder skips."""

import numpy as np

from diffeval.metrics.distribution.seed_numpy import seeded
from diffeval.metrics.fid.metric import Fid
from diffeval.types.context import EvalContext


def _draw():
    return int(np.random.randint(0, 1_000_000))


def test_seed_restores_numpy_state():
    assert seeded(7, _draw) == seeded(7, _draw)
    np.random.seed(3)
    seeded(11, _draw)
    restored = int(np.random.randint(0, 1_000_000))
    np.random.seed(3)
    assert restored == int(np.random.randint(0, 1_000_000))


def test_fewer_than_two_images_skips(tmp_path):
    (tmp_path / "a.png").write_bytes(b"x")
    result = Fid().compute([], EvalContext(tmp_path, tmp_path, "cpu", 0, None, None, 1))
    text = " ".join(str(item) for item in result.protocol.values())
    assert result.status == "skipped" and "299" in text and "does not pre-resize" in text
