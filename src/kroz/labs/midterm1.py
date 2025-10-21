"""
Midterm 1
"""

import datetime

from kroz.app import KrozApp
from kroz.flow import FlowContext
from kroz.questions.lesson02 import (
    FreeMemory,
    OsRelease,
)
from kroz.questions.lesson03 import PathAttrs, RelativePaths
from kroz.questions.lesson04 import FileType, LinkInfo, MakeLink, WordInBigfile

app = KrozApp("Midterm 1", state_file="midterm1")


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
