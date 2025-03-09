
import pathlib 

from ..files import random_big_dir, random_big_file, setup_files, check_files

class DeleteTheMs:

    def setup(self):
        self.files = random_big_dir()
        print("""Remove all files with names that start with the letter "m" (lower case).""")
        return "Press Enter to Continue: "

    def check(self):
        self.files['files'] = filter(lambda x: not x[0].startswith('m'), self.files['files'])
        check_files(self.files)

class DeleteTheQuotes:

    def setup(self):
        files = random_big_dir()
        print("""Remove all files with names that contain a single quote (') character.""")
        return('Press Enter to continue.')

    def check(self):
        # Check that non-matching files are there. 
        self.files['files'] = filter(lambda x: "'" not in x[0], self.files['files'])
        check_files(self.files)
