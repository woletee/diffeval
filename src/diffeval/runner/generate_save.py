"""Generate in chunks, save each PNG, and drop the pixels from memory."""

from pathlib import Path

from diffeval.runner.relpath import relpath
from diffeval.runner.save_png import save_png

CHUNK = 64


def generate_save(backend, requests, folder: Path, output_dir) -> list:
    samples = []
    for start in range(0, len(requests), CHUNK):
        for sample in backend.generate(requests[start:start + CHUNK]):
            path = folder / f"{sample.prompt_id}.png"
            save_png(sample.image, path)
            sample.path, sample.image = relpath(path, Path(output_dir)), None
            samples.append(sample)
    return samples
