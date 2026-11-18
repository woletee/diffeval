"""GenEval 2 Soft-TIFA definition text."""

from diffeval.bench.geneval2_files import COMMIT
from diffeval.metrics.geneval2.judge_load import MODEL

PROTOCOL = {
    "paper": "Kamath et al. 2025, GenEval 2 (arXiv:2512.16853)",
    "reference": f"facebookresearch/GenEval2@{COMMIT[:7]} evaluation.py",
    "judge": MODEL,
    "method": "soft_tifa_gm",
    "question": "'{question} Answer in one word.', one image, greedy, one new token",
    "formula": "100 * mean over prompts of the geometric mean of accepted-answer first-token probabilities",
    "data_license": "CC BY-NC 4.0",
}
