"""Seed NumPy around a call and restore the previous state."""

import numpy as np


def seeded(seed, fn):
    state = np.random.get_state()
    np.random.seed(seed)
    try:
        return fn()
    finally:
        np.random.set_state(state)
