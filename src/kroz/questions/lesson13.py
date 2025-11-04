"""
# Lesson 13: Scripting and Startup

After this lesson you should be able to:

- Write a shell script
- Control the startup environment
- Create aliases

Reading:

- Chapter 24
"""

from kroz.flow.base import KrozFlowABC
from kroz.flow.interaction import Interaction

title = "Scripting and Startup"

state = "script"

walks: dict[str, list[KrozFlowABC]] = {
    "Look at the Environment": [
        Interaction(
            """
# Looking at the Environment

There are a number of variables in the environment. To see them all use the 
`printenv` command. 

```console
$ printenv 
```
                    """,
            lambda cmd: cmd.command == "printenv",
        ),
        Interaction(
            """
The `printenv` command can print a single variable too:

```console
$ printenv USER
```
                    """,
            lambda cmd: cmd.command == "printenv" and cmd.args == ["USER"],
        ),
        Interaction(
            """
There are a lot more variables than just environment variables. To see all of 
the available variables use the `set` command. The `set` command produces a lot 
of output because it shows not only variables but stored functions. 

```console
$ set | less
```
                    """,
            lambda cmd: cmd[0].command == "set" and cmd[1].command == "less",
        ),
        Interaction(
            """
The `echo` command is also a great way to look at a variable. When you use `echo`
you have to remember to use the dollar sign so that the substitution happens:

```console
$ echo $HOME
```
                    """,
            lambda cmd: cmd.command == "echo" and cmd.args == ["$HOME"],
        ),
        Interaction(
            """
Aliases aren't shown by set. If you want to see your aliases use the `alias` 
command:

```console
$ alias
```
                    """,
            lambda cmd: cmd.command == "alias",
        ),
    ],
    "Set a variable and make an alias": [
        Interaction(
            """
Aliases aren't shown by set. If you want to see your aliases use the `alias` 
command:

```console
$ alias
```
                    """,
            lambda cmd: cmd.command == "alias",
        ),
    ],
}

questions: list[KrozFlowABC] = []

lab: dict[str, list[KrozFlowABC]] = {}
