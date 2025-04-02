"""
Worker safe API for interacting with a KROZ App.
"""

from textual.message import Message
from textual.worker import get_current_worker


class ProgressMessage(Message):
    """A message to indicate the progress of a slow running task."""

    def __init__(self, *, state="progress", percent=None, message=None):
        self.state = state
        self.percent = percent
        self.message = message
        super().__init__()


class progress:
    def __enter__(self):
        self._app = get_current_worker().node
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def stop(self):
        self._app.post_message(ProgressMessage(state="stop"))

    def busy(self):
        self._app.post_message(ProgressMessage(state="busy"))

    def update(self, percent=None, message=None):
        self._app.post_message(
            ProgressMessage(state="progress", percent=percent, message=message)
        )


def notify(message, title=None):
    get_current_worker().node.notify(message, title=title)
