"""
The practice midterm2.
"""

from kroz.app import KrozApp
from kroz.labs.exam import exam
from kroz.questions.lesson02 import FreeMemory, OsRelease
from kroz.questions.lesson03 import PathAttrs, RelativePaths
from kroz.questions.lesson04 import FileType, LinkInfo, MakeLink, WordInBigfile
from kroz.questions.lesson07 import CountOranges, SortedWords
from kroz.questions.lesson08 import (
    DeepMessage,
)
from kroz.questions.lesson09 import Islands2
from kroz.questions.lesson10 import (
    ChildFind,
    ThisGrandparent,
)

app = KrozApp("Practice Midterm 2", state_file="practice2")


@app.main
def run():
    return exam(
        OsRelease("VERSION_CODENAME"),
        FreeMemory(key="used"),
        FileType(),
        RelativePaths(),
        WordInBigfile(cols=5, find=(2, 2)),
        PathAttrs(
            path_type=PathAttrs.PathType.DIR, type=PathAttrs.AttrType.INODE
        ),
        LinkInfo(type=LinkInfo.Info.TARGET_PATH_INDIRECT),
        MakeLink(name="practice2", rel=True),
        Islands2(),
        CountOranges(),
        SortedWords(),
        DeepMessage(),
        ThisGrandparent(),
        ChildFind(ChildFind.ResourceType.CPU),
    )


def main():
    try:
        assert input("What's the password? ") == "blink"
    except AssertionError:
        print("Sorry.")
        return

    app.run()


if __name__ == "__main__":
    main()
