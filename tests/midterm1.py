import platform
import subprocess
import psutil 
import os
import stat
import pathlib
import datetime 
import random 
from re import sub
import atexit 

from lifealgorithmic.secrets import vault
from lifealgorithmic.linux.test import test, ask as input
from lifealgorithmic.linux.files import randpath, make_flag, random_big_file

vault.setkey("blarny234")
vault.setfile(f'{os.environ["HOME"]}/.midterm1')

debug = False

@test.question
def find_day(year):
    """
    What day of the week is December 1st, {year}?

    """
    exp = datetime.date(year,12,1).strftime('%A').lower()
    if debug:
        print('DEBUG:', exp)
    got = input().strip().lower()
    assert got == exp, """That's not what I expected."""


@test.question
def distro():
    """
    What is the version of the Linux distribution on this VM? 

    """
    osname = subprocess.run(". /etc/os-release && echo $VERSION", shell=True, stdout=subprocess.PIPE) \
            .stdout.decode('utf-8').strip().lower()
    if debug:
        print('DEBUG:', osname)
    got = input().strip().lower()
    assert got.startswith(osname.split()[0]), f"That's not correct."


@test.question
def free_mem():
    """
    What is the amount of free memory on this VM (in KB)?
    """
    exp = round(psutil.virtual_memory().free // 1024, -6) 
    if debug:
        print('DEBUG:', exp)
    assert round(int(input()), -6) == exp, """Remember the command that shows memory."""


@test.question
def file_type(file):
    """
    What is the type of the file below? 

        {file}

    """
    exp = 'elf'
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
def first_word():
    """
    I just (re)created a file called "bigfile" in the current directory. What is the first word in it? 
    """
    bigfile = random_big_file()
    with open(bigfile) as fh:
        first_word = fh.readline().split()[0].casefold()
    if debug:
        print("DEBUG:", first_word)
    got = input().strip().casefold()
    assert got == first_word, """That's not correct.""" 


@test.question
def bigfile_size():
    """
    I just (re)created a file called "bigfile" in the current directory. What is its size in bytes? 
    """
    bigfile = random_big_file()
    exp = os.stat(bigfile).st_size
    if debug:
        print("DEBUG:", exp)
    got = int(input())
    assert got == exp, """That's not correct.""" 


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

    
@test.question
def make_link():
    """
    In your home directory make a symbolic link named "myself" that points to /proc/self

    """
    link = pathlib.Path(os.environ.get("HOME")) / 'myself'
    target = pathlib.Path('/proc/self')
    assert link.is_symlink(), """A link named "myself" doesn't exist in your home directory."""
    assert target.resolve() == link.resolve(), """The link isn't pointing to the right place."""
    

def update_code():
    print("Your confirmation code is:", vault.confirmation({'score': test.score}))

def main():

    print("""

** Welcome to Midterm #1 for Spring 2022 **

When you start the test on Canvas you'll get a secret code. 
To begin the test enter the code below:

    """)
    code = input("secret code: ")
    if code.lower() != "lefty2022":
        print("That is not the correct code.")
        exit()

    def exit_hook():
        print("\n\nYou finished the test. You can restart it any time.")
        print(f"Your score is {test.score} of {test.total}")
        print("Your confirmation code is:", vault.confirmation({'score': test.score}))
    atexit.register(exit_hook)

    find_day(points=10, year=2022+random.randint(100,200))
    update_code()

    distro(points=10)
    update_code()
    
    free_mem(points=10)
    update_code()
    
    file_type(points=10, file=pathlib.Path('/bin/cat'))
    update_code()
    
    relative_path2(points=10, dir1=randpath.random_dir(), dir2=randpath.random_dir())
    update_code()
    
    resolve_link(points=10, link=randpath.find(lambda x: x.is_symlink()))
    update_code()
    
    first_word(points=10)
    update_code()
    
    bigfile_size(points=10)
    update_code()
    
    link_type(points=10, link=randpath.find(lambda x: x.is_symlink() and not pathlib.Path(os.readlink(x)).is_absolute()))
    update_code()
    
    make_link(points=10)
    

if __name__ == '__main__':
    main()

