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
    WordInBigfile(find=[None, 1]).show()
    CountOranges().show()
    UniqueWords(points=10).show()
    SortedWords().show()
    WordInBigfile(from_bottom=True, find=[None, 1]).show()
    WordInBigfile().show()
    WordInBigfile(from_right=True).show()

    return app.confirmation()


if __name__ == "__main__":
    app.run()
