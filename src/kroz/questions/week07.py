"""Questions for Week 7"""


from kroz.question import Question
import kroz.random as random
from kroz.random.bigfile import random_big_file

import textual.validation


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
        is not a part of another word (i.e. "oranges" and "orangeade" do not 
        count)?

        Hint: Look in the manual for `grep`.
        """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._file = random_big_file(rows=10000, cols=100)
        self._solution = None

    def setup_attempt(self):
        self._file.setup()
        self._solution = int(
            self.shell(f"grep -iw orange {self._file.path}  | wc -l")
        )

    def cleanup_attempt(self):
        self._file.cleanup()

    def check(self, answer: str):
        assert int(answer) == self._solution, f"""
            # Not Correct 

            That was not the correct answer. The correct answer is {self._solution}
            but will change after you exit this screen. 
            """


class SortedWords(Question):
    """Sort words in a file."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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

    def setup_attempt(self):
        self._file.setup()
        self._word = self.shell(f"sort {self._file.path} | head -n 1").strip()

    def cleanup_attempt(self):
        self._file.cleanup()

    def check(self, answer):
        assert answer.strip() == self._word, (
            f"""That's not the correct answer. {self._word}"""
        )


class UniqueWords(Question):
    """Unique words in a file."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._file = random_big_file(rows=random.randint(2000, 4000), cols=1)

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

    def setup_attempt(self):
        self._file.setup()
        self._answer = int(
            self.shell(f"sort {self._file.path} | uniq | wc -l")
        )

    def cleanup_attempt(self):
        self._file.cleanup()

    def check(self, answer):
        assert int(answer) == self._answer, f"""
            # Not Correct 

            That was not the correct answer. The correct answer is {self._answer}
            but will change after you exit this screen. 
            """

