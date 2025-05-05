"""
Randomized system paths.
"""

import locale
from os import PathLike
import pathlib
from collections.abc import Generator
import re
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

    def grep(
        self, pattern: str, flags: str
    ) -> Generator[tuple[int, list[str]]]:
        """
        Emulate grep to return lines in the file.

        Returns a tuple containing the line number with the list of
        words on the line.
        """

        reflags = 0
        regex = f"{pattern}"
        for flag in flags:
            if flag == "w":
                regex = f"\\s{pattern}(\\W|\\s)+"
            elif flag == "i":
                reflags |= re.IGNORECASE
            else:
                raise ValueError(f"Unsupported grep flag: {flag}")
        regex = re.compile(regex)
        for i, line in enumerate(self.lines()):
            if re.search(regex, " " + line, reflags) is not None:
                yield (
                    i + 1,
                    line,
                )

    def grep_wc(self, pattern: str, flags: str) -> int:
        """grep | wc"""
        return len(list(self.grep(pattern, flags)))

    def sort(self, flags=None):
        """Emulates the behavior of sort()

        WARNING: This is LANG specific. See the sort manpage and Pythons's
        locale library.
        """

        lang, cat = locale.getlocale()
        assert lang == "en_US" and cat == "UTF-8", (
            """This question assumes that sort is using the en_US.UTF-8 locale.."""
        )
        assert flags is None, "Flags is not yet implemented."

        return sorted(self.lines(), key=str.lower)


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
