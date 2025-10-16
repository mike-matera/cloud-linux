"""
# Lesson 10: Processes

After this lesson you should be able to:

- Run a process in the background
- Send signals

Reading:

- Chapter 10
"""

import multiprocessing
import os
import time
from enum import Enum
from random import shuffle

import psutil
from textual.validation import Integer

from kroz.flow.base import KrozFlowABC
from kroz.flow.interaction import Interaction
from kroz.flow.question import (
    MultipleChoiceQuestion,
    Question,
    ShortAnswerQuestion,
    TrueOrFalseQuestion,
)
from kroz.random import randint

title = "Working with Processes"

state = "process"


class ThisProcess(Question):
    text = """
    # What is My PID? 

    What is the Process ID (PID) of this program? 

    *Hint: This program contains "cis90" on the command line.*
    """

    validators = Integer()

    def check(self, answer: str) -> None:
        assert os.getpid() == int(answer), """
        That's not correct. 
        
        Here are a few tips: 

        * Try making a pipeline with `ps` and `grep` to make it easier to find
          this process. 
        * Other people may also be doing this lab. Make sure the process you
          find belongs to you. 
        """


class ThisParent(Question):
    text = """
    # What is My PPID? 

    What is the **Parent** Process ID (PPID) of this program? 
    """

    validators = Integer()

    def check(self, answer: str) -> None:
        ps = psutil.Process(pid=os.getpid())
        assert ps.ppid() == int(answer), """
        That's not correct. 
        
        Here are a few tips: 

        * The PPID is listed on the same line as the PID in the output of `ps`. 
        * Try making a pipeline with `ps` and `grep` to make it easier to find
          this process. 
        * Other people may also be doing this lab. Make sure the process you
          find belongs to you. 
        """


class ThisGrandparent(Question):
    text = """
    # What is My Grandparent? 

    What is the **Granparent** (The PPID of the PPID) Process ID of this
    program? 
    """

    validators = Integer()

    def check(self, answer: str) -> None:
        ps = psutil.Process(pid=os.getpid())
        parent = ps.parent()
        if parent is None:
            raise RuntimeError("There was an internal error.")
        assert parent.ppid() == int(answer), """ 
        That's not correct.         
        """


class TopBackground(Question):
    text = """
    # Stop Top 

    In a separate terminal start the `top` command and then put it in the
    background. 
    
    **Press Enter to continue.**
    """

    placeholder = "Press Enter"

    def check(self, answer):
        for ps in psutil.process_iter():
            if ps.uids()[0] == os.getresuid()[0] and ps.name() == "top":
                assert ps.status() == "stopped", (
                    """The top program is not in the background."""
                )
                return
        assert False, """I couldn't find the top program."""


