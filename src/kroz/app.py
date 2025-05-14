"""
The Kroz Application Player

This module is a UI for Linux labs.
"""

from contextlib import contextmanager
import os
import pathlib
import subprocess
from enum import Enum
from typing import Any, Callable
import uuid

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

from kroz.screen import KrozScreen, QuestionScreen
from kroz.secrets import ConfirmationCode, JsonBoxFile
from kroz.widget.score_header import ScoreHeader
from kroz.question import Question


_setuphooks = []

_default_config = {
    "default_path": pathlib.Path(os.environ.get("HOME", os.getcwd())),
    "random_seed": None,
    "secret": None,
    "home": None,
    "state_file": None,
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

    def __init__(
        self,
        title: str,
        default_path: str = None,
        random_seed: int = None,
        secret: str = None,
        home: str = None,
        state_file: str = None,
        **user_config,
    ):
        super().__init__()
        self.title = title
        self._main_func = lambda: ...
        self._main_worker = None
        self._config = {}
        self._user_config = user_config
        if default_path:
            self._user_config["default_path"] = default_path
        if random_seed:
            self._user_config["random_seed"] = random_seed
        if secret:
            self._user_config["secret"] = secret
        if home:
            self._user_config["home"] = home
        if state_file:
            self._user_config["state_file"] = state_file
        self._showing = None
        self._progress_screen = None
        self._state = None

    def compose(self):
        yield ScoreHeader()
        yield Footer()

    def _run_user_app(self):
        global _setuphooks, _default_config
        try:
            self._config = _default_config
            self._config.update(self._user_config)
            if self._config["secret"] is None:
                self._config["secret"] = str(uuid.getnode())
            if self._config["home"] is None:
                self._config["home"] = pathlib.Path.home() / ".kroz"
            self._config["home"] = pathlib.Path(self._config["home"])
            if not self._config["home"].exists():
                self._config["home"].mkdir(parents=True)
            else:
                if not self._config["home"].is_dir():
                    raise RuntimeError(
                        f"The home configuration must be a directory: {self._config['home']}"
                    )
            if self._config["state_file"] is not None:
                self._state = JsonBoxFile(
                    self._config["secret"],
                    self._config["home"] / self._config["state_file"],
                )
                if "checkpoints" not in self._state:
                    self._state["checkpoints"] = {}

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
        self._main_worker._question_group = False

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """Called when the worker state changes."""
        if event.worker.name == "main" and event.worker.is_finished:
            cc = ConfirmationCode(key=self.config["secret"])
            self.exit(
                0,
                message=f"Your confirmation code is: {cc.confirmation({'score': self.score})}",
            )

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

    def show(self, screen: str | Screen, classes: str = "") -> Any:
        """Show a screen."""

        worker = get_current_worker()
        if worker.is_cancelled:
            raise KrozApp.CancelledWorkerException()
        result = self.call_from_thread(self._show, screen, classes)
        if worker.is_cancelled:
            raise KrozApp.CancelledWorkerException()
        return result

    async def _show(self, screen: str | Screen, classes: str) -> None:
        if isinstance(screen, str):
            self._showing = KrozScreen(
                screen, title="Welcome", classes=classes
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

    def ask(self, question: Question) -> Question.Result:
        """Ask the question."""
        worker = get_current_worker()
        checkpoint_result = Question.Result.INCORRECT
        if (
            question.checkpoint is not None
            and question.checkpoint in self.state["checkpoints"]
            and self.state["checkpoints"][question.checkpoint]
            == "Result.CORRECT"
        ):
            if worker._question_group:
                raise RuntimeError(
                    "You can't checkpoint questions in a group."
                )
            self.score += question.points
            return Question.Result.CHECKPOINTED
        try:
            question.setup()
            tries_left = question.tries
            while question.tries == 0 or tries_left > 0:
                question.setup_attempt()

                if tries_left >= 2:
                    self.notify(
                        f"You have {tries_left} tries left.",
                        title="Notice",
                        severity="warning",
                    )
                elif tries_left == 1:
                    self.notify(
                        "You have one try left!",
                        title="Last Try",
                        severity="error",
                    )
                answer = self.show(
                    QuestionScreen(
                        text=question.text,
                        placeholder=question.placeholder,
                        validators=question.validators,
                        can_skip=question.can_skip,
                    )
                )
                if answer is None:
                    if worker._question_group:
                        raise KrozApp.GroupFailedException()

                    checkpoint_result = Question.Result.SKIPPED
                    return Question.Result.SKIPPED

                try:
                    result = question.check(answer)
                except AssertionError as e:
                    result = e
                except Exception as e:
                    result = e
                    if question.debug:
                        raise e

                try:
                    if isinstance(result, Exception):
                        if isinstance(result, AssertionError):
                            border_title = "Incorrect Answer"
                        else:
                            border_title = (
                                f"Error: {result.__class__.__name__}"
                            )
                        self.show(
                            KrozScreen(
                                str(result),
                                title=border_title,
                                classes="feedback",
                            )
                        )
                        tries_left -= 1
                    else:
                        self.update_score(question.points)
                        self.show(
                            KrozScreen(
                                "# Congratulations" if not result else result,
                                title="Success",
                                classes="congrats",
                            )
                        )
                        self.score += question.points
                        checkpoint_result = Question.Result.CORRECT
                        return Question.Result.CORRECT
                finally:
                    question.cleanup_attempt()
        finally:
            question.cleanup()
            if question.checkpoint is not None:
                self.state["checkpoints"][question.checkpoint] = str(
                    checkpoint_result
                )
                self.state.store()

        return Question.Result.INCORRECT

    @contextmanager
    def group(self, checkpoint=None):
        """
        A context manager to group questions together. If any of the questions
        in the group are skipped or answered incorrectly, the group exits
        without asking any further questions. A question group is useful when
        a set of questions build on each other and when the desired behavior of
        the lab is to allow students to skip ahead, bypassing the entire group.
        """
        worker = get_current_worker()
        old_group = worker._question_group
        worker._question_group = True

        try:
            yield
        except KrozApp.GroupFailedException:
            pass
        finally:
            self._group = old_group

    @property
    def config(self):
        """A dictionary of configuration parameters."""
        return self._config

    @property
    def state(self):
        """A dictionary that's persisted in a state file."""
        if self._state is None:
            raise RuntimeError("No state file was given, can't save state.")
        return self._state
