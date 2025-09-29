"""
# Lesson 2: The Command Line

After this lesson you should be able to:

- Describe the anatomy of a command
- Use the keyboard to navigate the command line
- The terminal and the shell

Reading:

- Chapter 1
"""

import datetime
import random
import re
from enum import Enum

import textual.validation

from kroz.flow.base import KrozFlowABC
from kroz.flow.interaction import Interaction
from kroz.flow.question import (
    MultipleChoiceQuestion,
    Question,
    ShortAnswerQuestion,
    TrueOrFalseQuestion,
)

title = "Anatomy of a Command"

state = "anatomy"


class FreeMemory(Question):
    """Use the `free` command."""

    def __init__(self, key: str, **kwargs):
        """Key should correspond exactly to a column from `free`"""
        super().__init__(**kwargs)
        self.get_key(key)  # Validate
        self._key = key

    validators = textual.validation.Integer()
    placeholder = "Enter a number in bytes"

    @property
    def text(self):
        return f"""
            # System Memory 
            
            What is the amount of **{self._key}** memory on this system?"""

    def check(self, answer):
        answer = int(answer)
        solution = self.get_key(self._key)
        assert abs(solution - answer) < (solution * 0.1), """
            That's not the correct answer. 
            
            *It's possible that memory values change rapidly. Please check your 
            work and try again.*
            """

    @staticmethod
    def get_key(key):
        """Get a value based on the column key header"""
        data = Question.shell("free").split("\n")
        cols = data[0].split()
        mem = data[1].split()
        assert key in cols, """Invalid key for free"""
        return int(mem[cols.index(key) + 1])


class NewYearFuture(Question):
    """Use the `cal` program."""

    DAYS = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    placeholder = "Enter a day of the week"
    validators = textual.validation.Regex(
        f"({'|'.join(DAYS)})",
        re.I,
        failure_description="""Enter the full name of a day (e.g. "Sunday")""",
    )

    def __init__(self, *, year: int | None = None, **kwargs):
        super().__init__(**kwargs)
        if year is not None:
            self._year = year
        else:
            self._year = random.randint(2040, 2150)
        self._solution = NewYearFuture.DAYS[
            datetime.date(self._year, 1, 1).isoweekday() - 1
        ]

    @property
    def text(self):
        return f"""
        # Future New Year
        
        On what day of the week does new year's **day** fall on in the
        year {self._year}?"""

    def check(self, answer):
        assert self._solution.lower() == answer.strip().lower(), """
            That is not correct. Check the notes for a command that shows
            you a calendar. Using arguments you can have it show you any year
            and month.
            """


class WhatsUname(Question):
    """Test using the uname command."""

    class Keys(Enum):
        ALL = ("-a", "all information about the machine")
        KERNEL_NAME = ("-s", "the kernel name")
        NODENAME = ("-n", "the network node hostname")
        KERNEL_RELEASE = ("-r", "the kernel release")
        KERNEL_VERSION = ("-v", "the kernel version")
        MACHINE = ("-m", "the machine hardware name")
        PROCESSOR = ("-p", "the processor type")
        HARDWARE_PLATFORM = ("-i", "the hardware platform")
        OPERATING_SYSTEM = ("-o", "the operating system")

    def __init__(self, key: Keys, **kwargs):
        super().__init__(**kwargs)
        assert isinstance(key, WhatsUname.Keys), """Bad key"""
        self._key = key.value
        self._solution = self.shell(f"uname {self._key[0]}").strip()
        assert self._solution != "", """That is a bad key."""

    @property
    def text(self):
        return f"""
        # System Information 

        Use a command from this week to show you {self._key[1]}. Enter the 
        result of running the command in the box.
        """

    def check(self, answer):
        assert answer.strip() == self._solution, """
        That's not correct. If you're stuck, look at the commands from this week 
        and ask each of them for help by using the `-h` or `--help` argument. 
        This question asks you for specific information that you can find in the 
        command help for one of this week's commands. 
        """


class OsRelease(Question):
    """Ask about the /etc/os-release file."""

    def __init__(self, key, **kwargs):
        super().__init__(**kwargs)
        with open("/etc/os-release") as fh:
            self._keys = {
                parts[0]: parts[1].replace('"', "").strip()
                for parts in (line.split("=") for line in fh)
            }
        assert key in self._keys, """Bad key"""
        self._key = key
        self._solution = self._keys[self._key]

    @property
    def text(self):
        return f"""
        # Operating System Information 

        Use a command to show you the "{self._key}" of the Linux operating 
        system. Enter it in the box below. 
        """

    def check(self, answer):
        assert self._solution == answer.replace('"', "").strip(), """
            That's not correct. The command that shows you operating system
            information also shows a lot of other information. Make sure you find
            the exact information that I asked for. 
            """


