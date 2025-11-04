"""
# Lesson 9: File Permissions

After this lesson you should be able to:

- Understand users and groups
- Control access to files
- Change your password

Reading:

- Chapter 9

Commands:

1. `id`
1. `chmod`
1. `chgrp`
1. `umask`

"""

import grp
import os
import pwd
import textwrap
from pathlib import Path

from kroz.flow.base import KrozFlowABC
from kroz.flow.interaction import Interaction
from kroz.flow.question import MultipleChoiceQuestion, ShortAnswerQuestion
from kroz.random.path import CheckDir, CheckFile, CheckPath

from .lesson05 import Islands

title = "Working with Permissions"

state = "islands2"


class Islands2(Islands):
    """The islands with perms."""

    def setup(self):
        super().setup()
        try:
            grp.getgrnam("cis90")
            cis90_grp = "cis90"
        except KeyError:
            cis90_grp = "adm"  # for testing on my machine

        self.check_files = CheckPath(
            "Oceans",
            files=[
                CheckDir("", group=cis90_grp, perms=0o777),
                CheckDir("Pacific", group=cis90_grp, perms=0o770),
                CheckDir("Atlantic", group=cis90_grp, perms=0o550),
                CheckDir("Indian", group=cis90_grp, perms=0o700),
                CheckDir("Fictional", group=cis90_grp, perms=0o700),
            ],
        )
        for file in self.start_files.files:
            assert isinstance(file, CheckFile), "Internal error."
            if "Pacific" in file.contents:
                newpath = Path("Pacific") / file.path
                newperms = 0o660
            elif "Atlantic" in file.contents:
                newpath = Path("Atlantic") / file.path
                newperms = 0o440
            elif "Indian" in file.contents:
                newpath = Path("Indian") / file.path
                newperms = 0o600
            elif "fiction" in file.contents:
                newpath = Path("Fictional") / file.path
                newperms = 0o600
            else:
                raise ValueError("Ooops:", file.contents)
            self.check_files.files.append(
                CheckFile(
                    newpath,
                    contents=file.contents,
                    perms=newperms,
                    group=cis90_grp,
                )
            )

    @property
    def text(self):
        return textwrap.dedent("""
        # Island Permissions 
        
        I have created a directory called `Islands` with the island files from 
        the previous island assignment. For this assignment update the 
        permissions of your island files to match the following:
                               
        {}
        """).format(self.check_files.markdown(detail=True))


