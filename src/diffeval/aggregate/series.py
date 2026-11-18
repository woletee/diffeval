"""Per-seed values and statuses for one metric."""


def series(per_seed: list[dict], name: str) -> dict:
    values = []
    statuses = []
    higher = None
    for seed in per_seed:
        metrics = seed.get("metrics", [])
        match = next((item for item in metrics if item["name"] == name), None)
        if match is None:
            values.append(None)
            statuses.append("skipped")
        elif match["status"] != "ok":
            values.append(None)
            statuses.append(match["status"])
        else:
            values.append(match["value"])
            statuses.append("ok")
        if match is not None and higher is None:
            higher = match.get("higher_is_better")
    return {"per_seed": values, "statuses": statuses, "higher_is_better": higher}
