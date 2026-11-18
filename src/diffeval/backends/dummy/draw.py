"""Draw a rectangle, ellipse, or triangle."""

from PIL import ImageDraw


def draw(image, shape: str, box, color):
    pen = ImageDraw.Draw(image)
    if shape == "ellipse":
        pen.ellipse(box, fill=color)
    elif shape == "triangle":
        left, top, right, bottom = box
        mid = (left + right) // 2
        pen.polygon([(left, bottom), (mid, top), (right, bottom)], fill=color)
    else:
        pen.rectangle(box, fill=color)
    return image
