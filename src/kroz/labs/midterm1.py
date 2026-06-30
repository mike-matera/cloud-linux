"""
Midterm 1
"""

from kroz.app import KrozApp
from kroz.labs.exam import exam
from kroz.questions.lesson02 import (
    FreeMemory,
    OsRelease,
)
from kroz.questions.lesson03 import PathAttrs, RelativePaths
from kroz.questions.lesson04 import FileType, LinkInfo, MakeLink, WordInBigfile

app = KrozApp("Midterm 1", state_file="midterm1")


@app.main
def run():
    return exam(
        OsRelease("PRETTY_NAME", points=20),
        FreeMemory(key="free", points=10),
        FileType(points=10),
        RelativePaths(verbose=False, points=10),
        LinkInfo(type=LinkInfo.Info.TARGET_PATH, points=10),
        WordInBigfile(cols=5, find=(3, 2), points=10),
        PathAttrs(type=PathAttrs.AttrType.INODE, points=10),
        LinkInfo(type=LinkInfo.Info.TARGET, points=10),
        MakeLink(name="midterm1", rel=False, points=10),
        timelimit=120,
    )


def main():
    try:
        assert input("What's the password? ") == "meatball"
    except AssertionError:
        print("Sorry.")
        return

    app.run()


if __name__ == "__main__":
    main()
