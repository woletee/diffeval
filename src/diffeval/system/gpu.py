"""CUDA, otherwise MPS, otherwise null."""


def gpu():
    try:
        import torch
    except ImportError:
        return None
    from diffeval.system.gpu_cuda import gpu_cuda
    from diffeval.system.gpu_mps import gpu_mps
    return gpu_cuda(torch) or gpu_mps(torch)
