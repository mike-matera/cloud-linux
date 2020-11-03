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
from lifealgorithmic.linux.disks import VolumeGroup, PhysicalVolume, LogicalVolume, capture


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

def midterm_fa2020() :
    '''
** Welcome to the CIS-90 midterm for fall 2020 ** 

'''
    print(midterm_fa2020.__doc__)
    setup_files(start_files)
    test.run(debug=False)
    print("All done!\n\n")    

if __name__ == '__main__' :
    midterm_fa2020()