walks: dict[str, list[KrozFlowABC]] = {
    "What you can and can't do": [
        Interaction(
            """
UNIX was designed from the start to be an operating system that lets multiple
users share the same computer. When multiple users share the same computer there
has to be limits on what any user can do, so that users can keep their private 
data safe. File permissions in UNIX do this by specifying three groups:

1. The owner of a file or directory 
1. The group the file or directory belongs to 
1. Everyone else 

Try to access the `/etc/shadow` file using cat:

```console 
$ cat /etc/shadow 
```

What happens?
""",
            lambda cmd: cmd.command == "cat" and "/etc/shadow" in cmd.args,
        ),
        Interaction(
            """
You got an error! 

That's because regular users can't view the shadow file. Let's look at why:

```console
$ ls -l /etc/shadow 
``` 

Look closely at the permissions. 
""",
            lambda cmd: cmd.command == "ls"
            and "-l" in cmd.args
            and "/etc/shadow" in cmd.args,
        ),
        ShortAnswerQuestion("Who owns `/etc/shadow`?", "root", can_skip=False),
        ShortAnswerQuestion(
            "What group does `/etc/shadow` belong to?",
            "shadow",
            can_skip=False,
        ),
        MultipleChoiceQuestion(
            "What can you do with the `/etc/shadow` file?",
            "Nothing",
            "Read it",
            "Write it",
            "Read and Write it",
        ),
        Interaction(
            """
The `id` command shows you who you are and, importantly, what groups you belong
to. Use the `id` command like this: 

```console
$ id 
``` 

What groups are you a part of?
""",
            lambda cmd: cmd.command == "id" and cmd.args == [],
        ),
        ShortAnswerQuestion(
            "What is your primary group **ID** (a.k.a. group number)?",
            str(pwd.getpwuid(os.getuid()).pw_gid),
            can_skip=False,
        ),
    ],
    "Use chmod to change permissions.": [
        Interaction(
            """
Let's take a look at what you can accomplish with the `chmod` command. The 
`chmod` command lets you set the permissions of files that belong to you. That
way you get to decide who can do what with your files. 

To start this activity, let's go to your `~/bin` dirctory: 

```console 
$ cd ~/bin
``` 

This directory is special. You'll see why in a bit... 
""",
            lambda cmd: cmd.command == "cd"
            and cmd.cwd == Path().home() / "bin",
        ),
        Interaction(
            """
Let's look at contents of `~/bin`:

```console
$ ls -la
```
""",
            lambda cmd: cmd.command == "ls" and "-la" in cmd.args,
        ),
        Interaction(
            """
In your `~/bin` directory you'll that the files are executable, they are all 
personal commands! Try the `banner` command:

```console
$ banner hello
```
""",
            lambda cmd: cmd.command == "banner" and len(cmd.args) > 0,
        ),
        Interaction(
            """
Fun! 

The `banner` command is a program file. You can see its binary contents with the
`xxd` command. Take a look:

```console
$ xxd banner
```
""",
            lambda cmd: cmd.command == "xxd" and cmd.args == ["banner"],
        ),
        Interaction(
            """
You can take away your ability to execute the `banner` command:

```console
$ chmod u-x banner
```
""",
            lambda cmd: cmd.command == "chmod"
            and cmd.args == ["u-x", "banner"],
        ),
        Interaction(
            """
Let's check out the permissions on `banner` now:

```console
$ ls -l banner
```

Notice the change?
""",
            lambda cmd: cmd.command == "ls"
            and "-l" in cmd.args
            and "banner" in cmd.args,
        ),
        Interaction(
            """
Now try running the `banner` command again:

```console
$ banner test 1 2 3 
```
""",
            lambda cmd: cmd.command == "banner" and len(cmd.args) > 0,
        ),
        Interaction(
            """
Notice the error? 

You can take away your ability to read it too:

```console
$ chmod u-r banner
```
""",
            lambda cmd: cmd.command == "chmod"
            and cmd.args == ["u-r", "banner"],
        ),
        Interaction(
            """
Let's check out the permissions on `banner` now:

```console
$ ls -l banner
```

Notice the change?
""",
            lambda cmd: cmd.command == "ls"
            and "-l" in cmd.args
            and "banner" in cmd.args,
        ),
        Interaction(
            """
Now try to read the file again:

```console
$ xxd banner
```
""",
            lambda cmd: cmd.command == "xxd" and cmd.args == ["banner"],
        ),
        Interaction(
            """
Now `banner` is really broken! Don't worry, you can fix the permissions just as
easily as you broke them:

```console
$ chmod u+rx banner
```
""",
            lambda cmd: cmd.command == "chmod"
            and cmd.args == ["u+rx", "banner"],
        ),
        Interaction(
            """
Make sure it's fixed:

```console
$ banner test 1 2 3 
```
""",
            lambda cmd: cmd.command == "banner" and len(cmd.args) > 0,
        ),
    ],
}

questions: list[KrozFlowABC] = [
    MultipleChoiceQuestion(
        """
After running the following commands:

```console
$ ls -l somefile
-r-xr-xr-x 2 myuser adm 4096 Sep  4 15:51 somefile
$ chmod 600 somefile
```

What will *myuser* be able to do to `somefile`?
""",
        "Read and Write",
        "Read only",
        "Write only",
        "Read, Write and Execute",
        "Nothing",
    ),
    MultipleChoiceQuestion(
        """
After running the following commands:

```console
$ ls -l somefile
-r-xr-xr-x 2 myuser adm 4096 Sep  4 15:51 somefile
$ chmod 606 somefile
```

What will users in the *adm* group be able to do to `somefile`?
""",
        "Nothing",
        "Read and Write",
        "Read only",
        "Write only",
        "Read, Write and Execute",
    ),
    MultipleChoiceQuestion(
        """
After running the following commands:

```console
$ ls -ld somedir
dr-xr-xr-x 2 myuser adm 4096 Sep  4 15:51 somedir
$ chmod 400 somedir
```

What will *myuser* be able to successfully do to `somedir`?
""",
        "ls somedir",
        "Nothing",
        "cd somedir",
        "touch somedir/newfile",
        "rmdir somedir",
    ),
]

lab: dict[str, list[KrozFlowABC]] = {
    "Sort the Islands -- Part 2": [
        Islands2(),
    ],
}
