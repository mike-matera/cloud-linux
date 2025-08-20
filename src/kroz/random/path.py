"""
Tools for building randomized paths and checkers.
"""

import itertools
import pathlib
import shutil
import subprocess
import textwrap
from collections.abc import Generator
from dataclasses import dataclass, field

from kroz.app import KrozApp
from kroz.validation import IsPermission

CONTENT_LIMIT: int = 1024 * 32


@dataclass
class CheckItem:
    path: pathlib.Path
    owner: str | None = field(default=None, kw_only=True)
    group: str | None = field(default=None, kw_only=True)
    perms: int | None = field(default=None, kw_only=True)

    def __init__(
        self,
        path: str | pathlib.Path,
        *,
        owner: str | None = None,
        group: str | None = None,
        perms: int | None = None,
    ):
        self.path = pathlib.Path(path)
        if self.path.is_absolute():
            raise ValueError("A check item must not be absolute.")
        self.owner = owner
        self.group = group
        self.perms = perms


@dataclass
class CheckFile(CheckItem):
    contents: str = ""

    def __init__(
        self,
        path: str | pathlib.Path,
        contents: str = "",
        *,
        owner: str | None = None,
        group: str | None = None,
        perms: int | None = None,
    ):
        super().__init__(path=path, owner=owner, group=group, perms=perms)
        self.contents = contents


@dataclass(init=False)
class CheckDir(CheckItem):
    pass


@dataclass
class CheckLink(CheckItem):
    target: pathlib.Path

    def __init__(
        self,
        path: str | pathlib.Path,
        target: str | pathlib.Path,
        *,
        owner: str | None = None,
        group: str | None = None,
        perms: int | None = None,
    ):
        super().__init__(path=path, owner=owner, group=group, perms=perms)
        self.target = pathlib.Path(target)


