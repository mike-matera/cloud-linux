# Lesson 10 Commands

## XXXX: MOVED HERE 

## The `$PATH` Environment Variable 

Where do commands come from? Commands are files that are located in Linux's system directories. A special environment varialbe `$PATH` controls where the shell looks for commands when you enter one. Use the `echo` command to show you the path: 

```bash 
$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
```

The path is a list of directories separated by a colon (`:`). The above path has the following parts: 

| Directory | About | 
| --- | --- | 
| `/usr/local/sbin` | Extra administrator commands. | 
| `/usr/local/bin` | Extra commands. | 
| `/usr/sbin` | Administrator commands. | 
| `/usr/bin` | General commands. | 
| `/usr/games` | Games |
| `/usr/local/games` | Extra games. | 
| `/snap/bin` | Commands installed by snap packages. | 

> The `$PATH` is searched in order!

### Try This 

What happens when you delete your path? Try it.

```bash 
$ PATH="" 
``` 

Most commands are now unavailable! With no `$PATH` only shell built-in commands work. You can still use `cd`, `echo` and you can still set a variable. If you find that you have a broken `$PATH` you can fix it by ensuring *at least* the following directories are present: 

1. `/bin`
2. `/usr/bin`
3. `/sbin`
4. `/usr/sbin`

Run a command to restore your path. 


## Trapped on the Island 

During the midterm you'll login to a special server. When you login you'll find a broken path. Can you restore your path and escape the island? 

Try for yourself by logging in to: `sun-hwa-v.cis.cabrillo.edu`

<script id="asciicast-SUJNNjm8EJFd7hmO9DRn9dtXz" src="https://asciinema.org/a/SUJNNjm8EJFd7hmO9DRn9dtXz.js" async></script>


### XXX: END OF MOVE

This page has the commands for lesson 10. 

| Command | Action | 
| --- | --- | 
| `alias` | Create an alias for a command (or commands). | 
| `unalias` | Remove an alias created with `alias`. | 
| `set` | Show all variables and functions. | 
| `env` | Show all *environment* variables. | 
| `export` | Assign an environment variable. | 
| `exec` | Run a program, replacing the shell. | 
| `source` | Execute a script as if it were typed into the shell. | 

