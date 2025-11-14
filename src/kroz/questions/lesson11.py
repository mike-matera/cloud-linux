"""
# Lesson 11: The Environment

After this lesson you should be able to:

- Read and set environment variables
- Understand $PATH

Reading:

- Chapter 11
"""

from kroz.flow.base import KrozFlowABC
from kroz.flow.interaction import Interaction
from kroz.flow.question import MultipleChoiceQuestion

title = "The Environment"

state = "env"

walks: dict[str, list[KrozFlowABC]] = {
    "Variables and Environment Variables": [
        Interaction(
            """
# Setting Variables 
                    
There are two kinds of variables in the shell, regular variables and *environment* variables. 
In this walkthrough we'll examine both. Start by setting a regular variable:

```console
$ regvar="regular"
```
""",
            filter=lambda cmd: cmd.command == 'regvar="regular"'
            or cmd.command == "regvar=regular",
        ),
        Interaction(
            """
Now let's set an environment variable:

```conosle
$ export envvar="environment"
```
""",
            filter=lambda cmd: cmd.command == "export"
            and 'envvar="environment"' in cmd.args
            or "envvar=environment" in cmd.args,
        ),
        Interaction(
            """
Check that they both exist:

```conosle
$ echo regular: $regvar 
$ echo env: $envvar
```
""",
            filter=[
                lambda cmd: cmd.command == "echo" and "$regvar" in cmd.args,
                lambda cmd: cmd.command == "echo" and "$envvar" in cmd.args,
            ],
        ),
        Interaction(
            """
Now start a new shell. In your new shell check the variables. Exit your new shell
afterwards.

```conosle
$ bash
$ echo regular: $regvar 
$ echo env: $envvar
$ exit
```
""",
            filter=lambda cmd: cmd.command == "exit",
        ),
    ]
}

questions: list[KrozFlowABC] = [
    MultipleChoiceQuestion(
        """What is the output of:
        ```
        foo = hello 
        echo $foo
        ```
        """,
        "It's an error",
        "`hello`",
        "`foo`",
        "`$foo`",
    ),
    MultipleChoiceQuestion(
        """What is the output of:
        ```
        foo=hello
        echo $foo
        ```
        """,
        "`hello`",
        "It's an error",
        "`foo`",
        "`$foo`",
    ),
]

lab: dict[str, list[KrozFlowABC]] = {}
