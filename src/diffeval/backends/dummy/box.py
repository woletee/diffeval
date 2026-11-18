"""Seed-shifted box inside the image."""


def box(seed: int, width: int, height: int) -> tuple[int, int, int, int]:
    span_w = max(1, width // 4)
    span_h = max(1, height // 4)
    left = abs(seed) % max(1, width - span_w + 1)
    top = abs(seed // 3) % max(1, height - span_h + 1)
    return left, top, left + span_w, top + span_h
