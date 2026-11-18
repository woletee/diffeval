"""Pick cuda, mps, or cpu."""


def pick_device(requested: str | None) -> str:
    if requested:
        return requested
    import torch
    if torch.cuda.is_available():
        return "cuda"
    mps = getattr(torch.backends, "mps", None)
    if mps is not None and mps.is_available():
        return "mps"
    return "cpu"
