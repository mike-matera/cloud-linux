"""
Files and directories.
"""

import os
import stat
import pathlib
from random import random 

from cloud_linux.lab import LinuxLab, ask as input
from cloud_linux.labs.files import setup_files, check_files
from cloud_linux.secrets import vault

debug = False 
vault.setkey("blarny234")
vault.setfile(f'{os.environ["HOME"]}/.islands')
test = LinuxLab(debug=debug)

start_files = [    
    ['Hawaii',   None, None, 'Island in the Pacific ocean'],
    ['Samoa',    None, None, 'Island in the Pacific ocean'],
    ['Kiribati', None, None, 'Island in the Pacific ocean'],
    ['Ireland',  None, None, 'Island in the Atlantic ocean'],
    ['Madeira',  None, None, 'Island in the Atlantic ocean'],
    ['Azores',   None, None, 'Island in the Atlantic ocean'],
    ['Langkawi', None, None, 'Island in the Indian ocean'],
    ['Sabang',   None, None, 'Island in the Indian ocean'],
    ['Nublar',   None, None, 'Island in Fiction'],
    ['Hydra',    None, None, 'Island in Fiction'],
]

end_files = [
    ['Pacific/Hawaii',   None, None, 'Island in the Pacific ocean'],
    ['Pacific/Samoa',    None, None, 'Island in the Pacific ocean'],
    ['Pacific/Kiribati', None, None, 'Island in the Pacific ocean'],
    ['Atlantic/Ireland', None, None, 'Island in the Atlantic ocean'],
    ['Atlantic/Madeira', None, None, 'Island in the Atlantic ocean'],
    ['Atlantic/Azores',  None, None, 'Island in the Atlantic ocean'],
    ['Indian/Langkawi',  None, None, 'Island in the Indian ocean'],
    ['Indian/Sabang',    None, None, 'Island in the Indian ocean'],
    ['Fictional/Nublar', None, None, 'Island in Fiction'],
    ['Fictional/Hydra',  None, None, 'Island in Fiction'],
]


@test.question
def test_pacific():
    """I'm about to check the Pacific islands."""
    check_files({
        'files': end_files[0:3], 
        'basedir': pathlib.Path.home() / 'Oceans'
        }, extra=True)


@test.question
def test_atlantic():
    """I'm about to check the Atlantic islands."""
    check_files({
        'files': end_files[3:6], 
        'basedir': pathlib.Path.home() / 'Oceans'
        }, extra=True)


@test.question
def test_indian():
    """I'm about to check the Indian islands."""
    check_files({
        'files': end_files[6:8], 
        'basedir': pathlib.Path.home() / 'Oceans'
        }, extra=True)


@test.question
def test_fictional():
    """I'm about to check the Fictional islands."""
    check_files({
        'files': end_files[8:], 
        'basedir': pathlib.Path.home() / 'Oceans'
        }, extra=True)

@test.question
def test_extras():
    """I'm about to check for extraneous files."""
    check_files({
        'files': end_files, 
        'basedir': pathlib.Path.home() / 'Oceans'
        }, extra=False)

def main():
    print("""
    I have created a directory called "Islands" in your home directory. 
    Inside of "Islands" you will see 10 files named after islands. Each island 
    file contains the name of the ocean it is in. Reorganize the files so 
    that they are in directories named after their oceans. The reorganized 
    files should be in a directory called "Oceans" in the current directory.  
    
    The "Oceans" directory should look like this: 

    .
    |-- Oceans
        |-- Atlantic
        |-- Pacific
        |-- Indian
        |-- Fictional

    """)

    setup_files({
        'files': start_files, 
        'basedir': pathlib.Path.home() / 'Islands'
    })

    input("Check for the files and press Enter.")

    test_pacific(points=4)
    test_atlantic(points=4)
    test_indian(points=4)
    test_fictional(points=4)
    test_extras(points=4)
    
    print(f"Your score is {test.score} of {test.total}")
    print("Your confirmation code is:", vault.confirmation({'score': test.score}))


if __name__ == '__main__' :
    main()
