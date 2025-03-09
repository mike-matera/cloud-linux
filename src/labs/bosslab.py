"""
Solve problems like a boss.
"""

import os
import pathlib
import random 
import subprocess

from cloud_linux.lab import LinuxLab, ask as input
from cloud_linux.labs.files import randpath, \
    random_big_dir, setup_files, check_files
from cloud_linux.secrets import vault

debug = False 
vault.setkey("blarny234")
vault.setfile(f'{os.environ["HOME"]}/.bosslab')
test = LinuxLab(debug=debug)

@test.question
def delete_the_ms(count):
    """
    I have just (re)created a directory called "Rando" in your home directory.

    Remove all files with names that start with the letter "m" (lower case). 
    """
    files = random_big_dir(count=count)

    input('Press Enter to continue.')

    files['files'] = filter(lambda x: not x[0].startswith('m'), files['files'])
    check_files(files)


@test.question
def delete_the_quotes(count):
    """
    I have just (re)created a directory called "Rando" in your home directory.

    Remove all files with names that contain a single quote (') character. 
    """
    files = random_big_dir(count=count)

    input('Press Enter to continue.')

    files['files'] = filter(lambda x: "'" not in x[0], files['files'])
    check_files(files)


@test.question
def deep_file(message):
    """
    I just created a directory called "Files/deep" in your home directory. Explore 
    it until you get to the deepest subdirectory in it. Inside the deepest 
    subdirectory you will find a secret file. What are the contents of the file? 
    """
    path = pathlib.Path.home() / pathlib.Path("Files/deep/there's/a/light/over/at/the/Frankenstein/place/there's/a/li/ii/ii/ii/ii/ii/ii/ight/burning/in/the/fire/place")
    file = path / '.secret'
    subprocess.run(['mkdir', '-p', path])
    with open(file, 'w') as fh:
        fh.write(str(message) + "\n")
    
    if debug:
        print('DEBUG:', str(message))
    got = input().strip()
    assert got == str(message), "That's not the message."


@test.question
def delete_by_contents(count):
    """
    I have just (re)created a directory called "Rando" in your home directory.

    Remove all files that contain the word "deleteme" in them. 
    """
    files = random_big_dir(count=count, setup=False)
    for file in random.sample(files['files'], count//5):
        file[3] = "deleteme"

    setup_files(files)

    input('Press Enter to continue.')

    # Check that non-matching files are there. 
    files['files'] = filter(lambda x: x[3] != "deleteme", files['files'])
    check_files(files)


def main():
    delete_the_ms(points=5, count=500)
    delete_the_quotes(points=5, count=500)
    deep_file(points=5, message=randpath.random_file())
    delete_by_contents(points=5, count=500)

    print(f"Your score is {test.score} of {test.total}")
    print("Your confirmation code is:", vault.confirmation({'score': test.score}))


if __name__ == '__main__' :
    main()
