"""Embed image files and the reference bank."""

from PIL import Image

import numpy as np

from diffeval.metrics.cmmd.embed_batch import embed_batch
from diffeval.metrics.cmmd.resize import resize_image
from diffeval.metrics.images import list_images

CHUNK = 32


def embed_paths(model, processor, paths, device):
    chunks = []
    for start in range(0, len(paths), CHUNK):
        images = [resize_image(Image.open(path)) for path in paths[start:start + CHUNK]]
        chunks.append(embed_batch(model, processor, images, device))
    return np.concatenate(chunks) if chunks else None


def embed_dir(model, processor, folder, device):
    return embed_paths(model, processor, list_images(folder), device)


def paired(context, model, processor):
    generated = embed_dir(model, processor, context.generated_dir, context.device)
    if context.cmmd_ref_embed is not None:
        return generated, np.load(context.cmmd_ref_embed)
    return generated, embed_dir(model, processor, context.reference_dir, context.device)
