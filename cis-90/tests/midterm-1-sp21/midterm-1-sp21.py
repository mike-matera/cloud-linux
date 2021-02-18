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
import json 
import nacl.secret
import nacl.pwhash
import getpass
import json 

from lifealgorithmic.linux.test import LinuxTest

secret = "flibbertyjibbit"
test = LinuxTest(secret)

docs = list(pathlib.Path('/usr/share/doc').glob('**/*'))

def random_file():
    global docs 
    while True:
        c = random.choice(docs)
        if c.is_file() and not c.is_symlink():
            return c 

def random_dir():
    global docs 
    while True:
        c = random.choice(docs)
        if c.is_dir() and not c.is_symlink():
            return c 

@test.question(10, file=random_file())
def file_size(file):
    """
    What is the size of the following file in bytes? 

      {file}

    """
    if test.config.get(file_size.__name__) is not None:
        return

    got = int(input("Enter the size: "))
    exp = file.stat().st_size
    assert got == exp, f"""That's not right.""" 

    test.config[file_size.__name__] = 1 

@test.question(10, dir1=pathlib.Path(os.getcwd()), dir2=random_dir())
def relative_path(dir1, dir2):
    """
    What is the relative path between the following two directories?

      from: {dir1}
        to: {dir2}
        
    """
    if test.config.get(relative_path.__name__) is not None:
        return

    got = pathlib.Path(input("Enter the path: "))
    rel = (dir1 / got).resolve()
    if test.debug:
        print("That makes:", rel)

    assert dir2 == rel, f"""That's not right.""" 

    test.config[relative_path.__name__] = 1 

def midterm_sp2021() :
    '''
    ** Welcome to the fist CIS-90 midterm for spring 2021 ** 
    '''

    print(midterm_sp2021.__doc__)
    test.run(debug=True)
    print("All done!\n\n")    


if __name__ == '__main__' :
    midterm_sp2021()
