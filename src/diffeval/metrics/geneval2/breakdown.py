"""Per-skill (arithmetic) and per-atom-count (geometric) scores, as soft_tifa_analysis.py."""

from diffeval.metrics.geneval2.means import arithmetic, geometric

SKILLS = ("object", "attribute", "count", "position", "verb")


def by_skill(score_lists: list[list[float]], skill_lists: list[list[str]]) -> dict:
    groups = {}
    for scores, skills in zip(score_lists, skill_lists, strict=True):
        for score, skill in zip(scores, skills, strict=True):
            if skill not in SKILLS:
                raise ValueError(f"unrecognized skill {skill!r}")
            groups.setdefault(skill, []).append(score)
    return {skill: 100 * arithmetic(groups[skill]) for skill in SKILLS if skill in groups}


def by_atom_count(score_lists: list[list[float]], atom_counts: list[int]) -> dict:
    groups = {}
    for scores, count in zip(score_lists, atom_counts, strict=True):
        groups.setdefault(count, []).append(geometric(scores))
    return {count: 100 * arithmetic(groups[count]) for count in sorted(groups)}
