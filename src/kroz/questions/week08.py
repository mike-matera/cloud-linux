import pathlib

from kroz import KrozApp
from kroz.flow.question import (
    Question,
)
from kroz.random.bigdir import random_directory
from kroz.random.words import random_words


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


class RandomRandoTick(Question):
    """Random directory stuff"""

    placeholder = "Enter to continue."

    text = """
    # Remove the "'" Files

    Remove all files with names that contain a single quote (') character. 
    """

    def setup(self):
        self._rd = random_directory(500)
        self._rd.setup()

    def cleanup(self):
        self._rd.cleanup()

    def check(self, answer):
        target = self._rd.filter(lambda x: "'" not in str(x.path))
        target.full_report(verbose=2)


class RandomDeleteMe(Question):
    """Random directory stuff"""

    placeholder = "Enter to continue."

    text = """
    # Remove the "'" Files

    Remove all files that contain the word "delete" in them. 
    """

    def setup(self):
        self._rd = random_directory(500)
        self._rd.setup()

    def cleanup(self):
        self._rd.cleanup()

    def check(self, answer):
        target = self._rd.filter(lambda x: "delete" not in str(x.contents))
        target.full_report(verbose=2)


class DeepMessage(Question):
    placeholder = "What is the secret word?"

    text = """
    # Deep Directory 

    Look in ~/Files and find the hidden message.
    """

    def setup(self):
        self._answer = random_words().choice()
        path = KrozApp.appconfig("default_path") / pathlib.Path(
            "Files/deep/there's/a/light/over/at/the/Frankenstein/place/there's/a/li/ii/ii/ii/ii/ii/ii/ight/burning/in/the/fire/place"
        )
        file = path / ".secret"
        path.mkdir(parents=True, exist_ok=True)
        with open(file.resolve(), "w") as fh:
            fh.write(self._answer + "\n")

    def check(self, answer):
        assert answer.strip() == self._answer, """That's not correct!"""


app = KrozApp("Like a BOSS!", state_file="bosslab")

WELCOME = """
# Use Linux Like a BOSS!

In this lab you will use the advanced command features you learned in X Y 
"""
