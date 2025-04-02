"""
Abstract Question Base
"""

from abc import ABC, abstractmethod


class Question(ABC):
    def __init__(self, *, points: int = None):
        self._points = points

    @property
    @abstractmethod
    def text(self): ...

    @abstractmethod
    def check(self, answer): ...

    def setup(self): ...

    def cleanup(self): ...
