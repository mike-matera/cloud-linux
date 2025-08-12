"""
The protocol and implementation of an interaction in KROZ.
"""

import base64
import hashlib
import json
import textwrap
from abc import abstractmethod
from pathlib import Path
from typing import Callable

from quart import Quart, request
from textual.message import Message
from textual.widgets import Markdown

from kroz import KrozApp
from kroz.flow import KrozFlowABC
from kroz.flow.base import FlowResult
from kroz.screen import KrozScreen


class CommandLineCommand(str):
    """
    Helpers for UNIX commands
    """

    def __new__(cls, *, cmd: str, cwd: str | Path, result: int):
        return super().__new__(cls, cmd)

    def __init__(self, *, cmd: str, cwd: str | Path, result: int):
        self._cwd = Path(cwd)
        self._result = result

    @property
    def command(self) -> str:
        return self.split()[0]

    @property
    def args(self) -> list[str]:
        return self.split()[1:]

    @property
    def cwd(self) -> Path:
        return self._cwd

    @property
    def result(self) -> int:
        return self._result


class InteractionABC(KrozFlowABC):
    """
    Base class for a KROZ interaction.
    """

    @abstractmethod
    def on_command(self, command: CommandLineCommand) -> bool:
        """
        **Required.** Check the command entered by the user. This method should
        return `True` if the answer is correct and raise an exception or return
        `False` if the answer is incorrect. `AssertionError`s will have their
        messages interpreted as Markdown and be displayed as feedback to the
        student. Other exceptions will be displayed as feedback with no stack
        trace, unless debugging is enabled. When debugging is on
        non-`AssertionError`s will crash the app and be displayed on the
        console.

        This runs in the application's event loop.
        """

    def show(self) -> FlowResult:
        app = KrozApp.running()
        screen = InteractionScreen(self)
        self.answer = app.show(screen=screen)
        if self.answer is not None:
            return FlowResult.CORRECT
        else:
            return FlowResult.SKIPPED


class Interaction(InteractionABC):
    """A simple interaction."""

    def __init__(
        self, text: str, filter: Callable[[CommandLineCommand], bool], **kwargs
    ):
        super().__init__(**kwargs)
        self.text = text
        self.filter = filter
        self.name = hashlib.sha1(text.encode("utf-8")).hexdigest()

    def on_command(self, command: CommandLineCommand) -> bool:
        return self.filter(command)


class InteractionScreen(KrozScreen):
    """
    An interaction monitors a user's other shells and responds to the commands
    they enter.
    """

    class CommandLineEvent(Message):
        """A message to indicate the progress of a slow running task."""

        def __init__(self, cmd: CommandLineCommand):
            super().__init__()
            self.cmd = cmd

    def __init__(
        self,
        inter: InteractionABC,
        *,
        title: str | None = None,
        can_skip: bool = False,
        **kwargs,
    ):
        super().__init__(
            inter.text, title="🔴 Listening...", can_skip=can_skip, **kwargs
        )
        self._inter = inter
        self._server = Quart(__name__)
        self._server.add_url_rule(
            "/", view_func=self._receive_command, methods=["POST"]
        )

    def on_mount(self):
        self.run_worker(self._run_server(), exclusive=True, exit_on_error=True)

    async def on_interaction_screen_command_line_event(
        self, event: "InteractionScreen.CommandLineEvent"
    ):
        md = self.query_one(Markdown)
        try:
            if self._inter.on_command(event.cmd):
                KrozApp.running().notify("Congratulations!", timeout=5)
                self.dismiss(str(event.cmd))
            else:
                md.border_title = f"❌ {event.cmd}"
                self.classes = "feedback"
        except AssertionError as e:
            md.border_title = f"❌ {event.cmd}"
            self.classes = "feedback"
            md.update(
                textwrap.dedent(
                    f"""
            {self._inter.text}

            {str(e)}
            """
                )
            )
        except Exception:
            md.border_title = f"❌ {event.cmd}"
            self.classes = "feedback"

    async def _run_server(self):
        sockpath = Path.home().absolute() / ".kroz"
        if not sockpath.exists():
            sockpath.mkdir()
        await self._server.run_task(
            host=f"unix://{Path.home().absolute()}/.kroz/command.sock"
        )

    async def _receive_command(self):
        try:
            if request.is_json:
                req = json.loads(await request.data)
                self.post_message(
                    InteractionScreen.CommandLineEvent(
                        CommandLineCommand(
                            cmd=base64.b64decode(req["cmd"])
                            .decode("utf-8")
                            .strip(),
                            cwd=Path(
                                base64.b64decode(req["cwd"])
                                .decode("utf-8")
                                .strip()
                            ),
                            result=req["result"],
                        )
                    )
                )
        except Exception as e:
            self.log(f"ERROR: {e}")
        finally:
            return "okay"
