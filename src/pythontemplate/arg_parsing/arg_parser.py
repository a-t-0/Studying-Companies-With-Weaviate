from typing import List

from typeguard import typechecked


@typechecked
def parse_skip_upload(*, args: List[str]) -> bool:
    """Parses the --skip-upload argument from a list of arguments.

    Args:   args: A list of command-line arguments.

    Returns:   True if the --skip-upload argument is present, False otherwise.
    """
    return "--skip-upload" in args
