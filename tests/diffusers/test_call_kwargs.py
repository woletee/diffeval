"""Call kwargs carry one CPU generator per request."""

import sys
import types

from diffeval.backends.diffusers.call_kwargs import call_kwargs
from diffeval.types.request import GenerationRequest


def test_call_kwargs(monkeypatch):
    def _gen(device):
        box = types.SimpleNamespace(device=device)
        box.manual_seed = lambda seed, box=box: setattr(box, "seed", seed) or box
        return box
    torch = types.ModuleType("torch")
    torch.Generator = _gen
    monkeypatch.setitem(sys.modules, "torch", torch)
    pipe = types.SimpleNamespace(__call__=lambda prompt, **kwargs: None)
    requests = [GenerationRequest("a", "red", 1, 64, 64), GenerationRequest("b", "blue", 2, 64, 64)]
    body = call_kwargs(pipe, requests, None, 0.0)
    gens = body["generator"]
    assert "num_inference_steps" not in body and body["width"] == 64 and body["guidance_scale"] == 0.0
    assert [item.seed for item in gens] == [1, 2] and gens[0] is not gens[1] and gens[0].device == "cpu"
