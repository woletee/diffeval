"""Register fid."""

from diffeval.metrics.distribution.call import score_distribution
from diffeval.metrics.distribution.protocol import PROTOCOL
from diffeval.registry.register import register
from diffeval.registry.tables import METRICS


class Fid:
    name = "fid"
    description = "FID via clean-fid, mode clean, Inception-v3."
    higher_is_better = False
    requires_references = True
    protocol = PROTOCOL

    def compute(self, samples, context):
        return score_distribution("fid", context, self.protocol, "inception_v3")


register(METRICS, "fid")(Fid)
