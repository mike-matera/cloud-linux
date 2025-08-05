"""
Lab for week 3.
"""

from pathlib import Path

from kroz import KrozApp
from kroz.flow import FlowContext
from kroz.questions.lesson03 import (
    FlagFile,
    PathAttrs,
    RelativePaths,
    questions,
)

app = KrozApp("The Filesystem", state_file="fs")


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

    with FlowContext("questions", progress=True) as flow:
        for q in questions:
            flow.run(q)

        flow.run(FlagFile(type=FlagFile.FlagType.NAME, points=3))
        flow.run(FlagFile(type=FlagFile.FlagType.DIR, points=2))
        flow.run(PathAttrs(type=PathAttrs.AttrType.SIZE, points=5))
        flow.run(PathAttrs(type=PathAttrs.AttrType.INODE, points=5))
        flow.run(RelativePaths(from_path=Path.home(), points=5))

    app.show(
        """
        # Complete! 

        You've completed the lab. Your score is {} out of {}. 

        You will receive a confirmation code on the command line to submit to canvas.

        """.format(app.score, 20),
        classes="welcome",
        title="Bye!",
    )


if __name__ == "__main__":
    app.run()
