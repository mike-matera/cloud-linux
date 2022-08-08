"""
Filesystem lab
"""

import os
import stat
import pathlib 

from cloud_linux.secrets import vault
from cloud_linux.labs.test import test, ask as input
from cloud_linux.labs.files import randpath, make_flag

vault.setkey("blarny234")
vault.setfile(f'{os.environ["HOME"]}/.fslab')

debug = False

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
    

def main():
    flag_file(points=4)
    flag_path(points=4)
    file_size(points=4, file=randpath.random_file())
    relative_path(points=4, dir1=pathlib.Path(os.getcwd()), dir2=randpath.random_dir())
    flag_inode(points=4)

    print(f"Your score is {test.score} of {test.total}")
    print("Your confirmation code is:", vault.confirmation({'score': test.score}))


if __name__ == '__main__' :
    main()
