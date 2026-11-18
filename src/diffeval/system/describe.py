"""Platform, GPU, and attention flags."""

import platform

from diffeval.system.gpu import gpu
from diffeval.system.sdp_flags import sdp_flags


def describe() -> dict:
    return {"platform": platform.platform(), "gpu": gpu(), "torch_attention": sdp_flags()}
