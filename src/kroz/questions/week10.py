"""
Questions about Processes
"""

import multiprocessing
import os
import time
from enum import Enum
from random import shuffle

import psutil
from textual.validation import Integer

from kroz.flow.question import (
    Question,
)
from kroz.random import randint


class ThisProcess(Question):
    text = """
    # What is My PID? 

    What is the Process ID (PID) of this program? 

    TODO: Tell students the name to look for.
    """

    validators = Integer()

    def check(self, answer: str) -> None:
        assert os.getpid() == int(answer), """
        That's not correct. 
        
        Here are a few tips: 

        * Try making a pipeline with `ps` and `grep` to make it easier to find this process. 
        * Other people may also be doing this lab. Make sure the process you find belongs to you. 
        """


class ThisParent(Question):
    text = """
    # What is My PPID? 

    What is the **Parent** Process ID (PPID) of this program? 

    TODO: Tell students the name to look for.
    """

    validators = Integer()

    def check(self, answer: str) -> None:
        ps = psutil.Process(pid=os.getpid())
        assert ps.ppid() == int(answer), """
        That's not correct. 
        
        Here are a few tips: 

        * The PPID is listed on the same line as the PID in the output of `ps`. 
        * Try making a pipeline with `ps` and `grep` to make it easier to find this process. 
        * Other people may also be doing this lab. Make sure the process you find belongs to you. 
        """


class ThisGrandparent(Question):
    text = """
    # What is My Grandparent? 

    What is the **Granparent** (The PPID of the PPID) Process ID of this program? 

    TODO: Tell students the name to look for.
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
    background. **Press Enter to continue.**
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
