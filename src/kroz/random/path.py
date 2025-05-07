"""
Tools for building randomized paths and checkers.
"""

from collections.abc import Generator
import getpass
import grp
import subprocess
import pathlib
from dataclasses import dataclass, field
import os
import shutil
from typing import Self


def default_perms():
    umask = os.umask(0o777)
    os.umask(umask)
    return ~umask & 0o666


@dataclass
class CheckFile:
    path: pathlib.Path
    contents: str = ""
    owner: str = field(default=getpass.getuser())
    group: str = field(default=grp.getgrgid(os.getegid()))
    perms: int = field(default_factory=default_perms)

    def __post_init__(self):
        self.path = pathlib.Path(self.path)
        if self.path.is_absolute():
            raise ValueError("A CheckFile path must not be absolute.")


@dataclass
class CheckPath:
    basepath: pathlib.Path
    files: list[CheckFile] = field(default_factory=list)

    def __post_init__(self):
        self._validate()

    def _validate(self):
        self.basepath = pathlib.Path(self.basepath).resolve()
        if self.basepath == pathlib.Path.home():
            raise ValueError(
                "A CheckPath must never be rooted in the $HOME directory."
            )

    @classmethod
    def from_path(cls: type[Self], path: str | pathlib.Path) -> Self:
        """Create a CheckPath object from a real path."""
        path = pathlib.Path(path)
        cp = cls(path)
        for file in path.glob("**/*"):
            if not file.is_symlink() and file.is_file():
                try:
                    f = CheckFile(
                        file.relative_to(path),
                        owner=file.owner(),
                        group=file.group(),
                        perms=file.stat().st_mode & 0o777,
                    )
                    with open(file) as fh:
                        f.contents = fh.read()
                    cp.files.append(f)

                except Exception:
                    # Choked on a file. Ignore it.
                    pass
        return cp

    def sync(self) -> None:
        """
        Synchronize the directory structure with the data structure. If the
        `basepath` does not exist it will be created. If it does exist the
        the contents will be deleted.

        This is destructive. Be careful.
        """
        self._validate()
        if self.basepath.exists():
            for item in self.basepath.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
        else:
            self.basepath.mkdir()

        for file in self.files:
            realpath = self.basepath / file.path
            realpath.parent.mkdir(parents=True, exist_ok=True)
            with open(realpath, "w") as fh:
                fh.write(file.contents)
            realpath.chmod(file.perms)
            subprocess.run(
                f"chgrp {file.group} {realpath}", shell=True, check=True
            )

    def check(self) -> Generator[str]:
        """Compare two paths"""

        other = CheckPath.from_path(self.path)

        other_paths = {x.path: x for x in other.files}
        other_path_set = set((p.path for p in other.files))

        my_paths = {x.path: x for x in self.files}
        my_path_set = set((p.path for p in self.files))

        for p in sorted(
            my_path_set.intersection(other_path_set),
            key=lambda x: len(x.parts),
        ):
            # Check common files:
            my_file = my_paths[p]
            other_file = other_paths[p]
            if my_file.contents != other_file.contents:
                print("Bad contents!", p)
            if my_file.owner != other_file.owner:
                print("Bad owner!", p)
            if my_file.group != other_file.group:
                print("Bad group!", p)
            if my_file.perms != other_file.perms:
                print("Bad perms!", p)

        for p in sorted(
            my_path_set.difference(other_path_set), key=lambda x: len(x.parts)
        ):
            # Missing from other_paths
            print("Missing:", my_paths[p])

        for p in sorted(
            other_path_set.difference(my_path_set), key=lambda x: len(x.parts)
        ):
            # Missing from other_paths
            print("Extra:", other_paths[p])
