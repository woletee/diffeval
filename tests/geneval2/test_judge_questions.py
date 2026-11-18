"""question_scores sends the reference wording and keeps soft, hard, or VQAScore values."""

from diffeval.metrics.geneval2.judge_questions import question_scores

_META = {"vqa_list": [["How many toys are in the image?", "two"], ["Are the toys metal?", "Yes"]]}


def _ask(log):
    def ask(image, text, answers):
        log.append((image, text, answers))
        return (" 2", 0.75) if text.startswith("How many") else ("No", 0.25)
    return ask


def test_soft_hard_and_vqascore():
    log = []
    assert question_scores(_ask(log), "img", "two metal toys", _META, "soft_tifa_gm") == [0.75, 0.25]
    assert log[0] == ("img", "How many toys are in the image? Answer in one word.", ["two", "Two", " two", " Two", "2", " 2"])
    assert question_scores(_ask([]), "img", "two metal toys", _META, "tifa") == [1, 0]
    assert question_scores(_ask(log), "img", "two metal toys", _META, "vqascore") == [0.25]
    assert log[-1][1] == 'Does this image show "two metal toys"? Answer the question with Yes or No.'
