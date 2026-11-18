"""Enable xformers attention."""


def apply_xformers(pipe) -> None:
    pipe.enable_xformers_memory_efficient_attention()
