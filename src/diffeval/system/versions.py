"""Package versions recorded in results.json."""

import platform

from diffeval.system.version_of import version_of


def versions() -> dict:
    return {
        "diffeval": version_of("diffeval"),
        "python": platform.python_version(),
        "numpy": version_of("numpy"),
        "pillow": version_of("pillow"),
        "pyyaml": version_of("pyyaml"),
        "torch": version_of("torch"),
        "diffusers": version_of("diffusers"),
        "transformers": version_of("transformers"),
        "accelerate": version_of("accelerate"),
        "clean-fid": version_of("clean-fid"),
    }
