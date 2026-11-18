"""Compare diffeval's question scores with the reference's, question by question."""

from diffeval.metrics.geneval2.total import total


def compare(ours: list[list[float]], reference: list[list[float]]) -> dict:
    if [len(scores) for scores in ours] != [len(scores) for scores in reference]:
        raise SystemExit("diffeval and the reference scored different numbers of questions")
    diffs = [abs(a - b) for mine, theirs in zip(ours, reference) for a, b in zip(mine, theirs)]
    return {"questions": len(diffs), "max_diff": max(diffs), "diffeval": total(ours, "soft_tifa_gm"), "reference": total(reference, "soft_tifa_gm")}
