"""Compose pipeline call kwargs."""

from diffeval.backends.diffusers.kwargs_generator import generators
from diffeval.backends.diffusers.kwargs_prompt import prompt_kwargs
from diffeval.backends.diffusers.kwargs_sampling import sampling_kwargs
from diffeval.backends.diffusers.kwargs_size import size_kwargs


def call_kwargs(pipe, requests, steps, guidance) -> dict:
    body = prompt_kwargs(requests)
    body.update(sampling_kwargs(pipe, steps, guidance))
    body.update(size_kwargs(pipe, requests[0].width, requests[0].height))
    gens = generators([item.seed for item in requests])
    body["generator"] = gens[0] if len(requests) == 1 else gens
    return body
