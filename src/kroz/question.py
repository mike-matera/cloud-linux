"""
Abstract Question Base
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Iterable
from textual.validation import Validator


class Question(ABC):
    """
    The base class of a question for the KROZ player.
    """

    class Result(Enum):
        CORRECT = 1
        INCORRECT = 2
        SKIPPED = 3

    text: str = None
    validators: Iterable[Validator] = []
    placeholder: str = "Answer"

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

        FIXME: Debugging!
        """

    def setup(self) -> None:
        """
        This optional method is called before the question is displayed to the
        user. Use it to setup the question if needed.
        """

    def cleanup(self):
        """
        This optional method is called after the question is answered correctly
        or it has been skipped. Use it to cleanup after the question if
        necessary.
        """
