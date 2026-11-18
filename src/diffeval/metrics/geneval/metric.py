"""Register geneval and return skipped."""

from diffeval.metrics.geneval.protocol import PROTOCOL
from diffeval.metrics.geneval.tags import TAGS
from diffeval.metrics.skipped import skipped
from diffeval.registry.register import register
from diffeval.registry.tables import METRICS


class Geneval:
    name = "geneval"
    description = "GenEval v1 stub. The Mask2Former detector is not imported."
    higher_is_better = True
    requires_references = False
    protocol = PROTOCOL

    def compute(self, samples, context):
        details = {"by_tag": {tag: None for tag in TAGS}}
        return skipped(self.name, "GenEval detector is not in v1", True, self.protocol, details)


register(METRICS, "geneval")(Geneval)
