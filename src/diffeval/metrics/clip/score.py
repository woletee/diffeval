"""Per-image CLIP scores for one seed."""

from diffeval.metrics.clip.features import features
from diffeval.metrics.clip.formula import clip_score
from diffeval.metrics.clip.load import load_clip
from diffeval.metrics.clip.sample_image import sample_image
from diffeval.metrics.ok import ok
from diffeval.metrics.skipped import skipped

CHUNK = 32


def score_seed(samples, context, protocol):
    loaded = load_clip(protocol["model"])
    if loaded is None:
        return skipped("clip_score", "metrics extra is not installed", True, protocol)
    model, processor = loaded
    model.to(context.device)
    cosines = []
    for start in range(0, len(samples), CHUNK):
        part = samples[start:start + CHUNK]
        images = [sample_image(sample, context.generated_dir) for sample in part]
        image_f, text_f = features(model, processor, images, [sample.prompt for sample in part], context.device)
        cosines.extend((image_f * text_f).sum(dim=-1).tolist())
    return ok("clip_score", float(clip_score(cosines, protocol["weight"])), True, protocol)
