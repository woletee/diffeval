"""The bundled core suite lists four prompts, two seeds, and four drawings."""

from pathlib import Path

from diffeval.cli.main import main
from diffeval.tasks.resolve import resolve


def test_core_suite(capsys):
    suite = resolve("core")
    prompts = [(item.id, item.prompt) for item in suite.prompts]
    refs = Path(suite.reference_dir)
    assert suite.name == "core" and suite.seeds == (0, 1) and (suite.width, suite.height) == (512, 512)
    assert suite.metrics == ("clip_score", "cmmd", "fid", "kid")
    assert prompts == [("red_cube", "a red cube"), ("blue_sphere", "a blue sphere"), ("green_triangle", "a green triangle"), ("yellow_star", "a yellow star")]
    assert all((refs / f"{item[0]}.png").is_file() for item in prompts)
    assert main(["list", "tasks"]) == 0 and "core" in capsys.readouterr().out
