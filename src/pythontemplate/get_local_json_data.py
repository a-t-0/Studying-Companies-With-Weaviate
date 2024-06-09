"""Example python file with a function."""

from typeguard import typechecked


@typechecked
def add_two(*, x: int) -> int:
    """Adds a value to an incoming number."""
    return x + 2
