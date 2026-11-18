"""list backends prints dummy."""

from diffeval.cli.main import main


def test_list_backends(capsys):
    assert main(["list", "backends"]) == 0
    text = capsys.readouterr().out
    assert "dummy" in text and "diffusers" in text
