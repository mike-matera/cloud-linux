"""
The Kroz UI Module
"""

import asyncio
from enum import Enum
import inspect
import subprocess
import sys
import textwrap
from textual import on
from textual.app import App, RenderResult
from textual.binding import Binding
from textual.screen import ModalScreen, Screen
from textual.worker import Worker, WorkerState, WorkType
from textual.widgets import Header, Footer, MarkdownViewer, Label, Input, Static, ProgressBar, RichLog
from textual.widget import Widget
from textual.containers import Horizontal, HorizontalGroup, Vertical, Container
from textual.widgets._header import HeaderIcon, HeaderTitle, HeaderClock, HeaderClockSpace
from textual.reactive import Reactive
from rich.text import Text 

from kroz.question import Question

class ScoreHeader(Header):

    class HeaderScore(Widget):
        DEFAULT_CSS = """
        HeaderScore {
            background: $foreground-darken-1 5%;
            color: $foreground;
            text-opacity: 85%;
            content-align: center middle;
            dock: right;
            width: 20;
            padding: 0 1;
        }
        """

        def __init__(self):
            super().__init__()
            self._total = 0
            self._score = 0 
            self._format = ""

        def render(self) -> RenderResult:
            return Text(self._format.format(score=self._score, total=self._total))
        
        async def set_total(self, total: int) -> None:
            self._total = total
            self.refresh()

        async def set_score(self, score: int) -> None:
            self._score = score 
            self.refresh()

        async def set_format(self, format: str) -> None:
            self._format = format 
            self.refresh() 

    def __init__(self):
        super().__init__()
        self._total = None
        self._score = None
        self._score_widget = ScoreHeader.HeaderScore()

    def compose(self):
        yield HeaderIcon().data_bind(Header.icon)
        yield HeaderTitle()
        yield self._score_widget

    def on_mount(self):
        self.watch(self.app, "total", self._score_widget.set_total)
        self.watch(self.app, "score", self._score_widget.set_score)            
        self.watch(self.app, "progress_format", self._score_widget.set_format)            

class WelcomeView(ModalScreen[bool]):

    BINDINGS = [
        ("enter", "dismiss", "Start the Lab"),
        ("ctrl+q", "app.cleanup_quit", "Quit")
        ]

    def __init__(self, welcome):
        super().__init__()
        self._welcome = welcome 

    def compose(self):
        yield ScoreHeader()
        yield MarkdownViewer(textwrap.dedent(self._welcome), show_table_of_contents=False)
        yield Footer()

class QuestionView(Screen[bool]):

    BINDINGS = [
        Binding("up", "key_up", "Scroll Up", priority=True),
        Binding("down", "key_down", "Scroll Down", priority=True),
        Binding("pageup", "key_pageup", "Page Up", priority=True, show=False,),
        Binding("pagedown", "key_pagedown", "Page Down", priority=True, show=False,),
        Binding("ctrl+q", "app.cleanup_quit", "Quit", priority=True),
    ]

    CSS_PATH = "app.tcss"

    def __init__(self, question):
        super().__init__()
        self._question = question 
        self._answer = Input(placeholder="Answer", classes="answer")
        self._instructions = MarkdownViewer(textwrap.dedent(self._question.text),
                                            show_table_of_contents=False,)

    def compose(self):
        yield ScoreHeader()
        yield Footer()
        yield Container(
            self._instructions,
            HorizontalGroup(
                Label("Answer:", classes="answer_label"),
                self._answer,
                classes="answer_container",
            ),
            classes="main",
        )

    def on_mount(self):
        self.set_focus(self._answer)
        self.refresh_bindings()

    def key_down(self, key):
        if self._instructions.scrollbars_enabled[0]:
            self._instructions.action_scroll_down()
            self.refresh_bindings()

    def key_up(self, key):
        if self._instructions.scrollbars_enabled[0]:
            self._instructions.action_scroll_up()
            self.refresh_bindings()

    def key_pagedown(self, key):
        if self._instructions.scrollbars_enabled[0]:
            self._instructions.action_page_down()
            self.refresh_bindings()

    def key_pageup(self, key):
        if self._instructions.scrollbars_enabled[0]:
            self._instructions.action_page_up()
            self.refresh_bindings()

    def check_action(self, action: str, parameters: tuple[object, ...]):
        if action in ["key_up", "key_pageup", "key_down", "key_pagedown"]:
            return self._instructions.scrollbars_enabled[0]
        else:
            return True 

    @on(Input.Submitted)
    def foobar(self, event: Input.Changed) -> None:
        self.dismiss(True)

