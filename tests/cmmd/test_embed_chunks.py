"""Embedding walks the paths in chunks and stacks the rows in order."""

from PIL import Image

import numpy as np

from diffeval.metrics.cmmd import embed_paths


def test_chunks(tmp_path, monkeypatch):
    paths = []
    for index in range(5):
        paths.append(tmp_path / f"{index}.png")
        Image.new("RGB", (8, 8), (index, 0, 0)).save(paths[-1])
    sizes = []
    fake = lambda model, processor, images, device: sizes.append(len(images)) or np.array([[img[0, 0, 0] * 255] for img in images])
    monkeypatch.setattr(embed_paths, "embed_batch", fake)
    monkeypatch.setattr(embed_paths, "CHUNK", 2)
    rows = embed_paths.embed_paths(None, None, paths, "cpu")
    assert sizes == [2, 2, 1] and np.allclose(rows[:, 0], range(5))
