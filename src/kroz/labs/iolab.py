"""
Some lab called iolab or whatever.
"""

import kroz

from kroz.question import Question
import time


class NumberGuess(Question):
    """Guess a number"""

    @property
    def text(self):
        return """
            # Guess a Number

            Guess a number between 1 and 100
        """

    async def check(self, answer):
        return int(answer) == 69

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
    with kroz.progress() as p:
        for progress in range(0, 100, 2):
            p.update(percent=progress)
            time.sleep(0.02)


@app.cleanup
def cleanup():
    with kroz.progress() as p:
        p.update(message="Deleting bifile")
        time.sleep(1)
        p.update(message="Removing files in Rando")
        time.sleep(2)


@app.main
def main():
    q1 = NumberGuess(points=10)
    app.ask(q1)

    with kroz.progress() as p:
        for progress in range(0, 100, 2):
            p.update(
                percent=progress, message=f"Doing other stuff: {progress}%"
            )
            time.sleep(0.01)

    kroz.notify(
        "The file `bigfile` has been updated and contains new data.",
        title="Wrote bigfile",
    )

    q2 = NumberGuess(points=10)
    app.ask(q2)

    q3 = NumberGuess(points=10)
    app.ask(q3)


if __name__ == "__main__":
    quit(app.run())
