"""
Package to make the use of ASCII art easier.
"""

import functools
from importlib.resources import files
import textwrap


def from_file(filename, indent=0):
    art = files("kroz.ascii").joinpath(filename).read_text()
    return textwrap.indent(art, prefix=" " * indent)


robot = functools.partial(from_file, filename="robot.txt")
tux = functools.partial(from_file, filename="tux.txt")
