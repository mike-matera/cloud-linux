"""
Make a directory of random files.
"""

from os import PathLike
import pathlib
from typing import Union
from kroz import setup_hook
from kroz.app import get_appconfig
from .path import CheckPath, CheckFile
from .bigfile import RandomBigFile
from .words import random_words

CONFIG_KEY = "ranomdir_name"
DEFAULT_FILENAME = "Random"


class RandomDirectory:
    """A directory of random files with random contents."""

    def __init__(
        self,
        name: Union[str | PathLike[str]],
        count: int,
        rows: int,
        cols: int,
        *,
        sep: str = " ",
        end: str = "\n",
    ):
        self.name = pathlib.Path(name)
        self.count = count
        self.rows = rows
        self.cols = cols
        self.sep = sep
        self.end = end
        self.checkpath = None

    def setup(self):
        """Create the directory."""
        self.checkpath = CheckPath(self.name)
        for _ in range(self.count):
            rbf = RandomBigFile(
                name=None,
                rows=self.rows,
                cols=self.cols,
                sep=self.sep,
                end=self.end,
            )
            rbf.setup()
            self.checkpath.files.append(
                CheckFile(random_words().choice(), contents=rbf)
            )
        self.checkpath.sync()

    def filter(self, function):
        """Return a CheckPath that's filtered by the function."""
        return self.checkpath.filter(function)

    def cleanup(self):
        """Clean up the random directory."""
        self.checkpath.cleanup()


def random_directory(
    count: int,
    *,
    rows: int = 100,
    cols: int = 10,
    sep: str = " ",
    end: str = "\n",
):
    return RandomDirectory(
        name=get_appconfig("default_path") / get_appconfig(CONFIG_KEY),
        count=count,
        rows=rows,
        cols=cols,
        sep=sep,
        end=end,
    )


setup_hook(defconfig={CONFIG_KEY: DEFAULT_FILENAME})
