"""
Lab for week 04
"""

from kroz import KrozApp
from kroz.questions.week03 import PathAttrs
from kroz.questions.week04 import FileType, WordInBigfile

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

        Make sure to watch the lesson before you continue. 
        """,
        classes="welcome",
        title="Welcome!",
    )

    app.ask(
        PathAttrs(
            path_type=PathAttrs.PathType.DIR, type=PathAttrs.AttrType.INODE
        )
    )

    app.ask(WordInBigfile(find=(1, 1)))
    app.ask(FileType())


if __name__ == "__main__":
    print("Your confirmation code is:", app.run())
