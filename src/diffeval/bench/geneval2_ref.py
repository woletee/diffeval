"""The pinned GenEval 2 reference evaluation.py and the command that runs it."""

import sys
from pathlib import Path

from diffeval.bench.fetch import fetch
from diffeval.bench.geneval2_files import COMMIT

EVAL_URL = f"https://raw.githubusercontent.com/facebookresearch/GenEval2/{COMMIT}/evaluation.py"


def reference_command(out: Path, data: Path, images: Path, scores: Path) -> list[str]:
    script = fetch(EVAL_URL, out / "reference" / "evaluation.py")
    args = ["--benchmark_data", str(data), "--image_filepath_data", str(images), "--method", "soft_tifa_gm", "--output_file", str(scores)]
    return [sys.executable, str(script), *args]
