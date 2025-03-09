"""
File types and contents lab.
"""
import os
import stat
import pathlib
from random import random 

from cloud_linux.lab import LinuxLab, ask as input
from cloud_linux.labs.files import randpath, random_big_file
from cloud_linux.secrets import vault

debug = False 
vault.setkey("blarny234")
vault.setfile(f'{os.environ["HOME"]}/.fileslab')
test = LinuxLab(debug=debug)

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
    I just created a file called "~/bigfile" your home directory. 
    
    What is the first word in it? 
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
def relative_path(dir1, dir2):
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
    directory_inode(3, dir=randpath.random_dir())
    first_word(4)
    file_type(3, file=randpath.find(lambda x: x.suffix == '.gz' and not x.is_symlink()))
    relative_path(3, dir1=randpath.random_dir(), dir2=randpath.random_dir())
    resolve_link(4, link=randpath.find(lambda x: x.is_symlink()))
    link_type(3, link=randpath.find(lambda x: x.is_symlink()))

    print(f"Your score is {test.score} of {test.total}")
    print("Your confirmation code is:", vault.confirmation({'score': test.score}))


if __name__ == '__main__' :
    main()
