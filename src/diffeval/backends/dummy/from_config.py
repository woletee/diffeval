"""Batch size and an unused pipeline id."""


def from_config(config: dict) -> dict:
    raw = config.get("batch_size", 1)
    if type(raw) is not int or raw < 1:
        raise ValueError("batch_size must be a positive int")
    pipeline = config.get("pipeline")
    if pipeline is not None and not isinstance(pipeline, str):
        raise ValueError("pipeline must be a string")
    kept = ("dtype", "steps", "guidance", "variant")
    stored = {key: config.get(key) for key in kept}
    stored.update(batch_size=raw, pipeline=pipeline)
    return stored
