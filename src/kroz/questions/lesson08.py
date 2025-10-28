"""
# Lesson 8: Like a Boss

After this lesson you should be able to:

- Use wildcards
- Use quotes to change the meaning of a command
- Go faster with tab completion

Reading:

- Chapters 7 and 8

"""

import getpass
import pathlib

from kroz.app import KrozApp
from kroz.flow.base import KrozFlowABC
from kroz.flow.interaction import Interaction
from kroz.flow.question import (
    MultipleChoiceQuestion,
    Question,
)
from kroz.random.bigdir import random_directory
from kroz.random.words import random_words

title = "Like a Boss!"

state = "theboss"


class RandomRando(Question):
    """Random directory stuff"""

    placeholder = "Enter to continue."

    text = """
    # Remove the "m" Files

    I have just (re)created a directory called "Random" in your home directory.
    Remove all files with names that start with the letter "m" (lower case). """

    def setup(self):
        self._rd = random_directory(500)
        self._rd.setup()

    def cleanup(self):
        self._rd.cleanup()

    def check(self, answer):
        target = self._rd.filter(lambda x: not str(x.path).startswith("m"))
        target.full_report(verbose=2)


class RandomRandoTick(Question):
    """Random directory stuff"""

    placeholder = "Enter to continue."

    text = """
    # Remove the "'" Files

    Remove all files with names that contain a single quote (') character. 
    """

    def setup(self):
        self._rd = random_directory(500)
        self._rd.setup()

    def cleanup(self):
        self._rd.cleanup()

    def check(self, answer):
        target = self._rd.filter(lambda x: "'" not in str(x.path))
        target.full_report(verbose=2)


class RandomDeleteMe(Question):
    """Random directory stuff"""

    placeholder = "Enter to continue."

    text = """
    # Remove the "'" Files

    Remove all files that contain the word "delete" in them. 
    """

    def setup(self):
        self._rd = random_directory(500)
        self._rd.setup()

    def cleanup(self):
        self._rd.cleanup()

    def check(self, answer):
        target = self._rd.filter(lambda x: "delete" not in str(x.contents))
        target.full_report(verbose=2)


class DeepMessage(Question):
    placeholder = "What is the secret word?"

    text = """
    # Deep Directory 

    Look in ~/Files and find the hidden message.
    """

    def setup(self):
        self._answer = random_words().choice()
        path = KrozApp.appconfig("default_path") / pathlib.Path(
            "Files/deep/there's/a/light/over/at/the/Frankenstein/place/there's/a/li/ii/ii/ii/ii/ii/ii/ight/burning/in/the/fire/place"
        )
        file = path / ".secret"
        path.mkdir(parents=True, exist_ok=True)
        with open(file.resolve(), "w") as fh:
            fh.write(self._answer + "\n")

    def check(self, answer):
        assert answer.strip() == self._answer, """That's not correct!"""


