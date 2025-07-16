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

    def show(self) -> Result:
        """Run the flow. Call's derived class's run()."""

        app = get_app()

        # Apply Groups
        groups: list[dict] = app.state.get("_in_group", None)
        if groups is not None:
            assert isinstance(groups, list)
            for group in reversed(groups):
                assert isinstance(group, dict)
                for key, value in group.items():
                    if key == "name":
                        seq_no = app.state.get("_sequence_no", 0, store=True)
                        self.name = f"{value}{seq_no}"
                        app.state["_sequence_no"] = seq_no + 1
                    else:
                        setattr(self, key, value)

        # Search checkpoints.
        if "checkpoints" not in app.state:
            app.state["checkpoints"] = {}

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
            print(f"DICK: {checkpoint_result.result}")
            if (
                checkpoint_result.result
                == KrozFlow.Result.QuestionResult.CORRECT
            ):
                print("MOTHERFUCKER")
                app.score += self.points
            elif (
                self.debug
                and checkpoint_result.result
                == KrozFlow.Result.QuestionResult.SKIPPED
            ):
                print("COCKSUCKER")
                app.score += self.points
        finally:
            if self.checkpoint:
                app.state["checkpoints"][self.name] = {
                    "message": checkpoint_result.message,
                    "result": str(checkpoint_result.result),
                }
                app.state.store()

        return checkpoint_result


@contextmanager
def settings(
    **kwargs,
):
    """
    A context manager to override common settings in subsequent invocations of a
    flow.
    """
    app = get_app()
    groups: list[dict] = app.state.get("_in_group", [], store=True)
    assert isinstance(groups, list)
    groups.append(kwargs)
    try:
        yield
    finally:
        groups.pop()