class ChildFind(Question):
    class ResourceType(Enum):
        COUNT = ("", "Enter the number of child processes I have created.")
        MEMORY = (
            "mem",
            "Enter the `PID` of the child process that's using the most **memory**.",
        )
        CPU = (
            "cpu",
            "Enter the `PID` of the child process that's using the most **CPU**. ",
        )
        NICE = (
            "nice",
            "Enter the `PID` of the child process that's the **nicest**.",
        )

    @property
    def text(self) -> str:
        return f"""
            # Find a Child Process 

            I have just launched a random number of child processes.
            {self.type.value[1]}
            """

    validators = Integer()

    def __init__(self, type: ResourceType, **kwargs):
        self.type = type
        self.workers = randint(5, 10)
        super().__init__(**kwargs)

    def worker(self, barrier, memory: int, cpu: float, nice: int):
        barrier.wait()  # Wait for all the workers to start
        dummy_mem = " " * 1024 * 1024 * memory  # noqa: F841
        os.nice(nice)
        while True:
            if cpu > 0:
                now = time.monotonic()
                while time.monotonic() < (now + cpu):
                    pass  # Busy wait.
                time.sleep(1 - cpu)
            else:
                time.sleep(10)

    def setup(self) -> None:
        barrier = multiprocessing.Barrier(self.workers + 4)
        processes = [
            multiprocessing.Process(
                target=self.worker,
                name=ChildFind.ResourceType.CPU.value[0],
                args=(barrier, 0, 0.25, 0),
            ),
            multiprocessing.Process(
                target=self.worker,
                name=ChildFind.ResourceType.MEMORY.value[0],
                args=(barrier, 200, 0, 0),
            ),
            multiprocessing.Process(
                target=self.worker,
                name=ChildFind.ResourceType.NICE.value[0],
                args=(barrier, 0, 0, 19),
            ),
        ] + [
            multiprocessing.Process(
                target=self.worker, name="dummy", args=(barrier, 0, 0, 0)
            )
            for _ in range(self.workers)
        ]
        shuffle(processes)
        for p in processes:
            p.start()
        barrier.wait()

    def cleanup(self):
        for p in multiprocessing.active_children():
            p.kill()
            p.join()

    def _find(self, answer):
        for p in multiprocessing.active_children():
            if p.pid == int(answer) and p.name == self.type.value[0]:
                return
        assert False, "That's not the correct PID."

    def check(self, answer):
        if self.type == ChildFind.ResourceType.COUNT:
            assert int(answer) == len(multiprocessing.active_children()), (
                """That's not the correct number of children."""
            )
        elif self.type == ChildFind.ResourceType.MEMORY:
            self._find(answer)
        elif self.type == ChildFind.ResourceType.CPU:
            self._find(answer)
        elif self.type == ChildFind.ResourceType.NICE:
            self._find(answer)


