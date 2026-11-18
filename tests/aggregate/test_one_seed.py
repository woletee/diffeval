"""One value gives that mean and a null std."""

from diffeval.aggregate.table import aggregate


def test_one_seed_null_std():
    per_seed = [{"metrics": [{"name": "score", "value": 2, "status": "ok"}]}]
    row = aggregate(per_seed)["score"]
    assert row["mean"] == 2
    assert row["std"] is None
    assert row["n"] == 1
