"""Answer probability sums first tokens, counting a repeated token each time, as the reference does."""

from diffeval.metrics.geneval2.judge_tokens import answer_prob, first_token_ids


class _Tokenizer:
    ids = {"two": [5, 9], "Two": [6], " two": [5], " Two": [7], "2": [8], " 2": [8, 1]}

    def encode(self, text):
        return self.ids[text]


def test_first_tokens_and_sum():
    token_ids = first_token_ids(_Tokenizer(), ["two", "Two", " two", " Two", "2", " 2"])
    assert token_ids == [5, 6, 5, 7, 8, 8]
    row = [0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.125, 0.0625, 0.03125, 0.5]
    assert answer_prob(row, token_ids) == 0.25 * 2 + 0.125 + 0.0625 + 0.03125 * 2
