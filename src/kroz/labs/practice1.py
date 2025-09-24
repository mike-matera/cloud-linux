"""
The practice midterm.
"""

import datetime

from kroz.flow.base import FlowContext
from kroz.questions.lesson02 import FreeMemory, NewYearFuture, OsRelease
from kroz.questions.lesson03 import PathAttrs, RelativePaths
from kroz.questions.lesson04 import FileType, LinkInfo, MakeLink, WordInBigfile


def run():
    from kroz.app import KrozApp

    app = KrozApp("Practice Midterm 1")

    def run():
        if "started" not in app.state:
            app.state["started"] = datetime.datetime.now()
        try:
            with FlowContext("questions", progress=True, points=10) as flow:
                flow.run(NewYearFuture(tries=1))
                flow.run(OsRelease("VERSION_CODENAME"))
                flow.run(FreeMemory(key="used"))
                flow.run(FileType())
                flow.run(RelativePaths())
                flow.run(WordInBigfile(cols=5, find=(2, 2)))
                flow.run(PathAttrs(type=PathAttrs.AttrType.PERMS))
                flow.run(LinkInfo(type=LinkInfo.Info.TARGET))
                flow.run(MakeLink(name="practice1", rel=True))
        finally:
            app.state["exited"] = datetime.datetime.now()

    app.main(run)
    app.run()


def main():
    try:
        assert input("What's the password? ") == "polpetta"
    except:
        print("Sorry.")
        return

    run()


if __name__ == "__main__":
    main()
