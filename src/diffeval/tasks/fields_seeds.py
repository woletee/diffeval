"""Non-empty list of distinct seeds."""

from diffeval.tasks.errors import SuiteError


def seeds(data: dict) -> dict:
    raw = data.get("seeds")
    if not isinstance(raw, list) or not raw:
        raise SuiteError("seeds must be a non-empty list of ints")
    if any(type(item) is not int for item in raw):
        raise SuiteError("seeds must be ints")
    if len(set(raw)) != len(raw):
        raise SuiteError("seeds must not repeat")
    return {"seeds": tuple(raw)}
