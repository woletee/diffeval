"""A sample's pixels, read back from its saved PNG when the runner dropped them."""

from PIL import Image


def sample_image(sample, folder):
    if sample.image is not None:
        return sample.image.convert("RGB")
    with Image.open(folder / f"{sample.prompt_id}.png") as image:
        return image.convert("RGB")
