"""
# Lesson 9: File Permissions

After this lesson you should be able to:

- Understand users and groups
- Control access to files
- Change your password

Reading:

- Chapter 9

Commands:

1. `chmod`
1. `chgrp`

"""

import grp
import textwrap
from pathlib import Path

from kroz.flow.base import KrozFlowABC
from kroz.random.path import CheckDir, CheckFile, CheckPath

from .lesson05 import Islands

title = "Working with Permissions"

state = "islands2"


class Islands2(Islands):
    """The islands with perms."""

    def setup(self):
        try:
            grp.getgrnam("cis90")
            cis90_grp = "cis90"
        except KeyError:
            cis90_grp = "adm"  # for testing on my machine

        self.check_files = CheckPath(
            "Oceans",
            files=[
                CheckDir("", group=cis90_grp, perms=0o777),
                CheckDir("Pacific", group=cis90_grp, perms=0o660),
                CheckDir("Atlantic", group=cis90_grp, perms=0o440),
                CheckDir("Indian", group=cis90_grp, perms=0o600),
                CheckDir("Fictional", group=cis90_grp, perms=0o600),
            ],
        )
        for file in self.start_files.files:
            assert isinstance(file, CheckFile), "Internal error."
            if "Pacific" in file.contents:
                newpath = Path("Pacific") / file.path
                newperms = 0o660
            elif "Atlantic" in file.contents:
                newpath = Path("Atlantic") / file.path
                newperms = 0o440
            elif "Indian" in file.contents:
                newpath = Path("Indian") / file.path
                newperms = 0o600
            elif "fiction" in file.contents:
                newpath = Path("Fictional") / file.path
                newperms = 0o600
            else:
                raise ValueError("Ooops:", file.contents)
            self.check_files.files.append(
                CheckFile(
                    newpath,
                    contents=file.contents,
                    perms=newperms,
                    group=cis90_grp,
                )
            )

    @property
    def text(self):
        return textwrap.dedent("""
        # Island Permissions 
        
        I have created a directory called `Islands` with the island files from 
        the previous island assignment. For this assignment update the 
        permissions of your island files to match the following:
                               
        {}
        """).format(self.check_files.markdown(detail=True))


walks: dict[str, list[KrozFlowABC]] = {}

questions: list[KrozFlowABC] = []

lab: dict[str, list[KrozFlowABC]] = {
    "Sort the Islands -- Part 2": [
        Islands2(),
    ],
}
