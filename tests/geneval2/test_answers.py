"""Accepted answers match the reference lists, including its 'other' quirk."""

from diffeval.metrics.geneval2.answers import accepted, tifa_hit


def test_count_question():
    assert accepted("How many toys are in the image?", "two") == ["two", "Two", " two", " Two", "2", " 2"]
    assert accepted("How many cats are there?", "twelve")[4:] == ["other", " other"]


def test_yes_question_and_hit():
    answers = accepted("Is the backpack green?", "Yes")
    assert answers == ["Yes", "yes", " yes", " Yes"]
    assert tifa_hit("YES", answers) == 1 and tifa_hit(" Yes", answers) == 1 and tifa_hit("No", answers) == 0
