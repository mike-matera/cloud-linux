"""
Abstract Question Base
"""

from abc import ABC, abstractmethod
from enum import Enum
import random
import re
import subprocess
import textwrap
from typing import Iterable
import textual
from textual.validation import Validator
import textual.validation


class Question(ABC):
    """
    The base class of a question for the KROZ player.
    """

    class Result(Enum):
        CORRECT = 1
        INCORRECT = 2
        SKIPPED = 3
        CHECKPOINTED = 4

    # The displayed text of the question. Interpreted as Markdown
    text: str | property

    # Textual Validators that will be used by the input. Help students get the
    # right type of answer (e.g. int)
    validators: Validator | Iterable[Validator] | property = []

    # Placeholder that will show in the empty Input. Help students figure out
    # what the answer should look like.
    placeholder: str | property = "Answer"

    # Number of tries
    tries: int | property = 0
    can_skip: bool | property = True
    points: int | property = 0
    checkpoint: bool | property = False
    debug: bool | property = False

    def __init__(self, **kwargs):
        self._name: str | None = None
        for key in kwargs:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            else:
                raise RuntimeError(f"Invalid keyword argument: {key}")

    @property
    def name(self) -> str:
        """
        This is the identifier used to checkpoint this question. It should be
        unique inside of a lab to ensure checkpoints work correctly. If not
        specified it will be the name of the class.
        """
        if self._name:
            return self._name
        else:
            return f"{self.__module__}.{self.__class__.__name__}"

    @name.setter
    def name(self, value):
        """Set the name so subclasses and instances can override the name."""
        self._name = value

    @abstractmethod
    def check(self, answer: str) -> None:
        """
        **Required.** Check the answer as entered by the user. This method
        should return if the answer is correct and raise an exception if the
        answer is incorrect. `AssertionError`s will have their messages
        interpreted as Markdown and be displayed as feedback to the student.
        Other exceptions will be displayed as feedback with no stack trace,
        unless debugging is enabled. When debugging is on non-`AssertionError`s
        will crash the app and be displayed on the console.
        """

    def setup(self) -> None:
        """
        This optional method is called once before the question is first
        displayed to the student. Put setup tasks that only run once in it.
        """

    def cleanup(self):
        """
        This optional method is called after the user has finished the question
        successfully or unsuccessfully. Any final cleanup tasks should run
        here.
        """

    def setup_attempt(self) -> None:
        """
        This optional method is called each time before the question is
        displayed to the student. If the question allows multiple attempts it
        will be called just before every attempt.
        """

    def cleanup_attempt(self):
        """
        This optional method is called each time after the question has been
        answered. Use it to cleanup after the attempt if necessary.
        """

    def shell(self, command):
        """
        A helper to run a command in the shell, returning the contents of stdout
        and raising an exception if the command exits with an error status.
        """
        return subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            encoding="utf-8",
        ).stdout


class MultipleChoiceQuestion(Question):
    """A multiple choice question for the KROZ player."""

    placeholder = "Enter the choice number."

    def __init__(
        self, text: str, *choices: str, help: str | None = None, **kwargs
    ):
        super().__init__(**kwargs)
        self._text = text
        self._solution = choices[0]
        self._choices = list(choices)
        self._help = help
        self.name = text

    @property
    def validators(self) -> list[textual.validation.Validator]:
        return [
            textual.validation.Integer(minimum=1, maximum=len(self._choices))
        ]

    @property
    def text(self):
        random.shuffle(self._choices)
        text = textwrap.dedent(f"""
        # Multiple Choice 

        {self._text}

        """)
        for i, c in enumerate(self._choices):
            text += f"{i + 1}. {c}\n"
        return text

    def check(self, answer):
        assert self._choices[int(answer) - 1] == self._solution, (
            self._help if self._help is not None else "That's not correct."
        )


class TrueOrFalseQuestion(Question):
    """A true or false question for the KROZ player."""

    placeholder = "Enter t or f"

    def __init__(
        self, text: str, solution: bool, help: str | None = None, **kwargs
    ):
        super().__init__(**kwargs)
        self._text = text
        self._solution = solution
        self._help = help
        self.name = text

    validators = [
        textual.validation.Regex(
            r"\s*[tf]\s*", re.I, failure_description="""Enter t or f"""
        )
    ]

    @property
    def text(self):
        text = f"""
        # True or False?

        {self._text}

        """
        return text

    def check(self, answer):
        assert self._solution == (answer.strip() in ["T", "t"]), (
            self._help if self._help is not None else "That's not correct."
        )


class ShortAnswerQuestion(Question):
    """A (vert) short answer question for the KROZ player."""

    def __init__(
        self, text: str, solution: str, help: str | None = None, **kwargs
    ):
        super().__init__(**kwargs)
        self._text = text
        self._solution = solution
        self._help = help
        self.name = text

    @property
    def text(self):
        text = f"""
        # Question

        {self._text}

        """
        return text

    def check(self, answer):
        assert self._solution == answer.strip(), (
            self._help if self._help is not None else "That's not correct."
        )
