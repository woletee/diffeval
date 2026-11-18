"""The same prompt and seed produce the same bytes."""

# Importing the package registers the dummy backend.
import diffeval
from diffeval.registry.tables import BACKENDS
from diffeval.types.request import GenerationRequest


def _request(seed: int) -> GenerationRequest:
    return GenerationRequest("red_cube", "a red cube", seed, 32, 32)


def _bytes(seed: int, batch_size: int) -> bytes:
    backend = BACKENDS["dummy"].from_config({"batch_size": batch_size})
    image = backend.generate([_request(seed)])[0].image
    return image.tobytes()


def test_same_seed_same_bytes():
    assert _bytes(0, 1) == _bytes(0, 4)
    pair = [_request(1), _request(2)]
    one = BACKENDS["dummy"].from_config({"batch_size": 1}).generate(pair)
    two = BACKENDS["dummy"].from_config({"batch_size": 2}).generate(pair)
    assert one[0].image.tobytes() == two[0].image.tobytes()
    assert one[1].image.tobytes() == two[1].image.tobytes()
