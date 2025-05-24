"""
Questions for Week 4 covering Chapter 3
"""

from enum import Enum
import os
from pathlib import Path
import re
from typing import Callable
from kroz.question import Question
import kroz.random as random
from kroz.random.bigfile import random_big_file
from kroz.random.real_path import random_real_path
from kroz.validation import AbsolutePath, NotEmpty

from textual.validation import Regex


class WordInBigfile(Question):
    """Find a particular word in a big big file."""

    def __init__(
        self,
        rows=100000,
        cols=100,
        find=(None, None),
        from_bottom=False,
        from_right=False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._file = random_big_file(rows=rows, cols=cols)
        self._find = [*find]
        if find[0] is None:
            if not from_bottom:
                self._find[0] = random.randint(0, rows - 1) + 1
            else:
                self._find[0] = random.randint(1 - rows, -1)

        if find[1] is None:
            if not from_right:
                self._find[1] = random.randint(0, cols - 1) + 1
            else:
                self._find[1] = random.randint(1 - cols, -1)

    @property
    def text(self):
        if self._find[0] >= 0:
            line_no = self._find[0]
        else:
            line_no = f"{-self._find[0]} from the **bottom** of the file."

        if self._find[1] >= 0:
            word_no = self._find[1]
        else:
            word_no = f"{-self._find[1]} from the **end** of the line."

        return f"""
        # Find the Word 

        I have just created the file called:
         
        `{self._file.path}`
        
        Inside of it you will find a lot of words. To solve this challenge find 
        the word in the following place: 

        * Line number: {line_no} 
        * Word number: {word_no}

        Enter the word in the answer box below.
        """

    placeholder = "Word"
    validators = []

    def setup(self):
        self._file.setup()

    def cleanup(self):
        self._file.cleanup()

    def check(self, answer):
        solution = self._file.word_at(self._find[0], self._find[1])
        assert answer.strip() == solution, """
        # Incorrect!

        That is not the correct word.
        """


class FileType(Question):
    """Examine the type of an existing file."""

    def __init__(
        self,
        filter: Callable[[Path], bool] = lambda p: True,
        path: str | Path | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if path is None:
            self._path = random_real_path().find_one(
                filter=lambda p: not p.is_symlink()
                and p.is_file()
                and filter(p),
                normalize=lambda p: p.suffix,
            )
        else:
            self._path = Path(path)
            assert not self._path.is_symlink() and self._path.is_file(), (
                "Invalid path."
            )
        self._solution = self.shell(f"file -b {self._path}").strip()

    validators = NotEmpty()

    @property
    def placeholder(self):
        return "File type"

    @property
    def text(self):
        return f"""
        # File Type

        What is the type of this file?

            {self._path}

        """

    def check(self, answer: str):
        assert (
            self._solution.lower().split()[0] == answer.lower().split()[0]
        ), f"Bad type: {self._solution}"


class LinkInfo(Question):
    """Examine the properties of a symbolic link."""

    class Info(Enum):
        TARGET = (
            "What is the target of the symbolic link?",
            NotEmpty(),
            "Path",
        )
        TARGET_PATH = (
            "What is the **absolute path** of the target of the symbolic link?",
            AbsolutePath(),
            "Path",
        )
        REL_OR_ABS = (
            "Is the **target** of the link relative or absolute?",
            Regex(
                regex=r"relative|absolute",
                flags=re.I,
                failure_description='Type "relative" or "absolute"',
            ),
            "relative or absolute",
        )

    def __init__(
        self,
        type: Info,
        path: str | Path | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if path is None:
            self._path = random_real_path().find_one(
                filter=lambda p: p.is_symlink()
            )
        else:
            self._path = Path(path)
            assert self._path.is_symlink(), "Invalid path."

        self._type = type

    @property
    def validators(self):
        return self._type.value[1]

    @property
    def placeholder(self):
        return self._type.value[2]

    @property
    def text(self):
        return f"""
        # Symbolic Link Information 

        The following path points to a symbolic link:

            {self._path}

        {self._type.value[0]}
        """

    def check(self, answer: str):
        if self._type == LinkInfo.Info.TARGET:
            assert answer.strip() == os.readlink(self._path), (
                """That's not correct."""
            )
        elif self._type == LinkInfo.Info.TARGET_PATH:
            assert (
                Path(answer.strip())
                == (
                    self._path.parent / Path(os.readlink(self._path))
                ).resolve()
            ), (
                f"""That's not correct: {(self._path.parent / Path(os.readlink(self._path))).resolve()}"""
            )
        elif self._type == LinkInfo.Info.REL_OR_ABS:
            if answer.lower() == "absolute":
                assert Path(os.readlink(self._path)).is_absolute(), (
                    """That's not correct."""
                )
            else:
                assert not Path(os.readlink(self._path)).is_absolute(), (
                    """That's not correct."""
                )
        else:
            raise ValueError("Bad type")
