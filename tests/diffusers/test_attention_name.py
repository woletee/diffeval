"""Attention classification names sdpa and xformers."""

from types import SimpleNamespace

from diffeval.backends.diffusers.attention_name import attention_name


class AttnProcessor2_0:
    pass


class XFormersAttnProcessor:
    pass


def test_attention_names():
    sdpa = SimpleNamespace(attn_processors={"block": AttnProcessor2_0()})
    xformers = SimpleNamespace(attn_processors={"block": XFormersAttnProcessor()})
    assert attention_name(sdpa) == "sdpa" and attention_name(xformers) == "xformers"
