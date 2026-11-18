"""higher or lower from a metric flag."""


def direction(higher_is_better) -> str:
    if higher_is_better is None:
        return "n/a"
    return "higher" if higher_is_better else "lower"
