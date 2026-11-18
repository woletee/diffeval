"""The suite mapping for GenEval 2 rows, with each prompt's questions in meta."""

from diffeval.bench.geneval2_files import COMMIT


def _prompt(index: int, row: dict) -> dict:
    meta = {"vqa_list": row["vqa_list"], "skills": row["skills"], "atom_count": row["atom_count"]}
    return {"id": f"g{index:05d}", "prompt": row["prompt"], "meta": meta}


def geneval2_suite(rows: list[dict], seed: int, size: int) -> dict:
    name = "geneval2" if len(rows) >= 800 else f"geneval2-{len(rows)}"
    suite = {"name": name, "description": f"GenEval 2 prompts at facebookresearch/GenEval2@{COMMIT[:7]}, first {len(rows)}"}
    suite.update(seeds=[seed], width=size, height=size, metrics=["geneval2"])
    suite["prompts"] = [_prompt(index, row) for index, row in enumerate(rows)]
    return suite
