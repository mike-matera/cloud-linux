"""
Randomized system paths.
"""

import pathlib
from collections import namedtuple
from collections.abc import Callable, Generator, Hashable
from typing import Iterable

import kroz.random as random
from kroz.app import KrozApp

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
            except:  # noqa: E722
                return False

        self._trees = {
            tree.root: [
                path
                for path in pathlib.Path(tree.root).glob(tree.glob)
                if can_stat(path)
            ]
            for tree in search
        }

    def random_file(self):
        return self.find_one(
            lambda c: c.is_file() and not c.is_symlink()
        ).resolve()

    def random_dir(self):
        return self.find_one(
            lambda c: c.is_dir() and not c.is_symlink()
        ).resolve()

    def random_link(self):
        return self.find_one(lambda c: c.is_symlink())

    def find_one(
        self,
        filter: Callable[[pathlib.Path], bool],
        normalize: None | Callable[[pathlib.Path], Hashable] = None,
    ):
        """Search the candidate files until a condition matches."""
        for path in self.find(filter, normalize=normalize):
            return path
        raise RuntimeError("No path found!")

    def find(
        self,
        filter: Callable[[pathlib.Path], bool],
        normalize: None | Callable[[pathlib.Path], Hashable] = None,
    ) -> Generator[pathlib.Path]:
        """Return a generator of paths that match the filter"""
        if self._trees is None:
            raise RuntimeError(
                "Paths have not been initialized. You have not run setup()."
            )
        if normalize is None:
            normals = self._trees
        else:
            normals = {}
            for root in self._trees:
                for path in self._trees[root]:
                    # Only consider a normal that matches the filter.
                    if filter(path):
                        key = normalize(path)
                        if key not in normals:
                            normals[key] = [path]
                        else:
                            normals[key].append(path)

        for tree in random.sample(list(normals), k=len(normals)):
            for path in random.sample(normals[tree], k=len(normals[tree])):
                if filter(path):
                    yield path


_paths = RandomRealPath()


def random_real_path():
    global _paths
    return _paths


def _setup():
    global _paths
    _paths.setup(KrozApp.appconfig(CONFIG_KEY))


KrozApp.setup_hook(
    hook=_setup,
    defconfig={CONFIG_KEY: DEFAULT_PATHS},
)
