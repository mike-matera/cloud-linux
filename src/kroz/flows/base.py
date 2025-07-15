"""
Base Class for a KROZ flow
"""

from abc import ABC, abstractmethod
from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum

from kroz.app import get_app


class KrozFlow(ABC):
    """
    Abstract base of KROZ flows. Provides grouping and checkpointing services.
    """

    class _GroupFailedException(BaseException):
        pass

    @dataclass
    class Result:
        """Result of a question."""

        class QuestionResult(Enum):
            CORRECT = 1
            INCORRECT = 2
            SKIPPED = 3

        message: str | None
        result: QuestionResult

    # The displayed text of the question. Interpreted as Markdown
    text: str | property = ""
    can_skip: bool = True
    points: int = 0
    checkpoint: bool = False
    debug: bool = False

    def __init__(self, **kwargs):
        self._name: str | None = None
        for key in kwargs:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            else:
                raise RuntimeError(f"Invalid keyword argument: {key}")

    @abstractmethod
    def run(self) -> Result: ...

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

    @contextmanager
    def group(self, checkpoint=None):
        """
        A context manager to group questions together. If any of the questions
        in the group are skipped or answered incorrectly, the group exits
        without asking any further questions. A question group is useful when
        a set of questions build on each other and when the desired behavior of
        the lab is to allow students to skip ahead, bypassing the entire group.
        """
        app = get_app()
        old_group = app.state.get("in_group", False, store=True)
        try:
            yield
        except KrozFlow._GroupFailedException:
            pass
        finally:
            self._group = old_group

    def show(self) -> Result:
        """Run the flow. Call's derived class's run()."""

        app = get_app()

        if self.debug or app._debug:
            self.debug = True
            self.can_skip = True

        checkpoint_result = KrozFlow.Result(
            message=None, result=KrozFlow.Result.QuestionResult.INCORRECT
        )
        if (
            self.checkpoint
            and self.name in app.state["checkpoints"]
            and app.state["checkpoints"][self.name]["result"]
            == "QuestionResult.CORRECT"
        ):
            app.score += self.points
            return KrozFlow.Result(
                message=app.state["checkpoints"][self.name]["message"],
                result=KrozFlow.Result.QuestionResult.CORRECT,
            )
        try:
            checkpoint_result = self.run()
        finally:
            if self.checkpoint:
                app.state["checkpoints"][self.name] = {
                    "message": checkpoint_result.message,
                    "result": str(checkpoint_result.result),
                }
                app.state.store()

        return checkpoint_result
