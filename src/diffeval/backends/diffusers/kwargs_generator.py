"""One CPU generator per seed."""


def generators(seeds):
    import torch
    return [torch.Generator(device="cpu").manual_seed(int(seed)) for seed in seeds]
