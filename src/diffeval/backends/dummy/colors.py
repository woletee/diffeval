"""Background and foreground from a prompt hash."""

import hashlib


def colors(prompt: str) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    digest = hashlib.sha256(prompt.encode("utf-8")).digest()
    background = (digest[0], digest[1], digest[2])
    foreground = ((digest[3] + 128) % 256, digest[4], digest[5])
    return background, foreground
