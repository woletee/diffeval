"""Attach the eager AttnProcessor."""


def apply_eager(pipe) -> None:
    from diffusers.models.attention_processor import AttnProcessor
    pipe.set_attn_processor(AttnProcessor())
