"""
Lab for week 3.
"""

from pathlib import Path

from kroz import KrozApp
from kroz.flows.base import settings
from kroz.questions.week03 import FlagFile, PathAttrs, RelativePaths, questions

app = KrozApp("The Filesystem", state_file="fs", debug=True)


@app.main
def main():
    app.show(
        """
        # Navigating the File System 

        Welcome! This lab tests your understanding of how to navigate the file 
        system. It covers the topics in class and in Chapter 2 of the book. 
        You should be familiar with these commands: 

        1. `cd`
        2. `pwd`
        3. `ls` 

        Make sure to watch the lesson before you continue. 
        """,
        classes="welcome",
        title="Welcome!",
    )

    with settings(checkpoint=True, name="week3"):
        for q in questions:
            q.show()

        FlagFile(type=FlagFile.FlagType.NAME, points=3).show()
        FlagFile(type=FlagFile.FlagType.DIR, points=2).show()
        PathAttrs(type=PathAttrs.AttrType.SIZE, points=5).show()
        PathAttrs(type=PathAttrs.AttrType.INODE, points=5).show()
        RelativePaths(from_path=Path.home(), points=5).show()

    app.show(
        """
        # Complete! 

        You've completed the lab. Your score is {} out of {}. 

        You will receive a confirmation code on the command line to submit to canvas.

        """.format(app.score, 20),
        classes="welcome",
        title="Bye!",
    )

    return app.confirmation()


if __name__ == "__main__":
    app.run()
