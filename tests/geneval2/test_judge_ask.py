"""ask() calls the chat template and generate as the reference does and reads the first-step softmax."""

import pytest

_CHAT = {"tokenize": True, "add_generation_prompt": True, "return_dict": True, "return_tensors": "pt"}
_GENERATE = {"max_new_tokens": 1, "do_sample": False, "output_scores": True, "return_dict_in_generate": True}


def test_ask_matches_softmax(fake_judge):
    torch = pytest.importorskip("torch")
    from diffeval.metrics.geneval2.judge_ask import ask, messages

    model = fake_judge.model(torch.tensor([[0.0, 1.0, 2.0, 3.0]]))
    pred, prob = ask(fake_judge.processor, model, "img", "Is it red? Answer in one word.", ["Yes", "yes"])
    probs = torch.softmax(torch.tensor([0.0, 1.0, 2.0, 3.0]), dim=-1)
    assert pred == "tok3" and prob == pytest.approx(float(probs[2]) + float(probs[1]))
    calls = fake_judge.calls
    assert calls["generate"] == dict(_GENERATE, input_ids="ids@cpu") and calls["chat"] == _CHAT
    assert calls["messages"] == messages("img", "Is it red? Answer in one word.")
