"""Metric names in first-seen order."""


def names(per_seed: list[dict]) -> list[str]:
    found = []
    for seed in per_seed:
        for metric in seed.get("metrics", []):
            name = metric["name"]
            if name not in found:
                found.append(name)
    return found
