# Your First Commands 

The page has the commands for lesson 1. The commands for this lesson are: 

| Command | Action | 
| --- | --- | 
| `cal`	| Show calendar |
| `date` | Show current time and date | 
| `df` | Show the available disk space |
| `free` | Show the available memory | 
| `clear` | Clear the terminal screen | 
| `hostname` | Show the host name of the computer being accessed |
| `who` | Shows who is currently logged in | 
| `history` | Show previous commands | 
| `ssh` | Connect and login to remote system | 
| `exit` | Terminate your shell and log off | 

## The Anatomy of a Command 

Commands are words separated by spaces. The first word is the name of the command. Subsequent words are called *arguments*. A special kind of argument called a *switch* or *flag* begins with the dash (`-`) character. 

Here's an example of a simple command with no arguments: 

```bash 
$ cal
```

The `cal` command shows a calendar of the current month. Many UNIX commands take the `-h` or `--help` switch as an argument. See what happens to the `date` command when you add the `-h` option. 

```bash
$ cal -h 
``` 

The `cal` command will show you any month or year you like. With one argument, a year, `cal` prints every month in that year: 

```bash
$ cal 1976
```

Run the command above but substitute the year you were born. What day were you born on? Commands can take any number of arguments. You can add a month to the `cal` command to print only a particular month in a year. This example prints the calendar for January 2030: 

```bash
$ cal 01 2030
```

## Using SSH to Connect to Another Computer 

The Secure Shell (`ssh`) command connects your terminal to another computer. When your terminal is connected the commands you issue will be run on the remote machine. The `exit` command ends the connection. The `ssh` command works on Windows (10 and above), Mac and Linux. The `ssh` command works like this:

```bash
$ ssh <user-name>@<computer-name>
```

For example, this command logs me into opus.

```bash
$ ssh mmatera@opus.cis.cabrillo.edu 
```

> **Note:** This semester we're using `opus.cis.cabrillo.edu` not `opus3`. 

Here's a of how I login to opus3: 

<script id="asciicast-nWkxAMoq8WWTBXR16HaVUarwy" src="https://asciinema.org/a/nWkxAMoq8WWTBXR16HaVUarwy.js" async></script>


