"""
Week 5 Questions 
"""

from pathlib import Path
import textwrap
from kroz.question import Question
from kroz.random.path import CheckDir, CheckFile, CheckPath


class Islands(Question):
    """The islands with perms."""

    placeholder = "Enter to Continue"

    def __init__(self, **kwargs):
        self.start_files = CheckPath(
            "Islands",
            files=[
                CheckFile(
                    "hawaii", "Hawaii is an island in the Pacific ocean"
                ),
                CheckFile("samoa", "Samoa is an island in the Pacific ocean"),
                CheckFile(
                    "kiribati", "Kiribati is an island in the Pacific ocean"
                ),
                CheckFile(
                    "ireland", "Ireland is an island in the Atlantic ocean"
                ),
                CheckFile(
                    "madeira", "Madeira is an island in the Atlantic ocean"
                ),
                CheckFile(
                    "azores", "Azores is an island in the Atlantic ocean"
                ),
                CheckFile(
                    "langkawi", "Langkawi is an island in the Indian ocean"
                ),
                CheckFile("Sabang", "Sabang is an island in the Indian ocean"),
                CheckFile(
                    "nublar",
                    "Nublar is a fictional island in the movie Jurassic Park",
                ),
                CheckFile(
                    "hydra", "Hydra is a fictional island in the show Lost"
                ),
            ],
        )

        self.check_files = CheckPath(
            "Oceans",
            files=[
                CheckDir(""),
                CheckDir("Pacific"),
                CheckDir("Atlantic"),
                CheckDir("Indian"),
                CheckDir("Fictional"),
            ],
        )
        for file in self.start_files.files:
            assert isinstance(file, CheckFile), "Internal error."
            if "Pacific" in file.contents:
                newpath = Path("Pacific") / file.path
            elif "Atlantic" in file.contents:
                newpath = Path("Atlantic") / file.path
            elif "Indian" in file.contents:
                newpath = Path("Indian") / file.path
            elif "fiction" in file.contents:
                newpath = Path("Fictional") / file.path
            else:
                raise ValueError("Ooops:", file.contents)
            self.check_files.files.append(
                CheckFile(
                    newpath,
                    contents=file.contents,
                )
            )

    @property
    def text(self): 
        return textwrap.dedent("""
        # Sort the Islands 
        
        I have created a directory called `Islands` that looks like this:
                               
        {}

        Inside of `Islands` you will see files named after islands. Each island 
        file contains the name of the ocean it is in. Reorganize the files so 
        that they are in directories named after their oceans. The reorganized 
        files should be in a directory called `Oceans`.  The `Oceans` directory 
        should look like this: 

        {}
        """).format(self.start_files.markdown(), self.check_files.markdown(detail=True))

    def setup(self):
        self.start_files.sync()

    def cleanup(self):
        self.start_files.cleanup()

    def check(self, answer):
        self.check_files.full_report(verbose=2)
