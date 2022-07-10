"""
Solve problems like a boss.
"""

import os
import pathlib
import random 
import subprocess

from lifealgorithmic.secrets import vault
from lifealgorithmic.linux.test import test, ask as input
from lifealgorithmic.linux.files import randpath, \
    random_big_dir, setup_files, check_files

vault.setkey("blarny234")
vault.setfile(f'{os.environ["HOME"]}/.bosslab')

debug = False 

@test.question
def delete_the_ms(count, basedir):
    """
    I have just created a directory called "{basedir}" with {count} randomly named files.

    Remove all files with names that start with the letter "m" (lower case). 
    """
    files = random_big_dir(count=count)
    setup_files(files, basedir=basedir)

    input('Press Enter to continue.')

    # Check that non-matching files are there. 
    check_files(filter(lambda x: not x[0].startswith('m'), files), basedir=basedir)

    for file in map(lambda p: basedir / pathlib.Path(p[0]), filter(lambda x: x[0].startswith('m'), files)):
        assert not file.exists(), f"""The file {file} still exists!"""


@test.question
def delete_the_quotes(count, basedir):
    """
    I have just created a directory called "{basedir}" with {count} randomly named files.

    Remove all files with names that contain a single quote (') character. 
    """
    files = random_big_dir(count=count)
    setup_files(files, basedir=basedir)

    input('Press Enter to continue.')

    # Check that non-matching files are there. 
    check_files(filter(lambda x: "'" not in x[0], files), basedir=basedir)

    for file in map(lambda p: basedir / pathlib.Path(p[0]), filter(lambda x: "'" in x[0], files)):
        assert not file.exists(), f"""The file {file} still exists!"""


@test.question
def deep_file(message):
    """
    I just created a directory called "deep" in the "Files" directory. Explore 
    it until you get to the deepest subdirectory in it. Inside the deepest 
    subdirectory you will find a secret file. What are the contents of the file? 
    """
    path = pathlib.Path("Files/deep/there's/a/light/over/at/the/Frankenstein/place/there's/a/li/ii/ii/ii/ii/ii/ii/ight/burning/in/the/fire/place")
    file = path / '.secret'
    subprocess.run(['mkdir', '-p', path])
    with open(file, 'w') as fh:
        fh.write(str(message) + "\n")
    
    if debug:
        print('DEBUG:', str(message))
    got = input().strip()
    assert got == str(message), "That's not the message."


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


def main():
    delete_the_ms(points=5, count=500, basedir="./Rando")
    delete_the_quotes(points=5, count=500, basedir="./Rando")
    deep_file(points=5, message=randpath.random_file())
    delete_by_contents(points=5, count=500, basedir="./Rando")

    print(f"Your score is {test.score} of {test.total}")
    print("Your confirmation code is:", vault.confirmation({'score': test.score}))


if __name__ == '__main__' :
    main()
