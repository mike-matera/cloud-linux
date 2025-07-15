"""
Testing my fun weird idea....
"""

import kroz
from kroz.interaction import interaction

app = kroz.KrozApp("Command line spy!")


@app.main
def main():
    app.show("# Welcome here is some text about stuff.")
    interaction(
        """ 
Commands are words separated by spaces. The first word is the name of the
command. Subsequent words are called arguments. A special kind of argument
called a switch or flag begins with the dash (-) character.

Try running this command in a separate shell:

```console 
$ cal
```
""",
        lambda cmd: cmd.command == "cal",
    )
    interaction(
        """ 
The cal command shows a calendar of the current month. Many UNIX commands take
the -h or --help switch as an argument. See what happens to the date command
when you add the -h option.

Try running this command in a separate shell:

```console 
$ cal -h
```
""",
        lambda cmd: cmd.command == "cal" and ["-h"] == cmd.args,
    )

    interaction(
        """ 
The cal command will show you any month or year you like. With one argument, a
year, cal prints every month in that year. With two arguments it prints just the
month that you asked for

```console 
$ cal 1980
```

```console 
$ cal december 1980
$ cal 12 1980
```

Run the command above but substitute the year and month you were born. **What
day of the week were you born on?**

""",
        lambda cmd: cmd.command == "cal" and 1925 < int(cmd.args[1]) < 2025,
    )

    interaction(
        """ 
There are many commands that show you information about the computer the shell
is running on. The `df` command displays information about disks. When you give
it the `~` argument it shows how much space is available in your home directory.
Try it to see how much is left.

```console 
$ df ~
Filesystem              1K-blocks       Used Available Use% Mounted on
/dev/mapper/crypthome2 1920748800 1025448568 797657788  57% /home
```

The output of `df` is a table. Compare the output of my computer to the one your
shell is on.
""",
        lambda cmd: cmd.command == "df" and ["~"] == cmd.args,
    )

    interaction(
        """ 
The `free` command displays information about RAM.

```console 
$ free
               total        used        free      shared  buff/cache   available
Mem:       130992164    16494376    18840136      340348    97244672   114497788
Swap:        8388604      581152     7807452
```

The output of `free` is a table. Compare the output of my computer to the one
your shell is on.
""",
        lambda cmd: cmd.command == "free" and [] == cmd.args,
    )

    interaction(
        """ 
Sometimes programs run until you ask them to exit. The `free` command can 
monitor your computer by printing updated statistics periodically. Try running 
`free` like below. Notice that the prompt doesn't come back.

```console 
$ free -s 1 -L 
```

**Press Ctrl+C to exit the program and return to the prompt.**
""",
        lambda cmd: cmd.command == "free" and cmd.result != 0,
    )

    return "Congratulations, your journey is complete."


if __name__ == "__main__":
    quit(app.run())
