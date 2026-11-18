"""MPS entry when torch reports Apple GPU."""


def gpu_mps(torch):
    mps = getattr(torch.backends, "mps", None)
    if mps is None or not mps.is_available():
        return None
    return {"name": "Apple MPS", "index": 0, "count": 1, "total_memory": None}
