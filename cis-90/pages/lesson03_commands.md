# Commands for Files and Navigation

The page has the commands for lesson 3. The commands for this lesson are: 

| Command | Action | 
| --- | --- | 
| `cat` | View a text file. |
| `cd` | Change the working directory. | 
| `ls` | List files in the working directory. | 
| `pwd` | Show the working directory. | 

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

