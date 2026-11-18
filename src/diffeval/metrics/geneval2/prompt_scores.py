"""Ask the judge every question for one seed: {prompt_id: [question scores]}."""

from functools import partial

from diffeval.metrics.clip.sample_image import sample_image
from diffeval.metrics.geneval2.judge_ask import ask
from diffeval.metrics.geneval2.judge_questions import question_scores


def prompt_scores(judge, samples, folder, method: str) -> dict:
    processor, model = judge
    asker = partial(ask, processor, model)
    scores = {}
    for sample in samples:
        if not (sample.meta or {}).get("vqa_list"):
            raise ValueError(f"prompt {sample.prompt_id} has no GenEval 2 questions; build the suite with diffeval-geneval2")
        scores[sample.prompt_id] = question_scores(asker, sample_image(sample, folder), sample.prompt, sample.meta, method)
    return scores
