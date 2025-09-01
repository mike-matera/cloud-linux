"""
# Lesson 4: Managing Files

After this lesson you should be able to:

- Understand file types
- View file contents
- Make links

Reading:

- Chapter 3

Commands:

1. `ls`
1. `file`
1. `less`
1. `cat`
1. `ln -s`
"""

import os
import re
from enum import Enum
from pathlib import Path
from typing import Callable

from textual.validation import Regex

import kroz.random as random
from kroz.app import KrozApp
from kroz.flow.base import KrozFlowABC
from kroz.flow.interaction import Interaction
from kroz.flow.question import (
    MultipleChoiceQuestion,
    Question,
    ShortAnswerQuestion,
    TrueOrFalseQuestion,
)
from kroz.questions.lesson03 import RelativePaths
from kroz.random.bigfile import random_big_file
from kroz.random.real_path import random_real_path
from kroz.validation import AbsolutePath, NotEmpty

title = "Working with Files"

state = "files"


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
        self._rows = rows
        self._cols = cols
        self._find = [*find]
        self._from_bottom = from_bottom
        self._from_right = from_right

    def setup(self):
        if self._find[0] is None:
            if not self._from_bottom:
                self._find[0] = random.randint(0, self._rows - 1) + 1
            else:
                self._find[0] = random.randint(1 - self._rows, -1)

        if self._find[1] is None:
            if not self._from_right:
                self._find[1] = random.randint(0, self._cols - 1) + 1
            else:
                self._find[1] = random.randint(1 - self._cols, -1)

        self._file = random_big_file(rows=self._rows, cols=self._cols)
        self._file.setup()

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
        self._path = path
        self._filter = filter

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

    def setup(self):
        if self._path is None:
            self._path = random_real_path().find_one(
                filter=lambda p: not p.is_symlink()
                and p.is_file()
                and self._filter(p),
                normalize=lambda p: p.suffix,
            )
        else:
            self._path = Path(self._path)
            assert not self._path.is_symlink() and self._path.is_file(), (
                "Invalid path."
            )
        self._solution = self.shell(f"file -b {self._path}").strip()

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
        self._path = path
        self._type = type

    def setup(self):
        if self._path is None:
            self._path = random_real_path().find_one(
                filter=lambda p: p.is_symlink()
            )
        else:
            self._path = Path(self._path)
            assert self._path.is_symlink(), "Invalid path."

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
        assert isinstance(self._path, Path)
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


