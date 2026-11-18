"""Backend name and config dict from CLI args."""


def backend_name(args) -> str:
    if args.backend:
        return args.backend
    if args.pipeline:
        return "diffusers"
    return "dummy"


def backend_config(args) -> dict:
    raw = {"pipeline": args.pipeline, "dtype": args.dtype, "steps": args.steps, "guidance": args.guidance, "device": args.device, "attention": getattr(args, "attention", None), "variant": getattr(args, "variant", None), "batch_size": getattr(args, "batch_size", None)}
    return {key: value for key, value in raw.items() if value is not None}
