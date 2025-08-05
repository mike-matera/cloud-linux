"""
Some lab called iolab or whatever.
"""

import kroz
from kroz.flow import FlowContext
from kroz.questions.lesson04 import WordInBigfile
from kroz.questions.lesson07 import CountOranges, SortedWords, UniqueWords

WELCOME = """
# I/O Lab 

Foo!
"""


app = kroz.KrozApp("The I/O Lab")


@app.main
def main():
    app.show(WELCOME, classes="welcome")
    with FlowContext("challenges", progress=True, name="lab07_") as flow:
        flow.run(WordInBigfile(find=[None, 1]))
        flow.run(CountOranges())
        flow.run(UniqueWords())
        flow.run(SortedWords())
        flow.run(WordInBigfile(from_bottom=True, find=[None, 1]))
        flow.run(WordInBigfile())
        flow.run(WordInBigfile(from_right=True))


if __name__ == "__main__":
    app.run()
