"""Load float16 and bfloat16 as float32 on CPU."""

from diffeval.backends.diffusers.dtype_name import parse_dtype, torch_dtype


def coerce_dtype(requested: str | None, device: str):
    name = parse_dtype(requested)
    if device == "cpu" and name in ("float16", "bfloat16"):
        name = "float32"
    return torch_dtype(name), name
