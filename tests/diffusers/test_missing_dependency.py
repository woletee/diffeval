"""prepare names the diffusers extra when the library is missing."""

import builtins

import pytest

from diffeval.backends.diffusers.backend import DiffusersBackend


def test_prepare_names_extra(monkeypatch):
    real = builtins.__import__
    def blocked(name, *args, **kwargs):
        if name.split(".")[0] in {"diffusers", "torch"}:
            raise ImportError(name)
        return real(name, *args, **kwargs)
    monkeypatch.setattr(builtins, "__import__", blocked)
    backend = DiffusersBackend.from_config({"pipeline": "org/model"})
    with pytest.raises(RuntimeError, match=r"diffeval\[diffusers\]"):
        backend.prepare()
