"""A batch mixing set and unset negative prompts sends strings only."""

from diffeval.backends.diffusers.kwargs_prompt import prompt_kwargs
from diffeval.types.request import GenerationRequest


def test_mixed_negative():
    requests = [GenerationRequest("a", "red", 0, 64, 64), GenerationRequest("b", "blue", 0, 64, 64, "blurry")]
    assert prompt_kwargs(requests)["negative_prompt"] == ["", "blurry"]


def test_no_negative():
    requests = [GenerationRequest("a", "red", 0, 64, 64), GenerationRequest("b", "blue", 0, 64, 64)]
    assert "negative_prompt" not in prompt_kwargs(requests)
