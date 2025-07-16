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

    with FlowContext(checkpoint=True, points=0) as flow:
        for i, q in enumerate(questions):
            flow.run(q)

    with FlowContext(checkpoint=True, points=3) as flow:
        flow.run(
            PathAttrs(
                path_type=PathAttrs.PathType.DIR, type=PathAttrs.AttrType.INODE
            )
        )
        flow.run(WordInBigfile(find=(1, 1)))
        flow.run(FileType())
        flow.run(RelativePaths())
        flow.run(LinkInfo(type=LinkInfo.Info.TARGET_PATH))
        flow.run(LinkInfo(type=LinkInfo.Info.REL_OR_ABS))
        flow.run(MakeLink(name="my_link"))

    return app.confirmation()


if __name__ == "__main__":
    app.run()
