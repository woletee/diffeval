"""GenEval 2 rows become a suite whose prompts carry their questions in meta."""

import yaml

from diffeval.bench.geneval2_suite import geneval2_suite
from diffeval.tasks.load_path import load_path

_ROW = {"prompt": "two metal toys", "atom_count": 3, "skills": ["count", "attribute"], "vqa_list": [["How many toys are in the image?", "two"], ["Are the toys metal?", "Yes"]]}


def test_suite_loads(tmp_path):
    data = geneval2_suite([_ROW, dict(_ROW, prompt="a pig")], 0, 1024)
    (tmp_path / "suite.yaml").write_text(yaml.safe_dump(data), encoding="utf-8")
    suite = load_path(tmp_path / "suite.yaml")
    assert suite.name == "geneval2-2" and suite.seeds == (0,) and (suite.width, suite.height) == (1024, 1024)
    assert [p.id for p in suite.prompts] == ["g00000", "g00001"] and suite.prompts[1].prompt == "a pig"
    assert suite.prompts[0].meta == {"vqa_list": _ROW["vqa_list"], "skills": _ROW["skills"], "atom_count": 3}