@dataclass
class CheckPath:
    basepath: pathlib.Path
    files: list[CheckItem] = field(default_factory=list)

    def __init__(
        self,
        basepath: str | pathlib.Path,
        files: list[CheckItem] = list(),
    ):
        self.basepath = pathlib.Path(basepath)
        self.files = files.copy()
        self._validate()

    def _validate(self):
        self.basepath = pathlib.Path(self.basepath)
        if not self.basepath.is_absolute():
            self.basepath = (
                pathlib.Path(KrozApp.appconfig("default_path")) / self.basepath
            )
        self.basepath = pathlib.Path(self.basepath).resolve()
        try:
            self.basepath.relative_to(KrozApp.appconfig("default_path"))
        except ValueError:
            raise ValueError(
                "The basepath of a CheckPath must be relative to the application's default_path."
            )
        if self.basepath == pathlib.Path.home():
            raise ValueError(
                "A CheckPath base path must never be the $HOME directory."
            )

    @staticmethod
    def from_path(path: str | pathlib.Path) -> "CheckPath":
        """Create a CheckPath object from a real path."""
        path = pathlib.Path(path)
        cp = CheckPath(path)

        if not path.exists():
            return cp

        for file in itertools.chain([path], path.glob("**/*")):
            try:
                if file.is_symlink():
                    f = CheckLink(
                        file.relative_to(path),
                        file.readlink(),
                        owner=file.owner(),
                        group=file.group(),
                        perms=file.lstat().st_mode & 0o777,
                    )
                elif file.is_file():
                    f = CheckFile(
                        file.relative_to(path),
                        owner=file.owner(),
                        group=file.group(),
                        perms=file.stat().st_mode & 0o777,
                    )
                    if file.stat().st_size <= CONTENT_LIMIT:
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
                    raise RuntimeError(f"I don't understand this file: {file}")

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
            if isinstance(file, CheckLink):
                realpath.symlink_to(file.target)
            elif isinstance(file, CheckFile):
                with open(realpath, "w") as fh:
                    fh.write(file.contents)
                    # Ensure file ends with \n
                    if file.contents[-1] != "\n":
                        fh.write("\n")
            elif isinstance(file, CheckDir):
                realpath.mkdir(exist_ok=True)
            else:
                raise RuntimeError(f"What is this: {file}")

            if file.perms is not None and not realpath.is_symlink():
                ## BUG: Path.chmod() follows symlinks.
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

    def check(
        self, extra_ok=False, missing_ok=False
    ) -> Generator[tuple[pathlib.Path, str, str], None, None]:
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
                        "The base path is missing or can't be read.",
                    )
                else:
                    if not missing_ok:
                        yield (
                            p.path,
                            "Missing",
                            "The file/directory is missing or can't be read.",
                        )
            else:
                my_file = my_paths[p.path]
                other_file = other_paths[p.path]
                if isinstance(my_file, CheckFile) and isinstance(
                    other_file, CheckFile
                ):
                    if my_file.contents.strip() != other_file.contents.strip():
                        yield (
                            p.path,
                            "Wrong contents",
                            f"{my_file.contents.strip()} != {other_file.contents.strip()}",
                        )
                elif isinstance(my_file, CheckDir) and isinstance(
                    other_file, CheckDir
                ):
                    # No directory specific checks.
                    pass
                elif isinstance(my_file, CheckLink) and isinstance(
                    other_file, CheckLink
                ):
                    if (self.basepath / my_file.path).readlink() != (
                        other.basepath / other_file.path
                    ).readlink():
                        yield (
                            p.path,
                            "Wrong link target.",
                            f"{(self.basepath / my_file.path).readlink()} != {(other.basepath / other_file.path).readlink()}",
                        )
                else:
                    yield (
                        p.path,
                        "Wrong type",
                        f"The path {other_file.path} is not a {my_file.__class__.__name__.replace('Check', '').lower()}.",
                    )

                # Check common attributes.
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

        if not extra_ok:
            for p in sorted(
                other_path_set.difference(my_path_set),
                key=lambda x: len(x.parts),
            ):
                if self.basepath / p != self.basepath:
                    yield (
                        p,
                        "Exists",
                        "The file, directory link should be removed.",
                    )

    def filter(self, function) -> "CheckPath":
        """Create a new CheckPath with files filtered by a function."""
        return CheckPath(
            self.basepath, files=list(filter(function, self.files))
        )

    def find(self, path: str | pathlib.Path) -> CheckItem:
        """Find a CheckItem by its name"""
        for item in self.files:
            if item.path == pathlib.Path(path):
                return item
        raise FileNotFoundError()

    def find_file(self, path: str | pathlib.Path) -> CheckFile:
        """Find a file by its name"""
        f = self.find(path)
        assert isinstance(f, CheckFile), """Path was not a file."""
        return f

    def find_dir(self, path: str | pathlib.Path) -> CheckDir:
        """Find a file by its name"""
        f = self.find(path)
        assert isinstance(f, CheckDir), """Path was not a directory."""
        return f

    def find_link(self, path: str | pathlib.Path) -> CheckLink:
        """Find a file by its name"""
        f = self.find(path)
        assert isinstance(f, CheckLink), """Path was not a file."""
        return f

    def short_report(self, missing_ok=False, extra_ok=False, verbose=0):
        for error in self.check(missing_ok=missing_ok, extra_ok=extra_ok):
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

    def full_report(self, missing_ok=False, extra_ok=False, verbose=0):
        errors = list(self.check(missing_ok=missing_ok, extra_ok=extra_ok))
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

    def markdown(self, *, detail: bool = True, depth: int = 0):
        """
        A markdown representation of the expected path that's similar to the
        output of the `tree` command.
        """
        paths = {self.basepath / file.path: file for file in self.files}
        tree = {str(self.basepath): {"check": None, "files": {}}}
        if self.basepath in paths:
            tree[str(self.basepath)]["check"] = paths[self.basepath]
        for file in self.files:
            root = tree[str(self.basepath)]
            pathparts = self.basepath
            for part in file.path.parts:
                if part not in root["files"]:
                    root["files"][part] = {"check": None, "files": {}}
                pathparts /= part
                if pathparts in paths:
                    root["files"][part]["check"] = paths[pathparts]
                root = root["files"][part]

        def pretty(
            root: dict, *, depth: int = 0, maxdepth: int = 0, preamble=""
        ) -> str:
            if maxdepth and depth >= maxdepth:
                return ""
            rval = ""
            for i, (key, val) in enumerate(root.items()):
                details = ""
                if detail and val["check"] is not None:
                    details = []
                    if val["check"].owner is not None:
                        details.append(f"owner={val['check'].owner}")
                    if val["check"].group is not None:
                        details.append(f"group={val['check'].group}")
                    if val["check"].perms is not None:
                        permtype = "-"
                        if isinstance(val["check"], CheckDir):
                            permtype = "d"
                        elif isinstance(val["check"], CheckLink):
                            permtype = "l"
                        perms = f"{permtype}{IsPermission.to_string(val['check'].perms)}"
                        details.append(perms)
                    if details:
                        details = f"[{' '.join(details)}] "
                    else:
                        details = ""

                if i == len(root) - 1:
                    stub = "└── "
                    new_preamble = preamble + "    "
                else:
                    stub = "├── "
                    new_preamble = preamble + "│   "

                if depth == 0:
                    stub = ""
                    new_preamble = ""
                    key = str(self.basepath).replace(
                        str(pathlib.Path.home()), "~"
                    )

                rval += f"{preamble}{stub}{details}{key}\n"
                rval += pretty(
                    val["files"],
                    depth=depth + 1,
                    maxdepth=maxdepth,
                    preamble=new_preamble,
                )

            return rval

        return f"```\n{pretty(root=tree, maxdepth=depth)}\n```"
