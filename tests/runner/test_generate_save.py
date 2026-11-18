"""Chunked generation saves every PNG and keeps no pixels in memory."""

from diffeval.backends.dummy.backend import DummyBackend
from diffeval.runner import generate_save as module
from diffeval.types.request import GenerationRequest


def test_chunks(tmp_path, monkeypatch):
    monkeypatch.setattr(module, "CHUNK", 2)
    requests = [GenerationRequest(f"p{i}", f"prompt {i}", 0, 8, 8) for i in range(5)]
    samples = module.generate_save(DummyBackend.from_config({}), requests, tmp_path / "seed_0", tmp_path)
    assert [s.prompt_id for s in samples] == [f"p{i}" for i in range(5)]
    assert all(s.image is None and (tmp_path / s.path).is_file() for s in samples)
