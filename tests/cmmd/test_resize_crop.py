"""CMMD resize center-crops to a square before the 336 bicubic resize."""

from PIL import Image

import numpy as np

from diffeval.metrics.cmmd.resize import resize_image


def test_center_crop():
    image = Image.new("RGB", (300, 100), (255, 0, 0))
    image.paste((0, 0, 255), (100, 0, 200, 100))
    out = resize_image(image)
    assert out.shape == (336, 336, 3) and out.dtype == np.float32
    assert np.allclose(out[:, :, 2], 1.0) and np.allclose(out[:, :, 0], 0.0)
