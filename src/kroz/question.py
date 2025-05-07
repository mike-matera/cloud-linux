"""
Abstract Question Base
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Iterable
from textual.validation import Validator

from kroz import get_app


from kroz.screen import KrozScreen, QuestionScreen


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
    tries: int = 0
    can_skip: bool = True
    points: int = 0

    def __init__(self, **kwargs):
        for key in kwargs:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            else:
                raise RuntimeError(f"Invalid keyword argument: {key}")

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

    def ask(self) -> Result:
        """Ask the question."""
        app = get_app()
        self.setup()
        tries_left = self.tries
        try:
            while self.tries == 0 or tries_left > 0:
                answer = app.show(
                    QuestionScreen(
                        text=self.text,
                        placeholder=self.placeholder,
                        validators=self.validators,
                        can_skip=self.can_skip,
                    )
                )
                if answer is None:
                    return Question.Result.SKIPPED

                try:
                    result = self.check(answer)
                except Exception as e:
                    result = e

                if isinstance(result, Exception):
                    if isinstance(result, AssertionError):
                        border_title = "Incorrect Answer"
                    else:
                        border_title = f"Error: {result.__class__.__name__}"
                    app.show(
                        KrozScreen(
                            str(result),
                            title=border_title,
                            classes="feedback",
                        )
                    )
                    tries_left -= 1
                else:
                    app.update_score(self.points)
                    app.show(
                        KrozScreen(
                            "# Congratulations" if not result else result,
                            title="Success",
                            classes="congrats",
                        )
                    )
                    return Question.Result.CORRECT

            return Question.Result.INCORRECT

        finally:
            self.cleanup()
