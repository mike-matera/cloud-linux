"""
Helpers for files.
"""

import pathlib
import random 
import subprocess
import pwd
import os 
import logging 

from cloud_linux.labs.words import randword

class RandomPath:
    """
    Get random extant files or directories on the system.
    """

    DEFAULT_PATHS = [
        ('/etc', '**/*'),
        ('/bin', '**/*'),
        ('/dev', '**/*'),
        ('/usr/bin', '**/*'),
        ('/usr/sbin', '**/*'),
        ('/usr/share', '*/*'),
        ('/sys', '*/*/*'),
        ('/boot', '**/*'),
        ('/lib', '*/*'),
    ]

    def __init__(self, search=DEFAULT_PATHS, debug=False):
        self.docs = None
        self.search = search
        self.debug = debug
    
    def _build(self):
        self.docs = []

        def can_stat(f):
            try:
                f.stat()
                return True
            except:
                return False 

        for path in self.search:
            inpath = list(filter(can_stat, pathlib.Path(path[0]).glob(path[1])))
            if self.debug:
                print(f"DEBUG: {path} yields {len(inpath)} files.")    
            self.docs.append(inpath)

    def random_file(self):
        return self.find(lambda c: c.is_file() and not c.is_symlink()).resolve()

    def random_dir(self):
        return self.find(lambda c: c.is_dir() and not c.is_symlink()).resolve()

    def find(self, filt):
        """Search the candidate files until a condition matches."""
        if self.docs is None:
            self._build()
        random.shuffle(self.docs)
        for path in self.docs:
            choices = list(filter(filt, path))
            if len(choices) > 0:
                return random.choice(choices)


def setup_files(files):
    """
    Setup a file structure. 
    
    files is a dictionary with the keys:
        basedir - A Path where the files will be created 
        files - A sequence of four-tuples: 
            (path, (user, group), mode, contents) 
                (user, group) can be None, individual user and group can also be None
                mode can be None 
                contents can be None 

    If basedir does not exist it will be created. If it does exist the contents will be removed.
    """

    assert 'basedir' in files and isinstance(files['basedir'], pathlib.Path)
    assert not files['basedir'].exists() or not pathlib.Path.home().samefile(files['basedir'])
    assert 'files' in files 
    
    if files['basedir'].exists():
        for item in list(files['basedir'].iterdir()):
            if item.is_dir():
                subprocess.run(f"rm -rf {item}", shell=True, cwd=files['basedir'])
            else:
                item.unlink()
    else:
        subprocess.run(f"mkdir -p {files['basedir']}", shell=True)

    for path, ownership, mode, contents in files['files']:
        target = files['basedir'] / path
        subprocess.run(f'mkdir -p {target.parent}', shell=True)
        with open(target, 'w') as fh:
            fh.write(contents)
        if mode is not None:
            subprocess.run(f"chmod {mode} {target}", shell=True)
        if ownership is not None:
            if ownership[0] is not None:
                subprocess.run(f"chown {ownership[0]} {target}", shell=True)
            if ownership[1] is not None:
                subprocess.run(f"chgrp {ownership[1]} {target}", shell=True)

def check_files(files, extra=False):
    """
    Check the contents of files. files is the the same as setup_files.       
    """
    assert 'basedir' in files and isinstance(files['basedir'], pathlib.Path)
    assert 'files' in files 

    exists = list(files['basedir'].glob('**/*'))

    for path, ownership, mode, contents in files['files']:
        path = files['basedir'] / path
        assert path.exists(), f"""The file {path} does not exist."""
        stat = path.stat()
        if contents is not None:
            with open(path) as fh:
                assert contents == fh.read(), f"The contents of {path} don't match."
        if mode is not None:
            rmode = stat.st_mode & 0b111111111
            assert mode == rmode, f"The permissions on {path} don't match."
        if ownership is not None:
            if ownership[0] is not None:
                assert stat.st_uid == ownership[0], f"""The owner of {path} doesn't match."""
            if ownership[1] is not None:
                assert stat.st_gid == ownership[1], f"""The group of {path} doesn't match."""

        exists.remove(pathlib.Path(path).resolve())

    if not extra:
        # Filter out base directories
        for ex in list(exists):
            for path, _, _, _ in files['files']:
                if ex.samefile((files['basedir'] / pathlib.Path(path)).parent):
                    exists.remove(ex)
                    break
        assert len(exists) == 0, f"""The file {str(exists[0])} exists and shouldn't"""

def make_flag():
    """
    Create or recreate the flag in the user's home directory. Return the path and secret.
    """
    global randpath
    flag_file = pathlib.Path(f'{os.environ["HOME"]}/flag').resolve()
    gecos = pwd.getpwuid(os.getuid())[4]
    secret_file = randpath.random_file()
    flag_text = f"""

    Welcome {gecos.split(',')[0]} this is your flag file. 
    There's trouble on the island today!

    Your secret file is: {secret_file}

"""
    with open(flag_file, 'w') as fh:
        fh.write(flag_text)

    return {
        'path': flag_file,
        'secret': secret_file
    }

def random_big_file(name=pathlib.Path(os.environ.get('HOME','.')) / 'bigfile', shape=(100000, 12), sep=' ', end='\n'):
    """
    Create a large text file with dictionary words in the current directory.
    """    
    bigfile = pathlib.Path(name).resolve()
    with open(bigfile, 'w') as fh:
        for _ in range(shape[0]):
            for _ in range(shape[1]):
                fh.write(randword.choice() + sep)
            fh.write(end)
    
    return bigfile

def random_big_dir(count=1000, setup=True, basedir=pathlib.Path.home() / "Rando"):
    """
    Create a directory with a large number of randomly named files. This changes 
    the filesystem and returns a structure suitable for check_files.
    """
    logging.info(f"I'm (re)creating {count} random files in the directory {basedir}.")
    files = {
        'basedir': basedir,
        'files': list(map(lambda x: [x, None, None, x], random.sample(randword.words, count))),
    }
    if setup:
        setup_files(files)
    return files

# 
# For convenience 
#
randpath = RandomPath()
