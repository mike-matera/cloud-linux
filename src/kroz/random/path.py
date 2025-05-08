"""
Tools for building randomized paths and checkers.
"""

from collections.abc import Generator
import subprocess
import pathlib
from dataclasses import dataclass, field
import shutil
from typing import Self


@dataclass
class CheckFile:
    path: pathlib.Path
    contents: str = ""
    owner: str = field(default=None)
    group: str = field(default=None)
    perms: int = field(default=None)

    def __post_init__(self):
        self.path = pathlib.Path(self.path)
        if self.path.is_absolute():
            raise ValueError("A CheckFile path must not be absolute.")


@dataclass
class CheckDir:
    path: pathlib.Path
    owner: str = field(default=None)
    group: str = field(default=None)
    perms: int = field(default=None)

    def __post_init__(self):
        self.path = pathlib.Path(self.path)
        if self.path.is_absolute():
            raise ValueError("A CheckDir path must not be absolute.")


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

        if not path.exists():
            return cp

        root = CheckDir(
            "",
            owner=path.owner,
            group=path.group(),
            perms=path.stat().st_mode & 0o777,
        )
        cp.files.append(root)

        for file in path.glob("**/*"):
            if not file.is_symlink():
                try:
                    if file.is_file():
                        f = CheckFile(
                            file.relative_to(path),
                            owner=file.owner(),
                            group=file.group(),
                            perms=file.stat().st_mode & 0o777,
                        )
                        with open(file) as fh:
                            f.contents = fh.read()
                    elif file.is_dir():
                        f = CheckDir(
                            file.relative_to(path),
                            owner=file.owner(),
                            group=file.group(),
                            perms=file.stat().st_mode & 0o777,
                        )
                    else:
                        raise RuntimeError("Not a file I know about.")

                    cp.files.append(f)

                except (OSError, RuntimeError):
                    # Choked for some reason. Ignore it.
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
            if isinstance(file, CheckFile):
                realpath.parent.mkdir(parents=True, exist_ok=True)
                if file.contents is not None:
                    with open(realpath, "w") as fh:
                        fh.write(file.contents)
                        fh.write("\n")
            elif isinstance(file, CheckDir):
                realpath.mkdir(parents=True, exist_ok=True)
            else:
                raise ValueError("Invalid file:", file)

            if file.perms is not None:
                realpath.chmod(file.perms)
            if file.group is not None:
                subprocess.run(
                    f"chgrp {file.group} {realpath}",
                    shell=True,
                    check=True,
                )

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
                        self.basepath,
                        "Missing",
                        f"The path {self.basepath} is missing",
                    )
                else:
                    yield (
                        p.path,
                        "Missing",
                        f"The path {p.path} is missing in {self.basepath}",
                    )
            else:
                my_file = my_paths[p.path]
                other_file = other_paths[p.path]
                if my_file.__class__ is not other_file.__class__:
                    yield (
                        p.path,
                        "Type mismatch.",
                        f"{p.path} should be a file, not a directory."
                        if isinstance(my_file, CheckFile)
                        else f"{p.path} should be a directory, not a file.",
                    )
                if (
                    my_file.owner is not None
                    and my_file.owner != other_file.owner
                ):
                    yield (
                        p.path,
                        "Owner doesn't match.",
                        f"{my_file.owner} != {other_file.owner}",
                    )
                if (
                    my_file.group is not None
                    and my_file.group != other_file.group
                ):
                    yield (
                        p.path,
                        "Group doesn't match.",
                        f"{my_file.group} != {other_file.group}",
                    )
                if (
                    my_file.perms is not None
                    and my_file.perms != other_file.perms
                ):
                    yield (
                        p.path,
                        "Permissions doesn't match.",
                        f"{my_file.perms:o} != {other_file.perms:o}",
                    )
                if isinstance(my_file, CheckFile) and my_file.contents:
                    if my_file.contents.strip() != other_file.contents.strip():
                        yield (
                            p.path,
                            "File contents don't match.",
                            f"{my_file.contents.strip()} != {other_file.contents.strip()}",
                        )

        for p in sorted(
            other_path_set.difference(my_path_set), key=lambda x: len(x.parts)
        ):
            yield (
                p,
                "Extra",
                "The file exists but it should not.",
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
            raise AssertionError(f"""
# Error 

The following paths have errors: 

{"\n".join((f"* {e[0]}" for e in errors))}
            """)
        if verbose == 1:
            raise AssertionError(f"""
# Error 

Errors have been detected:
                                 
| Path | Error | 
| --- | --- | 
{"\n".join((f"| {e[0]} | {e[1]} |" for e in errors))}
            """)
        if verbose == 2:
            raise AssertionError(f"""
# Error 

Errors have been detected:
                                 
| Path | Error | Detail | 
| --- | --- | --- | 
{"\n".join((f"| {e[0]} | {e[1]} | {e[2]} |" for e in errors))}
            """)
