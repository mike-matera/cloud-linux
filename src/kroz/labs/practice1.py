"""
The practice midterm.
"""

from kroz.app import KrozApp
from kroz.labs.exam import exam
from kroz.questions.lesson02 import FreeMemory, NewYearFuture, OsRelease
from kroz.questions.lesson03 import PathAttrs, RelativePaths
from kroz.questions.lesson04 import FileType, LinkInfo, MakeLink, WordInBigfile

app = KrozApp("Practice Midterm 1")


@app.main
def run():
    exam(
        NewYearFuture(tries=1),
        OsRelease("VERSION_CODENAME"),
        FreeMemory(key="used"),
        FileType(),
        RelativePaths(),
        WordInBigfile(cols=5, find=(2, 2)),
        PathAttrs(type=PathAttrs.AttrType.PERMS),
        LinkInfo(type=LinkInfo.Info.TARGET),
        MakeLink(name="practice1", rel=True),
    )


def main():
    try:
        assert input("What's the password? ") == "polpetta"
    except AssertionError:
        print("Sorry.")
        return

    app.run()


if __name__ == "__main__":
    main()
