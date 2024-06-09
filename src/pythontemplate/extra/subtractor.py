"""Example python file with a function."""

from typeguard import typechecked


@typechecked
def subtract_two(*, x: int) -> int:
    """Subtracts a value to an incoming number."""
    return x - 2
