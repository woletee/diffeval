"""--seeds rejects repeats; --width and --height reject zero and negatives."""

import pytest

from diffeval.cli.parser import build_parser


def _parse(*flags):
    return build_parser().parse_args(["run", "--suite", "core", *flags])


@pytest.mark.parametrize("flags", [("--seeds", "0,0,1"), ("--width", "0"), ("--height", "-64"), ("--width", "x")])
def test_rejected(flags, capsys):
    with pytest.raises(SystemExit):
        _parse(*flags)
    assert flags[1] in capsys.readouterr().err


def test_accepted():
    args = _parse("--seeds", "0,1", "--width", "64", "--height", "32")
    assert args.seeds == (0, 1) and (args.width, args.height) == (64, 32)
