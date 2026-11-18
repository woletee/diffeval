"""Register kid."""

from diffeval.metrics.distribution.call import score_distribution
from diffeval.metrics.distribution.protocol import PROTOCOL
from diffeval.registry.register import register
from diffeval.registry.tables import METRICS


class Kid:
    name = "kid"
    description = "KID via clean-fid, mode clean, polynomial degree 3."
    higher_is_better = False
    requires_references = True
    protocol = PROTOCOL

    def compute(self, samples, context):
        return score_distribution("kid", context, self.protocol)


register(METRICS, "kid")(Kid)
