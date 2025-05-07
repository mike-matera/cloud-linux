"""
Randomized system paths.
"""

from os import PathLike
import pathlib
from collections.abc import Generator
from typing import Union
from .words import random_words
from kroz import setup_hook, get_appconfig

CONFIG_KEY = "bigfile_name"
DEFAULT_FILENAME = "bigfile"


class RandomBigFile:
    """A large file with random words in it."""

    def __init__(
        self,
        name: Union[str | PathLike[str]],
        rows: int,
        cols: int,
        *,
        sep: str = " ",
        end: str = "\n",
    ):
        """
        Create a file with a particular shape (rows, columns)
        """
        self._name = name
        self._rows = rows
        self._cols = cols
        self._sep = sep
        self._end = end
        self._path = pathlib.Path(self._name).resolve()
        self._words = []

    def setup(self):
        """Create the file."""
        words = random_words()

        self._words = [words.choices(self._cols) for _ in range(self._rows)]

        with open(self._path, "w") as fh:
            for line in self.lines():
                fh.write(line)

    def cleanup(self):
        """Remove the file."""
        self._path.unlink()

    @property
    def path(self):
        """The path of the bigfile."""
        return self._path

    def lines(self) -> Generator[str]:
        """Iterate over the lines in the file."""
        for line in self._words:
            yield self._sep.join(line) + self._end

    def word_at(self, line: int, column: int) -> str:
        """Return the word at a particular position (starting at 1)"""
        assert line != 0, """There is no line 0"""
        assert column != 0, """There is no column 0"""
        if line > 0:
            line -= 1
        if column > 0:
            column -= 1
        return self._words[line][column]

    def line_at(self, line: int) -> str:
        """Return a particular line (starting at 1)"""
        assert line != 0, """There is no line 0"""
        if line > 0:
            line -= 1
        return self._sep.join(self._words[line]) + self._end


def random_big_file(
    rows,
    cols,
    *,
    sep=" ",
    end="\n",
):
    return RandomBigFile(
        get_appconfig("default_path") / get_appconfig(CONFIG_KEY),
        rows=rows,
        cols=cols,
        sep=sep,
        end=end,
    )


setup_hook(defconfig={CONFIG_KEY: DEFAULT_FILENAME})
