"""An unknown suite exits 2."""

from diffeval.cli.main import main


def test_unknown_suite():
    assert main(["run", "--suite", "missing-suite", "--backend", "dummy"]) == 2
