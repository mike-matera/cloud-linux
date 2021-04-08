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

test = LinuxTest("Day after election day nerves and bummer.")

start_files = [    
    ['Hawaii', '644', 'Island in the Pacific ocean'],
    ['Samoa', '644', 'Island in the Pacific ocean'],
    ['Kiribati', '644', 'Island in the Pacific ocean'],
    ['Ireland', '644', 'Island in the Atlantic ocean'],
    ['Madeira', '644', 'Island in the Atlantic ocean'],
    ['Azores', '644', 'Island in the Atlantic ocean'],
    ['Langkawi', '644', 'Island in the Indian ocean'],
    ['Sabang', '644', 'Island in the Indian ocean'],
    ['Nublar', '644', 'Island in Fiction'],
    ['Hydra', '644', 'Island in Fiction'],
]

end_files = [
    ['Pacific/Hawaii',   '640', 'Island in the Pacific ocean'],
    ['Pacific/Samoa',    '640', 'Island in the Pacific ocean'],
    ['Pacific/Kiribati', '640', 'Island in the Pacific ocean'],
    ['Atlantic/Ireland', '600', 'Island in the Atlantic ocean'],
    ['Atlantic/Madeira', '600', 'Island in the Atlantic ocean'],
    ['Atlantic/Azores',  '600', 'Island in the Atlantic ocean'],
    ['Indian/Langkawi',  '400', 'Island in the Indian ocean'],
    ['Indian/Sabang',    '400', 'Island in the Indian ocean'],
    ['Fiction/Nublar',   '440', 'Island in Fiction'],
    ['Fiction/Hydra',    '440', 'Island in Fiction'],
]

def setup_files(files, startdir=pathlib.Path("Files")):
    subprocess.run(f"rm -rf {startdir}", shell=True)
    subprocess.run(f"mkdir {startdir}", shell=True)
    for path, mode, contents in files:
        with open(startdir / path, 'w') as fh:
            fh.write(contents)
        subprocess.run(f"chmod {mode} {startdir / path}", shell=True)


def check_files(files, startdir=pathlib.Path("Oceans")):
    for path, mode, contents in files:
        with open(startdir / path) as fh:
            assert contents == fh.read(), f"The contents of {path} don't match."
        stat = os.stat(startdir / path)
        rmode = oct(stat.st_mode & 0b111111111)[2:]
        assert mode == rmode, f"The permissions on {path} don't match."


@test.question2(20)
def make_files():
    """
    I have created a directory called "Files" in the current direcory. 
    Inside of "Files" you will see 10 files named after islands. Each island 
    file contains the name of the ocean it is in. Reorganize the files so 
    that they are in directories named after their oceans. The resulting 
    directory structure should be relative to the working directory of 
    the test (probably your home direcory) and look like this: 

    (wd)/
       Oceans/
         Atlantic/
         Pacific/
         ... 

    The "Oceans" directory should be in the current directory. Set the 
    permissions on the island files as described below:

      1. No islands should be readable, writable or executable by others
      2. Pacific islands should be r/w for the user and read only for the group
      3. Atlantic islands should r/w for the user an no group access 
      4. Indian islands should read only for the user and no group access
      5. Fictional islands should be read only for the user and group.

    """
    setup_files(start_files)
    input("Check for the files and press Enter.")


@test.question2(10)
def test_pacific():
    """I'm about to check the Pacific islands."""
    check_files(end_files[0:3])


@test.question2(10)
def test_atlantic():
    """I'm about to check the Atlantic islands."""
    check_files(end_files[3:6])


@test.question2(10)
def test_indian():
    """I'm about to check the Indian islands."""
    check_files(end_files[6:8])


@test.question2(10)
def test_fictional():
    """I'm about to check the Fictional islands."""
    check_files(end_files[8:])


@test.question2(10, interactive=True)
def deep_file():
    """
    I just created a directory called "deep" in the "Files" directory. Explore 
    it until you get to the deepest subdirectory in it. Inside the deepest 
    subdirectory you will find a secret file. What are the contents of the file? 
    """
    message = 'emacs'
    path = pathlib.Path("Files/deep/there's/a/light/over/at/the/Frankenstein/place")
    file = path / '.secret'
    subprocess.run(['mkdir', '-p', path])
    with open(file, 'w') as fh:
        fh.write(message + "\n")
    
    got = input("What's the secret message? ").strip()
    assert got == message, "That's not the message."


@test.question2(10, interactive=True)
def this_process():
    """
    What is the process ID of the midterm process?
    """
    got = input("Enter the PID? ") 
    assert int(got) == os.getpid(), """That's not correct."""


@test.question2(10, interactive=True)
def fork_kill():
    """
    When you hit Enter the test will launch a child process. Find the child 
    process and kill it with signal number 9. 
    """
    input("Hit enter to create the child process. ")
    pid = os.fork()
    if pid == 0:
        os.execlp('tail', 'tail', '-n', '0', '-f', '/etc/passwd')
        exit(0)
    else:
        print(f"Waiting for you to kill the child process.")
        ecode = os.waitpid(pid, 0)
        assert ecode[1] == 9, """The program wasn't killed with signal 9.""" 


@test.question2(10, interactive=True)
def count_files():
    """
    Count all of the regular files (not links or directories) under the /usr
    directory, including all of its subdirectories.  
    """
    got = int(input("How many files are there? "))
    find = subprocess.run('find /usr -type f | wc -l', encoding='utf-8', shell=True, stdout=subprocess.PIPE)
    files = int(find.stdout.strip())
    assert got == files, "That's not the right number of files."


def midterm_sp2021() :
    '''
    ** Welcome to the CIS-90 midterm for spring 2021 ** 
    '''

    print(midterm_sp2021.__doc__)
    test.run(debug=False)
    print("All done!\n\n")    


if __name__ == '__main__' :
    midterm_sp2021()
