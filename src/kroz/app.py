"""
The Kroz UI Module
"""

from contextlib import contextmanager
from enum import Enum
import subprocess
import textwrap
from textual.app import App
from textual.screen import ModalScreen
from textual.worker import Worker, WorkType, get_current_worker
from textual.widgets import (
    Footer,
    MarkdownViewer,
    Label,
    ProgressBar,
    RichLog,
)
from textual.containers import Vertical
from textual.reactive import Reactive
from textual.message import Message
from textual.worker import WorkerState

from kroz.question import Question
from kroz.screen.question import QuestionScreen
from kroz.widget.score_header import ScoreHeader


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


class WelcomeView(ModalScreen[bool]):
    BINDINGS = [
        ("enter", "dismiss", "Start the Lab"),
        ("ctrl+q", "app.cleanup_quit", "Quit"),
    ]

    CSS_PATH = "app.tcss"

    def __init__(self, welcome):
        super().__init__()
        self._welcome = welcome
        self._ready = False

    def compose(self):
        yield ScoreHeader()
        yield Footer()
        yield MarkdownViewer(
            textwrap.dedent(self._welcome),
            show_table_of_contents=False,
            classes="content",
        )

    def make_ready(self):
        self._ready = True
        self.refresh_bindings()

    def check_action(self, action: str, parameters: tuple[object, ...]):
        if self.is_mounted and action == "dismiss":
            return self._ready


class KrozApp(App):
    """A UI application."""

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

    def __init__(self, title: str, welcome: str):
        super().__init__()
        self.title = title
        self._setup_func = lambda: ...
        self._setup_worker = None
        self._cleanup_func = lambda: ...
        self._cleanup_worker = None
        self._main_func = lambda: ...
        self._main_worker = None
        self._restart = False
        self._welcome = WelcomeView(welcome)
        self._progress_screen = None
        self._cleaning = False

    def compose(self):
        yield ScoreHeader()
        yield Footer()

    def setup(self, func: WorkType):
        """Decorator for the setup() function."""

        def setup_wrapper():
            try:
                func()
            except KrozApp.CancelledWorkerException:
                # Ignore me.
                pass

        self._setup_func = setup_wrapper
        return setup_wrapper

    def _setup(self):
        self._setup_worker = self.run_worker(
            self._setup_func, "setup", thread=True
        )

    def cleanup(self, func: WorkType):
        """Decorator for the cleanup() function."""
        self._cleanup_func = func
        return func

    def _cleanup(self):
        self._cleanup_worker = self.run_worker(
            self._cleanup_func, "cleanup", thread=True
        )

    def main(self, func: WorkType):
        """Decorator for the main() function."""

        def main_wrapper():
            try:
                func()
            except KrozApp.CancelledWorkerException:
                # Ignore me.
                pass

        self._main_func = main_wrapper
        return main_wrapper

    def _main(self):
        self._main_worker = self.run_worker(
            self._main_func, "main", thread=True
        )

    async def on_mount(self):
        self._setup()
        self.push_screen(self._welcome, lambda w: self._main())

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """Called when the worker state changes."""
        if event.worker.name == "setup" and event.state == WorkerState.SUCCESS:
            self._welcome.make_ready()
        elif (
            event.worker.name == "main" and event.state == WorkerState.SUCCESS
        ):
            self._cleaning = True
            self._cleanup()
        elif (
            event.worker.name == "cleanup"
            and event.state == WorkerState.SUCCESS
        ):
            self.exit(0, message="Put the confirmation code here.")

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

    def action_cleanup_quit(self):
        # Are we already closing?
        if self._cleaning:
            return

        self._cleaning = True
        self.workers.cancel_all()

        # Kill the progress popup if it's there
        if isinstance(self.screen_stack[-1], ProgressScreen):
            self.pop_screen()

        self._cleanup()

    def ask(
        self,
        question: Question,
        points: int = 0,
        tries: int = 0,
        can_skip: bool = True,
    ) -> Question.Result:
        # Kill the main worker if it asks a question after a cancel.
        if get_current_worker().is_cancelled:
            raise KrozApp.CancelledWorkerException()
        result = self.call_from_thread(
            self._ask, question, points, tries, can_skip
        )
        if self._group and result != Question.Result.CORRECT:
            raise KrozApp.GroupFailedException()

    async def _ask(
        self, question: Question, points: int, tries: int, can_skip: bool
    ) -> Question.Result:
        return await self.push_screen_wait(
            QuestionScreen(question, points, tries, can_skip)
        )

    def post_message(self, message: Message):
        # Kill canceled workers that send a progress message.
        if (
            isinstance(message, progress.ProgressMessage)
            and get_current_worker().is_cancelled
        ):
            raise KrozApp.CancelledWorkerException()

        super().post_message(message)

    @contextmanager
    def group(self):
        worker = get_current_worker()
        old_group = worker._question_group
        self._group = True
        try:
            yield
        except KrozApp.GroupFailedException:
            pass
        finally:
            self._group = old_group
