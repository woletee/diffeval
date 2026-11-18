"""Classify the current attention processor."""


def attention_name(pipe) -> str:
    processors = getattr(pipe, "attn_processors", None) or {}
    if not processors:
        return "none"
    cls = type(next(iter(processors.values()))).__name__
    if "xformers" in cls.lower():
        return "xformers"
    if cls == "AttnProcessor2_0":
        return "sdpa"
    if cls == "AttnProcessor":
        return "eager"
    return cls
