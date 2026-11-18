"""Walk requests in batches."""

from diffeval.backends.diffusers.one_batch import one_batch
from diffeval.types.sample import Sample


def _sample(request, image) -> Sample:
    return Sample(request.prompt_id, request.prompt, request.seed, request.width, request.height, image, None, request.negative_prompt, request.meta)


def generate(pipe, requests, batch_size, steps, guidance):
    samples = []
    size = max(1, int(batch_size))
    for start in range(0, len(requests), size):
        chunk = list(requests[start:start + size])
        images = one_batch(pipe, chunk, steps, guidance)
        samples.extend(_sample(request, image) for request, image in zip(chunk, images))
    return samples
