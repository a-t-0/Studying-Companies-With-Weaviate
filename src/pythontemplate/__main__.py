"""Entry point for the project."""

from src.pythontemplate.adder import add_two

some_val: int = 2
print(f"Hello world. {some_val}+2={add_two(x=some_val)}")
