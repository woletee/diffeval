"""Published steps and guidance by model id."""

SCHNELL = "black-forest-labs/FLUX.1-schnell"
PRESETS = {SCHNELL: {"steps": 4, "guidance": 0.0}}


def preset_for(pipeline: str) -> dict:
    return PRESETS.get(pipeline, {})
