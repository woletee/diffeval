"""Per-skill and per-atom-count scores follow soft_tifa_analysis.py."""

import pytest

from diffeval.metrics.geneval2.breakdown import by_atom_count, by_skill

_SCORES = [[0.2, 0.8], [0.25, 1.0, 0.6]]
_SKILLS = [["count", "object"], ["count", "object", "attribute"]]


def test_by_skill_and_atom_count():
    assert by_skill(_SCORES, _SKILLS) == pytest.approx({"object": 90.0, "attribute": 60.0, "count": 22.5})
    assert list(by_skill(_SCORES, _SKILLS)) == ["object", "attribute", "count"]
    assert by_atom_count([[0.25, 1.0], [0.81, 1.0], [1.0]], [3, 3, 4]) == pytest.approx({3: 70.0, 4: 100.0})


def test_unknown_skill():
    with pytest.raises(ValueError):
        by_skill([[0.5]], [["style"]])
