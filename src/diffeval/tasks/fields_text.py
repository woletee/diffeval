"""Suite name and description."""

from diffeval.tasks.errors import SuiteError


def name_and_description(data: dict) -> dict:
    name = data.get("name")
    description = data.get("description", "")
    if not isinstance(name, str) or not name:
        raise SuiteError("name must be a non-empty string")
    if not isinstance(description, str):
        raise SuiteError("description must be a string")
    return {"name": name, "description": description}
