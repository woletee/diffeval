"""Assemble a Suite from parsed fields."""

from diffeval.types.suite import Suite


def build_suite(fields: dict) -> Suite:
    return Suite(**fields)
