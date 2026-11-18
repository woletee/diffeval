"""One RGB image for a prompt and a seed."""

import hashlib

from PIL import Image

from diffeval.backends.dummy.box import box
from diffeval.backends.dummy.colors import colors
from diffeval.backends.dummy.draw import draw

_SHAPES = ("rectangle", "ellipse", "triangle")


def render(prompt: str, seed: int, width: int, height: int) -> Image.Image:
    background, foreground = colors(prompt)
    image = Image.new("RGB", (width, height), background)
    kind = _SHAPES[hashlib.sha256(prompt.encode("utf-8")).digest()[6] % 3]
    return draw(image, kind, box(seed, width, height), foreground)
