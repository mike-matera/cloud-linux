"""
Some lab called islands2 or whatever.
"""

import grp
from pathlib import Path

import kroz
from kroz.question import Question
from kroz.random.path import CheckDir, CheckPath, CheckFile

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
    debug = True

    try:
        grp.getgrnam("cis90")
        cis90_grp = "cis90"
    except KeyError:
        cis90_grp = "adm"  # for testing on my machine

    text = """
    # Sort the Islands with Permissions 
    
    I have created a directory called "Islands" in your home directory. 
    Inside of "Islands" you will see 10 files named after islands. Each island 
    file contains the name of the ocean it is in. Reorganize the files so 
    that they are in directories named after their oceans. The reorganized 
    files should be in a directory called "Oceans" in the current directory.  
    
    The "Oceans" directory should look like this: 

        .
        |-- Oceans
            |-- Atlantic
            |-- Pacific
            |-- Indian
            |-- Fictional

    In addition you must set permissions on the files and directories in Oceans.
    Here are the rules you must follow: 

    1. The Oceans directory and all subdirectories and files should be have the 'cis90' group.
    2. No files or directories should be publicly readable, writable or executable.
    3. Files in the Atlantic and Pacific oceans should be read only for the user and group. 
    4. Files in the Indian and Fictional oceans should be read/write for the user only. 

"""

    def setup(self):
        self.start_files = CheckPath(
            "Islands",
            files=[
                CheckFile(
                    "Hawaii", "Hawaii is an island in the Pacific ocean"
                ),
                CheckFile("Samoa", "Samoa is an island in the Pacific ocean"),
                CheckFile(
                    "Kiribati", "Kiribati is an island in the Pacific ocean"
                ),
                CheckFile(
                    "Ireland", "Ireland is an island in the Atlantic ocean"
                ),
                CheckFile(
                    "Madeira", "Madeira is an island in the Atlantic ocean"
                ),
                CheckFile(
                    "Azores", "Azores is an island in the Atlantic ocean"
                ),
                CheckFile(
                    "Langkawi", "Langkawi is an island in the Indian ocean"
                ),
                CheckFile("Sabang", "Sabang is an island in the Indian ocean"),
                CheckFile(
                    "Nublar",
                    "Nublar is a fictional island in the movie Jurassic Park",
                ),
                CheckFile(
                    "Hydra", "Hydra is a fictional island in the show Lost"
                ),
            ],
        )

        self.check_files = CheckPath(
            "Oceans",
            files=[
                CheckDir("", group=self.cis90_grp),
                CheckDir("Pacific", group=self.cis90_grp),
                CheckDir("Atlantic", group=self.cis90_grp),
                CheckDir("Indian", group=self.cis90_grp),
                CheckDir("Fictional", group=self.cis90_grp),
            ],
        )

        self.start_files.sync()
        for file in self.start_files.files:
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
                    group=self.cis90_grp,
                )
            )

    def check(self, answer):
        self.check_files.full_report(verbose=2)


@app.main
def main():
    app.show(WELCOME, classes="welcome")
    app.ask(Islands2())


if __name__ == "__main__":
    quit(app.run())
