"""
Will it work? 

1. Make a layout of files and folders from a source layout and perms. 
2. Find a file 
3. A simple pipeline 
4. Process control or use PS. 

"""

import os
import re
import tempfile
import subprocess
import pwd
import hmac
import crypt
import sys
import random
import datetime
import collections
import atexit
import pathlib 

from lifealgorithmic.linux.test import LinuxTest

test = LinuxTest("Ohhh my gooooshh asdfasdf")

start_files = [    
    ['cat', '644', 'felis sylvesteris (animal)'],
    ['dog', '644', 'xxx (animal)'],
    ['lizard', '644', 'xxx (animal)'],
    ['pitosporum', '644', 'xxx (plant)'],
]

end_files = [
    ['animals/cat', '644', 'felis sylvesteris (animal)'],
    ['animals/dog', '644', 'xxx (animal)'],
    ['animals/lizard', '644', 'xxx (animal)'],
    ['plants/pitosporum', '644', 'xxx (plant)'],
]


def setup_files(files, startdir=pathlib.Path("Organisms")):
    subprocess.run(f"rm -rf {startdir}", shell=True)
    subprocess.run(f"mkdir {startdir}", shell=True)
    for path, mode, contents in files:
        with open(startdir / path, 'w') as fh:
            fh.write(contents)
        subprocess.run(f"chmod {mode} {startdir / path}", shell=True)


def check_files(files, startdir=pathlib.Path("Output")):
    for path, mode, contents in files:
        with open(startdir / path) as fh:
            assert contents == fh.read(), f"The contents of {path} don't match."
        stat = os.stat(startdir / path)
        rmode = oct(stat.st_mode & 0b111111111)[2:]
        assert mode == rmode, f"The permissions on {path} don't match."


@test.question(20)
def files():
    """
    Create the following files:
    foo 
    bar 
    bak
    """
    check_files(end_files)


@test.question(10)
def deep_file():
    """
    I just created a directory called "deep" in your home directory. Explore it until
    you get to the deepest subdirectory in it. Inside the deepest subdirectory you will 
    find a secret file. What are the contents of the file? 
    """
    message = 'fliberdyjibit'
    path = pathlib.Path("deep/there's/a/light/over/at/the/Frankenstein/place")
    file = path / '.secret'
    subprocess.run(['mkdir', '-p', path])
    with open(file, 'w') as fh:
        fh.write(message)
    
    got = input("What's the secret message?")
    assert got == message, "That's not the message."


@test.question(10)
def this_process():
    """
    What is the process ID of this process?
    """
    got = input("Enter the PID? ") 
    assert int(got) == os.getpid(), """That's not correct."""


@test.question(10)
def fork_kill():
    """
    This program just started another process. Find the child process and kill it with signal 9. 
    """
    pid = os.fork()
    if pid == 0:
        os.execlp('tail', 'tail', '-n', '0', '-f', '/etc/passwd')
        exit(0)
    else:
        print(f"Waiting for you to kill the child process.")
        ecode = os.waitpid(pid, 0)
        assert ecode[1] == 9, """The program wasn't killed right.""" 


@test.question(10)
def count_files():
    """
    Count all of the file in the /usr directory. 
    """
    got = int(input("How many files are there? "))
    find = subprocess.run('find /usr | wc -l', encoding='utf-8', shell=True, stdout=subprocess.PIPE)
    files = int(find.stdout.strip())
    assert got == files, "That's not the right number of files."


def midterm_fa2020() :
    '''
    ** Welcome to the CIS-90 midterm for fall 2020 ** 
    '''

    print(midterm_fa2020.__doc__)
    setup_files(start_files)
    test.run(debug=False, only=["count_files"])
    print("All done!\n\n")    

# Mike Gleason

if __name__ == '__main__' :
    midterm_fa2020()
