"""
# Lesson 5. Files and Directories

- Make and remove directories
- Copy and move files

Reading:

- Chapter 4
"""

import textwrap
from pathlib import Path
from typing import Type

from kroz.flow.base import KrozFlowABC
from kroz.flow.interaction import Interaction
from kroz.flow.question import MultipleChoiceQuestion, Question
from kroz.random.path import CheckDir, CheckFile, CheckPath
from kroz.screen import KrozScreen

questions: list[Question] = []


class Islands(Question):
    """The islands with perms."""

    placeholder = "Enter to Continue"

    def setup(self):
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
                    "azores", "Azores are islands in the Atlantic ocean"
                ),
                CheckFile(
                    "langkawi", "Langkawi is an island in the Indian ocean"
                ),
                CheckFile("sabang", "Sabang is an island in the Indian ocean"),
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

        self.start_files.sync()

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
        """).format(
            self.start_files.markdown(), self.check_files.markdown(detail=True)
        )

    def cleanup(self):
        self.start_files.cleanup()

    def check(self, answer):
        self.check_files.full_report(verbose=2)


class Movies(Question):
    """Simple check for the movies activity."""

    text = """
# Hold on a sec... 

Press `Enter` to check your `Movies` directory. The rest of this activity assumes 
that you have those files in place.
"""

    def __init__(self, stage: int):
        self.stage = stage

    def check(self, answer):
        if self.stage == 1:
            check_files = CheckPath(
                "Movies",
                [
                    CheckFile("Casablanca"),
                    CheckFile("The Wizard of Oz"),
                    CheckFile("Alien"),
                    CheckFile("Forrest Gump"),
                    CheckFile("The Shining"),
                    CheckFile("Up"),
                ],
            )
        elif self.stage == 2:
            check_files = CheckPath(
                "Movies",
                [
                    CheckDir("Horror"),
                    CheckDir("Classics"),
                    CheckDir("Animated"),
                    CheckFile("Classics/Casablanca"),
                    CheckFile("Classics/The Wizard of Oz"),
                    CheckFile("Horror/Alien"),
                    CheckFile("Classics/Forrest Gump"),
                    CheckFile("Horror/The Shining"),
                    CheckFile("Animated/Up"),
                ],
            )
        else:
            raise ValueError("Internal error.")
        check_files.full_report(extra_ok=True, verbose=2)


title = "File Management"

state = "fmgmt"

welcome = KrozScreen(
    """
# File Management 

This lesson covers how to create, copy, move and delete both files and directories.
You will learn about the commands:

1. `cp`
2. `mv`
3. `mkdir` and `rmdir`
3. `rm`
3. `ln -s`
        """,
    classes="welcome",
    title="Welcome!",
)

walks: dict[str, list[KrozFlowABC | Type[KrozFlowABC]]] = {
    "Organize Movies": [
        Interaction(
            """
# Let's Create Some Movies

In your home directory create a folder called `Movies`. 

```console
$ mkdir Movies
```
""",
            filter=lambda cmd: cmd.command == "mkdir"
            and cmd.args == ["Movies"]
            and cmd.cwd == Path().home(),
        ),
        Interaction(
            """
Now change into your `~/Movies` directory:

```console
$ cd Movies
```
""",
            filter=lambda cmd: cmd.command == "cd"
            and cmd.args[0].startswith("Movies")
            and cmd.cwd == Path().home() / "Movies",
        ),
        Interaction(
            """
# Let's Create Some Movies

The `touch` command creates an empty file. It's handy for stuff like this so 
we're going to use it to create some files that have the names of movies. Later,
we'll sort them. Start by creating one of my favorite movies *Casablanca*. 

```console
$ touch Casablanca
```
""",
            filter=lambda cmd: cmd.command == "touch"
            and (cmd.cwd / "Casablanca").exists(),
        ),
        Interaction(
            """
Now another classic:

**BE CAREFUL WITH THIS ONE!** The quotes are required for this command. If  you
don't add the quotes `touch` will create **THREE** files instead of one. 

```console
$ touch "The Wizard of Oz"
```
""",
            filter=lambda cmd: cmd.command == "touch"
            and (cmd.cwd / "The Wizard of Oz").exists(),
        ),
        Interaction(
            """
Everyone likes Tom Hanks:

**REMEMBER THE QUOTES!** 

```console
$ touch "Forrest Gump"
```
""",
            filter=lambda cmd: cmd.command == "touch"
            and (cmd.cwd / "Forrest Gump").exists(),
        ),
        Interaction(
            """
How about some 1970's SciFi Horror:

```console
$ touch Alien
```
""",
            filter=lambda cmd: cmd.command == "touch"
            and (cmd.cwd / "Alien").exists(),
        ),
        Interaction(
            """
A Stanley Kubrick masterpiece of horror. I heard that Steven King didn't like it:

**REMEMBER THE QUOTES!** 

```console
$ touch "The Shining"
```
""",
            filter=lambda cmd: cmd.command == "touch"
            and (cmd.cwd / "The Shining").exists(),
        ),
        Interaction(
            """
An animated gem:

```console
$ touch Up
```
""",
            filter=lambda cmd: cmd.command == "touch"
            and (cmd.cwd / "Up").exists(),
        ),
        Movies(stage=1),
        Interaction(
            """
