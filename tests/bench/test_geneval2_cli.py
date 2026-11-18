"""diffeval-geneval2 reads a local data file and writes suite.yaml without a download."""

import json

from diffeval.bench.geneval2_cli import main
from diffeval.tasks.load_path import load_path

_ROW = {"prompt": "a cat", "atom_count": 1, "skills": ["object"], "vqa_list": [["Are there any cats in the image?", "Yes"]]}


def test_cli_writes_suite(tmp_path, capsys):
    (tmp_path / "geneval2_data.jsonl").write_text(json.dumps(_ROW) + "\n" + json.dumps(_ROW) + "\n", encoding="utf-8")
    assert main(["--out", str(tmp_path), "--limit", "1"]) == 0
    assert "CC BY-NC 4.0" in capsys.readouterr().out
    suite = load_path(tmp_path / "suite.yaml")
    assert suite.name == "geneval2-1" and suite.prompts[0].meta["skills"] == ["object"]
