"""Tests whether the adder function indeed adds 2 to a given input."""

import unittest

from typeguard import typechecked


class Test_adder_sub(unittest.TestCase):
    """Object used to test a parse_creds function."""

    # Initialize test object
    @typechecked
    def __init__(self, *args, **kwargs):  # type:ignore[no-untyped-def]
        super().__init__(*args, **kwargs)

    @typechecked
    def test_add_two_input_sub(self) -> None:
        """Tests if add_two function adds 2 to an integer."""
        print("Hello")


if __name__ == "__main__":
    unittest.main()
