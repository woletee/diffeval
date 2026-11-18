"""Two skipped seeds give a null mean, status skipped, and n 0."""

from diffeval.aggregate.table import aggregate


def test_two_skipped():
    per_seed = [
        {"metrics": [{"name": "score", "value": None, "status": "skipped"}]},
        {"metrics": [{"name": "score", "value": None, "status": "skipped"}]},
    ]
    row = aggregate(per_seed)["score"]
    assert row["mean"] is None
    assert row["status"] == "skipped"
    assert row["n"] == 0
    assert row["per_seed"] == [None, None]
