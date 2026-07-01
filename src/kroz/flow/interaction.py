"""
The protocol and implementation of an interaction in KROZ.
"""

import base64
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

    def __init__(self, *, cmd: str, cwd: str | Path, result: int):
        """Parse the incoming command."""

        self._cmd = self._parse_shell_command(cmd)
        self._cwd = Path(cwd)
        self._result = result

    @staticmethod
    def _parse_shell_command(cmd: str) -> list[str]:
        """
        Parse a shell command string into multiple commands, splitting on | and ;.
        Properly handles escaped semicolons and pipes (\\; and \\|).
        Respects quoted strings, where delimiters inside quotes are not treated as separators.

        Args:
            cmd: The command string to parse.

        Returns:
            A list of command strings, split on unescaped delimiters outside quotes.
        """
        commands = []
        current_cmd = []
        i = 0
        in_single_quote = False
        in_double_quote = False

        while i < len(cmd):
            char = cmd[i]

            # Handle quote state changes
            if char == "'" and not in_double_quote:
                in_single_quote = not in_single_quote
                current_cmd.append(char)
                i += 1
            elif char == '"' and not in_single_quote:
                in_double_quote = not in_double_quote
                current_cmd.append(char)
                i += 1
            elif (
                char == "\\"
                and i + 1 < len(cmd)
                and cmd[i + 1] in (";", "|", '"', "'")
            ):
                # Escaped relevant character add them both.
                current_cmd.append(cmd[i])
                current_cmd.append(cmd[i + 1])
                i += 2
            elif (
                char in (";", "|")
                and not in_single_quote
                and not in_double_quote
            ):
                # Unescaped delimiter outside quotes: split here
                cmd_str = "".join(current_cmd).strip()
                if cmd_str:
                    commands.append(cmd_str)
                current_cmd = []
                i += 1
            else:
                current_cmd.append(char)
                i += 1

        # Add the last command if any
        cmd_str = "".join(current_cmd).strip()
        if cmd_str:
            commands.append(cmd_str)

        return commands if commands else [""]

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
            cmd=self._cmd[key], cwd=self.cwd, result=self._result
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
        self.result = FlowResult.INCOMPLETE
        screen = InteractionScreen(self, can_skip=self.can_skip)
        if app.show(screen=screen) is not None:
            self.result = FlowResult.CORRECT
        else:
            self.result = FlowResult.INCORRECT
        return self.result


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

    def on_command(self, command: CommandLineCommand) -> bool | None:
        try:
            self.answer = str(command)
            self.log()
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
        self._command: str = ""

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
                    if len(self._command) > 0:
                        newcommand = CommandLineCommand(
                            cmd=self._command,
                            cwd=base64.b64decode(req["cwd"])
                            .decode("utf-8")
                            .strip(),
                            result=req["result"],
                        )
                        self.post_message(
                            InteractionScreen.CommandLineEvent(cmd=newcommand)
                        )
                elif "cmd" in req:
                    self._command = (
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
