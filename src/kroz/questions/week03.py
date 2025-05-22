"""
Questions for the third week of class.

Chapter 2 of the book.

"""

from enum import Enum
import grp
import os
from pathlib import Path
import pwd
import textwrap
from kroz.app import get_appconfig
import kroz.ascii
from kroz.question import (
    Question,
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
)
from textual.validation import Integer


questions = []


class FlagFile(Question):
    """Create a file and ask about its contents."""

    class FlagType(Enum):
        NAME = 1
        DIR = 2
        FULL = 3

    def __init__(self, type: FlagType):
        self._type = type

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
        self._secret = random_real_path().random_file().resolve()
        self._flag = Path(get_appconfig("default_path")) / "flag"
        with open(self._flag, "w") as fh:
            fh.write(self.flag())

    def cleanup(self):
        self._flag.unlink(missing_ok=True)

    @property
    def text(self):
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


class FileAttrs(Question):
    """Examine the attributes of an existing file."""

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

    def __init__(self, type: AttrType):
        self._type = type

    def setup(self):
        self._path = random_real_path().random_file().resolve()

    @property
    def placeholder(self):
        return self._type.value[0]

    @property
    def text(self):
        return f"""
        # File {self._type.value[0]}

        {self._type.value[1]} the file:

            {self._path}

        """

    @property
    def validators(self):
        return self._type.value[2]

    def check(self, answer):
        if self._type == FileAttrs.AttrType.SIZE:
            assert int(answer) == self._path.stat().st_size, (
                """That's not correct."""
            )
        elif self._type == FileAttrs.AttrType.INODE:
            assert int(answer) == self._path.stat().st_ino, (
                """That's not correct."""
            )
        elif self._type == FileAttrs.AttrType.OWNER:
            assert answer == pwd.getpwuid(self._path.stat().st_uid).pw_name, (
                """That's not correct."""
            )
        elif self._type == FileAttrs.AttrType.GROUP:
            assert answer == grp.getgrgid(self._path.stat().st_gid).gr_name, (
                """That's not correct."""
            )
        elif self._type == FileAttrs.AttrType.PERMS:
            assert (
                IsPermission.from_string(answer)
                == self._path.stat().st_mode & 0o777
            ), """That's not correct."""
        elif self._type == FileAttrs.AttrType.BLOCKS:
            assert int(answer) == self._path.stat().st_blocks, (
                """That's not correct."""
            )
        else:
            raise ValueError("Bad type")
