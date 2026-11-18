"""A different seed produces different bytes."""

# Importing the package registers the dummy backend.
import diffeval
from diffeval.registry.tables import BACKENDS
from diffeval.types.request import GenerationRequest


def test_other_seed_and_describe():
    backend = BACKENDS["dummy"].from_config({"pipeline": "ignored"})
    one = GenerationRequest("red_cube", "a red cube", 0, 32, 32)
    two = GenerationRequest("red_cube", "a red cube", 1, 32, 32)
    images = backend.generate([one, two])
    assert images[0].image.tobytes() != images[1].image.tobytes()
    assert images[0].image.mode == "RGB"
    info = backend.describe()
    assert info["device"] == "cpu"
    assert info["attention_backend"] == "none"
    assert info["pipeline"] == "ignored"