class MakeLink(Question):
    """Make a symbolic link."""

    def __init__(
        self,
        name: str | Path,
        target: str | Path | None = None,
        rel: bool | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._path = Path(name)
        self._target = target
        self._rel = rel

    def setup(self):
        if not self._path.is_absolute():
            self._path = (
                (KrozApp.appconfig("default_path")) / self._path
            ).absolute()
        else:
            try:
                self._path.relative_to(KrozApp.appconfig("default_path"))
            except ValueError:
                raise RuntimeError(
                    "The path of a link must be relative to the app's default_path"
                )

        self._path = Path(self._path).absolute()
        if self._target is None:
            self._target = random_real_path().random_file()
        else:
            self._target = Path(self._target)

    @property
    def text(self):
        rel = ""
        if self._rel is not None:
            if self._rel:
                rel = "The link should be a relative link."
            else:
                rel = "The link should be an absolute link."
        return f"""
        # Make a Symbolic Link 

        Make a symbolic link named `{str(self._path).replace(str(Path.home()), "~")}` 
        that points to `{self._target}`. 
        **{rel}** 
        
        When you have made the link type `Enter` to continue.
        """

    placeholder = "Enter to continue"

    def check(self, answer):
        assert isinstance(self._target, Path)
        assert self._path.exists(), (
            f"""I can't find anything with at {self._path}"""
        )
        assert self._path.is_symlink(), (
            f"""The path `{self._path}` is not a symbolic link."""
        )
        assert self._path.readlink().resolve() == self._target.resolve(), (
            f"""The link `{self._path}` doesn't point to the right place."""
        )
        if self._rel is not None:
            if self._rel:
                assert not self._path.readlink().is_absolute(), (
                    f"""The link `{self._path}` is not relative."""
                )
            else:
                assert self._path.readlink().is_absolute(), (
                    f"""The link `{self._path}` is not absolute."""
                )


walks: dict[str, list[KrozFlowABC]] = {
    "Examine the types of files.": [
        Interaction(
            """
In your home directory, examine the type of the `Poems` directory:

```console
$ file Poems
```
""",
            lambda cmd: cmd.command == "file"
            and cmd.args[0].startswith("Poems")
            and cmd.cwd == Path().home(),
        ),
        Interaction(
            """
Now look at `what_am_i`:

```console
$ file what_am_i
```
""",
            lambda cmd: cmd.command == "file"
            and cmd.args[0].startswith("what_am_i")
            and cmd.cwd == Path().home(),
        ),
        Interaction(
            """
Now look at `text.err`:

```console
$ file text.err
```
""",
            lambda cmd: cmd.command == "file"
            and cmd.args[0].startswith("text.err")
            and cmd.cwd == Path().home(),
        ),
        Interaction(
            """
Look at `Poems/Angelou/bird`:

```console
$ file Poems/Angelou/bird
```
""",
            lambda cmd: cmd.command == "file" and cmd.args[0].endswith("bird"),
        ),
        Interaction(
            """
When a file is ASCII text it can be read with `cat`. But when it's too long for
the screen `cat` can be inconvenient. When you want to browse through a file using
the arrow keys, Page Up and Page Down use the `less` command instead of `cat`:

```console
$ less Poems/Angelou/bird
```

**To quit the `less` command type `Q` on the keyboard.**
""",
            lambda cmd: cmd.command == "less" and cmd.args[0].endswith("bird"),
        ),
    ],
    """Link your favorite poem.""": [
        Interaction(
            """
A symbolic link is a shortcut that points to another file. The shortcut takes up 
almost no space so it's a good way to put a file in two places without copying 
it. Start off by going to your `Poems` directory. 

```console
$ cd ~/Poems
```
""",
            lambda cmd: cmd.command == "cd"
            and cmd.cwd == Path().home() / "Poems",
        ),
        Interaction(
            """
Now choose a poem by your favorite poet. It can be any poem you like. When you 
have your choice make a symbolic link to that poem. Here's an example:

My favorite poem is `Neruda/artichoke`. To make a link to it I do this:

```console
$ ln -s Neruda/artichoke favorite 
``` 

That says "make a link called `favorite` to `Neruda/artichoke`.
""",
            lambda cmd: cmd.command == "ln"
            and cmd.args[0] == "-s"
            and cmd.args[2] == "favorite",
        ),
        Interaction(
            """
Let's take a look at your favorite. Use `ls -la` to see the link:

```console
$ ls -la favorite 
lrwxrwxrwx 1 maximus maximus 16 Aug  7 16:27 favorite -> Neruda/artichoke
```
""",
            lambda cmd: cmd.command == "ls" and "-la" in cmd.args,
        ),
        Interaction(
            """
Use cat to see `favorite` and you'll see that it contains the poem `artichoke`:

```console
$ cat favorite 
```
""",
            lambda cmd: cmd.command == "cat" and "favorite" in cmd.args,
        ),
    ],
}

questions: list[KrozFlowABC] = [
    MultipleChoiceQuestion(
        "Which of these is a *hidden* file?",
        ".file",
        "~/file",
        "file",
        "There are no hidden files",
    ),
    MultipleChoiceQuestion(
        "Which option to the `ls` command shows hidden files?",
        "-a",
        "-h",
        "-l",
        "-r",
    ),
    TrueOrFalseQuestion(
        "A files *extension* (e.g. `.jpeg`) determines the file type.",
        False,
        help="""
                        # File Types 
                        The type of a file is determined by its *contents*, not its 
                        name. In other words, the name of a file and what it 
                        contains are not strictly related. However, it's a good 
                        idea to name files appropriately so that, most of the time, 
                        a person doesn't need the `file` command to figure out 
                        what's inside of a file.
                        """,
    ),
    MultipleChoiceQuestion(
        "What is the difference between `cat` and `less`?",
        "`cat` prints the whole file while `less` lets you scroll through it.",
        "`less` as invented to replace `cat`.",
        "`cat` is a *pager* while `less` determines the file type.",
        "`less` is old and shouldn't be used anymore.",
    ),
    ShortAnswerQuestion(
        "What command lists the contents of a directory?", "ls"
    ),
    ShortAnswerQuestion(
        "What command shows what *type* of data a file contains?", "file"
    ),
    ShortAnswerQuestion(
        "What command lets you use the arrows keys to scroll through the contents of a file?",
        "less",
    ),
    ShortAnswerQuestion(
        "What command dumps the entire contents of a file to the terminal?",
        "cat",
    ),
    ShortAnswerQuestion("What command creates *symbolic links*?", "ln -s"),
]

lab: dict[str, list[KrozFlowABC]] = {
    "Find the first word": [WordInBigfile(find=(1, 1))],
    "What type of file?": [FileType()],
    "Relative paths": [RelativePaths()],
    "Find the link target": [LinkInfo(type=LinkInfo.Info.TARGET_PATH)],
    "Relative or absolute link": [LinkInfo(type=LinkInfo.Info.REL_OR_ABS)],
    "Make a symbolic link": [MakeLink(name="my_link")],
}