walks: dict[str, list[KrozFlowABC]] = {
    "Processes in the current session": [
        Interaction(
            """
# Long Running Programs

Most of the commands we use in the class exit right after they perform their 
task. When they exit the prompt returns. Some programs run until you stop them.
For example, the `ping` command runs until you stop it with `Ctrl-c`. Start the
`ping` command. 

```console
$ ping opus.cis.cabrillo.edu 
```

After a few *pongs* exit ping with `Ctrl-c`. 
""",
            lambda cmd: cmd.command == "ping" and cmd.result == 0,
        ),
        Interaction(
            """
# Putting a Process in the Background 

You can pause `ping` instead of killing it using the `Ctrl-z` key. This time 
start ping and put it into the background:

```console
$ ping opus.cis.cabrillo.edu 
```

After a few *pongs* put `ping` in background with `Ctrl-z`. 
""",
            lambda cmd: cmd.command == "ping" and cmd.result == 148,
        ),
        Interaction(
            """
A process can be brought back to the foreground with `fg`:

```console
$ fg 
```

After a few more *pongs* put ping back into the background with `Ctrl-z`. 
""",
            lambda cmd: cmd.command == "fg" and cmd.result == 148,
        ),
        Interaction(
            """
# Running in the Background 

A program can run when it's in the background. To let `ping` run again while 
still being able to enter a command run `bg`:

```console
$ bg 
```
""",
            lambda cmd: cmd.command == "bg" and cmd.result == 0,
        ),
        Interaction(
            """
# Wait? What!? 

Ping is running **and** you have a prompt. Pres `Enter` a few times to look for 
the prompt. Try running the `ls` command:

```console
$ ls
```
""",
            lambda cmd: cmd.command == "ls",
        ),
        Interaction(
            """
# Let's Fix This 

You can kill `ping` by bringing it into the foreground and then stopping it with
`Ctrl-c`. 

```console
$ fg
```
""",
            lambda cmd: cmd.command == "fg",
        ),
    ],
    "Using `jobs` and `killall`": [
        Interaction(
            """
# Start Background Jobs 

The `sleep` program takes one argument, a number of seconds to wait. The `sleep`
program exits once it's done waiting. Let's use it to launch some jobs in the 
background:

```console
$ sleep 500 & 
```

**Run it five times!**
""",
            [
                lambda cmd: cmd.command == "sleep"
                and cmd.args == ["500"]
                and cmd.result == 0
            ]
            * 5,
        ),
        Interaction(
            """
Use the `jobs` command to see background jobs in your shell:

```console
$ jobs
[1]   Running                 sleep 500 &
[2]   Running                 sleep 500 &
[3]   Running                 sleep 500 &
[4]   Running                 sleep 500 &
[5]-  Running                 sleep 500 &
```

**You should see five copies as shown.**
""",
            lambda cmd: cmd.command == "jobs",
        ),
        Interaction(
            """
# The `kill` Command 

The `kill` command usually takes a process ID of a program. But when that
program is in the current shell you can use a shortcut. The `%5` argument says 
to kill job number 5:

```console
$ kill %5
```
""",
            lambda cmd: cmd.command == "kill" and cmd.args == ["%5"],
        ),
        Interaction(
            """
# The `killall` Command 

The `killall` command looks for all programs with a particular name and sends
them all a signal to cause them to exit. Use `killall` to kill the rest of the
`sleep` commands:

```console
$ killall sleep
```
""",
            lambda cmd: cmd.command == "killall" and cmd.args == ["sleep"],
        ),
    ],
    "Find this program": [
        Interaction(
            """
# Limits of `ps`

The `ps` program formats it's output to fit your screen. That makes it so that 
the full command line of a command usually gets cut off: 

```console
$ ps -elf 
```
""",
            lambda cmd: cmd.command == "ps" and cmd.args == ["-elf"],
        ),
        Interaction(
            """
You can see the full command lines by piping the output of `ps` through `less`:

```console
$ ps -elf | less
```
""",
            lambda cmd: cmd[0].command == "ps"
            and cmd[0].args == ["-elf"]
            and cmd[1].command == "less",
        ),
        Interaction(
            """
# Looking for a Particular Process?

You can use `grep` to find a process by it's name or a part of it's `ps` line:

```console
$ ps -elf | grep cis90 
```
""",
            lambda cmd: cmd[0].command == "ps"
            and cmd[0].args == ["-elf"]
            and cmd[1].command == "grep"
            and cmd[1].args[-1] == "cis90",
        ),
        Interaction(
            """
# You Can Filter Still...

You use another copy of `grep` to look for processes that you own:

```console
$ ps -elf | grep cis90 | grep $USER 
```
""",
            lambda cmd: cmd[0].command == "ps"
            and cmd[0].args == ["-elf"]
            and cmd[1].command == "grep"
            and cmd[1].args[-1] == "cis90"
            and cmd[2].command == "grep",
        ),
    ],
}

questions: list[KrozFlowABC] = [
    MultipleChoiceQuestion(
        "What is a characteristic of a *daemon program*?",
        "It waits in the background",
        "It's malicious",
        "It's started by a user",
        "It is part of the shell",
    ),
    TrueOrFalseQuestion("A program can have only one parent process.", True),
    TrueOrFalseQuestion("A program have any number of child processes.", True),
    MultipleChoiceQuestion(
        "What is the first program that's started by Linux?",
        "init",
        "start",
        "ProcessManager",
        "The shell",
    ),
    ShortAnswerQuestion(
        "What program interactively shows you all the processes running on the system?",
        "top",
    ),
    MultipleChoiceQuestion(
        "What is the alias for signal number 9?",
        "KILL",
        "INT",
        "STOP",
        "SEGV",
    ),
]

lab: dict[str, list[KrozFlowABC]] = {
    "Find the ID of this process.": [ThisProcess()],
    "Find my parent process ID": [ThisParent()],
    "Find my grandparent process ID": [ThisGrandparent()],
    "How many children?": [ChildFind(type=ChildFind.ResourceType.COUNT)],
    "Misbehaving child": [ChildFind(type=ChildFind.ResourceType.CPU)],
}
