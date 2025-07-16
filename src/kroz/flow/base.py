"""
Base Class for a KROZ flow
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from kroz import KrozApp


class KrozFlowABC(ABC):
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
    points: int | property = 0
    checkpoint: bool | property = False
    can_skip: bool | property = True

    debug: bool = False

    @abstractmethod
    def show(self) -> Result: ...

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


class FlowContext:
    """Context manager that groups flows."""

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.groups: list[dict] = KrozApp.running().state.get(
            "_in_group", [], store=True
        )
        assert isinstance(self.groups, list)

    def __enter__(self):
        self.groups.append(self.kwargs)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.groups.pop()

    @staticmethod
    def run(flow: KrozFlowABC) -> KrozFlowABC.Result:
        """Run the flow. Call's derived class's run()."""
        app = KrozApp.running()
        # Apply Groups
        groups: list[dict] = app.state.get("_in_group", None)
        if groups is not None:
            assert isinstance(groups, list)
            for group in reversed(groups):
                assert isinstance(group, dict)
                for key, value in group.items():
                    if key == "name":
                        seq_no = app.state.get("_sequence_no", 0, store=True)
                        flow.name = f"{value}{seq_no}"
                        app.state["_sequence_no"] = seq_no + 1
                    else:
                        try:
                            setattr(flow, key, value)
                        except AttributeError:
                            pass  # Classes can ignore overrides with properties

        # Search checkpoints.
        if "checkpoints" not in app.state:
            app.state["checkpoints"] = {}

        if flow.debug or app._debug:
            flow.debug = True
            if isinstance(flow.__class__.can_skip, property):
                # Defeat the property for debugging....
                flow.__class__.can_skip = True
            else:
                flow.can_skip = True

        checkpoint_result = KrozFlowABC.Result(
            message=None, result=KrozFlowABC.Result.QuestionResult.INCORRECT
        )
        if (
            flow.checkpoint
            and flow.name in app.state["checkpoints"]
            and app.state["checkpoints"][flow.name]["result"]
            == "QuestionResult.CORRECT"
        ):
            app.score += flow.points
            return KrozFlowABC.Result(
                message=app.state["checkpoints"][flow.name]["message"],
                result=KrozFlowABC.Result.QuestionResult.CORRECT,
            )
        try:
            checkpoint_result = flow.show()
            if (
                checkpoint_result.result
                == KrozFlowABC.Result.QuestionResult.CORRECT
            ):
                app.score += flow.points
            elif (
                flow.debug
                and checkpoint_result.result
                == KrozFlowABC.Result.QuestionResult.SKIPPED
            ):
                app.score += flow.points
        finally:
            if flow.checkpoint:
                app.state["checkpoints"][flow.name] = {
                    "message": checkpoint_result.message,
                    "result": str(checkpoint_result.result),
                }
                app.state.store()

        return checkpoint_result
