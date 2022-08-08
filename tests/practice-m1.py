import platform
import subprocess
import psutil 
import os
import stat
import pathlib
from random import random 
from re import sub

from cloud_linux.secrets import vault
from cloud_linux.labs.test import test, ask as input
from cloud_linux.labs.files import randpath, make_flag, random_big_file

vault.setkey("blarny234")
#vault.setfile(f'{os.environ["HOME"]}/.bosslab')

debug = False

@test.question
def kernel_version():
    """
    What is the full version of the Linux kernel running on this VM? 
    """
    exp = platform.uname().release
    if debug:
        print('DEBUG:', exp)
    assert input().strip() == exp, """Look for a version number."""

@test.question
def total_mem():
    """
    What is the total amount of memory on this VM (in KB)?
    """
    exp = int(psutil.virtual_memory().total / 1024)
    if debug:
        print('DEBUG:', exp)
    assert int(input()) == exp, """Remember the command that shows memory."""

@test.question
def distro():
    """
    What is the NAME of the Linux distribution on this VM? 
    """
    osname = subprocess.run(". /etc/os-release && echo $NAME", shell=True, stdout=subprocess.PIPE) \
            .stdout.decode('utf-8').strip().lower()
    if debug:
        print('DEBUG:', osname)
    got = input().strip().lower()
    assert got == osname, f"Look inside a file in /etc"


@test.question
def flag_file():
    """
    I've (re)created a file in your home directory called "flag". 
    Inside the flag file there's the name of a secret file. 
    
    What's the secret file?
    """
    f = make_flag()
    if debug:
        print("DEBUG:", f['secret'])
    got = input().strip()
    assert got == f['secret'], """That's not correct."""


@test.question
def flag_path():
    """
    I've (re)created a file in your home directory called "flag". 
    Inside the flag file there's the name of a secret file. 

    What is the absolute path of the flag file?
    """
    f = make_flag()
    exp = pathlib.Path(f['path']).resolve()
    if debug:
        print("DEBUG:", exp)
    got = input().strip()
    assert got == str(exp), """That's not correct.""" 


@test.question
def file_size(file):
    """
    What is the size of the following file in bytes? 

      {file}

    """
    exp = file.stat().st_size
    if debug:
        print("DEBUG:", exp)
    got = int(input())
    assert got == exp, f"""That's not right.""" 


@test.question
def flag_inode():
    """
    I've (re)created a file in your home directory called "flag". 
    Inside the flag file there's the name of a secret file. 

    What is the inode number of the flag file?
    """
    f = make_flag()
    exp = os.stat(f['path'])[stat.ST_INO]
    if debug:
        print("DEBUG:", exp)
    got = int(input())
    assert got == exp, """That's not the correct number.""" 
    

@test.question
def directory_inode(dir):
    """
    What is the inode number of the directory below?

        {dir}

    """
    exp = os.stat(dir)[stat.ST_INO]
    if debug:
        print("DEBUG:", exp)
    got = int(input())
    assert got == exp, """That's not the correct number.""" 


@test.question
def first_word():
    """
    I just created a file called "bigfile" in the current directory. What is the first word in it? 
    """
    bigfile = random_big_file()
    with open(bigfile) as fh:
        first_word = fh.readline().split()[0].casefold()
    if debug:
        print("DEBUG:", first_word)
    got = input().strip().casefold()
    assert got == first_word, """That's not correct.""" 


@test.question
def file_type(file):
    """
    What is the type of the file below? 

        {file}

    """
    exp = 'gzip compressed data'
    if debug:
        print("DEBUG:", exp)
    got = input().strip().casefold()
    assert got.startswith(exp), """That's not correct.""" 


@test.question
def relative_path2(dir1, dir2):
    """
    What is the relative path between the following two directories?

      from: {dir1}
        to: {dir2}

    """
    got = input().strip()
    assert not got.startswith('cd'), """The answer should not start with "cd"."""

    got = pathlib.Path(got)
    assert not got.is_absolute(), """That's an absolute path."""

    rel = (dir1 / got).resolve()
    if debug:
        print("That makes:", rel)

    assert dir2.resolve() == rel, f"""That's not right.""" 


@test.question
def resolve_link(link):
    """
    The file below is a symbolic link. Where is the link pointing? 

        {link}

    """
    exp = pathlib.Path(os.readlink(link))
    if debug:
        print("DEBUG:", exp)
    got = input().strip()
    assert got == str(exp), """That's not correct."""


@test.question
def link_type(link):
    """
    The file below is a symbolic link. Is the link relative or absolute? 

        {link}

    """
    link = pathlib.Path(os.readlink(link))
    if debug:
        print("DEBUG:", link)
    got = input('Say "relative" or "absolute": ').strip()
    assert got == 'relative' or got == 'absolute', """I don't understand that."""
    assert got == 'absolute' and link.is_absolute() \
        or got == 'relative' and not link.is_absolute(), """That's not correct."""


def main():

    kernel_version(points=5)
    total_mem(points=5)
    distro(points=5)
    flag_file(points=5)
    flag_path(points=5)
    file_size(points=5, file=randpath.random_file())
    flag_inode(points=5)
    directory_inode(points=5, dir=randpath.random_dir())
    first_word(points=5)
    file_type(points=5, file=randpath.find(lambda x: x.suffix == '.gz' and not x.is_symlink()))
    relative_path2(points=5, dir1=randpath.random_dir(), dir2=randpath.random_dir())
    resolve_link(points=5, link=randpath.find(lambda x: x.is_symlink()))
    link_type(points=5, link=randpath.find(lambda x: x.is_symlink()))

    #print(f"Your score is {test.score} of {test.total}")
    #print("Your confirmation code is:", vault.confirmation({'score': test.score}))

    print("""
** Congratulations! **

You finished the practice test. It is not graded so you don't have to turn anything in.
    """)


if __name__ == '__main__':
    main()

