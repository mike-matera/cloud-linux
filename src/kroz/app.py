"""
The Kroz UI Module
"""

from enum import Enum
from textual.app import App
from textual.worker import Worker, WorkerState, WorkType


class KrozApp(App):
    """A UI application."""

    class State(Enum):
        INIT = 1
        SETUP = 2
        MAIN = 3
        CLEANUP = 4
        EXIT = 5

    def __init__(self, title: str):
        super().__init__()
        self._title = title
        self._setup = None
        self._cleanup = None
        self._main = None
        self._state = KrozApp.State.INIT

    def setup(self, func: WorkType):
        """Decorator for the setup() function."""
        self._setup = func
        return func

    def cleanup(self, func: WorkType):
        """Decorator for the cleanup() function."""
        self._cleanup = func
        return func

    def main(self, func: WorkType):
        """Decorator for the main() function."""
        self._main = func
        return func

    def _call(self, func):
        """Call async or sync."""
        if func is not None:
            if callable(func):
                self.run_worker(func, thread=True)
            else:
                self.run_worker(func)

    def on_mount(self):
        if self._state == KrozApp.State.INIT:
            self._state = KrozApp.State.SETUP
            self._call(self._setup)
        else:
            self.log("Mount while not in init.")

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """Called when the worker state changes."""
        if self._state == self.State.SETUP:
            if event.state == WorkerState.SUCCESS:
                self._state = self.State.MAIN
                self._call(self._main)
            else:
                raise
        elif self._state == self.State.MAIN:
            pass
        elif self._state == self.State.CLEANUP:
            pass
        elif self._state == self.State.EXIT:
            pass
        else:
            raise ValueError("Unexpected state in state change:", event)

        self.log(event)
