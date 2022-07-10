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
from lifealgorithmic.linux.files import randpath, make_flag, random_big_file, setup_files, check_files, random_big_dir
from lifealgorithmic.linux.words import randword

vault.setkey("blarny234")
vault.setfile(f'{os.environ["HOME"]}/.midterm2')

debug = False

start_files = [    
    ['San Francisco',   None, None, 'San Francisco County\n'],
    ['Santa Cruz',    None, None, 'Santa Cruz County\n'],
    ['Los Angeles', None, None, 'Los Angeles County\n'],
    ['Fresno',  None, None, 'Fresno County\n'],
    ['Oakland',  None, None, 'Alameda County\n'],
    ['Eureka',   None, None, 'Humboldt County\n'],
    ['Watsonville', None, None, 'Santa Cruz County\n'],
    ['Aptos',   None, None, 'Santa Cruz County\n'],
    ['San Luis Obispo',   None, None, 'San Luis Obispo County\n'],
    ['Fortuna',    None, None, 'Humboldt County\n'],
]

end_files = [
    ['San Francisco/San Francisco',   None, None, 'San Francisco County\n'],
    ['Santa Cruz/Santa Cruz',    None, None, 'Santa Cruz County\n'],
    ['Los Angeles/Los Angeles', None, None, 'Los Angeles County\n'],
    ['Fresno/Fresno',  None, None, 'Fresno County\n'],
    ['Alameda/Oakland',  None, None, 'Alameda County\n'],
    ['Humboldt/Eureka',   None, None, 'Humboldt County\n'],
    ['Santa Cruz/Watsonville', None, None, 'Santa Cruz County\n'],
    ['Santa Cruz/Aptos',   None, None, 'Santa Cruz County\n'],
    ['San Luis Obispo/San Luis Obispo',   None, None, 'San Luis Obispo County\n'],
    ['Humboldt/Fortuna',    None, None, 'Humboldt County\n'],
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
def file_type(file):
    """
    What is the type of the file below? 

        {file}

    """
    exp = subprocess.run(f"file {file}", shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.split()[1]
    if debug:
        print("DEBUG:", exp)
    got = input().strip().casefold()
    assert got.startswith(exp.casefold()), """That's not correct.""" 

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
def deep_file():
    """
    I just (re)created a directory called "deep" in the "Files" directory. Explore 
    it until you get to the deepest subdirectory in it. Inside the deepest 
    subdirectory you will find a secret file. What are the contents of the file? 
    """

    message = randword.choice().casefold()
    path = pathlib.Path("Files/deep")
    subprocess.run(['rm', '-rf', path])
    for _ in range(random.randrange(20,50)):
        path /= randword.choice()
    file = path / '.secret'
    subprocess.run(['mkdir', '-p', path])
    with open(file, 'w') as fh:
        fh.write(str(message) + "\n")
    
    if debug:
        print('DEBUG:', str(message))
    got = input().strip()
    assert got == str(message), "That's not the message."

@test.question
def test_cities():
    """
    I have created a directory called "Cities" in your home directory. 
    Inside of "Cities" you will see 10 files named after cities in California. 
    Each city file contains the name of the county it is in. Reorganize the 
    files so that they are in directories named after their county. The 
    reorganized files should be in a directory called "California" in your 
    home directory.  
    
    The "California" directory should be organized by county with cities 
    inside of the county directory. For example: 

    .
    |-- California
        |-- Santa Cruz
            |-- Santa Cruz
    """

    setup_files(start_files, basedir=f'{os.environ["HOME"]}/Cities')
    input("Check for the files and press Enter.")
    check_files(end_files, basedir=f'{os.environ["HOME"]}/California')


@test.question
def find_top_line(line):
    """
    I have just created a file called "bigfile" in this directory. 

    What is the first word on line number {line:,}?
    """
    random_big_file()
    with open(vault.get('bigfile.path')) as fh:
        for _ in range(1, line+1):
            exp = fh.readline()
    exp = exp.split()[0].casefold()
    if debug:
        print("DEBUG:", exp)
    got = input().strip().casefold()
    assert got == exp, """That's not correct."""


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
def unique_words():
    """
    I have just (re)created a file called "bigfile" in this directory. 

    How many unique words are in bigfile? 
    """    
    random_big_file(shape=(2000,1))
    exp = int(subprocess.run('sort bigfile | uniq | wc -l', shell=True, 
        stdout=subprocess.PIPE).stdout.decode('utf-8'))
    if debug:
        print("DEBUG:", exp)
    got = int(input())
    assert got == exp, """That's not correct."""


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

def update_code():
    print("Your confirmation code is:", vault.confirmation({'score': test.score}))

def main():
    print("""

** Welcome to Midterm #2 for Spring 2022 **

When you start the test on Canvas you'll get a secret code. 
To begin the test enter the code below:

    """)

    code = input("secret code: ")
    if code.lower() != "fries2022":
        print("That is not the correct code.")
        exit()

    def exit_hook():
        print("\n\nYou finished the test. You can restart it any time.")
        print(f"Your score is {test.score} of 100")
        print("Your confirmation code is:", vault.confirmation({'score': test.score}))

    atexit.register(exit_hook)

    directory_inode(points=10, dir=randpath.random_dir())
    update_code()

    find_day(points=10, year=2022+random.randint(100,200))
    update_code()

    file_type(points=10, file=randpath.random_file())
    update_code()

    bigfile_size(points=10) 
    update_code()

    deep_file(points=10) 
    update_code()

    test_cities(points=20)
    update_code()

    find_top_line(points=10, line=random.randrange(10000,90000))
    update_code()

    sort_file(points=10)
    update_code()

    unique_words(points=10)
    update_code()

    delete_the_quotes(points=10, count=500, basedir="./Rando")
    update_code()

    resolve_link(points=10, link=randpath.find(lambda x: x.is_symlink()))
    update_code()



if __name__ == '__main__':
    main()
