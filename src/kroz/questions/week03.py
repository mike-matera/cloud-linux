"""
Questions for the third week of class.

Chapter 2 of the book.

"""

import os
from pathlib import Path
import pwd
import textwrap
from kroz.app import get_appconfig
import kroz.ascii
from kroz.question import (
    Question,
)
from kroz.random.real_path import random_real_path

questions = []


class FlagFile(Question):
    """Create a file and ask about its contents."""

    def flag(self):
        """Generate the flag text."""
        return textwrap.dedent("""

        {}                                

        Welcome {} this is your flag file. 
                                    
        Your secret file is: {}

        """).format(
            kroz.ascii.robot(),
            pwd.getpwuid(os.getuid())[4].split(",")[0],
            self._secret,
        )

    def setup(self):
        self._secret = random_real_path().random_file().resolve()
        self._flag = Path(get_appconfig("default_path")) / "flag"
        with open(self._flag, "w") as fh:
            fh.write(self.flag())

    def cleanup(self):
        self._flag.unlink(missing_ok=True)

    @property
    def text(self):
        return f"""
        # Find the Secret File 

        I have just created a file named: {self._flag.resolve()}

        The file contains a secret file. Look inside of the file and answer with
        the full path of the secret file. 
        """

    def check(self, answer):
        assert answer.strip() == str(self._secret), "Nope."
