"""
Randomized system paths.
"""

import pathlib
from collections.abc import Generator
from os import PathLike

from kroz.app import KrozApp

from .words import random_words

CONFIG_KEY = "bigfile_name"
DEFAULT_FILENAME = "bigfile"


class RandomBigFile:
    """A large file with random words in it."""

    def __init__(
        self,
        path: str | PathLike[str] | None,
        rows: int,
        cols: int,
        *,
        sep: str = " ",
        end: str = "\n",
    ):
        """
        Create a file with a particular shape (rows, columns)
        """
        if path is not None:
            self._path = pathlib.Path(path).resolve()
        else:
            self._path = None

        self._rows = rows
        self._cols = cols
        self._sep = sep
        self._end = end
        self._words = []

    def setup(self):
        """Create the file."""
        words = random_words()

        with KrozApp.progress() as progress:
            progress.update(message="Generating random words...")

            self._words = [
                words.choices(self._cols) for _ in range(self._rows)
            ]

            if self._path is not None:
                progress.update(message="Writing bigfile...")
                with open(self._path, "w") as fh:
                    for i, line in enumerate(self.lines()):
                        if (i % 1000) == 0:
                            progress.update(percent=(i / self._rows) * 100)
                        fh.write(line)

                KrozApp.running().notify(
                    f"{self._path} has been updated!",
                    title="File Updated",
                )

    def cleanup(self):
        """Remove the file."""
        assert self._path is not None, """This big file has no path."""
        self._path.unlink(missing_ok=True)

    @property
    def path(self) -> PathLike | None:
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

    def __str__(self):
        """Return the file contents."""
        return "".join(self.lines())


def random_big_file(
    rows,
    cols,
    *,
    sep=" ",
    end="\n",
):
    return RandomBigFile(
        KrozApp.appconfig("default_path") / KrozApp.appconfig(CONFIG_KEY),
        rows=rows,
        cols=cols,
        sep=sep,
        end=end,
    )


KrozApp.setup_hook(defconfig={CONFIG_KEY: DEFAULT_FILENAME})
