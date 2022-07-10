import subprocess
import os
import stat
import pathlib
import grp 
import random 

from lifealgorithmic.secrets import vault
from lifealgorithmic.linux.test import test, ask as input
from lifealgorithmic.linux.files import randpath, make_flag, random_big_file, \
    check_files, setup_files, random_big_dir

vault.setkey("blarny234")
vault.setfile(f'{os.environ["HOME"]}/.practice-m2')

debug = False 

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
def delete_by_contents(count, basedir):
    """
    I have just created a directory called "{basedir}" with {count} randomly named files.

    Remove all files that contain the word "deleteme" in them. 
    """
    files = random_big_dir(count=count)
    for file in random.sample(files, count//5):
        file[3] = "deleteme"

    setup_files(files, basedir=basedir)

    input('Press Enter to continue.')

    # Check that non-matching files are there. 
    check_files(filter(lambda x: x[3] != "deleteme", files), basedir=basedir)

    for file in map(lambda p: basedir / pathlib.Path(p[0]), filter(lambda x: x[3] == "deleteme", files)):
        assert not file.exists(), f"""The file {file} still exists!"""

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
def sort_file():
    """
    I have just (re)created a file called "bigfile" in this directory. 

    If the file is sorted in alphabetical order what would be the first word? 
    """    
    random_big_file(shape=(1000,1))
    exp = subprocess.run('sort bigfile | head -n 1', shell=True, 
        stdout=subprocess.PIPE).stdout.decode('utf-8').strip().casefold()
    if debug:
        print("DEBUG:", exp)
    got = input().strip().casefold()
    assert got == exp, """That's not correct."""

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
def test_locations():
    """I'm about to check the island locations."""
    check_files(
        ((e[0],None,None,e[3]) for e in end_files), 
        basedir=f'{os.environ["HOME"]}/Oceans',
    )

@test.question
def test_permissions():
    """I'm about to check the island permissions."""
    check_files(end_files, basedir=f'{os.environ["HOME"]}/Oceans')


def main():
    directory_inode(points=0, dir=randpath.random_dir())
    relative_path(points=0, dir1=randpath.random_dir(), dir2=randpath.random_dir())
    delete_by_contents(points=0, count=500, basedir=f'{os.environ["HOME"]}/Rando')
    sort_file(points=0)
    file_size(points=0, file=randpath.random_file())

    setup_files(start_files, basedir=f'{os.environ["HOME"]}/Islands')
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
    input("Check for the files and press Enter.")
    test_locations(points=0)

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
    input("Check for the files and press Enter.")
    test_permissions(points=0)

    print(f"Your score is {test.score} of {test.total}")
    print("Your confirmation code is:", vault.confirmation({'score': test.score}))


if __name__ == '__main__' :
    main()
