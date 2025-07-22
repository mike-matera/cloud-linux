"""
Walk through for week 3: The File System
"""

import kroz
from kroz.flow.base import FlowContext, FlowResult
from kroz.flow.interaction import Interaction
from kroz.flow.question import Menu

app = kroz.KrozApp("The File System", state_file="testflow")


@app.main
def main():
    while True:
        app.score = 0
        if FlowContext.flow_status("nav-ls") == FlowResult.CORRECT:
            app.score += 10
        if FlowContext.flow_status("nav-poems") == FlowResult.CORRECT:
            app.score += 10

        choice = FlowContext.run(
            Menu(
                message="""
                # Welcome!

                This walk through will get you familiar with navigating the filesystem. 

                **Choose a journey by entering a number and pressing `Enter`**
    """,
                items=[
                    f"{FlowContext.status_icon('nav-ls')} Explore your home directory with `ls`.",
                    f"{FlowContext.status_icon('nav-poems')} Take a trip through the Poems directory.",
                ],
            )
        )

        if choice.answer and int(choice.answer) == 1:
            with FlowContext("nav-ls"):
                navigation_ls()
        elif choice.answer and int(choice.answer) == 2:
            with FlowContext("nav-poems"):
                surf_poems()


def surf_poems():
    """Use relative and absolute paths in your Poems directory."""

    app.show("""
# Explore your Poems Directory        

Relative and absolute paths.
""")


def navigation_ls():
    """Learn about ls, pwd and cd."""

    FlowContext.run(
        Interaction(
            """ 
# There's No Place Like Home

Your *home directory* is the place where you keep your personal files. It's also
the initial *working directory* of the shell when you log in over `ssh`. On opus
your home directory has files that are used as examples in the class, Including
the `Poems` directory. 

The `cd` command navigates your shell through the file system. Running `cd` with
no arguments navigates to your home directory. Start off by navigating to your 
home directory:

```console
$ cd 
```

**Before you go further you should be in your home directory.** 
""",
            lambda cmd: cmd.command == "cd" and cmd.args == [],
        )
    )

    FlowContext.run(
        Interaction(
            """ 
# Check Where You Are

Now that you're in your home directory, let's issue some commands that are
useful when you're exploring the filesystem, starting with the `pwd` command
(short for Print Working Directory). The `pwd` command shows you where you
are. Like a GPS.


```console
$ pwd
```
""",
            lambda cmd: cmd.command == "pwd" and cmd.args == [],
        )
    )

    FlowContext.run(
        Interaction(
            """ 
# Take a Look Around

Directories have *contents*, other files and directories. The `ls` (short
for List) command shows the contents of the current working directory.  Use
the `ls` command to see the contents of your home directory:

```console
$ ls
```

What do you see there?
""",
            lambda cmd: cmd.command == "ls",
        )
    )

    FlowContext.run(
        Interaction(
            """ 
# Take a Longer Look

The `ls` command has many switches that control its output. The `-l` or
*long* flag changes the output to have each file or directory on its own
line. This gives you a lot more information: 

```console
$ ls -l
```
""",
            lambda cmd: cmd.command == "ls" and "-l" in cmd.args,
        )
    )

    FlowContext.run(
        Interaction(
            """ 
# Hidden Files

Files that begin with a `.` are called *hidden files*. They're not hidden
for security purposes, they're just hidden so they don't clutter up the view
when you run the `ls` command. Using the `-a` switch tells `ls` that you
want to see hidden files. 

```console
$ ls -a
```
""",
            lambda cmd: cmd.command == "ls" and "-a" in cmd.args,
        )
    )

    FlowContext.run(
        Interaction(
            """ 
# Combining Switches

Most commands let you combine switches when it makes sense. The `-l` and
`-a` switches can both be active when you run `ls`. You could apply them
both like this:

```console
$ ls -l -a 
```

However, commands that take switches often let you combine them into a
single flag. Try running `ls` like this:

```console
$ ls -la 
```
""",
            lambda cmd: cmd.command == "ls" and "-la" in cmd.args,
        )
    )

    FlowContext.run(
        Interaction(
            """ 
# One File or Directory at a Time

The `ls` command can also be given a file or directory as an argument. When no 
argument is given `ls` shows you the current working directory. An argument 
overrides that behavior to show you any directory you want:

```console
$ ls Poems
```

Running that command shows the the `Poems` directory. 
""",
            lambda cmd: cmd.command == "ls" and "Poems" in cmd.args,
        )
    )

    FlowContext.run(
        Interaction(
            """ 
# A Tree!

The `tree` command shows you a visual representation of a directory tree. 

```console 
$ tree Poems/
Poems/
├── Angelou
│   ├── bird
│   ├── diner
│   ├── woman
│   └── you
├── ant
...
```

""",
            lambda cmd: cmd.command == "tree"
            and any(("Poems" in arg for arg in cmd.args)),
        )
    )

    return "Congratulations, your journey is complete."


if __name__ == "__main__":
    app.run()
