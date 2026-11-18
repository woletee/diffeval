"""Map dtype strings to torch dtypes."""

_NAMES = {"float32": "float32", "fp32": "float32", "float16": "float16", "fp16": "float16", "bfloat16": "bfloat16", "bf16": "bfloat16"}


def parse_dtype(text: str | None) -> str | None:
    if text is None:
        return None
    if text not in _NAMES:
        raise ValueError(f"unknown dtype {text}")
    return _NAMES[text]


def torch_dtype(name: str | None):
    import torch
    table = {"float32": torch.float32, "float16": torch.float16, "bfloat16": torch.bfloat16}
    return None if name is None else table[name]


def label(dtype) -> str | None:
    if dtype is None:
        return None
    return str(dtype).split(".")[-1]
