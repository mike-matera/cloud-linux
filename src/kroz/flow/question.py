"""
The protocol and implementation of a question in KROZ.
"""

import random
import re
import subprocess
import textwrap
from abc import abstractmethod
from typing import Iterable, Sequence

import textual
import textual.validation
from textual import on
from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup
from textual.validation import Integer, Validator
from textual.widgets import (
    Input,
    Label,
)

from kroz.app import KrozApp
from kroz.flow.base import FlowResult, KrozFlowABC
from kroz.screen import KrozScreen


class Question(KrozFlowABC):
    """
    The base class of a question for KROZ.
    """

    # Textual Validators that will be used by the input. Help students get the
    # right type of answer (e.g. int)
    validators: Validator | Iterable[Validator] | property = []

    # Placeholder that will show in the empty Input. Help students figure out
    # what the answer should look like.
    placeholder: str | property = "Answer"

    # Number of tries
    tries: int | property = 0

    # Correct response feedback
    congrats: str | property | None = "# Congratulations"

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

    @staticmethod
    def shell(command):
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

    def show(self) -> FlowResult:
        """Ask the question."""

        app = KrozApp.running()
        try:
            self.setup()
            tries_left = self.tries
            while self.tries == 0 or tries_left > 0:
                self.setup_attempt()

                if tries_left >= 2:
                    app.notify(
                        f"You have {tries_left} tries left.",
                        title="Notice",
                        severity="warning",
                    )
                elif tries_left == 1:
                    app.notify(
                        "You have one try left!",
                        title="Last Try",
                        severity="error",
                    )
                self.answer = app.show(
                    QuestionScreen(
                        text=self.text,
                        placeholder=self.placeholder,
                        validators=self.validators,
                        can_skip=self.can_skip,
                    )
                )

                if self.answer is None:
                    return FlowResult.SKIPPED

                try:
                    check_result = self.check(self.answer)
                except AssertionError as e:
                    check_result = e
                except Exception as e:
                    check_result = e
                    if self.debug:
                        raise e

                try:
                    if isinstance(check_result, Exception):
                        if isinstance(check_result, AssertionError):
                            border_title = "Incorrect Answer"
                        else:
                            border_title = (
                                f"Error: {check_result.__class__.__name__}"
                            )
                        app.show(
                            KrozScreen(
                                str(check_result),
                                title=border_title,
                                classes="feedback",
                            )
                        )
                        tries_left -= 1
                    else:
                        app.update_score(self.points)
                        if self.congrats is not None:
                            app.show(
                                KrozScreen(
                                    self.congrats,
                                    title="Success",
                                    classes="congrats",
                                )
                            )
                        return FlowResult.CORRECT
                finally:
                    # Save this attempt
                    app.state.store()
                    self.cleanup_attempt()
        finally:
            self.cleanup()

        return FlowResult.INCORRECT


class MultipleChoiceQuestion(Question):
    """A multiple choice question for KROZ"""

    placeholder = "Enter the choice number."

    def __init__(
        self, text: str, *choices: str, help: str | None = None, **kwargs
    ):
        super().__init__(**kwargs)
        self._text = text
        self._solution = choices[0]
        self._choices = list(choices)
        self._help = help

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
    """A true or false question for KROZ."""

    placeholder = "Enter t or f"

    def __init__(
        self, text: str, solution: bool, help: str | None = None, **kwargs
    ):
        super().__init__(**kwargs)
        self._text = text
        self._solution = solution
        self._help = help

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
    """A (vert) short answer question for KROZ."""

    def __init__(
        self,
        text: str,
        solution: str | re.Pattern,
        help: str | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._text = text
        self._solution = solution
        self._help = help

    @property
    def text(self):
        text = f"""
        # Question

        {self._text}

        """
        return text

    def check(self, answer):
        if isinstance(self._solution, str):
            assert self._solution == answer.strip(), (
                self._help if self._help is not None else "That's not correct."
            )
        else:
            assert re.match(self._solution, answer.strip()) is not None, (
                self._help if self._help is not None else "That's not correct."
            )


class QuestionScreen(KrozScreen):
    """The visual component of a KROZ question."""

    def __init__(
        self,
        text: str,
        placeholder: str,
        validators: Validator | Iterable[Validator],
        **kwargs,
    ):
        super().__init__(text, **kwargs)
        self._placeholder = placeholder
        self._validators = validators

    def compose(self) -> ComposeResult:
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
        input: Input = self.query_one("Input")  # type: ignore
        query = self.query("#validation")
        if query:
            feedback = query.first()
        else:
            feedback = Label("", id="validation")
            await self.query_one(".answer").mount(feedback, before=0)

        if not event.validation_result or event.validation_result.is_valid:
            self.dismiss(event.value)
        else:
            self.query_one("#validation").update(  # type: ignore
                "\n".join(
                    (
                        f"❌ {x}"
                        for x in event.validation_result.failure_descriptions
                    )
                )
            )
        input.clear()


class Menu(Question):
    """A menu of options to choose from."""

    congrats = None
    placeholder = "Enter your choice..."
    can_skip = False

    def __init__(self, message: str, items: Sequence[str]):
        self._text = message
        self._items = items

    @property
    def text(self) -> str:
        text = textwrap.dedent(self._text) + "\n"
        for i, item in enumerate(self._items, start=1):
            text += f"  {i}. {item.strip()}\n"
        text += f"  {len(self._items) + 1}. Quit"
        return text

    @property
    def validators(self):
        return Integer(minimum=1, maximum=len(self._items) + 1)

    def check(self, answer):
        return
