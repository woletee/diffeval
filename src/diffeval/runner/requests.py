"""Generation requests for one seed."""

from diffeval.types.request import GenerationRequest


def requests_for(suite, seed: int, width: int, height: int) -> list:
    return [GenerationRequest(item.id, item.prompt, seed, width, height, item.negative_prompt, item.meta) for item in suite.prompts]
