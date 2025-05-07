"""
Some lab called islands2 or whatever.
"""

import grp

import kroz
from kroz.question import Question
from kroz.random.path import CheckPath, CheckFile

WELCOME = """
# Sort the Islands (Part 2) 

This lab builds on the original islands lab. It covers lessons X and Y. To do 
this lab you will need to understand the `chmod` and `chgrp` commands. 

Good luck!
"""


app = kroz.KrozApp("Sort the Islands (Part 2)")


class Islands2(Question):
    """The islands with perms."""

    placeholder = "Enter to Continue"

    try:
        cis90_grp = grp.getgrnam("cis90").gr_gid
    except Exception:
        cis90_grp = grp.getgrnam("adm").gr_gid  # for testing on my machine

    start_files = CheckPath(
        "/home/maximus/Islands",
        files=[
            CheckFile("Hawaii", "Island in the Pacific ocean"),
            CheckFile("Samoa", "Island in the Pacific ocean"),
            CheckFile("Kiribati", "Island in the Pacific ocean"),
            CheckFile("Ireland", "Island in the Atlantic ocean"),
            CheckFile("Madeira", "Island in the Atlantic ocean"),
            CheckFile("Azores", "Island in the Atlantic ocean"),
            CheckFile("Langkawi", "Island in the Indian ocean"),
            CheckFile("Sabang", "Island in the Indian ocean"),
            CheckFile("Nublar", "Island in Fiction"),
            CheckFile("Hydra", "Island in Fiction"),
        ],
    )

    end_files = CheckPath(
        "/home/maximus/Oceans",
        files=[
            CheckFile(
                "Pacific/Hawaii",
                "Island in the Pacific ocean",
                group=cis90_grp,
                perms=0o440,
            ),
            CheckFile(
                "Pacific/Samoa",
                "Island in the Pacific ocean",
                group=cis90_grp,
                perms=0o440,
            ),
            CheckFile(
                "Pacific/Kiribati",
                "Island in the Pacific ocean",
                group=cis90_grp,
                perms=0o440,
            ),
            CheckFile(
                "Atlantic/Ireland",
                "Island in the Atlantic ocean",
                group=cis90_grp,
                perms=0o440,
            ),
            CheckFile(
                "Atlantic/Madeira",
                "Island in the Atlantic ocean",
                group=cis90_grp,
                perms=0o440,
            ),
            CheckFile(
                "Atlantic/Azores",
                "Island in the Atlantic ocean",
                group=cis90_grp,
                perms=0o440,
            ),
            CheckFile(
                "Indian/Langkawi",
                "Island in the Indian ocean",
                group=cis90_grp,
                perms=0o600,
            ),
            CheckFile(
                "Indian/Sabang",
                "Island in the Indian ocean",
                group=cis90_grp,
                perms=0o600,
            ),
            CheckFile(
                "Fictional/Nublar",
                "Island in Fiction",
                group=cis90_grp,
                perms=0o600,
            ),
            CheckFile(
                "Fictional/Hydra",
                "Island in Fiction",
                group=cis90_grp,
                perms=0o600,
            ),
        ],
    )

    @property
    def text(self):
        return "Eat me"

    def setup(self):
        self.start_files.sync()

    def check(self, answer):
        for error in self.end_files.check():
            raise AssertionError(error)

        assert answer.strip() == "boo"


@app.main
def main():
    app.show(WELCOME)
    Islands2().ask()


if __name__ == "__main__":
    quit(app.run())
