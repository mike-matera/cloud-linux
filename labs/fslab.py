"""
Filesystem lab
"""

import os
import stat
import pathlib 

from lifealgorithmic.secrets import vault
from lifealgorithmic.linux.test import test, ask as input
from lifealgorithmic.linux.files import randpath, make_flag

vault.setkey("blarny234")
vault.setfile(f'{os.environ["HOME"]}/.fslab')

debug = False

@test.question
def flag_file():
    """
    I've created a file in your home directory called "flag". 
    Inside the flag file there's the name of a secret file. 
    
    What's the secret file?
    """
    make_flag()
    if debug:
        print("DEBUG:", vault.get('flag.secret'))
    got = input().strip()
    assert got == vault.get('flag.secret'), """That's not correct."""


@test.question
def flag_path():
    """
    What is the absolute path of the flag file?
    """
    make_flag()
    exp = pathlib.Path(vault.get('flag.path')).resolve()
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
    What is the inode number of the flag file?
    """
    make_flag()
    exp = os.stat(vault.get('flag.path'))[stat.ST_INO]
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
