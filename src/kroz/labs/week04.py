"""
Lab for week 04
"""

from kroz import KrozApp
from kroz.flows import settings
from kroz.questions.week03 import PathAttrs, RelativePaths
from kroz.questions.week04 import (
    FileType,
    LinkInfo,
    MakeLink,
    WordInBigfile,
    questions,
)

app = KrozApp(title="Files Lab", state_file="files", debug=True)


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

    with settings(checkpoint=True, points=100):
        for i, q in enumerate(questions):
            q.show()

        with settings(points=3):
            PathAttrs(
                path_type=PathAttrs.PathType.DIR, type=PathAttrs.AttrType.INODE
            ).show()
            WordInBigfile(find=(1, 1)).show()
            FileType().show()
            RelativePaths().show()
            LinkInfo(type=LinkInfo.Info.TARGET_PATH).show()
            LinkInfo(type=LinkInfo.Info.REL_OR_ABS).show()
            MakeLink(name="my_link").show()

    return app.confirmation()


if __name__ == "__main__":
    app.run()
