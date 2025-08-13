"""
# Lesson 6. Commands

- Identify a command
- Use the manual
- Create an alias

Reading:

- Chapter 5
"""

from typing import Type

from kroz.flow.base import KrozFlowABC
from kroz.flow.question import MultipleChoiceQuestion, Question
from kroz.screen import KrozScreen

title = "Getting Help"

state = "rtfm"

welcome = KrozScreen(
    """
# Getting Help  

Former students tell me that this is the most helpful lesson in this class. In 
it you learn how to use the online manual to figure out how commands work. Once
you can read the manual you can teach yourself anything you need to know.

You will learn about the commands:

1. `type`
2. `man`
3. `alias`
        """,
    classes="welcome",
    title="Welcome!",
)

walks: dict[str, list[KrozFlowABC | Type[KrozFlowABC]]] = {}


questions: list[Question] = [
    MultipleChoiceQuestion(
        "What command would you use to *rename* a file?",
        "mv",
        "cp",
        "ln -s",
        "rm",
    ),
]

lab: dict[str, list[Question]] = {}
