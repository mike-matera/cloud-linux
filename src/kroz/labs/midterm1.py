"""
Midterm 1
"""

import datetime

from kroz.app import KrozApp
from kroz.flow import FlowContext
from kroz.flow.base import FlowContext
from kroz.questions.lesson02 import (
    FreeMemory,
    OsRelease,
)
from kroz.questions.lesson03 import PathAttrs, RelativePaths
from kroz.questions.lesson04 import FileType, LinkInfo, MakeLink, WordInBigfile


def run():
    app = KrozApp("Midterm 1", state_file="midterm1")

    def run():
        if "started" not in app.state:
            app.state["started"] = datetime.datetime.now()
        try:
            with FlowContext(
                "questions", progress=True, points=100 / 9
            ) as flow:
                flow.run(OsRelease("PRETTY_NAME"))
                flow.run(FreeMemory(key="free"))
                flow.run(FileType())
                flow.run(RelativePaths())
                flow.run(LinkInfo(type=LinkInfo.Info.TARGET_PATH))
                flow.run(WordInBigfile(find=(3, 1)))
                flow.run(PathAttrs(type=PathAttrs.AttrType.BLOCKS))
                flow.run(LinkInfo(type=LinkInfo.Info.TARGET))
                flow.run(MakeLink(name="midterm1", rel=False))
        finally:
            app.state["exited"] = datetime.datetime.now()

    app.main(run)
    app.run()


def main():
    try:
        assert input("What's the password? ") == "meatball"
    except:
        print("Sorry.")
        return

    run()


if __name__ == "__main__":
    main()
