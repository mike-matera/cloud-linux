"""
Make a directory of random files.
"""

import pathlib
from os import PathLike

from kroz import KrozApp

from .bigfile import RandomBigFile
from .path import CheckFile, CheckPath
from .words import random_words

CONFIG_KEY = "ranomdir_name"
DEFAULT_FILENAME = "Random"


class RandomDirectory:
    """A directory of random files with random contents."""

    def __init__(
        self,
        name: str | PathLike[str],
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
                path=None,
                rows=self.rows,
                cols=self.cols,
                sep=self.sep,
                end=self.end,
            )
            rbf.setup()
            self.checkpath.files.append(
                CheckFile(random_words().choice(), contents=str(rbf))
            )
        self.checkpath.sync()
        KrozApp.running().notify(
            f"{self.checkpath.basepath} has been updated!",
            title="Directory Updated",
        )

    def filter(self, function):
        """Return a CheckPath that's filtered by the function."""
        assert self.checkpath is not None, """Setup has not been run."""
        return self.checkpath.filter(function)

    def cleanup(self):
        """Clean up the random directory."""
        assert self.checkpath is not None, """Setup has not been run."""
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
        name=KrozApp.appconfig("default_path") / KrozApp.appconfig(CONFIG_KEY),
        count=count,
        rows=rows,
        cols=cols,
        sep=sep,
        end=end,
    )


KrozApp.setup_hook(defconfig={CONFIG_KEY: DEFAULT_FILENAME})
