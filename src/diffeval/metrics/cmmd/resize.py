"""Center square crop, 8-bit bicubic resize to 336, then divide by 255."""

from PIL import Image

import numpy as np

SIZE = 336


def resize_image(image: Image.Image) -> np.ndarray:
    image = image.convert("RGB")
    width, height = image.size
    side = min(width, height)
    top, left = (height - side) // 2, (width - side) // 2
    square = image.crop((left, top, left + side, top + side))
    resized = square.resize((SIZE, SIZE), Image.Resampling.BICUBIC)
    return np.asarray(resized, dtype=np.float32) / 255.0
