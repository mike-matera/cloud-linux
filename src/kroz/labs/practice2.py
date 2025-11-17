"""
The practice midterm2.
"""

import datetime

from kroz.app import KrozApp
from kroz.flow.base import FlowContext
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
    if "started" not in app.state:
        app.state["started"] = datetime.datetime.now()
    try:
        with FlowContext("practice2", progress=False, points=0) as flow:
            flow.run(OsRelease("VERSION_CODENAME"))
            flow.run(FreeMemory(key="used"))
            flow.run(FileType())
            flow.run(RelativePaths())
            flow.run(WordInBigfile(cols=5, find=(2, 2)))
            flow.run(
                PathAttrs(
                    path_type=PathAttrs.PathType.DIR,
                    type=PathAttrs.AttrType.INODE,
                )
            )
            flow.run(LinkInfo(type=LinkInfo.Info.TARGET_PATH_INDIRECT))
            flow.run(MakeLink(name="practice2", rel=True))
            flow.run(Islands2())
            flow.run(CountOranges())
            flow.run(SortedWords())
            flow.run(DeepMessage())
            flow.run(ThisGrandparent())
            flow.run(ChildFind(ChildFind.ResourceType.CPU))
    finally:
        app.state["exited"] = datetime.datetime.now()


def main():
    try:
        assert input("What's the password? ") == "blink"
    except:
        print("Sorry.")
        return

    app.run()


if __name__ == "__main__":
    main()
