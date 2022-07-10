"""
Input/Output Processing
"""

import os
import psutil 

from lifealgorithmic.secrets import vault
from lifealgorithmic.linux.test import test, ask as input

vault.setkey("blarny234")
vault.setfile(f'{os.environ["HOME"]}/.processlab')

debug = False 

@test.question
def this_process():
    """
    What is the process ID of the "processlab" process?
    """
    if debug:
        print("DEBUG:", os.getpid())
    got = int(input()) 
    assert int(got) == int(os.getpid()), """That's not correct."""


@test.question
def my_grandparent():
    """
    What is the process ID of the parent of the parent (grandparent) of the "processlab" process?
    """
    procs = {p.pid: p.ppid() for p in psutil.process_iter(['ppid'])}
    exp = procs[procs[os.getpid()]]
    if debug:
        print("DEBUG:", exp)
    got = int(input()) 
    assert int(got) == exp, """That's not correct."""


@test.question
def fork_kill():
    """
    I just created a child process. Find it and stop it by sending a signal 9. 
    """
    pid = os.fork()
    if pid == 0:
        os.execlp('tail', 'tail', '-n', '0', '-f', '/etc/passwd')
    else:
        input("Press Enter after stopping the process: ")
        child, ecode = os.waitpid(pid, os.WNOHANG)
        assert ecode == 9, """The program wasn't killed with signal 9.""" 


@test.question
def top_background():
    """
    Start the "top" command in a separate shell and put it into the background. 
    """
    input("Press Enter when you're ready: ")
    for ps in psutil.process_iter():
        if ps.uids()[0] == os.getresuid()[0] and ps.name() == 'top':
            if debug:
                print("DEBUG:", ps)
            assert ps.status() == 'stopped', """The top program is not in the background."""
            return
    assert False, """I couldn't find the top program."""


@test.question
def top_stop():
    """
    Stop the "top" program that you started in the previous question.
    """
    input("Press Enter when you're ready: ")
    for ps in psutil.process_iter():
        if ps.uids()[0] == os.getresuid()[0] and ps.name() == 'top':
            assert False, """I found top still running."""


@test.question
def longest_process():
    """
    What is the PID of the process that has the longest accumulated run time? 
    """
    procs = sorted((p for p in psutil.process_iter(['cpu_times'])), 
        key = lambda proc: proc.cpu_times()[0] + proc.cpu_times()[1])

    exp = list(procs)[-1]
    if debug: 
        print("DEBUG:", exp)

    got = int(input()) 
    assert got == exp.pid, """That's not correct."""


def main():
    this_process(points=4)
    my_grandparent(points=4)
    fork_kill(points=4)
    top_background(points=4)
    top_stop(points=4)

    print(f"Your score is {test.score} of {test.total}")
    print("Your confirmation code is:", vault.confirmation({'score': test.score}))


if __name__ == '__main__' :
    main()
