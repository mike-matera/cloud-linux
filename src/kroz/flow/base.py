"""
Base Class for a KROZ flow
"""

import textwrap
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum

from kroz.app import KrozApp


class FlowResult(Enum):
    CORRECT = "CORRECT"
    INCORRECT = "INCORRECT"
    SKIPPED = "SKIPPED"
    INCOMPLETE = "INCOMPLETE"


class KrozFlowABC(ABC):
    """
    Abstract base of KROZ flows. Provides grouping and checkpointing services.
    """

    # The displayed text of the question. Interpreted as Markdown
    text: str | property = ""
    points: int | property = 0
    progress: bool | property = False
    can_skip: bool | property = True

    # Runtime data
    checkpoint: str | None = None
    answer: str | None = None
    result: FlowResult = FlowResult.INCOMPLETE

    debug: bool = False

    @abstractmethod
    def show(self) -> FlowResult: ...

    def __init__(self, **kwargs):
        for key in kwargs:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            else:
                raise RuntimeError(f"Invalid keyword argument: {key}")

    def __repr__(self):
        header = f"{self.__class__.__module__}:{self.__class__.__name__}"
        question = textwrap.dedent(self.text).strip()
        settings = "\n".join(
            f"{item}: {value}" for item, value in sorted(self.__dict__.items())
        )
        return f"""
{textwrap.indent(header, "+-- ", predicate=lambda x: True)}
{textwrap.indent(question, "| ", predicate=lambda x: True)}
+------
{textwrap.indent(settings, "| ", predicate=lambda x: True)}
+------
"""


@dataclass
class FlowStackFrame:
    flowname: str
    overrides: dict
    checkpoint_index: int = 0
    flows: list[KrozFlowABC] = field(default_factory=list)


class FlowStack:
    """The current FlowContext state."""

    def __init__(self):
        """The flow stack is always derived from the application state."""
        self.app = KrozApp.running()
        self.stack: list[FlowStackFrame] = self.app.state.get(
            "_flow",
            [FlowStackFrame(flowname="root", overrides={})],
            store=True,
        )
        self.checkpoints: dict[str, KrozFlowABC] = self.app.state.get(
            "checkpoints", {}, store=True
        )

    def checkpoint_key(self) -> str:
        top = self.stack[-1]
        return "-".join(
            [g.flowname for g in self.stack] + [str(top.checkpoint_index)]
        )

    def flow_key(self, flowname: str) -> str:
        return "-".join([g.flowname for g in self.stack] + [flowname])

    def push(self, ctx: FlowStackFrame) -> None:
        self.stack.append(ctx)

    def pop(self) -> FlowStackFrame:
        return self.stack.pop()

    def apply_overrides(self, flow: KrozFlowABC) -> None:
        """Apply flow overrides from the current stack."""

        over = {}
        for group in reversed(self.stack):
            over.update(group.overrides)

        # Apply flow overrides.
        for key, value in over.items():
            try:
                setattr(flow, key, value)
            except AttributeError:
                pass  # Classes can ignore overrides with properties

    def from_checkpoint(self, flow: KrozFlowABC) -> KrozFlowABC:
        """Return a flow that was restored from the current checkpoint."""
        if flow.progress:
            return self.checkpoints.get(self.checkpoint_key(), flow)
        else:
            return flow

    def record(self, flow: KrozFlowABC) -> None:
        top = self.stack[-1]
        flow.checkpoint = self.checkpoint_key()
        top.flows.append(flow)
        if flow.progress:
            self.checkpoints[flow.checkpoint] = flow
            self.stack[-1].checkpoint_index += 1
            self.app.state.store()


class FlowContext:
    """Context manager that groups flows."""

    def __init__(self, flowname: str, **kwargs):
        self.frame = FlowStackFrame(flowname=flowname, overrides=kwargs)
        self.stack = FlowStack()
        self.flowresults: dict[str, FlowResult] = KrozApp.running().state.get(
            "flowresults", {}, store=True
        )
        self.flowkey = self.stack.flow_key(flowname)

    def __enter__(self):
        self.stack.push(self.frame)
        self.flowresults[self.flowkey] = FlowResult.INCOMPLETE
        KrozApp.running().state.store()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        top = self.stack.pop()
        if exc_type is not None or any(
            (x.result == FlowResult.SKIPPED for x in top.flows)
        ):
            self.flowresults[self.flowkey] = FlowResult.SKIPPED
        elif all((x.result == FlowResult.CORRECT for x in top.flows)):
            self.flowresults[self.flowkey] = FlowResult.CORRECT
        else:
            self.flowresults[self.flowkey] = FlowResult.INCORRECT
        KrozApp.running().state.store()

    @staticmethod
    def is_complete(flowname: str):
        """Check if the flow has been previously completed"""
        stack = FlowStack()
        flowkey = stack.flow_key(flowname)
        flowresults: dict[str, FlowResult] = KrozApp.running().state.get(
            "flowresults", {}, store=True
        )
        return (
            flowresults.get(flowkey, FlowResult.INCOMPLETE)
            == FlowResult.CORRECT
        )

    @staticmethod
    def flow_status(flowname: str):
        stack = FlowStack()
        flowkey = stack.flow_key(flowname)
        flowresults: dict[str, FlowResult] = KrozApp.running().state.get(
            "flowresults", {}, store=True
        )
        return flowresults.get(flowkey, FlowResult.INCOMPLETE)

    @staticmethod
    def status_icon(flowname: str):
        status = FlowContext.flow_status(flowname)
        if status == FlowResult.INCOMPLETE:
            return "[ ]"  # Not started
        elif status == FlowResult.CORRECT:
            return "[X]"  # Complete
        elif status == FlowResult.SKIPPED:
            return "[~]"  # Not finished
        elif status == FlowResult.INCORRECT:
            return "[!]"  # Incorrect answers.

    @staticmethod
    def run(flow: KrozFlowABC) -> KrozFlowABC:
        """Run the flow. Call's derived class's run()."""
        stack = FlowStack()
        app = stack.app

        stack.apply_overrides(flow)

        if flow.debug or app._debug:
            flow.debug = True
            if not isinstance(flow.__class__.can_skip, property):
                flow.can_skip = True

        # Reset the flow if it's run already
        flow.result = FlowResult.INCOMPLETE

        saved_flow = stack.from_checkpoint(flow)
        if saved_flow.result != FlowResult.CORRECT:
            flow.result = flow.show()

        if saved_flow.result == FlowResult.CORRECT or (
            flow.debug and saved_flow.result == FlowResult.SKIPPED
        ):
            app.score += flow.points

        stack.record(flow)
        return flow
