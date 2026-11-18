"""Summed first-token probability of the accepted answers, as the reference computes it."""


def first_token_ids(tokenizer, answers: list[str]) -> list[int]:
    return [tokenizer.encode(answer)[0] for answer in answers]


def answer_prob(row, token_ids: list[int]) -> float:
    total = 0
    for token_id in token_ids:
        total += float(row[token_id])
    return total
