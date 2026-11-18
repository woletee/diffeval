"""Values 2 and 4 give mean 3 and sample std sqrt(2)."""

import math

from diffeval.aggregate.table import aggregate


def test_mean_and_sample_std():
    per_seed = [
        {"metrics": [{"name": "score", "value": 2, "status": "ok"}]},
        {"metrics": [{"name": "score", "value": 4, "status": "ok"}]},
    ]
    row = aggregate(per_seed)["score"]
    assert row["mean"] == 3
    assert row["std"] == math.sqrt(2)
    assert row["n"] == 2
    assert row["status"] == "ok"
    assert row["std_ddof"] == 1
    assert row["per_seed"] == [2, 4]