walks: dict[str, list[KrozFlowABC]] = {
    """Go wildcard!""": [
        Interaction(
            """
# Using Wildcard to Select Files 

In this walk through you'll use the `*` and `?` characters to have the shell 
*substitute* those characters onto your command line. Once you get the hang of 
globbing you'll be able to work faster and better. 

Let's start by going to your `~/Poems` directory:

```console
$ cd ~/Poems
```
                    """,
            filter=lambda cmd: cmd.command == "cd"
            and cmd.cwd == pathlib.Path().home() / "Poems",
        ),
        Interaction(
            """
# The Star 

The star `*` character is a wildcard that matches *zero or more* characters in a
file name. For example this shows us information about any file that starts with
the letter `s` in the `Shakespeare` directory:

```console
$ ls -l Shakespeare/s*
```
                    """,
            filter=lambda cmd: cmd.command == "ls"
            and cmd.args[-1] == "Shakespeare/s*",
        ),
        Interaction(
            """
The `*` can be in any position. This command finds the files that end in the 
number `5`:

```console
$ ls -l Shakespeare/*5
```
                    """,
            filter=lambda cmd: cmd.command == "ls"
            and cmd.args[-1] == "Shakespeare/*5",
        ),
        Interaction(
            """
You can have multiple `*`s. This command finds the files that have the number
`1` anywhere in the name: 

```console
$ ls -l Shakespeare/*1*
```
                    """,
            filter=lambda cmd: cmd.command == "ls"
            and cmd.args[-1] == "Shakespeare/*1*",
        ),
        Interaction(
            """
# The `?` is More Restrictive 

The `?` wildcard character matches *zero or one* character in the name of a
file. If you want to see `sonnet10` but not `sonnet1` you can use the `?` like
this:

```console
$ ls -l Shakespeare/sonnet1?
```
                    """,
            filter=lambda cmd: cmd.command == "ls"
            and cmd.args[-1] == "Shakespeare/sonnet1?",
        ),
    ],
    """Command substitution""": [
        Interaction(
            """
# Command Substitution 

Command substitution takes the output of a command and puts it on the command
line. It's similar to a pipe, but a pipe connects streams. It can be a bit
confusing at first. So let's try a few examples. 

This command takes the output of `ls` and puts it on the command line for `echo`:

```console
$ echo $(ls)
```

Notice how echo shows the names of files in the current directory.
""",
            filter=lambda cmd: cmd.command == "echo" and cmd.args == ["$(ls)"],
        ),
        Interaction(
            """
Here's a more practical example. The `which` command shows you the location of 
a command. Here's how to find the location of the `cp` command:

```console
$ which cp
/usr/bin/cp
```

What if we wanted to know more information about `cp`? We could use `ls`:

```console 
$ ls -l /usr/bin/cp 
-rwxr-xr-x 1 root root 141848 Apr  5  2024 /usr/bin/cp
``` 

But, we can do it in a single step with command substitution: 

```console
$ ls -l $(which cp)
```

***Run all three commands in this example.*** 
""",
            filter=[
                lambda cmd: cmd.command == "which" and cmd.args == ["cp"],
                lambda cmd: cmd.command == "ls"
                and "-l" in cmd.args
                and "/usr/bin/cp" in cmd.args,
                lambda cmd: cmd.command == "ls"
                and "-l" in cmd.args
                and cmd.line.endswith("$(which cp)"),
            ],
        ),
    ],
    "Can I quote you on that?": [
        Interaction(
            """
# Quotes and Quoting 

Quotes change the way the shell interprets special characters. For example, 
without quotes the shell treats all consecutive spaces as a single space:

```console 
$ echo This is a                test
This is a test
```

Enter an `echo` and put lots of spaces in the argument.
""",
            filter=[lambda cmd: cmd.command == "echo"],
        ),
        Interaction(
            """
When the spaces are *inside* quotes they lose their special meaning:

```console 
$ echo "This is a                test"
This is a                test
```

Put quotes around the arguments of your last command.
""",
            filter=[lambda cmd: cmd.command == "echo"],
        ),
        Interaction(
            f"""
Double quotes allow some of the shell's special characters to still work. For  
example, the dollar sign `$` keeps its meaning:

```console 
$ echo "My name is $USER"
My name is {getpass.getuser()}
```
""",
            filter=[
                lambda cmd: cmd.command == "echo"
                and any(["$USER" in x for x in cmd.args])
            ],
        ),
        Interaction(
            """
Single quotes are stronger. They don't let anything have a special meaning:

```console 
$ echo 'My name is $USER'
My name is $USER
```
""",
            filter=[
                lambda cmd: cmd.command == "echo"
                and any(["$USER'" in x for x in cmd.args])
            ],
        ),
        Interaction(
            """
It's possible to quote *just one character* with the backslash `\\` character.
Here's an example where the backslash only applies to the `$` character:

```console 
$ echo My name is \\$USER
My name is $USER
```
""",
            filter=[
                lambda cmd: cmd.command == "echo"
                and cmd.line.endswith("\\$USER")
            ],
        ),
        Interaction(
            """
Here's a practical example that will help you later. The `\\` can take the 
meaning away from the single quote. To see all the files that contain a `'` you
can use the `*` like this:

```console 
$ ls *\\'*
```
""",
            filter=[lambda cmd: cmd.command == "ls" and "*\\'*" in cmd.args],
        ),
    ],
}

questions: list[KrozFlowABC] = [
    MultipleChoiceQuestion(
        "What key sequence moves the cursor to the *beginning* of the line?",
        "Ctrl-a",
        "Ctrl-c",
        "Ctrl-d",
        "Alt-a",
    ),
    MultipleChoiceQuestion(
        "What key sequence moves the cursor to the *end* of the line?",
        "Ctrl-e",
        "Ctrl-c",
        "Ctrl-d",
        "Alt-a",
    ),
    MultipleChoiceQuestion(
        "What causes the shell to suggest a completion?",
        "Tab",
        "Ctrl-c",
        "Ctrl-d",
        "Alt-c",
    ),
    MultipleChoiceQuestion(
        "What keys visit your command history?",
        "Up and Down",
        "PageUp and PageDown",
        "Shift-Up and Shift-Down",
        "Tab Tab",
    ),
]

lab: dict[str, list[KrozFlowABC]] = {
    "Delete the `m` files.": [RandomRando()],
    "A harder filename to delete.": [RandomRandoTick()],
    "Delete files that contain `delete`.": [RandomDeleteMe()],
    "Find the deep meaning.": [DeepMessage()],
}
