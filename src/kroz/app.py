"""
The Kroz UI Module 
"""

from textual.app import App
from textual.worker import Worker

class KrozApp(App):
    """A UI application."""

    def __init__(self, title: str):
        super().__init__()
        self._title = title 
        self._setup = None 
        self._cleanup = None 
        self._main = None 

    def setup(self, func):
        """Decorator for the setup() function."""
        self._setup = func 
        return func

    def cleanup(self, func):
        """Decorator for the cleanup() function."""
        self._cleanup = func 
        return func

    def main(self, func):
        """Decorator for the main() function."""
        self._main = func 
        return func

    def _call(self, func):
        """Call async or sync."""
        if callable(func):
            self.run_worker(func, thread=True)
        else:
            self.run_worker(func)

    def on_mount(self):
        if self._setup:
            self._call(self._setup)
        try:
            if self._main:
                self._call(self._main)
        
        finally:
            if self._cleanup:
                self._call(self._cleanup)

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """Called when the worker state changes."""
        self.log(event)

