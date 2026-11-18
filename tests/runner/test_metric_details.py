"""Metric details, such as the image-count warning, reach the result row."""

from diffeval.metrics.ok import ok
from diffeval.runner.safe_metric import safe_metric


class _Warns:
    name = "warns"

    def compute(self, samples, context):
        return ok("warns", 1.0, False, {}, {"warning": "8 images is below 30000"})


class _Boom:
    name = "boom"

    def compute(self, samples, context):
        raise RuntimeError("broken")


def test_details_kept():
    assert safe_metric(_Warns(), [], None)["details"] == {"warning": "8 images is below 30000"}
    assert safe_metric(_Boom(), [], None)["details"] == {}
