"""Resolve steps and guidance to cli, preset, or pipeline-default."""

from diffeval.backends.diffusers.presets import preset_for


def _one(cli_value, preset_value):
    if cli_value is not None:
        return cli_value, "cli"
    if preset_value is not None:
        return preset_value, "preset"
    return None, "pipeline-default"


def sampling(config: dict) -> dict:
    found = preset_for(config["pipeline"])
    steps, steps_source = _one(config.get("steps"), found.get("steps"))
    guidance, guidance_source = _one(config.get("guidance"), found.get("guidance"))
    return {"steps": steps, "guidance": guidance, "steps_source": steps_source, "guidance_source": guidance_source}
