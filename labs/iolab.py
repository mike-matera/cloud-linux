"""
Input/Output Processing
"""

import os
import random
import subprocess 

from cloud_linux.lab import LinuxLab, ask as input
from cloud_linux.labs.files import randpath, random_big_file
from cloud_linux.secrets import vault

debug = False 
vault.setkey("blarny234")
vault.setfile(f'{os.environ["HOME"]}/.iolab')
test = LinuxLab(debug=debug)

@test.question
def find_top_line(line):
    """
    I have just (re)created a file called "bigfile" in your home directory. 

    What is the first word on line number {line:,}?
    """
    bf = random_big_file()
    with open(bf) as fh:
        for _ in range(1, line+1):
            exp = fh.readline()
    exp = exp.split()[0].casefold()
    if debug:
        print("DEBUG:", exp)
    got = input().strip().casefold()
    assert got == exp, """That's not correct."""


@test.question
def find_bottom_line(line):
    """
    I have just (re)created a file called "bigfile" your home directory. 

    What is the first word on the {line:,}th line from the *bottom*
    of the file (where the last line is the first from the bottom)?
    """
    lines = 100000
    bf = random_big_file(shape=(lines, 12))
    line = lines - line + 1
    with open(bf) as fh:
        for _ in range(1, line + 1):
            exp = fh.readline()
    exp = exp.split()[0].casefold()
    if debug:
        print("DEBUG:", exp)
    got = input().strip().casefold()
    assert got == exp, """That's not correct."""


@test.question
def find_long_line(line, word):
    """
    I have just (re)created a file called "bigfile" your home directory. 

    What is the {word:,}th word on the {line:,}th line from the *bottom*
    of the file (where the last line is the first from the bottom)?
    """
    lines = 10000
    words = 300
    bf = random_big_file(shape=(lines, words))
    line = lines - line + 1
    with open(bf) as fh:
        for _ in range(1, line + 1):
            exp = fh.readline()
    exp = exp.split()[word-1].casefold()
    if debug:
        print("DEBUG:", exp)
    got = input().strip().casefold()
    assert got == exp, """That's not correct."""


@test.question
def find_love():
    """
    I have just (re)created a file called "bigfile" in your home directory. 

    What is the first word on the first line that contains the word "love"? 
    Note: "love" should be lower case and can be a part of a word (e.g. "glove")
    """    
    bf = random_big_file()
    lines = subprocess.run(f'grep love {bf}', shell=True, 
        stdout=subprocess.PIPE).stdout.decode('utf-8')
    exp = lines.split()[0].casefold()
    if debug:
        print("DEBUG:", exp)
    got = input().strip().casefold()
    assert got == exp, """That's not correct."""


@test.question
def count_oranges():
    """
    I have just (re)created a file called "bigfile" in yor home directory. 

    What how many lines contain the word "orange" or "Orange" where "orange" 
    is not a part of another word (i.e. "oranges" and "orangeade" do not count)?

    Hint: Look in the manual for grep.
    
    """    
    bf = random_big_file()
    exp = int(subprocess.run(f'grep -i -w "orange" {bf} | wc -l', shell=True, 
        stdout=subprocess.PIPE).stdout.decode('utf-8'))
    if debug:
        print("DEBUG:", exp)
    got = int(input())
    assert got == exp, """That's not correct."""


@test.question
def sort_file():
    """
    I have just (re)created a file called "bigfile" in your home directory. 

    If the file is sorted in alphabetical order what would be the first word? 
    """    
    bf = random_big_file(shape=(1000,1))
    exp = subprocess.run(f'sort {bf} | head -n 1', shell=True, 
        stdout=subprocess.PIPE).stdout.decode('utf-8').strip().casefold()
    if debug:
        print("DEBUG:", exp)
    got = input().strip().casefold()
    assert got == exp, """That's not correct."""


@test.question
def unique_words():
    """
    I have just (re)created a file called "bigfile" in your home directory. 

    How many unique words are in bigfile? 
    """    
    bf = random_big_file(shape=(2000,1))
    exp = int(subprocess.run(f'sort {bf} | uniq | wc -l', shell=True, 
        stdout=subprocess.PIPE).stdout.decode('utf-8'))
    if debug:
        print("DEBUG:", exp)
    got = int(input())
    assert got == exp, """That's not correct."""


def main():
    find_top_line(points=3, line=random.randrange(10000,90000))
    find_bottom_line(points=3, line=random.randrange(10000,90000))
    find_long_line(points=3, word=random.randrange(100,200), line=random.randrange(1000,9000))
    find_love(points=3)
    count_oranges(points=3)
    sort_file(points=3)
    unique_words(points=2)

    print(f"Your score is {test.score} of {test.total}")
    print("Your confirmation code is:", vault.confirmation({'score': test.score}))


if __name__ == '__main__' :
    main()
