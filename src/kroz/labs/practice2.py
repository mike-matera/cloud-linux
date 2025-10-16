"""
The practice midterm.
"""

import datetime

from kroz.app import KrozApp
from kroz.flow.base import FlowContext
from kroz.questions.lesson02 import FreeMemory, NewYearFuture, OsRelease
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

app = KrozApp("Practice Midterm 2")


@app.main
def run():
    if "started" not in app.state:
        app.state["started"] = datetime.datetime.now()
    try:
        with FlowContext("questions", progress=False, points=10) as flow:
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
        assert input("What's the password? ") == "blink"
    except:
        print("Sorry.")
        return

    app.run()


if __name__ == "__main__":
    main()
