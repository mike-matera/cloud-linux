"""
Some lab called iolab or whatever.
"""

import kroz
from kroz.questions.week04 import WordInBigfile
from kroz.questions.week07 import CountOranges, SortedWords, UniqueWords

WELCOME = """
# I/O Lab 

Foo!
"""


app = kroz.KrozApp("The I/O Lab")


@app.main
def main():
    app.show(WELCOME, classes="welcome")
    WordInBigfile(find=[None, 1]).ask()
    CountOranges().ask()
    UniqueWords(points=10).ask()
    SortedWords().ask()
    WordInBigfile(from_bottom=True, find=[None, 1]).ask()
    WordInBigfile().ask()
    WordInBigfile(from_right=True).ask()


if __name__ == "__main__":
    quit(app.run())
