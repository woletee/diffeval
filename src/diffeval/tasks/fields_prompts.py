"""Prompt list and duplicate ids, compared ignoring case."""

from diffeval.tasks.errors import SuiteError
from diffeval.tasks.one_prompt import one_prompt


def prompts(data: dict) -> dict:
    raw = data.get("prompts")
    if not isinstance(raw, list) or not raw:
        raise SuiteError("prompts must be a non-empty list")
    built = tuple(one_prompt(item) for item in raw)
    ids = [item.id.casefold() for item in built]
    if len(ids) != len(set(ids)):
        raise SuiteError("duplicate prompt id (ids are compared ignoring case)")
    return {"prompts": built}
