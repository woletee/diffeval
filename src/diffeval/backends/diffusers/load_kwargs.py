"""from_pretrained keyword arguments."""


def load_kwargs(config: dict, dtype) -> dict:
    body = {}
    if dtype is not None:
        body["torch_dtype"] = dtype
    if config.get("variant"):
        body["variant"] = config["variant"]
    return body
