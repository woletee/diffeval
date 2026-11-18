"""Generate samples in batch-size slices."""

from diffeval.backends.dummy.render import render
from diffeval.types.sample import Sample


def _one(request) -> Sample:
    image = render(request.prompt, request.seed, request.width, request.height)
    return Sample(request.prompt_id, request.prompt, request.seed, request.width, request.height, image, None, request.negative_prompt, request.meta)


def generate(requests, batch_size: int) -> list:
    size = max(1, batch_size)
    samples = []
    for start in range(0, len(requests), size):
        samples.extend(_one(item) for item in requests[start:start + size])
    return samples
