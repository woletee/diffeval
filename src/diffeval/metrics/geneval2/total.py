"""The benchmark score: 100 times the mean per-prompt score."""

from diffeval.metrics.geneval2.means import arithmetic, geometric

METHODS = ("soft_tifa_gm", "soft_tifa_am", "tifa", "vqascore")


def per_prompt(scores: list[float], method: str) -> float:
    if method not in METHODS:
        raise ValueError(f"unknown method {method!r}; choose from {', '.join(METHODS)}")
    return geometric(scores) if method == "soft_tifa_gm" else arithmetic(scores)


def total(score_lists: list[list[float]], method: str) -> float:
    if not score_lists:
        raise ValueError("no prompts to score")
    return 100 * arithmetic([per_prompt(scores, method) for scores in score_lists])
