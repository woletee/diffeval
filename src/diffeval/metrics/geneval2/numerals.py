"""Number words to digits, as return_numeric_string in the reference."""

_DIGITS = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10"}


def numeric(word: str) -> str:
    return _DIGITS.get(word, "other")
