"""Steps and guidance when the pipeline accepts them."""

import inspect


def _accepts(pipe, name: str) -> bool:
    params = inspect.signature(pipe.__call__).parameters
    varied = any(item.kind == inspect.Parameter.VAR_KEYWORD for item in params.values())
    return name in params or varied


def sampling_kwargs(pipe, steps, guidance) -> dict:
    body = {}
    if steps is not None and _accepts(pipe, "num_inference_steps"):
        body["num_inference_steps"] = steps
    if guidance is not None and _accepts(pipe, "guidance_scale"):
        body["guidance_scale"] = guidance
    return body
