"""Width and height, defaulting to 512."""

from diffeval.tasks.errors import SuiteError


def width_and_height(data: dict) -> dict:
    width = data.get("width", 512)
    height = data.get("height", 512)
    bad = type(width) is not int or type(height) is not int
    if bad or width < 1 or height < 1:
        raise SuiteError("width and height must be positive ints")
    return {"width": width, "height": height}
