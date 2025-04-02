"""
KROZ Lab Player Engine
"""

from kroz.app import KrozApp, ProgressMessage

from textual.worker import get_current_worker


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


__all__ = [KrozApp, progress, notify]
