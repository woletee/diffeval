"""One aggregate row."""

from diffeval.aggregate.mean import mean
from diffeval.aggregate.sample_std import sample_std
from diffeval.aggregate.series import series


def _status(statuses: list) -> str:
    ok_n = sum(item == "ok" for item in statuses)
    if statuses and ok_n == len(statuses):
        return "ok"
    if ok_n:
        return "partial"
    if statuses and not any(item == "error" for item in statuses):
        return "skipped"
    return "error"


def row(per_seed: list[dict], name: str) -> dict:
    data = series(per_seed, name)
    values = [item for item in data["per_seed"] if item is not None]
    data.update(mean=mean(values), std=sample_std(values), n=len(values))
    data["status"] = _status(data.pop("statuses"))
    data["name"] = name
    data["std_ddof"] = 1
    return data
