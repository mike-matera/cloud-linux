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
        for key in kwargs:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            else:
                raise RuntimeError(f"Invalid keyword argument: {key}")


class FlowContext:
    """Context manager that groups flows."""

    def __init__(self, flowname: str = "unnamed", **kwargs):
        self.kwargs = kwargs
        self.flowname = flowname
        self.serial = 0

    def __enter__(self):
        app = KrozApp.running()
        groups: list[dict] = app.state.get("_in_group", [], store=True)
        self.serial = app.state.get("_sequence", 0, store=True)
        app.state["_sequence"] = 0
        assert isinstance(groups, list)
        groups.append(self.__dict__)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        app = KrozApp.running()
        groups: list[dict] = app.state["_in_group"]
        groups.pop()
        app.state["_sequence"] = self.serial

    @staticmethod
    def run(flow: KrozFlowABC) -> KrozFlowABC.Result:
        """Run the flow. Call's derived class's run()."""
        app = KrozApp.running()

        # Apply flow overrides.
        groups: list[dict] = KrozApp.running().state.get("_in_group", [])
        overrides = {}
        for group in reversed(groups):
            assert isinstance(group, dict)
            overrides.update(group["kwargs"])

        for key, value in overrides.items():
            try:
                setattr(flow, key, value)
            except AttributeError:
                pass  # Classes can ignore overrides with properties

        # Search checkpoints.
        seq_no = app.state.get("_sequence", 0, store=True)
        if len(groups) != 0:
            check_key = "-".join(
                [g["flowname"] for g in groups] + [str(seq_no)]
            )
        else:
            check_key = f"nogroup-{seq_no}"

        app.state["_sequence"] = seq_no + 1
        checkpoints = app.state.get("checkpoints", {}, store=True)

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
            and check_key in checkpoints
            and checkpoints[check_key]["result"] == "QuestionResult.CORRECT"
        ):
            app.score += flow.points
            return KrozFlowABC.Result(
                message=checkpoints[check_key]["message"],
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
                checkpoints[check_key] = {
                    "message": checkpoint_result.message,
                    "result": str(checkpoint_result.result),
                }
                app.state.store()

        return checkpoint_result
