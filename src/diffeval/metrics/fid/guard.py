"""Require two images and a reference or stats."""

from diffeval.metrics.images import list_images


def fid_ready(context) -> str | None:
    if context.reference_dir is None and not context.clean_fid_stats:
        return "reference set is missing"
    if len(list_images(context.generated_dir)) < 2:
        return "fewer than two images"
    if context.reference_dir is not None and not context.clean_fid_stats and len(list_images(context.reference_dir)) < 2:
        return "fewer than two images"
    return None
