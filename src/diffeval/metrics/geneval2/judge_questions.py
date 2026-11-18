"""One prompt's question scores for a method, given an ask(image, text, answers) callable."""

from diffeval.metrics.geneval2.answers import accepted, tifa_hit
from diffeval.metrics.geneval2.templates import QUESTION, VQASCORE, YES


def question_scores(ask, image, prompt: str, meta: dict, method: str) -> list[float]:
    if method == "vqascore":
        return [ask(image, VQASCORE.format(prompt), list(YES))[1]]
    scores = []
    for question, answer in meta["vqa_list"]:
        answers = accepted(question, answer)
        pred, prob = ask(image, QUESTION.format(question), answers)
        scores.append(tifa_hit(pred, answers) if method == "tifa" else prob)
    return scores
