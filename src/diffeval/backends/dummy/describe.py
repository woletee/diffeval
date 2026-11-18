"""describe() for the dummy backend."""


def describe(config: dict) -> dict:
    return {
        "name": "dummy",
        "pipeline": config.get("pipeline"),
        "dtype": config.get("dtype"),
        "requested_dtype": config.get("dtype"),
        "steps": config.get("steps"),
        "guidance": config.get("guidance"),
        "steps_source": "pipeline-default",
        "guidance_source": "pipeline-default",
        "batch_size": config["batch_size"],
        "device": "cpu",
        "attention_backend": "none",
        "variant": config.get("variant"),
    }
