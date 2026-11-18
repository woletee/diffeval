"""GenEval 2 Soft-TIFA for one seed, with AM, per-skill, and per-atom-count details."""

from diffeval.metrics.geneval2 import judge_load, prompt_scores
from diffeval.metrics.geneval2.breakdown import by_atom_count, by_skill
from diffeval.metrics.geneval2.total import total
from diffeval.metrics.ok import ok
from diffeval.metrics.skipped import skipped


def score_seed(samples, context, protocol):
    judge = judge_load.load_judge(protocol["judge"])
    if judge is None:
        return skipped("geneval2", "geneval2 extra is not installed: pip install 'diffeval[geneval2]'", True, protocol)
    scores = prompt_scores.prompt_scores(judge, samples, context.generated_dir, protocol["method"])
    lists, metas = list(scores.values()), [sample.meta for sample in samples]
    details = {"soft_tifa_am": total(lists, "soft_tifa_am"), "question_scores": scores}
    details["by_skill"] = by_skill(lists, [meta["skills"] for meta in metas])
    details["by_atom_count"] = by_atom_count(lists, [meta["atom_count"] for meta in metas])
    return ok("geneval2", total(lists, protocol["method"]), True, protocol, details)
