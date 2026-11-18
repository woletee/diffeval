"""describe() after the pipeline loads."""


def describe(config: dict, state: dict) -> dict:
    sampling = state.get("sampling") or {"steps": None, "guidance": None, "steps_source": "pipeline-default", "guidance_source": "pipeline-default"}
    return {"name": "diffusers", "pipeline": config.get("pipeline"), "dtype": state.get("dtype_text"), "requested_dtype": config.get("dtype"), "steps": sampling["steps"], "guidance": sampling["guidance"], "steps_source": sampling["steps_source"], "guidance_source": sampling["guidance_source"], "batch_size": config.get("batch_size", 1), "device": state.get("device"), "attention_backend": state.get("attention"), "variant": config.get("variant")}
