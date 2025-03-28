"""
Abstract Question Base 
"""

from abc import ABC, abstractmethod


class Question(ABC):
    
    @property
    @abstractmethod
    def text(self):
        ... 

    @abstractmethod
    def check(self, answer):
        ... 

