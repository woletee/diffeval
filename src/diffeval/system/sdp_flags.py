"""PyTorch scaled-dot-product attention flags."""


def sdp_flags():
    try:
        import torch
    except ImportError:
        return None
    cuda = torch.backends.cuda
    return {
        "flash_sdp": cuda.flash_sdp_enabled(),
        "mem_efficient_sdp": cuda.mem_efficient_sdp_enabled(),
        "math_sdp": cuda.math_sdp_enabled(),
        "cudnn_sdp": cuda.cudnn_sdp_enabled(),
    }
