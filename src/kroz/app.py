"""
The Kroz Application Player

This module is a UI for Linux labs.
"""

import os
import pathlib
import subprocess
from enum import Enum
from typing import Any, Callable

from textual.app import App
from textual.containers import Vertical
from textual.message import Message
from textual.reactive import Reactive
from textual.screen import ModalScreen, Screen
from textual.widgets import (
    Footer,
    Label,
    ProgressBar,
    RichLog,
)
from textual.worker import Worker, WorkType, get_current_worker

from kroz.screen import KrozScreen
from kroz.widget.score_header import ScoreHeader


_setuphooks = []

_default_config = {
    "default_path": pathlib.Path(os.environ.get("HOME", os.getcwd()))
}


def get_app() -> dict:
    return get_current_worker().node


def get_appconfig(key: str) -> dict:
    return get_current_worker().node.config[key]


def setup_hook(*, hook: Callable[[], None] = None, defconfig={}) -> None:
    global _setuphooks, _default_config
    if hook is not None:
        _setuphooks.append(hook)
    _default_config.update(defconfig)


def notify(message, *, title=None, severity="information", timeout=None):
    get_current_worker().node.notify(
        message, title=title, severity=severity, timeout=timeout
    )


class progress:
    """
    Context manager API for long running tasks that wish to show visual
    progress to the user.
    """

    class ProgressMessage(Message):
        """A message to indicate the progress of a slow running task."""

        class State(Enum):
            START = 1
            UPDATE = 2
            STOP = 3

        def __init__(self, state, *, percent=None, message=None):
            super().__init__()
            self.state = state
            self.percent = percent
            self.message = message

    def __init__(self, title=None):
        super().__init__()
        self._title = title

    def __enter__(self):
        self._worker = get_current_worker()
        self._app = self._worker.node
        self._app.post_message(
            progress.ProgressMessage(
                state=progress.ProgressMessage.State.START,
                message=self._title,
            )
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._app.post_message(
            progress.ProgressMessage(progress.ProgressMessage.State.STOP)
        )

    def update(self, percent=None, message=None):
        self._app.post_message(
            progress.ProgressMessage(
                state=progress.ProgressMessage.State.UPDATE,
                percent=percent,
                message=message,
            )
        )


class ProgressScreen(ModalScreen):
    """A progress screen with log messages."""

    DEFAULT_CSS = """
        ProgressScreen {
            align: center middle;
        }

        #loading {
            width: 70;
            height: auto;
            text-style: bold;
            background: $foreground-darken-1 5%;
        }

        #loading_title {
            content-align: center middle;
            background: $foreground-darken-1 15%;
            color: $foreground;
            width: 100%;
        }

        #progress #bar {
            width: 70;
            background: $foreground-darken-1 15%;
            padding-left: 2;
            padding-right: 2;
        }

        #messages {
            width: 100%;
            height: auto;
            max-height: 20;
            padding-left: 2;
            padding-right: 0;
            padding-top: 1;
            padding-bottom: 1;
            overflow-y: auto;
        }
        """

    BINDINGS = [
        ("ctrl+q", "app.cleanup_quit", "Quit"),
    ]

    def __init__(self, title=None):
        super().__init__()
        if title is None:
            self._title = "🤖 Please Wait..."
        else:
            self._title = title
        self._task_log = RichLog(id="messages", wrap=True)
        self._progress = ProgressBar(
            show_percentage=False, show_eta=False, id="progress"
        )

    def compose(self):
        with Vertical(id="loading"):
            yield Label(self._title, id="loading_title")
            yield self._progress
            yield self._task_log


class ScoreMessage(Message):
    """A message that updates the score."""

    def __init__(self, update=None, to=None):
        super().__init__()
        self._update = update
        self._to = to


class KrozApp(App):
    """
    A Kroz UI application. The application enables the construction of gamified
    Linux labs. Client code provides a `main()` function that is called by the
    app and can optionally specify a `setup()` and `cleanup()` function.

    Application functions are run in their own Textual threaded workers so they
    will not block the UI. However, they are limited to the API provided by the
    Kroz package for thread safety.
    """

    class CancelledWorkerException(BaseException):
        pass

    class GroupFailedException(BaseException):
        pass

    BINDINGS = [
        ("ctrl+s", "shell_escape", "Shell"),
        ("ctrl+q", "app.cleanup_quit", "Quit"),
    ]

    score: Reactive[int] = Reactive(0)
    score_format: Reactive[str] = Reactive("Score: {score}")

    def __init__(self, title: str, *, user_config={}):
        super().__init__()
        self.title = title
        self._main_func = lambda: ...
        self._main_worker = None
        self._config = {}
        self._user_config = user_config
        self._showing = None
        self._progress_screen = None

    def compose(self):
        yield ScoreHeader()
        yield Footer()

    def _run_user_app(self):
        global _setuphooks, _default_config
        try:
            self._config = _default_config
            self._config.update(self._user_config)
            for hook in _setuphooks:
                hook()
            self._main_func()
        except KrozApp.CancelledWorkerException:
            # Don't propagate
            pass

    def main(self, func: WorkType):
        """Decorator for the main() function."""
        self._main_func = func
        return func

    async def on_mount(self):
        self._main_worker = self.run_worker(
            self._run_user_app, "main", thread=True
        )

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """Called when the worker state changes."""
        if event.worker.name == "main" and event.worker.is_finished:
            self.exit(0, message="Put the confirmation code here.")

    def on_score_message(self, msg: ScoreMessage):
        if msg._update:
            self.score += msg._update
        elif msg._to:
            self.score = msg._to

    def on_progress_progress_message(self, msg: progress.ProgressMessage):
        if msg.state == progress.ProgressMessage.State.START:
            self._progress_screen = ProgressScreen(msg.message)
            self.push_screen(self._progress_screen)
        elif msg.state == progress.ProgressMessage.State.STOP:
            self._progress_screen.dismiss()
            self._progress_screen = None
        elif msg.state == progress.ProgressMessage.State.UPDATE:
            if msg.percent:
                self._progress_screen._progress.total = 100
                self._progress_screen._progress.progress = msg.percent
            else:
                self._progress_screen._progress.total = None
            if msg.message:
                self._progress_screen._task_log.write(msg.message)

    def action_shell_escape(self):
        with self.suspend():
            subprocess.run("$SHELL", shell=True)

    async def action_cleanup_quit(self):
        self.workers.cancel_all()

    def post_message(self, message: Message):
        # Kill canceled workers that send a progress message.
        if (
            isinstance(message, progress.ProgressMessage)
            and get_current_worker().is_cancelled
        ):
            raise KrozApp.CancelledWorkerException()

        super().post_message(message)

    def show(self, screen: str | Screen) -> Any:
        """Show a screen."""

        worker = get_current_worker()
        if worker.is_cancelled:
            raise KrozApp.CancelledWorkerException()
        result = self.call_from_thread(self._show, screen)
        if worker.is_cancelled:
            raise KrozApp.CancelledWorkerException()
        return result

    async def _show(self, screen: str | Screen) -> None:
        if isinstance(screen, str):
            self._showing = KrozScreen(
                screen, title="Welcome", classes="welcome"
            )
        elif isinstance(screen, Screen):
            self._showing = screen
        else:
            raise ValueError("This must be a screen.")

        try:
            return await self.push_screen_wait(self._showing)
        finally:
            self._showing = None

    def set_score(self, points: int):
        self.post_message(ScoreMessage(to=points))

    def update_score(self, points: int):
        self.post_message(ScoreMessage(update=points))

    @property
    def config(self):
        """A dictionary of configuration parameters."""
        return self._config
