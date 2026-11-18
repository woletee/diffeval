"""Mean of weight * max(cosine, 0)."""


def clip_score(cosines, weight: float) -> float:
    scores = [weight * max(float(value), 0.0) for value in cosines]
    return sum(scores) / len(scores)
