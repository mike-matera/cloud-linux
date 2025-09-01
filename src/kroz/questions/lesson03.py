"""
# Lesson 3: The File System

After this lesson you should be able to:

- Navigate the filesystem
- Use relative and absolute paths
- List files

Reading:

- Chapter 2

Commands:

1. `cd`
1. `pwd`
1. `ls`
"""

import grp
import os
import pwd
import textwrap
from enum import Enum
from pathlib import Path

from textual.validation import Integer

import kroz.ascii
from kroz.app import KrozApp
from kroz.flow.interaction import Interaction
from kroz.flow.question import (
    MultipleChoiceQuestion,
    Question,
    ShortAnswerQuestion,
    TrueOrFalseQuestion,
)
from kroz.random.real_path import random_real_path
from kroz.validation import (
    AbsolutePath,
    ExistingPath,
    IsGroup,
    IsPermission,
    IsUser,
    PathIsDir,
    PathIsFile,
    RelativePath,
)

title = "The File System"

state = "filesystem"


class FlagFile(Question):
    """Create a file and ask about its contents."""

    class FlagType(Enum):
        NAME = 1
        DIR = 2
        FULL = 3

    def __init__(
        self, type: FlagType, path: str | Path | None = None, **kwargs
    ):
        super().__init__(**kwargs)
        self._type = type
        self._secret = path
        self._flag = None

    @property
    def validators(self):
        if self._type == FlagFile.FlagType.NAME:
            return []
        elif self._type == FlagFile.FlagType.DIR:
            return [AbsolutePath(), ExistingPath(), PathIsDir()]
        elif self._type == FlagFile.FlagType.FULL:
            return [AbsolutePath(), ExistingPath(), PathIsFile()]

    def flag(self):
        """Generate the flag text."""
        return textwrap.dedent("""

        {}                                

        Welcome {} this is your flag file. 
                                    
        Your secret file is: {}

        """).format(
            kroz.ascii.robot(),
            pwd.getpwuid(os.getuid())[4].split(",")[0],
            self._secret,
        )

    def setup(self):
        self._flag = KrozApp.appconfig("default_path") / "flag"
        if self._secret is None:
            self._secret = random_real_path().random_file().resolve()
        else:
            self._secret = Path(self._secret)

        with open(self._flag, "w") as fh:
            fh.write(self.flag())

    def cleanup(self):
        if self._flag is not None:
            self._flag.unlink(missing_ok=True)

    @property
    def text(self):
        assert isinstance(self._flag, Path)
        q = f"""
        # Find the Flag

        I have just created a file named: {self._flag.resolve()}

        **Look inside of the file.** You will see that it contains the location 
        of a secret file. """

        if self._type == FlagFile.FlagType.NAME:
            q += """Answer the question by entering the **name** of the secret file (not including the directory)."""
        elif self._type == FlagFile.FlagType.DIR:
            q += """Answer the question by entering the **directory** that the secret file is in."""
        elif self._type == FlagFile.FlagType.FULL:
            q += """Answer the question by entering the **absolute path** of the secret file."""

        return q

    def check(self, answer):
        assert isinstance(self._secret, Path)
        assert Path(answer) != self._flag, """
            # That's the Flag Itself!

            You entered the name of the flag file itself. The **secret** file is 
            inside of the flag file. Use the `cat` command to look inside of the 
            flag file to reveal the secret.
        """
        if self._type == FlagFile.FlagType.NAME:
            assert answer.strip() == self._secret.name, """
                That's not correct.
            """
        elif self._type == FlagFile.FlagType.DIR:
            assert Path(answer.strip()) == self._secret.parent, (
                """That's not correct."""
            )
        elif self._type == FlagFile.FlagType.FULL:
            answer = Path(answer.strip()).resolve()
            assert answer == self._secret, """
                That's not correct.
        """


