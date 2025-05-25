"""
Tools for building randomized paths and checkers.
"""

from collections.abc import Generator
import subprocess
import pathlib
from dataclasses import dataclass, field
import shutil
import textwrap
from typing import Self
from kroz import get_appconfig

CONTENT_LIMIT: int = 1024 * 32


@dataclass
class CheckFile:
    path: pathlib.Path
    contents: str = ""
    owner: str | None = field(default=None)
    group: str | None = field(default=None)
    perms: int | None = field(default=None)

    def __init__(
        self,
        path: str | pathlib.Path,
        contents: str = "",
        *,
        owner: str | None = None,
        group: str | None = None,
        perms: int | None = None,
    ):
        self.path = pathlib.Path(path)
        if self.path.is_absolute():
            raise ValueError("A check path or file must not be absolute.")
        self.contents = contents
        self.owner = owner
        self.group = group
        self.perms = perms


@dataclass
class CheckPath:
    basepath: pathlib.Path
    files: list[CheckFile] = field(default_factory=list)

    def __init__(
        self,
        basepath: str | pathlib.Path,
        files: list[CheckFile] = [],
    ):
        self.basepath = pathlib.Path(basepath)
        self.files = files
        self._validate()

    def _validate(self):
        self.basepath = pathlib.Path(self.basepath)
        if not self.basepath.is_absolute():
            self.basepath = (
                pathlib.Path(get_appconfig("default_path")) / self.basepath
            )
        self.basepath = pathlib.Path(self.basepath).resolve()
        try:
            self.basepath.relative_to(get_appconfig("default_path"))
        except ValueError:
            raise ValueError(
                "The basepath of a CheckPath must be relative to the application's default_path."
            )
        if self.basepath == pathlib.Path.home():
            raise ValueError(
                "A CheckPath base path must never be the $HOME directory."
            )

    @classmethod
    def from_path(cls: type[Self], path: str | pathlib.Path) -> Self:
        """Create a CheckPath object from a real path."""
        path = pathlib.Path(path)
        cp = cls(path)

        if not path.exists():
            return cp

        root = CheckFile(
            "",
            owner=path.owner(),
            group=path.group(),
            perms=path.stat().st_mode & 0o777,
        )
        cp.files.append(root)

        for file in path.glob("**/*"):
            try:
                f = CheckFile(
                    file.relative_to(path),
                    owner=file.owner(),
                    group=file.group(),
                    perms=file.stat().st_mode & 0o777,
                )
                if (
                    not file.is_symlink()
                    and file.is_file()
                    and file.stat().st_size <= CONTENT_LIMIT
                ):
                    with open(file) as fh:
                        f.contents = fh.read()
                cp.files.append(f)
            except (OSError, RuntimeError):
                # Choked for some reason. Ignore this path.
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
            self.basepath.mkdir(parents=True)

        for file in self.files:
            realpath = self.basepath / file.path
            realpath.parent.mkdir(parents=True, exist_ok=True)
            if file.contents is not None:
                with open(realpath, "w") as fh:
                    fh.write(file.contents)
                    fh.write("\n")
            if file.perms is not None:
                realpath.chmod(file.perms)
            if file.group is not None:
                subprocess.run(
                    f"chgrp {file.group} {realpath}",
                    shell=True,
                    check=True,
                )

    def cleanup(self):
        """Remove the contents of the basepath (but not the path itself)"""
        self._validate()
        if self.basepath.exists():
            for item in self.basepath.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()

    def check(self) -> Generator[tuple[pathlib.Path, str, str], None, None]:
        """Compare two paths"""

        other = CheckPath.from_path(self.basepath)

        other_paths = {x.path: x for x in other.files}
        other_path_set = set((p.path for p in other.files))

        my_paths = {x.path: x for x in self.files}
        my_path_set = set((p.path for p in self.files))

        # Run checks against expected files:
        for p in self.files:
            if p.path not in other_paths:
                if self.basepath / p.path == self.basepath:
                    yield (
                        pathlib.Path("."),
                        "Missing",
                        "The file/directory is missing or can't be read.",
                    )
                else:
                    yield (
                        p.path,
                        "Missing",
                        "The file/directory is missing or can't be read.",
                    )
            else:
                my_file = my_paths[p.path]
                other_file = other_paths[p.path]
                if my_file.__class__ is not other_file.__class__:
                    yield (
                        p.path,
                        "Wrong type",
                        "Is a directory instead of a file."
                        if isinstance(my_file, CheckFile)
                        else "Is a file instead of a directory.",
                    )
                if (
                    my_file.owner is not None
                    and my_file.owner != other_file.owner
                ):
                    yield (
                        p.path,
                        "Wrong owner",
                        f"{my_file.owner} != {other_file.owner}",
                    )
                if (
                    my_file.group is not None
                    and my_file.group != other_file.group
                ):
                    yield (
                        p.path,
                        "Wrong group",
                        f"{my_file.group} != {other_file.group}",
                    )
                if (
                    my_file.perms is not None
                    and my_file.perms != other_file.perms
                ):
                    yield (
                        p.path,
                        "Wrong permissions",
                        f"{my_file.perms:o} != {other_file.perms:o}",
                    )
                if (
                    my_file.contents is not None
                    and str(my_file.contents).strip()
                    != str(other_file.contents).strip()
                ):
                    yield (
                        p.path,
                        "Wrong contents",
                        f"{str(my_file.contents).strip()} != {str(other_file.contents).strip()}",
                    )

        for p in sorted(
            other_path_set.difference(my_path_set),
            key=lambda x: len(x.parts),
        ):
            if self.basepath / p != self.basepath:
                yield (
                    p,
                    "Exists",
                    "The file/directory should be removed.",
                )

    def filter(self, function) -> "CheckPath":
        """Create a new CheckPath with files filtered by a function."""
        return CheckPath(
            self.basepath, files=list(filter(function, self.files))
        )

    def short_report(self, verbose=0):
        for error in self.check():
            if verbose == 0:
                raise AssertionError(f"There is a problem with: {error[0]}")
            elif verbose == 1:
                raise AssertionError(f"""
                                     # Error
                                     
                                    {error[0]}: {error[1]}
                                    """)
            elif verbose == 2:
                raise AssertionError(f"""
                                     # Error
                                     
                                    {error[0]}: {error[1]}

                                    The reason is: {error[2]}
                                    """)

    def full_report(self, verbose=0):
        errors = list(self.check())
        if len(errors) == 0:
            return

        if verbose == 0:
            raise AssertionError(
                textwrap.dedent("""
                # Error 
                The following paths have errors:
                {}
                """).format(
                    "\n".join((f"* {self.basepath / e[0]}" for e in errors))
                )
            )
        if verbose == 1:
            raise AssertionError(
                textwrap.dedent("""
                # Error 

                Errors have been detected:
                                                
                | {} | Error | 
                | --- | --- | 
                {}
                """).format(
                    str(self.basepath).replace(str(pathlib.Path.home()), "~"),
                    "\n".join((f"| {e[0]} | {e[1]} |" for e in errors)),
                )
            )
        if verbose == 2:
            raise AssertionError(
                textwrap.dedent("""
                # Error 

                Errors have been detected:
                                                
                | {} | Error | Detail | 
                | --- | --- | --- | 
                {}
            """).format(
                    str(self.basepath).replace(str(pathlib.Path.home()), "~"),
                    "\n".join(
                        (f"| {e[0]} | {e[1]} | {e[2]} |" for e in errors)
                    ),
                )
            )
