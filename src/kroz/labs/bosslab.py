from kroz import KrozApp
from kroz.question import Question
from kroz.random.directory import random_directory

app = KrozApp("Like a BOSS!")

WELCOME = """
# Use Linux Like a BOSS!

In this lab you will use the advanced command features you learned in X Y 
"""


class RandomRando(Question):
    """Random directory stuff"""

    placeholder = "Enter to continue."

    text = """
    # Remove the "m" Files

    I have just (re)created a directory called "Rando" in your home directory.
    Remove all files with names that start with the letter "m" (lower case). """

    def setup(self):
        self._rd = random_directory(500)
        self._rd.setup()

    def cleanup(self):
        self._rd.cleanup()

    def check(self, answer):
        target = self._rd.filter(lambda x: not str(x.path).startswith("m"))
        target.full_report(verbose=2)


@app.main
def main():
    app.show(WELCOME, classes="welcome")
    app.ask(RandomRando())


if __name__ == "__main__":
    app.run()
