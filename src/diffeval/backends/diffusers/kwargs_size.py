"""Width and height when the pipeline accepts them."""

import inspect


def _accepts(pipe, name: str) -> bool:
    params = inspect.signature(pipe.__call__).parameters
    varied = any(item.kind == inspect.Parameter.VAR_KEYWORD for item in params.values())
    return name in params or varied


def size_kwargs(pipe, width, height) -> dict:
    body = {}
    if _accepts(pipe, "width"):
        body["width"] = width
    if _accepts(pipe, "height"):
        body["height"] = height
    return body
