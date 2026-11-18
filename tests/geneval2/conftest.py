"""A processor and model with the call shapes ask() uses, without weights."""

from types import SimpleNamespace

import pytest


class _Batch(dict):
    def to(self, device):
        return _Batch({key: f"{value}@{device}" for key, value in self.items()})


def _processor(calls):
    def chat(messages, **kwargs):
        calls.update(messages=messages, chat=kwargs)
        return _Batch(input_ids="ids")
    tokenizer = SimpleNamespace(encode=lambda text: {"Yes": [2], "yes": [1]}[text])
    return SimpleNamespace(apply_chat_template=chat, tokenizer=tokenizer, batch_decode=lambda t: [f"tok{int(t[0])}"])


@pytest.fixture
def fake_judge():
    calls = {}
    model = lambda logits: SimpleNamespace(device="cpu", generate=lambda **kw: calls.update(generate=kw) or SimpleNamespace(scores=[logits]))
    return SimpleNamespace(calls=calls, processor=_processor(calls), model=model)