# Let's Organize 

Let's put our movies in different subdirectories by genre. Let's start by 
creating a "Classics" genre:


```console
$ mkdir Classics
```
""",
            filter=lambda cmd: cmd.command == "mkdir"
            and cmd.args == ["Classics"],
        ),
        Interaction(
            """
Now move Casablanca into Classics:

```console
$ mv Casablanca Classics
```
""",
            filter=lambda cmd: cmd.command == "mv"
            and (cmd.cwd / "Classics" / "Casablanca").exists(),
        ),
        Interaction(
            """
Now move Casablanca into Classics:

```console
$ mv "The Wizard of Oz" Classics
```
""",
            filter=lambda cmd: cmd.command == "mv"
            and (cmd.cwd / "Classics" / "The Wizard of Oz").exists(),
        ),
        Interaction(
            """
Now move Forrest Gump into Classics:

```console
$ mv "Forrest Gump" Classics
```
""",
            filter=lambda cmd: cmd.command == "mv"
            and (cmd.cwd / "Classics" / "Forrest Gump").exists(),
        ),
        Interaction(
            """
Now make a Horror genre:

```console
$ mkdir Horror
```
""",
            filter=lambda cmd: cmd.command == "mkdir"
            and cmd.args == ["Horror"],
        ),
        Interaction(
            """
Now move Alien into Horror:

```console
$ mv Alien Horror
```
""",
            filter=lambda cmd: cmd.command == "mv"
            and (cmd.cwd / "Horror" / "Alien").exists(),
        ),
        Interaction(
            """
Now move The Shining into Horror:

```console
$ mv "The Shining" Horror
```
""",
            filter=lambda cmd: cmd.command == "mv"
            and (cmd.cwd / "Horror" / "The Shining").exists(),
        ),
        Interaction(
            """
Now make an Animated genre:

```console
$ mkdir Animated
```
""",
            filter=lambda cmd: cmd.command == "mkdir"
            and cmd.args == ["Animated"],
        ),
        Interaction(
            """
Now move Up into Animated:

```console
$ mv Up Animated
```
""",
            filter=lambda cmd: cmd.command == "mv"
            and (cmd.cwd / "Animated" / "Up").exists(),
        ),
        Movies(stage=2),
        Interaction(
            """
# Let's Make a Backup!

We want to make sure our movies are safe. Let's copy our movies into a backup
directory. Start by making a directory called `Backup`:

```console
$ mkdir Backup
```
""",
            filter=lambda cmd: cmd.command == "mkdir"
            and (cmd.cwd / "Backup").exists()
            and (cmd.cwd / "Backup").is_dir(),
        ),
        Interaction(
            """
Back up `Up`:

```console
$ cp Animated/Up Backup
```
""",
            filter=lambda cmd: cmd.command == "cp"
            and (cmd.cwd / "Backup" / "Up").exists(),
        ),
        Interaction(
            """
# Here's a Trick

The `*` character is the **wildcard**. You can use it to save time when you're 
copying multiple files at once.

```console
$ cp Classics/* Backup
```
""",
            filter=lambda cmd: cmd.command == "cp"
            and cmd.args[0] == "Classics/*"
            and cmd.args[1].startswith("Backup")
            and (cmd.cwd / "Backup" / "Casablanca").exists(),
        ),
        Interaction(
            """
Check out your `Backup` directory. It now contains both `Casablanca` and 
`The Wizard of Oz`:

```console
$ ls Backup
```
""",
            filter=lambda cmd: cmd.command == "ls"
            and any(["Backup" in arg for arg in cmd.args]),
        ),
        Interaction(
            """
# Copy a Directory

When you use `cp` to copy a whole directory you have to give the `-r` argument:

```console
$ cp -r Horror Backup
```
""",
            filter=lambda cmd: cmd.command == "cp"
            and "-r" in cmd.args
            and (cmd.cwd / "Backup" / "Horror").exists(),
        ),
        Interaction(
            """
# Time to Clean Up

The `rm` and `rmdir` commands delete files and directories. Let's start by 
removing the `Animated` directory. We have to make sure the directory is empty 
before we can remove it:

```console
$ rm Animated/Up
```
""",
            filter=lambda cmd: cmd.command == "rm"
            and not (cmd.cwd / "Animated" / "Up").exists(),
        ),
        Interaction(
            """
Now that the Animated directory is empty we can use `rmdir`:

```console
$ rmdir Animated
```
""",
            filter=lambda cmd: cmd.command == "rmdir"
            and not (cmd.cwd / "Animated").exists(),
        ),
        Interaction(
            """
# Dangerous use of `rm`

**WARNING!!**
**WARNING!!**
**WARNING!!**
**WARNING!!**

The `-r` flag to `rm` says "recursive". In other words the `rm -r` command will 
remove a directory and all of it's contents. Afterwards there is no way to get
your data back. So be careful! 

```console
$ rm -r Classics
```
""",
            filter=lambda cmd: cmd.command == "rm"
            and not (cmd.cwd / "Classics").exists(),
        ),
    ],
}


questions = [
    MultipleChoiceQuestion(
        "What command would you use to *rename* a file?",
        "mv",
        "cp",
        "ln -s",
        "rm",
    ),
]

lab = {
    "Sort the Islands!": [
        Islands(),
    ],
}
