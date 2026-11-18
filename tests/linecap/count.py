"""Count non-blank, non-comment, non-docstring lines."""


def code_lines(text: str) -> int:
    count = 0
    marker = ""
    for raw in text.splitlines():
        line = raw.strip()
        if marker:
            if marker in line:
                marker = ""
            continue
        if not line or line.startswith("#"):
            continue
        if line.startswith('"""') or line.startswith("'''"):
            mark = line[:3]
            if line.count(mark) == 1:
                marker = mark
            continue
        count += 1
    return count
