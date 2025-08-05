"""
Lab for week 2.
"""

import textwrap

from kroz import KrozApp
from kroz.ascii import tux
from kroz.flow import FlowContext
from kroz.questions.lesson02 import (
    FreeMemory,
    NewYearFuture,
    OsRelease,
)
from kroz.questions.lesson03 import PathAttrs, RelativePaths
from kroz.questions.lesson04 import FileType, LinkInfo, MakeLink, WordInBigfile

app = KrozApp("Midterm 1", state_file="mt1")


@app.main
def main() -> None:
    app.show(
        textwrap.dedent("""
        # Welcome to Midterm #1 

        """).format(tux(indent=4)),
        classes="welcome",
        title="Welcome!",
    )

    with FlowContext("questions", progress=True) as flow:
        flow.run(NewYearFuture())
        flow.run(OsRelease("VERSION"))
        flow.run(FreeMemory(key="free"))
        flow.run(FileType())
        flow.run(RelativePaths())
        flow.run(LinkInfo(type=LinkInfo.Info.TARGET_PATH))
        flow.run(WordInBigfile(find=(1, 1)))
        flow.run(PathAttrs(type=PathAttrs.AttrType.BLOCKS))
        flow.run(LinkInfo(type=LinkInfo.Info.REL_OR_ABS))
        flow.run(MakeLink(name="test_link", rel=True))


if __name__ == "__main__":
    app.run()
