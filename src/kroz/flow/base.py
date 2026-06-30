"""
Base Class for a KROZ flow
"""

import datetime
import textwrap
from abc import ABC, abstractmethod
from collections import namedtuple
from dataclasses import dataclass
from enum import Enum

from kroz.app import KrozApp

FlowResultValue = namedtuple("FlowResultValue", ["long", "short"])


class FlowResult(Enum):
    CORRECT = FlowResultValue(long="Correct", short="X")
    INCORRECT = FlowResultValue(long="Incorrect", short="!")
    SKIPPED = FlowResultValue(long="Skipped", short="~")
    INCOMPLETE = FlowResultValue(long="Incomplete", short=" ")

    def __str__(self):
        return self.value.long


@dataclass
class AttemptLogEntry:
    classname: str
    flow: str
    answer: str | None
    timestamp: datetime.datetime = datetime.datetime.now(datetime.UTC)


class KrozFlowABC(ABC):
    """
    Abstract base of KROZ flows.
    """

    # The displayed text of the question. Interpreted as Markdown
    text: str | property = ""
    can_skip: bool | property = True

    # Runtime data
    answer: str | None = None
    points: float | None = None
    result: FlowResult = FlowResult.INCOMPLETE

    debug: bool = False

    @abstractmethod
    def show(self) -> FlowResult: ...

    def log(self):
        app = KrozApp.running()
        if app.has_state:
            log = app.state.get("log", default=[], store=True)
            entry = AttemptLogEntry(
                classname=str(self.__class__),
                flow=repr(self),
                answer=self.answer,
            )
            log.append(entry)
            app.state.store()

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
            f"{item}: {value}"
            for item, value in sorted(self.__dict__.items())
            if item != "text" and not item.startswith("_")
        )
        return f"""
{textwrap.indent(header, "+-- ", predicate=lambda x: True)}
{textwrap.indent(question, "| ", predicate=lambda x: True)}
+------
{textwrap.indent(settings, "| ", predicate=lambda x: True)}
+------
"""

    def __getstate__(self) -> object:
        return {"text": self.text}
