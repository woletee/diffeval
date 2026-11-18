"""Register clip_score."""

from diffeval.metrics.clip.protocol import PROTOCOL
from diffeval.metrics.clip.score import score_seed
from diffeval.registry.register import register
from diffeval.registry.tables import METRICS


class ClipScore:
    name = "clip_score"
    description = "CLIPScore (Hessel et al. 2021), ViT-B/32, weight 2.5."
    higher_is_better = True
    requires_references = False
    protocol = PROTOCOL

    def compute(self, samples, context):
        return score_seed(samples, context, self.protocol)


register(METRICS, "clip_score")(ClipScore)
