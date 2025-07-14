"""
The Kroz Application Player

This module is a UI for Linux labs.
"""

import os
import pathlib
import uuid
from collections.abc import Callable
from enum import Enum
from typing import Any, Literal

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
from textual.worker import Worker, get_current_worker

from kroz.screen import KrozScreen
from kroz.secrets import ConfirmationCode, JsonBoxFile
from kroz.widget.score_header import ScoreHeader

_setuphooks = []

_default_config = {
    "default_path": pathlib.Path(os.environ.get("HOME", os.getcwd())),
    "random_seed": None,
    "secret": None,
    "config_dir": None,
    "state_file": None,
}


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


class KrozApp(App[str]):
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

    BINDINGS = [
        ("ctrl+q", "app.cleanup_quit", "Quit"),
    ]

    score: Reactive[int] = Reactive(0)
    score_format: Reactive[str] = Reactive("Score: {score}")

    def __init__(
        self,
        title: str,
        default_path: str | None = None,
        random_seed: int | None = None,
        secret: str | None = None,
        config_dir: str | None = None,
        state_file: str | None = None,
        debug: bool = False,
        **user_config,
    ):
        super().__init__()
        self.title = title
        self._debug = debug
        self._main_func: Callable[[], None] = lambda: None
        self._main_worker: Worker | None = None
        self._config = {}
        self._user_config = user_config
        if default_path:
            self._user_config["default_path"] = default_path
        if random_seed:
            self._user_config["random_seed"] = random_seed
        if secret:
            self._user_config["secret"] = secret
        if config_dir:
            self._user_config["config_dir"] = config_dir
        if state_file:
            self._user_config["state_file"] = state_file
        self._showing = None
        self._progress_screen: ProgressScreen | None = None
        self._state = None

    def compose(self):
        yield ScoreHeader()
        yield Footer()

    def _run_user_app(self):
        global _setuphooks, _default_config
        try:
            self._config = _default_config
            self._config.update(self._user_config)

            # Debugging overrides.
            if self._debug:
                self._config["secret"] = None
                self._config["config_dir"] = pathlib.Path(os.getcwd())
                self._config["default_path"] = pathlib.Path(os.getcwd())

            if self._config["secret"] is None:
                self._config["secret"] = str(uuid.getnode())
            if self._config["config_dir"] is None:
                self._config["config_dir"] = pathlib.Path.home() / ".kroz"
            self._config["config_dir"] = pathlib.Path(
                self._config["config_dir"]
            )
            if not self._config["config_dir"].exists():
                self._config["config_dir"].mkdir(parents=True)
            else:
                if not self._config["config_dir"].is_dir():
                    raise RuntimeError(
                        f"The home configuration must be a directory: {self._config['home']}"
                    )
            if self._config["state_file"] is not None:
                self._state = JsonBoxFile(
                    self._config["secret"],
                    (
                        self._config["config_dir"] / self._config["state_file"]
                    ).with_suffix(".krs"),
                )
                if "checkpoints" not in self._state:
                    self._state["checkpoints"] = {}

            for hook in _setuphooks:
                hook()
            self._main_func()  # type: ignore
        except KrozApp.CancelledWorkerException:
            # Don't propagate
            pass

    def main(self, func: Callable[[], None]):
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
            self.exit(result=self.confirmation(), return_code=0)

    def on_score_message(self, msg: ScoreMessage):
        if msg._update:
            self.score += msg._update
        elif msg._to:
            self.score = msg._to

    def on_progress_progress_message(self, msg: progress.ProgressMessage):
        if msg.state == progress.ProgressMessage.State.START:
            self._progress_screen = ProgressScreen(msg.message)
            self.push_screen(self._progress_screen)
        elif (
            self._progress_screen
            and msg.state == progress.ProgressMessage.State.STOP
        ):
            self._progress_screen.dismiss()
            self._progress_screen = None
        elif (
            self._progress_screen
            and msg.state == progress.ProgressMessage.State.UPDATE
        ):
            if msg.percent:
                self._progress_screen._progress.total = 100
                self._progress_screen._progress.progress = msg.percent
            else:
                self._progress_screen._progress.total = None
            if msg.message:
                self._progress_screen._task_log.write(msg.message)

    async def action_cleanup_quit(self):
        self.workers.cancel_all()

    def post_message(self, message: Message) -> bool:
        # Kill canceled workers that send a progress message.
        if (
            isinstance(message, progress.ProgressMessage)
            and get_current_worker().is_cancelled
        ):
            raise KrozApp.CancelledWorkerException()

        return super().post_message(message)

    def show(
        self, screen: str | Screen, classes: str = "", title: str | None = None
    ) -> Any:
        """Show a screen."""

        worker = get_current_worker()
        if worker.is_cancelled:
            raise KrozApp.CancelledWorkerException()
        result = self.call_from_thread(self._show, screen, classes, title)
        if worker.is_cancelled:
            raise KrozApp.CancelledWorkerException()
        return result

    async def _show(
        self, screen: str | Screen, classes: str, title: str
    ) -> None:
        if isinstance(screen, str):
            self._showing = KrozScreen(screen, classes=classes, title=title)
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

    # FIXME: (someday)... is accessing app.state[] really valid? Since show()
    # blocks this thread and Kroz doesn't do anything when a screen is not
    # showing it's probably not going to cause any trouble. Should it be
    # synchronized with a thread safe API?

    @property
    def state(self):
        """A dictionary that's persisted in a state file."""
        if self._state is None:
            raise RuntimeError("No state file was given, can't save state.")
        return self._state

    def confirmation(self):
        """Get the base64 encoded confirmation code."""
        return ConfirmationCode(key=self.config["secret"]).confirmation(
            {"score": self.score}
        )


def get_app() -> KrozApp:
    app: KrozApp = get_current_worker().node  # type: ignore
    assert isinstance(app, KrozApp)
    return app


def get_appconfig(key: str) -> Any:
    return get_app().config[key]


def setup_hook(
    *, hook: Callable[[], None] | None = None, defconfig={}
) -> None:
    global _setuphooks, _default_config
    if hook is not None:
        _setuphooks.append(hook)
    _default_config.update(defconfig)


def notify(
    message,
    *,
    title: str = "",
    severity: Literal["information"]
    | Literal["warning"]
    | Literal["error"] = "information",
    timeout: float | None = None,
):
    get_app().notify(message, title=title, severity=severity, timeout=timeout)
