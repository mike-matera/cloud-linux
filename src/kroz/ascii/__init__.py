"""
Package to make the use of ASCII art easier.
"""

import functools
from importlib.resources import files
import textwrap


def from_file(filename, format="raw", indent=0):
    art = files("kroz.ascii").joinpath(filename).read_text()
    if format == "raw":
        return textwrap.indent(art, prefix=" " * indent)
    elif format == "md":
        return textwrap.indent(f"```\n{art}```", prefix=" " * indent)


# def robot():
#    return files("kroz.ascii").joinpath("robot.txt").read_text()

robot = functools.partial(from_file, filename="robot.txt")
