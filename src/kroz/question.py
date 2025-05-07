"""
Abstract Question Base
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Iterable
from textual.validation import Validator

from kroz import get_app

from textual import on
from textual.widgets import (
    Label,
    Input,
)
from textual.containers import HorizontalGroup, VerticalGroup

from kroz.screen import KrozScreen


class QuestionScreen(KrozScreen):
    CSS_PATH = "app.tcss"

    def __init__(
        self,
        text: str,
        placeholder: str,
        validators: Iterable[Validator],
        **kwargs,
    ):
        super().__init__(text, **kwargs)
        self._placeholder = placeholder
        self._validators = validators
        self._result = None

    def compose(self):
        yield from super().compose()
        with VerticalGroup(classes="answer"):
            with HorizontalGroup():
                yield Label("$", id="prompt")
                yield Input(
                    placeholder=self._placeholder,
                    validate_on=["submitted"],
                    validators=self._validators,
                )

    def on_mount(self):
        super().on_mount()
        self.query_one("Input").focus()

    @on(Input.Submitted)
    async def submit(self, event: Input.Changed) -> None:
        query = self.query("#validation")
        if query:
            feedback = query.first()
        else:
            feedback = Label("", id="validation")
            await self.query_one(".answer").mount(feedback, before=0)

        if not event.validation_result or event.validation_result.is_valid:
            self.dismiss(event.value)
        else:
            self.query_one("#validation").update(
                "\n".join(
                    (
                        f"❌ {x}"
                        for x in event.validation_result.failure_descriptions
                    )
                )
            )


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
                try:
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

                    self.check(answer)
                    app.update_score(self.points)
                    app.show(
                        KrozScreen(
                            "# Congratulations",
                            title="Success",
                            classes="congrats",
                        )
                    )
                    return Question.Result.CORRECT

                except Exception as e:
                    if isinstance(e, AssertionError):
                        border_title = "Incorrect Answer"
                    else:
                        border_title = f"Error: {e.__class__.__name__}"

                    app.show(
                        KrozScreen(
                            str(e),
                            title=border_title,
                            classes="feedback",
                        )
                    )
                    tries_left -= 1

            return Question.Result.INCORRECT

        finally:
            self.cleanup()
