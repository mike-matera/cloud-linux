"""
Some lab called iolab or whatever.
"""

import kroz
from kroz.questions.week07 import CountOranges, SortedWords, UniqueWords
from kroz.questions.week04 import WordInBigfile



WELCOME = """
# I/O Lab 

Foo!
"""


app = kroz.KrozApp("The I/O Lab")


@app.main
def main():
    app.show(WELCOME, classes="welcome")
    app.ask(WordInBigfile(find=[None, 1]))
    app.ask(CountOranges())
    app.ask(UniqueWords(points=10))
    app.ask(SortedWords())
    app.ask(WordInBigfile(from_bottom=True, find=[None, 1]))
    app.ask(WordInBigfile())
    app.ask(WordInBigfile(from_right=True))


if __name__ == "__main__":
    quit(app.run())
