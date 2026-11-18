"""Error telling the user to install the extra."""


def require_diffusers() -> None:
    try:
        import diffusers
        import torch
    except ImportError as exc:
        raise RuntimeError("install the diffusers extra: pip install 'diffeval[diffusers]'") from exc
    return diffusers, torch
