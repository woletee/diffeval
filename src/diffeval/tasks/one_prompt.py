"""One prompt mapping."""

from diffeval.tasks.errors import SuiteError
from diffeval.tasks.prompt_id import check_id
from diffeval.types.prompt import Prompt


def one_prompt(item: dict) -> Prompt:
    if not isinstance(item, dict):
        raise SuiteError("prompt must be a mapping")
    text = item.get("prompt")
    if not isinstance(text, str) or not text.strip():
        raise SuiteError("prompt text must be a non-empty string")
    negative = item.get("negative_prompt")
    if negative is not None and not isinstance(negative, str):
        raise SuiteError("negative_prompt must be a string")
    meta = item.get("meta")
    if meta is not None and not isinstance(meta, dict):
        raise SuiteError("meta must be a mapping")
    return Prompt(check_id(item.get("id")), text, negative, meta)
