"""One pipeline call for a same-size batch."""

from diffeval.backends.diffusers.call_kwargs import call_kwargs


def one_batch(pipe, requests, steps, guidance):
    if len({(item.width, item.height) for item in requests}) != 1:
        raise ValueError("a batch must share width and height")
    result = pipe(**call_kwargs(pipe, requests, steps, guidance))
    images = result.images if hasattr(result, "images") else result[0]
    return list(images)
