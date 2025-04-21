"""
Some lab called iolab or whatever.
"""

import kroz

from kroz.question import Question
from textual.validation import Integer


class NumberGuess(Question):
    """Guess a number"""

    def __init__(self, limit=100):
        self._limit = limit

    @property
    def text(self):
        return f"""
            # Guess a Number
            Guess a number between 1 and {self._limit}
        """

    @property
    def placeholder(self):
        return f"A number between 1 and {self._limit}"

    @property
    def validators(self):
        return [Integer(minimum=1, maximum=self._limit)]

    def check(self, answer):
        assert int(answer) == 69, "You fucked it."


WELCOME = f"""
# I/O Lab 

{"This is foo." * 100}
"""


app = kroz.KrozApp("The I/O Lab", WELCOME)


@app.main
def main():
    with app.group():
        app.ask(NumberGuess(100), points=10)
        app.ask(NumberGuess(200), points=10)
        app.ask(NumberGuess(300), points=10)

    with app.group():
        app.ask(NumberGuess(100), points=10)
        app.ask(NumberGuess(200), points=10)
        app.ask(NumberGuess(300), points=10)


if __name__ == "__main__":
    quit(app.run())
