"""
Randomized system paths.
"""

from collections import namedtuple
from collections.abc import Callable, Generator
import pathlib
import random
from typing import Iterable

from kroz import setup_hook, get_appconfig

SearchTree = namedtuple("SearchTree", ["root", "glob"])
CONFIG_KEY = "random_path_search"
DEFAULT_PATHS = [
    SearchTree(root="/etc", glob="**/*"),
    SearchTree(root="/bin", glob="**/*"),
    SearchTree(root="/dev", glob="**/*"),
    SearchTree(root="/usr/bin", glob="**/*"),
    SearchTree(root="/usr/sbin", glob="**/*"),
    SearchTree(root="/usr/share", glob="*/*"),
    SearchTree(root="/sys", glob="*/*/*"),
    SearchTree(root="/boot", glob="**/*"),
    SearchTree(root="/lib", glob="*/*"),
]


class RandomRealPath:
    """
    Get random extant files or directories on the system.
    """

    def __init__(self):
        self._trees = None

    def setup(self, search: Iterable[SearchTree]):
        self._trees = []

        def can_stat(f):
            try:
                f.stat()
                return True
            except:
                return False

        self._trees = [
            [
                path
                for path in pathlib.Path(tree.root).glob(tree.glob)
                if can_stat(path)
            ]
            for tree in search
        ]

    def random_file(self):
        return self.find_one(
            lambda c: c.is_file() and not c.is_symlink()
        ).resolve()

    def random_dir(self):
        return self.find_one(
            lambda c: c.is_dir() and not c.is_symlink()
        ).resolve()

    def find_one(self, filter):
        """Search the candidate files until a condition matches."""
        for path in self.find(filter):
            return path
        raise RuntimeError("No path found!")

    def find(
        self, filter: Callable[[pathlib.Path], bool]
    ) -> Generator[pathlib.Path]:
        """Return a generator of paths that match the filter"""
        if self._trees is None:
            raise RuntimeError(
                "Paths have not been initialized. You have not run setup()."
            )
        for tree in random.sample(self._trees, k=len(self._trees)):
            for path in random.sample(tree, k=len(tree)):
                if filter(path):
                    yield path


_paths = RandomRealPath()


def random_real_path():
    global _paths
    return _paths


def _setup():
    global _paths
    _paths.setup(get_appconfig(CONFIG_KEY))


setup_hook(
    hook=_setup,
    defconfig={CONFIG_KEY: DEFAULT_PATHS},
)
