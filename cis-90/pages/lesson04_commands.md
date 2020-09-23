# Viewing File Contents and Metadata

The page has the commands for lesson 4. The commands for this lesson are: 

| Command | Action | 
| --- | --- | 
| `file` | View the type of the file. (e.g. JPEG, text) | 
| `cat` | View a text file. |
| `more` | View a large text file one page at a time. |  
| `less` | View a large text file using scrolling. `less` is an improved version of `more`. | 
| `head` | View the first few lines of a text file. | 
| `tail` | View the last few lines of a text file. | 
| `wc` | Count the lines in a text file. | 
| `xxd` | View the contents of a binary file. | 

## The Current Directory 

> **There's no place like home**!<br>
> Running `cd` with no arguments takes you to your home directory. 

When you use the file tool on your operating system the graphics on the screen show you files and folders at the same time and you pick what you want. On the command line you navigate folders by "walking" from one directory to another. The key concept that you have to remember is that of the `working directory`. That's the folder you're working in. Think of it like the place you're standing. 

To help you understand the place you are standing let's play a game from my childhood: [Beyond Zork: The Coconut of Quendor](https://archive.org/details/msdos_Beyond_Zork_-_The_Coconut_of_Quendor_1987)

In the game you walk from place to place. The graphic on the screen helps you see the effect of moving in different directions. When you use the command line the `cd` command moves you from place to place, the `ls` command shows you what's around and the `pwd` command shows you where you are. 

<script id="asciicast-8J4im3LsMAByO4z0YRjV44Prm" src="https://asciinema.org/a/8J4im3LsMAByO4z0YRjV44Prm.js" async></script>

## Arguments and File Names 

Many commands take arguments that contains the name of a file or a directory. So how you do you tell a command like `cat` where to find a file? In the previous example we named a file in the *current directory* and cat showed us the contents. Try this starting in your home directory.

```bash
$ cd
$ cd Poems 
$ cd Angelou
$ cat bird 
```

But what if we want to print the bird file from another place? There are two options. 

### Relative Paths 

A relative path is tells a command how to find a file starting from the current directory. 

```bash
$ cd
$ cat Poems/Angelou/bird 
```

In the example you start in the in your home directory. The relative path to a file changes when you change directories. Here are a few different ways to print the contents of the `bird` poem. Try running these commands: 

```bash 
$ cd 
$ cat Poems/Angelou/bird 
$ cd Poems 
$ cat Angelou/bird 
$ cd Angelou
$ cat bird
```

The special directory `..` refers to the directory *above* the current directory. Start from the `Angelou` directory and try the following commands: 

```bash
$ ls .. 
$ ls ../..
$ ls ../../..
```

### Absolute Paths 

Absolute paths are not relative to the current working directory. Absolute paths begin with the `/` character which signifies the root directory. The `pwd` command always shows you an absolute path:

```bash
$ pwd
/home/cis90/simben90
```

Here's the absolute path of my `bird` poem: 

```
$ cat /home/cis90/simben90/Poems/Angelou/bird 
```

The nice thing about an absolute path is that it works no matter where you are. The down side is that they are generally longer than a relative path. 

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

