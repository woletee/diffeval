"""Dispatch sdpa, xformers, eager, or detect."""

from diffeval.backends.diffusers.attention_eager import apply_eager
from diffeval.backends.diffusers.attention_name import attention_name
from diffeval.backends.diffusers.attention_sdpa import apply_sdpa
from diffeval.backends.diffusers.attention_xformers import apply_xformers


def apply_attention(pipe, choice: str | None) -> str:
    if choice == "sdpa":
        apply_sdpa(pipe)
    elif choice == "eager":
        apply_eager(pipe)
    elif choice == "xformers":
        apply_xformers(pipe)
    return attention_name(pipe)
