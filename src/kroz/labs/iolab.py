"""
Some lab called iolab or whatever.
"""

import kroz

from kroz.question import Question
from textual.validation import Integer

import time


class NumberGuess(Question):
    """Guess a number"""

    text = """
        # Guess a Number
        Guess a number between 1 and 100
    """

    validators = [Integer()]

    def check(self, answer):
        assert int(answer) == 69

    def setup(self):
        with kroz.progress() as p:
            p.update(message="Writing bigfile...")
            for progress in range(0, 100, 2):
                p.update(percent=progress)
                time.sleep(0.01)
        kroz.notify("The file `bigfile` has been updated.", title="Notice!")


WELCOME = """
# I/O Lab 

This is foo.
"""


app = kroz.KrozApp("The I/O Lab", WELCOME, total_score=100)


@app.setup
def setup():
    with kroz.progress("Doing setup()") as p:
        for progress in range(0, 100, 2):
            p.update(percent=progress)
            time.sleep(0.02)


@app.cleanup
def cleanup():
    with kroz.progress() as p:
        p.update(message="Deleting bifile")
        time.sleep(0.5)
        p.update(message="Removing files in Rando")
        time.sleep(0.5)


@app.main
def main():
    q1 = NumberGuess()
    app.ask(q1, points=10)

    q2 = NumberGuess()
    app.ask(q2, points=10)

    q3 = NumberGuess()
    app.ask(q3, points=10)


if __name__ == "__main__":
    quit(app.run())
