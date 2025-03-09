"""
Files and directories with permissions.
"""

import os
from random import random 
import grp
import pathlib 

from cloud_linux.lab import LinuxLab, ask as input
from cloud_linux.labs.files import setup_files, check_files
from cloud_linux.secrets import vault

debug = False 
vault.setkey("blarny234")
vault.setfile(f'{os.environ["HOME"]}/.islands2')
test = LinuxLab(debug=debug)

try:
    cis90_grp = grp.getgrnam('cis90').gr_gid
except Exception as e: 
    cis90_grp = grp.getgrnam('adm').gr_gid # for testing on my machine

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
    ['Pacific/Hawaii',   (None, cis90_grp), 0o440, 'Island in the Pacific ocean'],
    ['Pacific/Samoa',    (None, cis90_grp), 0o440, 'Island in the Pacific ocean'],
    ['Pacific/Kiribati', (None, cis90_grp), 0o440, 'Island in the Pacific ocean'],
    ['Atlantic/Ireland', (None, cis90_grp), 0o440, 'Island in the Atlantic ocean'],
    ['Atlantic/Madeira', (None, cis90_grp), 0o440, 'Island in the Atlantic ocean'],
    ['Atlantic/Azores',  (None, cis90_grp), 0o440, 'Island in the Atlantic ocean'],
    ['Indian/Langkawi',  (None, cis90_grp), 0o600, 'Island in the Indian ocean'],
    ['Indian/Sabang',    (None, cis90_grp), 0o600, 'Island in the Indian ocean'],
    ['Fictional/Nublar', (None, cis90_grp), 0o600, 'Island in Fiction'],
    ['Fictional/Hydra',  (None, cis90_grp), 0o600, 'Island in Fiction'],
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

    In addition you must set permissions on the files and directories in Oceans.
    Here are the rules you must follow: 

        1. The Oceans directory and all subdirectories and files should be have the 'cis90' group.
        2. No files or directories should be publicly readable, writable or executable.
        3. Files in the Atlantic and Pacific oceans should be read only for the user and group. 
        4. Files in the Indian and Fictional oceans should be read/write for the user only. 

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
