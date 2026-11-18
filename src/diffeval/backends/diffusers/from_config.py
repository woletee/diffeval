"""Require --pipeline and store backend settings."""


def from_config(config: dict) -> dict:
    pipeline = config.get("pipeline")
    if not isinstance(pipeline, str) or not pipeline:
        raise ValueError("diffusers backend requires --pipeline")
    raw = config.get("batch_size", 1)
    if type(raw) is not int or raw < 1:
        raise ValueError("batch_size must be a positive int")
    attention = config.get("attention")
    if attention not in (None, "sdpa", "xformers", "eager"):
        raise ValueError("attention must be sdpa, xformers, or eager")
    keys = ("dtype", "steps", "guidance", "variant", "device")
    stored = {key: config.get(key) for key in keys}
    stored.update(pipeline=pipeline, batch_size=raw, attention=attention)
    return stored