walks: dict[str, list[KrozFlowABC]] = {
    "First Commands": [
        Interaction(
            """ 
    Commands are words separated by spaces. The first word is the name of the
    command. Subsequent words are called arguments. A special kind of argument
    called a switch or flag begins with the dash (-) character.

    Try running this command in a separate shell:

    ```console 
    $ cal
    ```
    """,
            lambda cmd: cmd.command == "cal",
        ),
        Interaction(
            """ 
    The cal command shows a calendar of the current month. Many UNIX commands take
    the -h or --help switch as an argument. See what happens to the date command
    when you add the -h option.

    Try running this command in a separate shell:

    ```console 
    $ cal -h
    ```
    """,
            lambda cmd: cmd.command == "cal" and ["-h"] == cmd.args,
        ),
        Interaction(
            """ 
    The cal command will show you any month or year you like. With one argument, a
    year, cal prints every month in that year. With two arguments it prints just the
    month that you asked for

    ```console 
    $ cal 1980
    ```

    ```console 
    $ cal december 1980
    $ cal 12 1980
    ```

    Run the command above but substitute the year and month you were born. **What
    day of the week were you born on?**

    """,
            lambda cmd: cmd.command == "cal"
            and 1925 < int(cmd.args[1]) < 2025,
        ),
        Interaction(
            """ 
    There are many commands that show you information about the computer the shell
    is running on. The `df` command displays information about disks. When you give
    it the `~` argument it shows how much space is available in your home directory.
    Try it to see how much is left.

    ```console 
    $ df ~
    Filesystem              1K-blocks       Used Available Use% Mounted on
    /dev/mapper/crypthome2 1920748800 1025448568 797657788  57% /home
    ```

    The output of `df` is a table. Compare the output of my computer to the one your
    shell is on.
    """,
            lambda cmd: cmd.command == "df" and ["~"] == cmd.args,
        ),
        Interaction(
            """ 
    The `free` command displays information about RAM.

    ```console 
    $ free
                total        used        free      shared  buff/cache   available
    Mem:       130992164    16494376    18840136      340348    97244672   114497788
    Swap:        8388604      581152     7807452
    ```

    The output of `free` is a table. Compare the output of my computer to the one
    your shell is on.
    """,
            lambda cmd: cmd.command == "free" and [] == cmd.args,
        ),
        Interaction(
            """ 
    Sometimes programs run until you ask them to exit. The `free` command can 
    monitor your computer by printing updated statistics periodically. Try running 
    `free` like below. Notice that the prompt doesn't come back.

    ```console 
    $ free -s 1 -L 
    ```

    **Press Ctrl+C to exit the program and return to the prompt.**
    """,
            lambda cmd: cmd.command == "free" and cmd.result != 0,
        ),
    ]
}

questions: list[KrozFlowABC] = [
    TrueOrFalseQuestion(
        "The terminal and the shell are the same thing.",
        False,
    ),
    MultipleChoiceQuestion(
        "A **terminal** is...",
        "Both a program and a machine with a screen and a keyboard",
        "A program",
        "A machine with a screen and a keyboard",
        "Responsible for running commands",
    ),
    MultipleChoiceQuestion(
        """What keys access your command history?""",
        "The up and down arrows",
        "The Page Up and Page Down keys",
        "The right and left arrows",
        "The scroll wheel on the mouse",
    ),
    MultipleChoiceQuestion(
        """When we talk about the command line we're really referring to...""",
        "The shell",
        "The terminal",
        "Linux",
        "Any operating system",
    ),
    MultipleChoiceQuestion(
        """What is the name of your shell on Opus?""",
        "bash",
        "zsh",
        "wish",
        "fish",
    ),
    MultipleChoiceQuestion(
        """What program connects your computer to Opus?""",
        "ssh",
        "bash",
        "date",
        "cal",
    ),
    ShortAnswerQuestion(
        """What command shows you a calendar?""",
        "cal",
    ),
    ShortAnswerQuestion(
        """What command shows you information about the RAM memory on Opus?""",
        "free",
    ),
    ShortAnswerQuestion(
        """What command shows you information about the disks on Opus?""",
        "df",
    ),
    ShortAnswerQuestion(
        """What command exits the shell?""",
        "exit",
    ),
    ShortAnswerQuestion(
        """What command shows information about the system?""",
        "uname",
    ),
    ShortAnswerQuestion(
        """What command prints information about the version of Linux on Opus?""",
        "cat /etc/os-release",
    ),
    TrueOrFalseQuestion(
        """Commands give you help when you give them the `-h` or `--help` flag.""",
        True,
    ),
]

lab: dict[str, list[KrozFlowABC]] = {
    "Free Memory": [FreeMemory(key="total")],
    "Kernel Version": [WhatsUname(key=WhatsUname.Keys.KERNEL_VERSION)],
    "OS Name": [OsRelease(key="NAME")],
    "New Years Future": [NewYearFuture()],
}
