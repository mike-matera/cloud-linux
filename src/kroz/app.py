"""
The Kroz UI Module
"""

import asyncio
from enum import Enum
import inspect
import subprocess
import sys
import textwrap
from textual.app import App
from textual.binding import Binding
from textual.screen import ModalScreen, Screen
from textual.worker import Worker, WorkerState, WorkType
from textual.widgets import Header, Footer, MarkdownViewer, Label, Input, Static
from textual.containers import Horizontal, HorizontalGroup, Vertical, Container

from kroz.question import Question

class WelcomeView(ModalScreen[bool]):

    BINDINGS = [("enter", "go", "Start the Lab")]

    def __init__(self, welcome):
        super().__init__()
        self._welcome = welcome 

    def compose(self):
        yield Header()
        yield MarkdownViewer(textwrap.dedent(self._welcome), show_table_of_contents=False)
        yield Footer()

    def action_go(self):
        self.dismiss(True)

class QuestionView(Screen[bool]):

    BINDINGS = [
        Binding("up", "key_up", "Scroll Up", priority=True),
        Binding("down", "key_down", "Scroll Down", priority=True),
        Binding("pageup", "key_pageup", "Page Up", priority=True, show=False,),
        Binding("pagedown", "key_pagedown", "Page Down", priority=True, show=False,),
    ]

    CSS_PATH = "app.tcss"

    def __init__(self, question):
        super().__init__()
        self._question = question 
        self._answer = Input(placeholder="Answer", classes="answer")
        self._instructions = MarkdownViewer(textwrap.dedent(self._question.text),
                                            show_table_of_contents=False,)

    def compose(self):
        yield Header()
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

    def __init__(self, title: str, welcome):
        super().__init__()
        self._title = title
        self._setup_func = lambda: ... 
        self._setup_worker = None
        self._cleanup_func = lambda: ...
        self._cleanup_worker = None
        self._main_func = None
        self._main_worker = lambda: ... 
        self._restart = False
        self._state = KrozApp.State.INIT
        self._welcome = WelcomeView(welcome)

    def setup(self, func: WorkType):
        """Decorator for the setup() function."""
        self._setup_func = func
        return func

    def _setup(self):
        self._setup_worker = self.run_worker(self._setup_func)

    def cleanup(self, func: WorkType):
        """Decorator for the cleanup() function."""
        self._cleanup_func = func
        return func

    def _cleanup(self):
        self._cleanup_worker = self.run_worker(self._cleanup_func)

    def main(self, func: WorkType):
        """Decorator for the main() function."""
        self._main_func = func
        return func

    def _main(self):
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
                if self._setup_worker.error:
                    raise self.setup_worker.error
                if not self._welcome.is_active:                
                    self._state = self.State.MAIN
                    self._main()
        elif self._state == self.State.MAIN:
            if self._main_worker.is_finished:
                if self._setup_worker.error:
                    raise self.setup_worker.error
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

    async def ask(self, question: Question):
        q = QuestionView(question)
        await self.push_screen_wait(q)

    def action_shell_escape(self):
        with self.suspend():
            subprocess.run("$SHELL", shell=True)
