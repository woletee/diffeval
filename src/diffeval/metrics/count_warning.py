"""Warn when the image count is below the published setup."""


def count_warning(count: int, usual: int = 30000) -> str | None:
    if count >= usual:
        return None
    return f"{count} images is below the published COCO setup of {usual}"