class PathAttrs(Question):
    """Examine the attributes of an existing file."""

    class PathType(Enum):
        FILE = "file"
        DIR = "directory"
        LINK = "symbolic link"

    class AttrType(Enum):
        SIZE = ("Size", "What is the **size** of", [Integer()])
        INODE = ("Inode", "What is the **inode number** of", [Integer()])
        OWNER = ("Owner", "Who is the **owner** of", [IsUser()])
        GROUP = ("Group", "What is the **group** of", [IsGroup()])
        PERMS = (
            "Permissions",
            "What are the **permissions** of",
            [IsPermission()],
        )
        BLOCKS = ("Blocks", "How many **blocks** are used by", [Integer()])

    def __init__(
        self,
        type: AttrType,
        path: str | Path | None = None,
        path_type: PathType = PathType.FILE,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._type = type
        self._path_type = path_type
        self._path = path

    @property
    def placeholder(self):
        return self._type.value[0]

    @property
    def text(self):
        return f"""
        # Find the {self._type.value[0]}

        {self._type.value[1]} the {self._path_type.value}:

            {self._path}

        """

    def setup(self):
        if self._path is None:
            if self._path_type == PathAttrs.PathType.FILE:
                self._path = random_real_path().random_file()
            elif self._path_type == PathAttrs.PathType.DIR:
                self._path = random_real_path().random_dir()
            elif self._path_type == PathAttrs.PathType.LINK:
                self._path = random_real_path().random_link()
            else:
                raise ValueError("Bat path type.")
        else:
            self._path = Path(self._path)

    @property
    def validators(self):
        return self._type.value[2]

    def check(self, answer):
        assert isinstance(self._path, Path)
        if self._type == PathAttrs.AttrType.SIZE:
            assert int(answer) == self._path.stat().st_size, (
                """That's not correct."""
            )
        elif self._type == PathAttrs.AttrType.INODE:
            assert int(answer) == self._path.stat().st_ino, (
                """That's not correct."""
            )
        elif self._type == PathAttrs.AttrType.OWNER:
            assert answer == pwd.getpwuid(self._path.stat().st_uid).pw_name, (
                """That's not correct."""
            )
        elif self._type == PathAttrs.AttrType.GROUP:
            assert answer == grp.getgrgid(self._path.stat().st_gid).gr_name, (
                """That's not correct."""
            )
        elif self._type == PathAttrs.AttrType.PERMS:
            assert (
                IsPermission.from_string(answer)
                == self._path.stat().st_mode & 0o777
            ), """That's not correct."""
        elif self._type == PathAttrs.AttrType.BLOCKS:
            assert int(answer) == self._path.stat().st_blocks, (
                """That's not correct."""
            )
        else:
            raise ValueError("Bad type")


class RelativePaths(Question):
    """
    Ask students to construct relative paths.
    """

    def __init__(
        self,
        from_path: str | Path | None = None,
        to_path: str | Path | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._from = from_path
        self._to = to_path

    validators = [RelativePath()]

    @property
    def text(self):
        return f"""
        # Relative Path 

        What is the relative path between these two directories?

        * From: `{self._from}`
        * To: `{self._to}`
        """

    def setup(self):
        if self._from is None:
            self._from = random_real_path().random_dir().resolve()
        else:
            self._from = Path(self._from)
        if self._to is None:
            self._to = random_real_path().random_dir().resolve()
        else:
            self._to = Path(self._to)

    def check(self, answer):
        assert isinstance(self._from, Path)
        assert isinstance(self._to, Path)
        answer = Path(answer)
        calculated = (self._from / answer).resolve()

        feedback = textwrap.dedent(f"""
        # The Path Journey

        Consider the trip between the *from* and the *to* directories. Your answer
        should be a relative path that contains the entire journey. The journey 
        starts at **{self._from}**  and the path we take is your answer **{answer}**. 
        
        Here's what it looks like when we take the journey one step at a time: 
        """)
        loc = self._from
        for i, part in enumerate(answer.parts):
            loc /= part
            feedback += f"{i + 1}. {part} → {loc.resolve()}\n"

        feedback += f"\nThe end of the journey is **{loc.resolve()}** but should have been **{self._to}**\n"
        assert calculated == self._to, feedback


walks: dict[str, list[Interaction]] = {
    "Navigate the file system": [
        Interaction(
            """ 
# There's No Place Like Home

Your *home directory* is the place where you keep your personal files. It's also
the initial *working directory* of the shell when you log in over `ssh`. On opus
your home directory has files that are used as examples in the class, Including
the `Poems` directory. 

The `cd` command navigates your shell through the file system. Running `cd` with
no arguments navigates to your home directory. Start off by navigating to your 
home directory:

```console
$ cd 
```

**Before you go further you should be in your home directory.** 
""",
            lambda cmd: cmd.command == "cd" and cmd.args == [],
        ),
        Interaction(
            """ 
Now that you're in your home directory, let's issue some commands that are
useful when you're exploring the filesystem, starting with the `pwd` command
(short for Print Working Directory). The `pwd` command shows you where you
are. Like a GPS.


```console
$ pwd
```
""",
            lambda cmd: cmd.command == "pwd" and cmd.args == [],
        ),
        Interaction(
            """ 
Directories have *contents*, other files and directories. The `ls` (short
for List) command shows the contents of the current working directory.  Use
the `ls` command to see the contents of your home directory:

```console
$ ls
```

What do you see there?
""",
            lambda cmd: cmd.command == "ls",
        ),
        Interaction(
            """ 
# Take a Longer Look

The `ls` command has many switches that control its output. The `-l` or
*long* flag changes the output to have each file or directory on its own
line. This gives you a lot more information: 

```console
$ ls -l
```
""",
            lambda cmd: cmd.command == "ls" and "-l" in cmd.args,
        ),
        Interaction(
            """ 
Files that begin with a `.` are called *hidden files*. They're not hidden
for security purposes, they're just hidden so they don't clutter up the view
when you run the `ls` command. Using the `-a` switch tells `ls` that you
want to see hidden files. 

```console
$ ls -a
```
""",
            lambda cmd: cmd.command == "ls" and "-a" in cmd.args,
        ),
        Interaction(
            """ 
Most commands let you combine switches when it makes sense. The `-l` and
`-a` switches can both be active when you run `ls`. You could apply them
both like this:

```console
$ ls -l -a 
```

However, commands that take switches often let you combine them into a
single flag. Try running `ls` like this:

```console
$ ls -la 
```
""",
            lambda cmd: cmd.command == "ls" and "-la" in cmd.args,
        ),
        Interaction(
            """ 
The `ls` command can also be given a file or directory as an argument. When no 
argument is given `ls` shows you the current working directory. An argument 
overrides that behavior to show you any directory you want:

```console
$ ls Poems
```

Running that command shows the the `Poems` directory. 
""",
            lambda cmd: cmd.command == "ls"
            and ("Poems" in cmd.args or "Poems/" in cmd.args),
        ),
        Interaction(
            """ 
# A Tree!

The `tree` command shows you a visual representation of a directory tree. 

```console 
$ tree Poems/
Poems/
├── Angelou
│   ├── bird
│   ├── diner
│   ├── woman
│   └── you
├── ant
...
```
""",
            lambda cmd: cmd.command == "tree"
            and any(("Poems" in arg for arg in cmd.args)),
        ),
    ],
    """Look at the poems in your `Poems` directory.""": [
        Interaction(
            """
Use the `cd` command to navigate into the `Poems` directory from your home
directory.
                    """,
            lambda cmd: cmd.cwd == Path().home() / "Poems",
        ),
        Interaction(
            """
Now that you're in the `~/Poems` directory you can navigate into the `Angelou`
directory:

```console
$ cd Angelou
```
                    """,
            lambda cmd: cmd.cwd == Path().home() / "Poems" / "Angelou",
        ),
        Interaction(
            """
The `cat` command will show you the `bird` poem when you're in the `Angelou`
directory:

```console
$ cat bird
```
                    """,
            lambda cmd: cmd.command == "cat" and "bird" in cmd.args,
        ),
        Interaction(
            """
Go back to your `Poems` directory by calling `cd` the special path `..`:

```console
$ cd ..
```
""",
            lambda cmd: cmd.command == "cd"
            and (cmd.args == [".."] or cmd.args == ["../"]),
        ),
        Interaction(
            """
Go back to your `Home` directory by calling `cd` the special path `..`:

```console
$ cd ..
```
""",
            lambda cmd: cmd.command == "cd"
            and (cmd.args == [".."] or cmd.args == ["../"])
            and cmd.cwd == Path().home(),
        ),
        Interaction(
            """
If you want to refer to the `bird` poem from another directory you have to tell
the shell how to find it. You do this using a path. The path to `bird` from your
home directory looks like this:

```console
$ cat Poems/Angelou/bird
```
                    """,
            lambda cmd: cmd.command == "cat"
            and "Poems/Angelou/bird" in cmd.args,
        ),
    ],
}


questions: list[Question] = [
    TrueOrFalseQuestion(
        "UNIX, like Windows uses a *hierarchical directory structure*.", True
    ),
    TrueOrFalseQuestion(
        "A directory is sometimes called a folder on other operating systems.",
        True,
    ),
    MultipleChoiceQuestion(
        "Which of the following is an **relative** path?",
        "Poems",
        "/home/student",
        "~/Poems/Neruda",
        "/dev/null",
        help="""
            Relative paths are paths that start at the current working 
            directory. Relative paths do not begin with a slash (**/**).
            """,
    ),
    MultipleChoiceQuestion(
        "Which of the following is an **absolute** path?",
        "Both ~/Poems/Neruda and /home/student",
        "/home/student",
        "~/Poems/Neruda",
        "Poems",
        help="""
            Absolute paths are paths that begin with the **root** directory. The
            root directory is represented by a slash (**/**). So absolute paths 
            always begin with a **/**. There's one exception, the **~** is a 
            shortcut for the absolute path of your home directory. 
            """,
    ),
    TrueOrFalseQuestion(
        "In UNIX a file that begins with a period (**.**) is called a *hidden* file.",
        True,
    ),
    ShortAnswerQuestion(
        "What is the command that shows you the **path** of the current working directory?",
        "pwd",
    ),
    ShortAnswerQuestion(
        "What is the command that changes current working directory?", "cd"
    ),
    ShortAnswerQuestion(
        "What is the command that shows the **contents** of the current working directory?",
        "ls",
    ),
]

lab: dict[str, list[Question]] = {
    "Name the flag": [FlagFile(type=FlagFile.FlagType.NAME)],
    "The flag directory": [FlagFile(type=FlagFile.FlagType.DIR)],
    "Find a file size": [PathAttrs(type=PathAttrs.AttrType.SIZE)],
    "Fine the inode": [PathAttrs(type=PathAttrs.AttrType.INODE)],
    "Relative to home": [RelativePaths(from_path=Path.home())],
}
