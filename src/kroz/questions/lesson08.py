"""
# Lesson 8. Like a Boss

- Wildcards
- Quotes
- Tab Completion

Reading:

- Chapters 7 and 8
"""

import pathlib
from typing import Type

from kroz import KrozApp
from kroz.flow.base import KrozFlowABC
from kroz.flow.interaction import Interaction
from kroz.flow.question import (
    Question,
)
from kroz.random.bigdir import random_directory
from kroz.random.words import random_words
from kroz.screen import KrozScreen

title = "Like a Boss!"

state = "theboss"

welcome = KrozScreen(
    """
# Like a Boss!

In this lesson you'll learn some tricks to make your work faster and more efficient. 
You'll learn how to: 

1. Use the glob characters `*` and `?` 
1. Use Tab completion 
1. Use quotes and backslashes to change the meaning of characters 
1. Use command substitution 
        """,
    classes="welcome",
    title="Welcome!",
)


class RandomRando(Question):
    """Random directory stuff"""

    placeholder = "Enter to continue."

    text = """
    # Remove the "m" Files

    I have just (re)created a directory called "Rando" in your home directory.
    Remove all files with names that start with the letter "m" (lower case). """

    def setup(self):
        self._rd = random_directory(500)
        self._rd.setup()

    def cleanup(self):
        self._rd.cleanup()

    def check(self, answer):
        target = self._rd.filter(lambda x: not str(x.path).startswith("m"))
        target.full_report(verbose=2)


class RandomRandoTick(Question):
    """Random directory stuff"""

    placeholder = "Enter to continue."

    text = """
    # Remove the "'" Files

    Remove all files with names that contain a single quote (') character. 
    """

    def setup(self):
        self._rd = random_directory(500)
        self._rd.setup()

    def cleanup(self):
        self._rd.cleanup()

    def check(self, answer):
        target = self._rd.filter(lambda x: "'" not in str(x.path))
        target.full_report(verbose=2)


class RandomDeleteMe(Question):
    """Random directory stuff"""

    placeholder = "Enter to continue."

    text = """
    # Remove the "'" Files

    Remove all files that contain the word "delete" in them. 
    """

    def setup(self):
        self._rd = random_directory(500)
        self._rd.setup()

    def cleanup(self):
        self._rd.cleanup()

    def check(self, answer):
        target = self._rd.filter(lambda x: "delete" not in str(x.contents))
        target.full_report(verbose=2)


class DeepMessage(Question):
    placeholder = "What is the secret word?"

    text = """
    # Deep Directory 

    Look in ~/Files and find the hidden message.
    """

    def setup(self):
        self._answer = random_words().choice()
        path = KrozApp.appconfig("default_path") / pathlib.Path(
            "Files/deep/there's/a/light/over/at/the/Frankenstein/place/there's/a/li/ii/ii/ii/ii/ii/ii/ight/burning/in/the/fire/place"
        )
        file = path / ".secret"
        path.mkdir(parents=True, exist_ok=True)
        with open(file.resolve(), "w") as fh:
            fh.write(self._answer + "\n")

    def check(self, answer):
        assert answer.strip() == self._answer, """That's not correct!"""


walks: dict[str, list[KrozFlowABC | Type[KrozFlowABC]]] = {
    """Go wildcard!""": [
        Interaction(
            """
# Using Wildcard to Select Files 

In this walk through you'll use the `*` and `?` characters to have the shell 
*substitute* those characters onto your command line. Once you get the hang of 
globbing you'll be able to work faster and better. 

Let's start by going to your `~/Poems` directory:

```console
$ cd ~/Poems
```
                    """,
            filter=lambda cmd: cmd.command == "cd"
            and cmd.cwd == pathlib.Path().home() / "Poems",
        ),
        Interaction(
            """
# The Star 

The star `*` character is a wildcard that matches *zero or more* characters in a
file name. For example this shows us information about any file that starts with
the letter `s` in the `Shakespeare` directory:

```console
$ ls -l Shakespeare/s*
```
                    """,
            filter=lambda cmd: cmd.command == "ls"
            and cmd.args[-1] == "Shakespeare/s*",
        ),
        Interaction(
            """
The `*` can be in any position. This command finds the files that end in the 
number `5`:

```console
$ ls -l Shakespeare/*5
```
                    """,
            filter=lambda cmd: cmd.command == "ls"
            and cmd.args[-1] == "Shakespeare/*5",
        ),
        Interaction(
            """
You can have multiple `*`s. This command finds the files that have the number
`1` anywhere in the name: 

```console
$ ls -l Shakespeare/*1*
```
                    """,
            filter=lambda cmd: cmd.command == "ls"
            and cmd.args[-1] == "Shakespeare/*1*",
        ),
        Interaction(
            """
# The `?` is More Restrictive 

The `?` wildcard character matches *zero or one* character in the name of a
file. If you want to see `sonnet10` but not `sonnet1` you can use the `?` like
this:

```console
$ ls -l Shakespeare/sonnet1?
```
                    """,
            filter=lambda cmd: cmd.command == "ls"
            and cmd.args[-1] == "Shakespeare/sonnet1?",
        ),
    ],
}

questions: list[Question] = []

lab: dict[str, list[Question]] = {}
