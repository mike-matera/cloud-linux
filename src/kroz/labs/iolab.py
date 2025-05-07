"""
Some lab called iolab or whatever.
"""

import random

import kroz

from kroz.question import Question
from kroz.random.file import random_big_file

import textual.validation


class WordInBigfile(Question):
    """Find a particular word in a big big file."""

    def __init__(
        self,
        rows=100000,
        cols=100,
        find=(None, None),
        from_bottom=False,
        from_right=False,
    ):
        self._file = random_big_file(rows=rows, cols=cols)
        self._find = [*find]
        if find[0] is None:
            if not from_bottom:
                self._find[0] = random.randint(0, rows - 1) + 1
            else:
                self._find[0] = random.randint(1 - rows, -1)

        if find[1] is None:
            if not from_right:
                self._find[1] = random.randint(0, cols - 1) + 1
            else:
                self._find[1] = random.randint(1 - cols, -1)

    @property
    def text(self):
        if self._find[0] >= 0:
            line_no = self._find[0]
        else:
            line_no = f"{-self._find[0]} from the **bottom** of the file."

        if self._find[1] >= 0:
            word_no = self._find[1]
        else:
            word_no = f"{-self._find[1]} from the **end** of the line."

        return f"""
        # Find the Word 

        I have just created the file called:
         
        `{self._file.path}`
        
        Inside of it you will find a lot of words. To solve this challenge find 
        the word in the following place: 

        * Line number: {line_no} 
        * Word number: {word_no}

        Enter the word in the answer box below.
        """

    placeholder = "Word"
    validators = []

    def setup(self):
        self._file.setup()

    def cleanup(self):
        self._file.cleanup()

    def check(self, answer):
        solution = self._file.word_at(self._find[0], self._find[1])
        assert answer.strip() == solution, """
        # Incorrect!

        That is not the correct word.
        """


class CountOranges(Question):
    """Use grep and wc together to find lines with a word."""

    validators = [textual.validation.Integer()]
    placeholder = "Number of lines"

    @property
    def text(self):
        return f"""
        # Find a Word

        I have just created the file called:
         
        `{self._file.path}`

        How many lines contain the word "orange" or "Orange" where "orange" 
        is not a part of another word (i.e. "oranges" and "orangeade" do not count)?

        Hint: Look in the manual for `grep`.
        """

    def __init__(
        self,
    ):
        self._file = random_big_file(rows=10000, cols=100)
        self._solution = None

    def setup(self):
        self._file.setup()
        self._solution = int(
            self.shell(f"grep -iw orange {self._file.path}  | wc -l")
        )

    def cleanup(self):
        self._file.cleanup()

    def check(self, answer: str):
        assert int(answer) == self._solution, (
            f"""The correct answer is: {self._solution}"""
        )


class SortedWords(Question):
    """Sort words in a file."""

    def __init__(self):
        self._file = random_big_file(rows=1000, cols=1)

    @property
    def text(self):
        return f"""
        # Sort a Big File

        I have just created the file called:
         
        `{self._file.path}`

        If the file is sorted in alphabetical order what would be the first word? 
    """

    placeholder = "Word"

    def setup(self):
        self._file.setup()
        self._word = self.shell(f"sort {self._file.path} | head -n 1").strip()

    def cleanup(self):
        self._file.cleanup()

    def check(self, answer):
        assert answer.strip() == self._word, (
            f"""That's not the correct answer. {self._word}"""
        )


class UniqueWords(Question):
    """Unique words in a file."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._file = random_big_file(rows=2000, cols=1)

    @property
    def text(self):
        return f"""
        # Unique Words

        I have just created the file called:
         
        `{self._file.path}`

        How many unique words are in it? 
    """

    validators = [textual.validation.Integer()]
    placeholder = "Number of unique words"

    def setup(self):
        self._file.setup()
        self._answer = int(
            self.shell(f"sort {self._file.path} | uniq | wc -l")
        )

    def cleanup(self):
        self._file.cleanup()

    def check(self, answer):
        assert int(answer) == self._answer, (
            f"""That's not the correct answer. {self._answer}"""
        )


WELCOME = f"""
# I/O Lab 

{"This is foo." * 100}
"""


app = kroz.KrozApp("The I/O Lab")


@app.main
def main():
    app.show(WELCOME)
    CountOranges().ask()
    UniqueWords(can_skip=True, points=10).ask()
    SortedWords().ask()
    WordInBigfile(find=[None, 1]).ask()
    WordInBigfile(from_bottom=True, find=[None, 1]).ask()
    WordInBigfile().ask()
    WordInBigfile(from_right=True).ask()
    print("Foo!")


if __name__ == "__main__":
    quit(app.run())
