"""Attach AttnProcessor2_0."""


def apply_sdpa(pipe) -> None:
    from diffusers.models.attention_processor import AttnProcessor2_0
    pipe.set_attn_processor(AttnProcessor2_0())
