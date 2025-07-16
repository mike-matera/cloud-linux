"""
Helper for streams of random words.
"""

from os import PathLike

import kroz.random as random
from kroz import KrozApp


class RandomWord:
    """
    Produce random words from the dictionary.
    """

    def __init__(self):
        """Create a word randomizer based on the selected dictionary."""
        self._words = []

    def setup(self, dictionary: str | PathLike[str]):
        """
        Initialize the randomizer. This must be done before any other calls
        can be used.
        """

        with open(dictionary) as fh:
            self._words = [w.strip() for w in fh]

    def choice(self) -> str:
        """Return a single random word."""
        if not self._words:
            raise RuntimeError(
                "The dictionary has not been initialized. You have not run setup()"
            )
        return random.choice(self._words)

    def choices(self, num: int) -> list[str]:
        """Return a list of random words."""
        if not self._words:
            raise RuntimeError(
                "The dictionary has not been initialized. You have not run setup()"
            )
        return random.choices(self._words, k=num)


_words = RandomWord()


def random_words() -> RandomWord:
    global _words
    return _words


def _setup():
    global _words
    _words.setup(KrozApp.appconfig("dictionary"))


KrozApp.setup_hook(
    hook=_setup,
    defconfig={
        "dictionary": "/usr/share/dict/words",
    },
)
