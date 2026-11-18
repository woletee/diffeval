"""Register cmmd."""

from diffeval.metrics.cmmd.protocol import PROTOCOL
from diffeval.metrics.cmmd.score import score_cmmd
from diffeval.registry.register import register
from diffeval.registry.tables import METRICS


class Cmmd:
    name = "cmmd"
    description = "CMMD (Jayasumana et al. 2024), ViT-L/14 at 336, L2-normalized embeddings."
    higher_is_better = False
    requires_references = True
    protocol = PROTOCOL

    def compute(self, samples, context):
        return score_cmmd(context)


register(METRICS, "cmmd")(Cmmd)
