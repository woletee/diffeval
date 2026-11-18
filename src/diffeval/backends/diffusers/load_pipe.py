"""Load AutoPipelineForText2Image and move it to the device."""


def load_pipe(pipeline_id, kwargs, device):
    from diffusers import AutoPipelineForText2Image
    return AutoPipelineForText2Image.from_pretrained(pipeline_id, **kwargs).to(device)


def prepare_pipe(config: dict) -> dict:
    from diffeval.backends.diffusers.attention_apply import apply_attention
    from diffeval.backends.diffusers.coerce_dtype import coerce_dtype
    from diffeval.backends.diffusers.dtype_name import label
    from diffeval.backends.diffusers.load_kwargs import load_kwargs
    from diffeval.backends.diffusers.missing_dep import require_diffusers
    from diffeval.backends.diffusers.pick_device import pick_device
    from diffeval.backends.diffusers.sampling import sampling
    require_diffusers()
    device = pick_device(config.get("device"))
    dtype, name = coerce_dtype(config.get("dtype"), device)
    pipe = load_pipe(config["pipeline"], load_kwargs(config, dtype), device)
    seen = label(getattr(pipe, "dtype", None)) or name
    attention = apply_attention(pipe, config.get("attention"))
    return {"pipe": pipe, "device": device, "dtype_text": seen, "sampling": sampling(config), "attention": attention}
