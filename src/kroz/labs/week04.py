"""
Lab for week 04
"""

from kroz import KrozApp
from kroz.flow import FlowContext
from kroz.questions.week03 import PathAttrs, RelativePaths
from kroz.questions.week04 import (
    FileType,
    LinkInfo,
    MakeLink,
    WordInBigfile,
    questions,
)

app = KrozApp(title="Files Lab", state_file="files")


@app.main
def main():
    app.show(
        """
        # Working with Files 

        Welcome! This lab gives you practice looking at the contents and metadata
        of files and directories. It covers the fourth week of class and chapter
        three of the book. Review these commands before starting the lab:

        1. `ls`
        2. `file`
        3. `less`
        3. `cat`
        3. `ln -s`

        Make sure to watch the lesson before you continue. 
        """,
        classes="welcome",
        title="Welcome!",
    )

    with FlowContext("questions", progress=True, points=0) as flow:
        for i, q in enumerate(questions):
            flow.run(q)

    with FlowContext("challenges", progress=True, name="week04") as flow:
        flow.run(
            PathAttrs(
                path_type=PathAttrs.PathType.DIR,
                type=PathAttrs.AttrType.INODE,
                points=2,
            )
        )
        flow.run(WordInBigfile(find=(1, 1), points=3))
        flow.run(FileType(points=3))
        flow.run(RelativePaths(points=3))
        flow.run(LinkInfo(type=LinkInfo.Info.TARGET_PATH, points=3))
        flow.run(LinkInfo(type=LinkInfo.Info.REL_OR_ABS, points=3))
        flow.run(MakeLink(name="my_link", points=3))


if __name__ == "__main__":
    app.run()
