"""
Midterm 2
"""

import textwrap
from pathlib import Path

from kroz.app import KrozApp
from kroz.flow.question import Question
from kroz.labs.exam import exam
from kroz.questions.lesson02 import (
    FreeMemory,
    NewYearFuture,
    OsRelease,
)
from kroz.questions.lesson03 import PathAttrs
from kroz.questions.lesson04 import FileType, LinkInfo, MakeLink, WordInBigfile
from kroz.questions.lesson07 import UniqueWords
from kroz.questions.lesson08 import (
    DeepMessage,
    RandomRando,
)
from kroz.questions.lesson10 import (
    ChildFind,
    ThisGrandparent,
)
from kroz.random.path import CheckDir, CheckFile, CheckPath

app = KrozApp("Midterm 2", state_file="midterm2")


class Counties(Question):
    """Counties."""

    placeholder = "Enter to Continue"

    def setup(self):
        self.start_files = CheckPath(
            "Cities",
            files=[
                CheckFile("San Francisco", "San Francisco County"),
                CheckFile("Santa Cruz", "Santa Cruz County"),
                CheckFile("Los Angeles", "Los Angeles County"),
                CheckFile("Fresno", "Fresno County"),
                CheckFile("Oakland", "Alameda County"),
                CheckFile("Eureka", "Humboldt County"),
                CheckFile("Watsonville", "Santa Cruz County"),
                CheckFile("Aptos", "Santa Cruz County"),
                CheckFile("San Luis Obispo", "San Luis Obispo County"),
                CheckFile("Fortuna", "Humboldt County"),
            ],
        )

        self.check_files = CheckPath(
            "Counties",
            files=[
                CheckDir("San Francisco"),
                CheckDir("Santa Cruz"),
                CheckDir("Los Angeles"),
                CheckDir("Fresno"),
                CheckDir("Alameda"),
                CheckDir("Humboldt"),
                CheckDir("San Luis Obispo"),
            ],
        )
        for file in self.start_files.files:
            assert isinstance(file, CheckFile), "Internal error."
            if "Francisco" in file.contents:
                newpath = Path("San Francisco") / file.path
                newperms = file.perms
            elif "Cruz" in file.contents:
                newpath = Path("Santa Cruz") / file.path
                newperms = 0o600
            elif "Angeles" in file.contents:
                newpath = Path("Los Angeles") / file.path
                newperms = file.perms
            elif "Fresno" in file.contents:
                newpath = Path("Fresno") / file.path
                newperms = file.perms
            elif "Alameda" in file.contents:
                newpath = Path("Alameda") / file.path
                newperms = file.perms
            elif "Humboldt" in file.contents:
                newpath = Path("Humboldt") / file.path
                newperms = file.perms
            elif "Obispo" in file.contents:
                newpath = Path("San Luis Obispo") / file.path
                newperms = file.perms
            else:
                raise ValueError(
                    f"Ooops: file: {file.path} contents: {file.contents}"
                )

            self.check_files.files.append(
                CheckFile(
                    newpath,
                    contents=file.contents,
                    perms=newperms,
                )
            )

        self.start_files.sync()

    @property
    def text(self):
        return textwrap.dedent("""
        # Sort the Cities
        
        I have created a directory called `Cities` that looks like this:
                               
        {}

        Inside of `Cities` you will see files named after cities. Sort the
        cities into their respective counties so they look like this:

        {}
        """).format(
            self.start_files.markdown(), self.check_files.markdown(detail=True)
        )

    def cleanup(self):
        self.start_files.cleanup()

    def check(self, answer):
        self.check_files.full_report(verbose=0)


@app.main
def run():
    return exam(
        OsRelease("ID_LIKE", points=10),
        FreeMemory(key="shared", points=10),
        FileType(points=10),
        WordInBigfile(cols=5, from_bottom=True, points=10),
        PathAttrs(
            path_type=PathAttrs.PathType.DIR,
            type=PathAttrs.AttrType.INODE,
            points=10,
        ),
        LinkInfo(type=LinkInfo.Info.TARGET_PATH_INDIRECT, points=10),
        MakeLink(name="midterm2", rel=False, points=10),
        NewYearFuture(tries=2, points=10),
        Counties(points=10),
        UniqueWords(points=10),
        RandomRando(points=10),
        DeepMessage(points=10),
        ThisGrandparent(points=10),
        ChildFind(ChildFind.ResourceType.NICE, points=10),
        timelimit=180,
    )


def main():
    try:
        assert input("What's the password? ") == "hildegard"
    except AssertionError:
        print("Sorry.")
        return

    app.run()


if __name__ == "__main__":
    main()
