"""diffeval-check-geneval2: rescore a geneval2 run with the reference evaluation.py and compare."""

import json
import subprocess

from diffeval.bench import geneval2_ref
from diffeval.bench.geneval2_check_args import check_args
from diffeval.bench.geneval2_compare import compare
from diffeval.bench.geneval2_files import geneval2_rows
from diffeval.bench.geneval2_inputs import run_inputs


def main(argv=None) -> int:
    args = check_args(argv)
    out = args.run / "geneval2-check"
    out.mkdir(parents=True, exist_ok=True)
    ours = run_inputs(args.run, args.seed, geneval2_rows(out, 800), out)
    subprocess.run(geneval2_ref.reference_command(out, out / "data.jsonl", out / "images.json", out / "reference_scores.json"), check=True)
    result = compare(ours, json.loads((out / "reference_scores.json").read_text(encoding="utf-8")))
    print(f"{result['questions']} questions, max difference {result['max_diff']:.2e} (tolerance {args.tolerance:g})")
    print(f"soft_tifa_gm diffeval {result['diffeval']:.4f} reference {result['reference']:.4f}")
    return 0 if result["max_diff"] <= args.tolerance else 1
