"""Register geneval2."""

from diffeval.metrics.geneval2.protocol import PROTOCOL
from diffeval.metrics.geneval2.score import score_seed
from diffeval.registry.register import register
from diffeval.registry.tables import METRICS


class Geneval2:
    name = "geneval2"
    description = "GenEval 2 Soft-TIFA (GM) with Qwen3-VL-8B, as facebookresearch/GenEval2."
    higher_is_better = True
    requires_references = False
    protocol = PROTOCOL

    def compute(self, samples, context):
        return score_seed(samples, context, self.protocol)


register(METRICS, "geneval2")(Geneval2)
