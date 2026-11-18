"""Python files under src and tests stay within 20 code lines."""

import importlib.util
import pathlib


def test_line_cap():
    path = pathlib.Path(__file__).with_name("count.py")
    spec = importlib.util.spec_from_file_location("linecap_count", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    over = [
        str(item)
        for root in (pathlib.Path("src"), pathlib.Path("tests"))
        for item in root.rglob("*.py")
        if module.code_lines(item.read_text(encoding="utf-8")) > 20
    ]
    assert over == []
