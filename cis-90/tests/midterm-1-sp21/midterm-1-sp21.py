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
import pwd
import json 

from lifealgorithmic.linux.test import LinuxTest

secret = "flibbertyjibbit"
test = LinuxTest(secret)

docs = list(pathlib.Path('/usr/share/doc').glob('**/*'))
docs += list(pathlib.Path('/etc').glob('**/*'))
docs += list(pathlib.Path('/bin').glob('**/*'))
docs += list(pathlib.Path('/usr/bin').glob('**/*'))
docs += list(pathlib.Path('/dev').glob('**/*'))

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


def make_flag():

    if not pathlib.Path('flag').exists() or test.config.get('secret_file') is None:

        gecos = pwd.getpwuid(os.getuid())[4]
        secret_file = random_file()
        flag_file = f"""
 Welcome {gecos.split(',')[0]} to the SUN-HWA. 
 There's trouble on the island today!

 Your secret file is: {secret_file}
        """

        test_files = [
            ['flag', '644', flag_file],
        ]
        
        test.setup_files(test_files, writemode='overwrite')
        inode = os.stat(pathlib.Path('flag')).st_ino
        test.config['secret_file'] = str(secret_file)
        test.config['flag_file.inode'] = inode

@test.question(10, setup=make_flag)
def flag_file():
    """Welcome to the test. I've created a file in the current directory called "flag". 
    Inside the flag file there's the name of a secret file. 
    
    What's the secret file?
    """
    if test.config.get(flag_file.__name__) is not None:
        return
    if test.debug:
        print("DEBUG:", test.config['secret_file'])
    got = input("What's the secret file? ")
    assert got == test.config['secret_file'], """That's not correct.""" 
    test.config[flag_file.__name__] = 1 


@test.question(10, setup=make_flag)
def flag_path():
    """
What is the absolute path of the flag file?

    """
    if test.config.get(flag_path.__name__) is not None:
        return
    exp = pathlib.Path("flag").resolve()
    if test.debug:
        print("DEBUG:", exp)
    got = input("Enter the path: ").strip()
    assert got == str(exp), """That's not correct.""" 
    test.config[flag_path.__name__] = 1 


@test.question(10, file=random_file())
def file_size(file):
    """
    What is the size of the following file in bytes? 

      {file}

    """
    if test.config.get(file_size.__name__) is not None:
        return

    exp = file.stat().st_size
    if test.debug:
        print("DEBUG:", exp)
    got = int(input("Enter the size: "))
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

@test.question(10, dir1=pathlib.Path(os.getcwd()), dir2=random_dir())
def flag_inode(dir1, dir2):
    """
    What is the inode number of the flag file?
    """
    if test.config.get(flag_inode.__name__) is not None:
        return

    exp = test.config['flag_file.inode'] 
    if test.debug:
        print("DEBUG:", exp)
    got = int(input("Enter the inode number: "))
    assert got == exp, """That's not the correct number.""" 
    
    test.config[flag_inode.__name__] = 1 


def create_deep_dir():

    words = []
    with open('/usr/share/dict/words') as w:
        for word in w:
            words.append(word.strip().casefold())

    longfile = pathlib.Path('deep/thoughs/by/jack/handy/it/seemed/that/the/crows/were/calling/his/name/thought/caw') 
    secret_word = random.choice(words) 
    if not longfile.exists() or test.config.get('secret_word') is None:

        test_files = [
            [longfile, '644', secret_word + "\n"],
        ]
        
        test.setup_files(test_files, writemode='overwrite')
        test.config['secret_word'] = secret_word

@test.question(10, setup=create_deep_dir)
def deep_dir():
    """
Deep inside of the "deep" directory there's a file with a secret word inside of it. 
Find the secret word.  
    """
    if test.config.get(deep_dir.__name__) is not None:
        return
    if test.debug:
        print("DEBUG:", test.config['secret_word'])
    got = input("What's the secret word? ")
    assert got == test.config['secret_word'], """That's not correct.""" 
    test.config[deep_dir.__name__] = 1 


@test.question(10)
def find_command():
    """
Where is the "xxd" command located? 

    """
    if test.config.get(find_command.__name__) is not None:
        return

    loc = subprocess.run('type xxd', shell=True, capture_output=True)
    output = loc.stdout.decode('utf-8')
    m = re.search(r'xxd\s+is\s+(\S+)', output)
    if m is None:
        raise ValueError("INTERNAL ERROR! REPORT TO MIKE")
    exp = m.group(1)
    if test.debug:
        print('DEBUG:', exp)
    got = input("Enter the path: ")
    assert got == exp, """That's not the right path."""
    test.config[find_command.__name__] = 1 


@test.question(10)
def file_type():
    """
What type of file is the "xxd" command? You will first have to locate it. 

    """
    if test.config.get(file_type.__name__) is not None:
        return

    got = input("Enter the type: ")
    exp = re.search(r'(?i)ELF 64-bit LSB', got)
    assert exp is not None, """That's not correct. Hint: Copy and paste the output of a command."""
    test.config[file_type.__name__] = 1 


@test.question(10, file="/etc/passwd")
def file_lines(file):
    """
How many lines are there in the {file} file? 

    """
    if test.config.get(file_lines.__name__) is not None:
        return

    with open(file) as fh:
        exp = len(list(fh.readlines()))

    if test.debug:
        print("DEBUG:", exp)

    got = int(input("Enter the number of lines: "))
    assert got == exp, """That's not correct."""
    test.config[file_lines.__name__] = 1 


def create_big_file():
    words = []
    with open('/usr/share/dict/words') as w:
        for word in w:
            words.append(word.strip().casefold())

    bigfile = pathlib.Path('bigfile') 
    first_word = random.choice(words)
    if not bigfile.exists() or test.config.get('first_word') is None:
        with open(bigfile, 'w') as fh:
            fh.write(first_word + " ")
            for i in range(100000):
                for j in range(12):
                    fh.write(random.choice(words) + " ")
                fh.write('\n')
        test.config['first_word'] = first_word


@test.question(10, setup=create_big_file)
def big_file():
    """
I just created a file called "bigfile". What is the first word in it? 
    """
    if test.config.get(big_file.__name__) is not None:
        return
    if test.debug:
        print("DEBUG:", test.config['first_word'])
    got = input("What's the first word? ")
    assert got == test.config['first_word'], """That's not correct.""" 
    test.config[big_file.__name__] = 1 


def midterm_sp2021() :
    '''
    ** Welcome to the fist CIS-90 midterm for spring 2021 ** 
    '''

    print(midterm_sp2021.__doc__)
    test.run(debug=True)
    print("All done!\n\n")    


if __name__ == '__main__' :
    midterm_sp2021()
