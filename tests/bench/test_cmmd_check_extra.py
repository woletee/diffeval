"""diffeval-check-cmmd names the metrics extra before downloading anything, and --help only prints help."""

import pytest

from diffeval.bench import cmmd_check
from diffeval.metrics.cmmd import embed_batch


def test_missing_extra(monkeypatch, capsys):
    monkeypatch.setattr(embed_batch, "load_vision", lambda name: None)
    monkeypatch.setattr(cmmd_check, "cmmd_samples", lambda folder: pytest.fail("downloaded samples"))
    assert cmmd_check.main([]) == 2
    assert "pip install 'diffeval[metrics]'" in capsys.readouterr().err


def test_help(capsys):
    with pytest.raises(SystemExit) as exit_info:
        cmmd_check.main(["--help"])
    assert exit_info.value.code == 0 and "7.696" in capsys.readouterr().out
