"""
# Lesson 6: Commands and Getting Help

After this lesson you should be able to:

- Identify a command
- Use the manual
- Create an alias

Reading:

- Chapter 5

Commands:

1. `type`
1. `man`
1. `alias`
"""

from kroz.flow.base import KrozFlowABC
from kroz.flow.question import (
    MultipleChoiceQuestion,
    ShortAnswerQuestion,
    TrueOrFalseQuestion,
)

title = "Getting Help"

state = "rtfm"

walks: dict[str, list[KrozFlowABC]] = {}


questions: list[KrozFlowABC] = [
    MultipleChoiceQuestion(
        """According to the book what is the most brutal man page of them all?""",
        "bash",
        "cat",
        "mount",
        "lvcreate",
    ),
    TrueOrFalseQuestion(
        "Manual pages on the web are more relevant than the ones on the system.",
        False,
    ),
    MultipleChoiceQuestion(
        """
Here is the help for a command:

```
mycommand [-t] [-v] name...
```

Which is of the following is true of this command:
""",
        "You must supply one or more `name` arguments",
        "The `-t` argument is required",
        "The `-v` argument is required",
        "The -h shows you command help",
    ),
    MultipleChoiceQuestion(
        """
Here is the help for a command:

```
mycommand {-t|-v} [name...]
```

Which is of the following is true of this command:
""",
        "One of `-t` or `-v` is required (but not both)",
        "You must supply one or more `name` arguments",
        "The `-t` argument is required",
        "The `-v` argument is required",
    ),
    MultipleChoiceQuestion(
        """
Here is the help for a command:

```
mycommand [-t|-v] [name]
```

Which is of the following is true of this command:
""",
        "It can be executed with no arguments",
        "You must supply one or more `name` arguments",
        "The `-t` argument is required",
        "The `-v` argument is required",
    ),
    MultipleChoiceQuestion(
        """
Here is the help for a command:

```
mycommand [-t|-v] name
mycommand -x name
```

Which is of the following is true of this command:
""",
        "It has two forms, one with `-x` and one without",
        "The `name` argument is optional",
        "The `-x` argument is required",
        "The `-t` argument is required",
    ),
]

lab: dict[str, list[KrozFlowABC]] = {
    "Enable X11 forwarding in SSH": [
        ShortAnswerQuestion(
            """What option in SSH enables X11 forwarding?""",
            "-X",
            help="Capitalization matters!",
        ),
    ],
    "Debugging in SSH": [
        ShortAnswerQuestion(
            """What option in SSH the maximum level of debugging?""",
            "-vvv",
            help="""
# Repeated Flags 

Sometimes repeating a flag give you *more* of that flag. For example if a 
command accepts `-a` it may also accept `-aa` to do the more of the same thing.
Look in the SSH manual for the flag that enables debugging and repeat it the 
maximum number of times. 
""",
        ),
    ],
    "Use an alternate key file.": [
        ShortAnswerQuestion(
            """
What arguments would you give to SSH to tell it to use `~/my_key` as an
*identity file* (a.k.a. private key). 
            """,
            "-i ~/my_key",
            help="""
# A Flag With Options 

Flags can have options. For example the SSH has the `-l` option where you can 
specify your username on the remote system. You would use it like this:

```console
$ ssh -l mich431 opus.cis.cabrillo.edu
```

When `-l` is on the command line the next argument will be interpreted as the 
name of a user. It's an error to omit the argument to `-l`. 
""",
        ),
    ],
    "Use SSH to run a command remotely.": [
        ShortAnswerQuestion(
            """
# SSH is Awesome 

Sometimes you just want to run a single command or script on a remote system 
instead of logging in. SSH lets you do that by placing a UNIX command as the 
last thing on the SSH command line. For example, You can just run `ls` on opus
from your home computer like this:

```console
MyComputer> ssh opus.cis.cabrillo.edu ls 
```

What command, when run from your home computer, runs the `top` program on opus?
""",
            "ssh -t opus.cis.cabrillo.edu top",
            help="""
# What's Missing? 

Run the `top` program in an interactive login and you can see that it's an 
interactive program. SSH needs an extra argument to run interactive programs 
directly. **Google it**. 
""",
        )
    ],
}
