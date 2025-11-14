"""
The protocol and implementation of an interaction in KROZ.
"""

import base64
import hashlib
import json
import textwrap
from abc import abstractmethod
from pathlib import Path
from typing import Callable, Literal

from quart import Quart, request
from textual.message import Message
from textual.widgets import Markdown

from kroz.app import KrozApp
from kroz.flow import KrozFlowABC
from kroz.flow.base import FlowResult
from kroz.screen import KrozScreen


class CommandLineCommand:
    """
    Helpers for UNIX commands
    """

    def __init__(self, *, cmd: list[str], cwd: str | Path, result: int):
        self._cmd = cmd
        self._cwd = Path(cwd)
        self._result = result

    @property
    def line(self) -> str:
        if len(self._cmd) == 1:
            return self._cmd[0]
        else:
            raise ValueError(".line access on a composite command.")

    @property
    def command(self) -> str:
        if len(self._cmd) == 1:
            return self._cmd[0].split()[0]
        else:
            raise ValueError(".command access on a composite command.")

    @property
    def args(self) -> list[str]:
        if len(self._cmd) == 1:
            return self._cmd[0].split()[1:]
        else:
            raise ValueError(".args access on a composite command.")

    @property
    def cwd(self) -> Path:
        return self._cwd

    @property
    def result(self) -> int:
        return self._result

    def __getitem__(self, key):
        return CommandLineCommand(
            cmd=[self._cmd[key]], cwd=self.cwd, result=self._result
        )

    def __len__(self) -> int:
        return len(self._cmd)

    def __str__(self) -> str:
        # BUG: I don't know how the commands were joined. Assuming pipe...
        return " | ".join(self._cmd)


class InteractionABC(KrozFlowABC):
    """
    Base class for a KROZ interaction.
    """

    # Default for flows.
    can_skip = False

    @abstractmethod
    def on_command(self, command: CommandLineCommand) -> bool | None:
        """
        **Required.** Check the command entered by the user. This method should
        return `True` if the answer is correct and raise an exception or return
        `False` if the answer is incorrect. Returning `None` will cause no
        visual change and the interaction will continue. `AssertionError`s will
        have their messages interpreted as Markdown and be displayed as feedback
        to the student. Other exceptions will be displayed as feedback with no
        stack trace, unless debugging is enabled. When debugging is on
        non-`AssertionError`s will crash the app and be displayed on the
        console.

        This runs in the application's event loop.
        """

    def show(self) -> FlowResult:
        app = KrozApp.running()
        screen = InteractionScreen(self, can_skip=self.can_skip)
        self.answer = app.show(screen=screen)
        if self.answer is not None:
            return FlowResult.CORRECT
        else:
            return FlowResult.SKIPPED


class Interaction(InteractionABC):
    """An interaction with multiple stages."""

    def __init__(
        self,
        text: str,
        filter: Callable[[CommandLineCommand], bool]
        | list[Callable[[CommandLineCommand], bool]],
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.text = text
        if isinstance(filter, list):
            self.filter = filter
        else:
            self.filter = [filter]
        self.stage = 0
        self.name = hashlib.sha1(text.encode("utf-8")).hexdigest()

    def on_command(self, command: CommandLineCommand) -> bool | None:
        try:
            if self.filter[self.stage](command):
                self.stage += 1
            else:
                self.stage = 0
                return False

            if self.stage == len(self.filter):
                return True
            else:
                return None
        except Exception as e:
            self.stage = 0
            raise e


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
        **kwargs,
    ):
        super().__init__(inter.text, title="O Listening...", **kwargs)
        self._inter = inter
        self._server = Quart(__name__)
        self._server.add_url_rule(
            "/", view_func=self._receive_command, methods=["POST"]
        )
        self._commands: list[str] = []

    def on_mount(self):
        self.run_worker(self._run_server(), exclusive=True, exit_on_error=True)

    async def on_interaction_screen_command_line_event(
        self, event: "InteractionScreen.CommandLineEvent"
    ):
        def render_title(status: Literal["ok", "err"]) -> str:
            parts = []
            if status == "ok":
                parts.append("O")
            else:
                parts.append("X")

            if event.cmd.result != 0:
                parts.append(f"⤷{event.cmd.result}")

            parts.append(str(event.cmd))
            return " ".join(parts)

        md = self.query_one(Markdown)
        try:
            result = self._inter.on_command(event.cmd)
            if result is not None:
                if result:
                    KrozApp.running().notify("Congratulations!", timeout=5)
                    self.dismiss(str(event.cmd))
                else:
                    md.border_title = render_title("err")
                    self.classes = "feedback"
            else:
                md.border_title = render_title("ok")
                self.classes = ""
        except AssertionError as e:
            md.border_title = render_title("err")
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
            md.border_title = render_title("err")
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
                if "result" in req and "cwd" in req:
                    if len(self._commands) > 0:
                        newcommand = CommandLineCommand(
                            cmd=self._commands,
                            cwd=base64.b64decode(req["cwd"])
                            .decode("utf-8")
                            .strip(),
                            result=req["result"],
                        )
                        self.post_message(
                            InteractionScreen.CommandLineEvent(cmd=newcommand)
                        )
                        self._commands = []
                elif "cmd" in req:
                    self._commands.append(
                        base64.b64decode(req["cmd"]).decode("utf-8").strip()
                    )
        except Exception as e:
            self.log(f"ERROR: {e}")
        finally:
            return "okay"

    def check_action(self, action: str, parameters: tuple[object, ...]):
        if action == "dismiss":
            return False
        else:
            return super().check_action(action, parameters)
