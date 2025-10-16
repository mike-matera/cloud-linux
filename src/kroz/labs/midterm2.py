"""
Midterm 1
"""

import datetime
import textwrap
from pathlib import Path

from kroz.app import KrozApp
from kroz.flow import FlowContext
from kroz.flow.question import Question
from kroz.questions.lesson02 import (
    FreeMemory,
    NewYearFuture,
    OsRelease,
)
from kroz.questions.lesson03 import PathAttrs, RelativePaths
from kroz.questions.lesson04 import FileType, LinkInfo, MakeLink, WordInBigfile
from kroz.questions.lesson07 import CountOranges, SortedWords, UniqueWords
from kroz.questions.lesson08 import (
    DeepMessage,
    RandomDeleteMe,
    RandomRando,
    RandomRandoTick,
)
from kroz.questions.lesson09 import Islands2
from kroz.questions.lesson10 import (
    ChildFind,
    ThisGrandparent,
    ThisParent,
    ThisProcess,
    TopBackground,
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
    if "started" not in app.state:
        app.state["started"] = datetime.datetime.now()
    try:
        with FlowContext("questions", progress=False, points=100 / 9) as flow:
            flow.run(OsRelease("PRETTY_NAME"))
            flow.run(FreeMemory(key="free"))
            flow.run(FileType())
            flow.run(RelativePaths(verbose=False))
            flow.run(LinkInfo(type=LinkInfo.Info.TARGET_PATH))
            flow.run(WordInBigfile(cols=5, find=(3, 2)))
            flow.run(PathAttrs(type=PathAttrs.AttrType.INODE))
            flow.run(LinkInfo(type=LinkInfo.Info.TARGET))
            flow.run(MakeLink(name="midterm1", rel=False))

            flow.run(NewYearFuture(tries=1))
            flow.run(OsRelease("VERSION_CODENAME"))
            flow.run(FreeMemory(key="used"))
            flow.run(FileType())
            flow.run(RelativePaths())
            flow.run(WordInBigfile(cols=5, find=(2, 2)))
            flow.run(PathAttrs(type=PathAttrs.AttrType.INODE))
            flow.run(LinkInfo(type=LinkInfo.Info.TARGET))
            flow.run(MakeLink(name="practice1", rel=True))
            flow.run(Islands2())
            flow.run(CountOranges())
            flow.run(SortedWords())
            flow.run(UniqueWords())
            flow.run(RandomRando())
            flow.run(RandomRandoTick())
            flow.run(RandomDeleteMe())
            flow.run(DeepMessage())
            flow.run(ThisProcess())
            flow.run(ThisParent())
            flow.run(ThisGrandparent())
            flow.run(TopBackground())
            flow.run(ChildFind(ChildFind.ResourceType.COUNT))

    finally:
        app.state["exited"] = datetime.datetime.now()


def main():
    try:
        assert input("What's the password? ") == "meatball"
    except:
        print("Sorry.")
        return

    app.run()


if __name__ == "__main__":
    main()