class KrozApp(App):
    """A UI application."""

    BINDINGS = [
        ("ctrl+s", "shell_escape", "Shell"),
        ("ctrl+q", "app.quit", "Quit"),
        ]

    class State(Enum):
        INIT = 1
        SETUP = 2
        MAIN = 3
        CLEANUP = 4

    total: Reactive[int] = Reactive(0)
    score: Reactive[int] = Reactive(0)
    progress_format: Reactive[str] = Reactive("Score: {score}/{total}")

    DEFAULT_CSS = """
        Screen {
            align: center middle;
        }

        #loading {
            width: 70;
            height: 20;
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
            height: 100%;
            padding-left: 2;
            padding-right: 0;
            padding-top: 1;
            padding-bottom: 1;
            overflow-y: auto;
        }

        """
    def __init__(self, title: str, welcome: str, *, total_score=0):
        super().__init__()
        self.title = title
        self.total = total_score
        self._setup_func = lambda: ... 
        self._setup_worker = None
        self._cleanup_func = lambda: ...
        self._cleanup_worker = None
        self._main_func = lambda: ...
        self._main_worker = None
        self._restart = False
        self._state = KrozApp.State.INIT
        self._welcome = WelcomeView(welcome)
        self._task_log = RichLog(id="messages", wrap=True)
        self._progress = ProgressBar(show_percentage=False, show_eta=False, id="progress")

    def compose(self):
        yield ScoreHeader()
        yield Footer()
        with Vertical(id="loading"):
            yield Label("🤖 Please Wait...", id="loading_title")
            yield self._progress
            yield self._task_log

    def setup(self, func: WorkType):
        """Decorator for the setup() function."""
        self._setup_func = func
        return func

    def _setup(self):
        self._task_log.clear()
        self._task_log.write("Running setup()...")
        self._progress.total = None
        self._setup_worker = self.run_worker(self._setup_func)

    def cleanup(self, func: WorkType):
        """Decorator for the cleanup() function."""
        self._cleanup_func = func
        return func

    def _cleanup(self):
        self._task_log.clear()
        self._task_log.write("Cleaning up.")
        self._progress.total = None
        self._cleanup_worker = self.run_worker(self._cleanup_func)

    def main(self, func: WorkType):
        """Decorator for the main() function."""
        self._main_func = func
        return func

    def _main(self):
        self._task_log.clear()
        self._progress.total = None
        self._main_worker = self.run_worker(self._main_func)

    async def on_mount(self):
        self.push_screen(self._welcome, lambda w: self.state_update())
        self.state_update()

    def state_update(self):
        if self._state == self.State.INIT:
            self._state = self.State.SETUP
            self._setup()
        if self._state == self.State.SETUP:
            if self._setup_worker.is_finished:
                if not self._welcome.is_active:                
                    self._state = self.State.MAIN
                    self._main()
        elif self._state == self.State.MAIN:
            if self._main_worker.is_finished:
                if self._setup_worker.is_cancelled:
                    self._restart = True
                self._state = self.State.CLEANUP
                self._cleanup()
        elif self._state == self.State.CLEANUP:
            if self._cleanup_worker.is_finished:
                if self._restart:
                    self._state = self.State.SETUP
                    self._setup()
                else:
                    # Do exit display
                    self.exit(result=0, message="Put the confirmation code here.")
        else:
            raise ValueError("Unexpected state in state change:", self._state)

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """Called when the worker state changes."""
        self.state_update()

    def action_shell_escape(self):
        with self.suspend():
            subprocess.run("$SHELL", shell=True)

    def action_cleanup_quit(self):
        # Are we already closing?
        if self._state == self.State.CLEANUP:
            return
        
        # Cancel any running workers
        # FIXME: This breaks for thread workers... 
        if self._setup_worker and self._setup_worker.is_running:
            self._setup_worker.cancel()
        if self._main_worker and self._main_worker.is_running:
            self._main_worker.cancel()

        # Show the main screeen...
        self.switch_screen(self.screen_stack[0])

        # Enter the cleanup state.
        self._state = self.State.CLEANUP
        self._cleanup()

    def thread_api(func):
        def wrapper(self: App, *args, **kwargs):
            self.call_from_thread(func, *args, **kwargs)

    async def ask(self, question: Question):
        self._task_log.clear()
        self._progress.total = 100 # Stop the animation
        self._progress.progress = 0
        try:
            q = QuestionView(question)
            correct = await self.push_screen_wait(q)
            if correct:
                self.score += 10 
        finally:
            self._progress.total = None

    def progress(self, *, percent=None, message=None):
        if percent is None:
            self._progress.total = None
        else:
            self._progress.total = 100 
            self._progress.progress = percent
    
        if message:
            self._task_log.write(message)
