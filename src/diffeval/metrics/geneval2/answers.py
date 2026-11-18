"""Answer strings whose first-token probability counts as correct, in the reference order."""

from diffeval.metrics.geneval2.numerals import numeric
from diffeval.metrics.geneval2.templates import YES


def accepted(question: str, answer: str) -> list[str]:
    if not question.startswith("How many"):
        return list(YES)
    digit = numeric(answer)
    return [answer, answer.capitalize(), " " + answer, " " + answer.capitalize(), digit, " " + digit]


def tifa_hit(pred: str, answers: list[str]) -> int:
    return int(pred.lower() in answers)
