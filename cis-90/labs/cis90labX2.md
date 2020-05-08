# Extra Credit Lab: Pathnames

## Objectives

This lab will give you additional practice using *relative* an *absolute* pathnames as arguments on various Linux commands.

## Procedure

There is a tarball named `dogs.tar` in the `/home/cis90/depot` directory. Copy this file to your home directory and extract the files using:

```bash
$ cd
$ cp ../depot/dogs.tar .
$ tar -xvf dogs.tar
```

You should now have a new `dogs` directory. Use the `tree` command to verify you have unpacked the files successfully:

```
$ tree dogs
dogs
├── England
│   ├── Austen
│   │   ├── author
│   │   ├── Persuasion
│   │   └── Sensibility
│   └── Shakespeare
│       ├── author
│       ├── Caesar
│       ├── Hamlet
│       └── Romeo
├── France
│   └── Verne
│       ├── author
│       ├── Island
│       └── Moon
├── Germany
│   ├── Goethe
│   │   ├── author
│   │   ├── Faust
│   │   └── Lament
│   └── Kafka
│       ├── author
│       └── Trial
├── Greece
│   ├── Aesop
│   │   ├── Ass
│   │   ├── author
│   │   ├── Fox
│   │   └── Shadow
│   └── Plato
│       ├── Apology
│       ├── author
│       └── Phaedo
├── Italy
│   └── Machiavelli
│       ├── author
│       └── War
├── readme
├── Russia
│   └── Tolstoy
│       ├── Anna
│       ├── author
│       └── Murad
├── Spain
│   └── Cervantes
│       ├── author
│       ├── Estramaduran
│       └── Quixote
├── Ukraine
│   └── Chekhov
│       ├── Art
│       ├── author
│       ├── Boys
│       ├── Dependents
│       └── Wife
└── USA
    ├── Alcott
    │   ├── author
    │   ├── Boys
    │   ├── Rose
    │   └── Women
    ├── Burroughs
    │   ├── author
    │   ├── Mars
    │   ├── Oakdale
    │   └── Tarzan
    ├── Dickinson
    │   ├── author
    │   ├── Home
    │   └── Sea
    └── Twain
        ├── author
        ├── Italian
        ├── Race
        └── Tale

24 directories, 51 files
```

This is a collection of literature excerpts that mention dogs in one way or another. Notice that the `dogs` directory contains directories named after countries. Each country directory had directories named after authors. Each author directory has files containing works or excerpts from that author. Each author directory also has a file named `author`, containing the name, birth year, death year, and country for that author.

Create a file named `labx2`. For each step in the lab you will construct a command and record it, one command per line in `labx2`. Preface each command with a tag to indicate the step. The tag should be the step number in parenthesis. Each command should fit on one line and not contain any semicolons. Your `labx2` file should have exactly 30 lines and look like the following:

```
(1) your command goes here
(2) your command goes here
(3) your command goes here
(4) your command goes here
(5) your command goes here
(6) your command goes here
(7) your command goes here
(8) your command goes here
(9) your command goes here
(10) your command goes here
(11) your command goes here
(12) your command goes here
(13) your command goes here
(14) your command goes here
(15) your command goes here
(16) your command goes here
(17) your command goes here
(18) your command goes here
(19) your command goes here
(20) your command goes here
(21) your command goes here
(22) your command goes here
(23) your command goes here
(24) your command goes here
(25) your command goes here
(26) your command goes here
(27) your command goes here
(28) your command goes here
(29) your command goes here
(30) your command goes here
```

You may find it helpful to have three Opus3 sessions running. In the first session display the output from the `tree` command on the `dogs` directory for quick reference. In a second session, use `vi` to record your commands in the `labx2` file, and in the third session test the commands you create.

## Review

- A way is needed to uniquely specify files and directories in the UNIX/Linux file tree. Because there can be more than one file with the same name just specifying the filename on a command would be ambiguous. *Absolute* and *relative* pathnames solve this need.

- The top or "root" of the file tree is the `/` directory. By typing `ls /` you can view the standard top level directories of the UNIX/Linux file tree.

- An *absolute* pathname specifies the location of a file or directory relative to the top of the Unix file tree. An *absolute* pathname specifies the complete path starting from `/` (the top or "root" of the file tree) all the way to the file or directory being specified. *Absolute* pathnames always start with a `/` and contain no spaces.

- A *relative* pathname specifies the location of a file or directory *relative* to the current working directory. The current working directory changes every time you change directories using the `cd` command. A *relative* pathname specifies the complete path starting from the current working directory all the way to the file or directory being specified. *Relative* pathnames never start with a `/` and contain no spaces.

- The `pwd` command will show you where you are in the UNIX/Linux file tree by displaying the current working directory. The current working directory is the starting point for all *relative* pathnames.

- Tip: To verify if a pathname is correct, use it as an argument to the `ls` command. If you are specifying a file the `ls` command will print the name of the target file only if the pathname is correct. Same goes for directories however, the `-d` option must be used so the ls command will display the name of the target directory rather than its contents.

- Correct pathnames are required as arguments to commands that work with files such as `mv`, `cp`, `ls`, `cd`, `head`, `tail`, `rm`, etc.

- The `.` directory means "here". It is hard linked to the current directory you are in. You may use `.` below when asked for a *relative* path.

- The `..` directory is the parent of the current directory. It is implemented as a hard link. You may use `..` when asked for a *relative* pathname below. Use it to work your way up the tree towards the top or "root" of the tree.

- The `~` directory is shorthand for the user's home directory. Don't use it below when asked for an *absolute* path since it changes based on the user.

- Example: the *absolute* pathname to the `sonnet1` file in Benji's `Shakespeare` directory is:

    ```
    /home/cis90/simben/poems/Shakespeare/sonnet1
    ```

    Note that this is like giving someone walking instructions from the top of the tree all the way to the specific `sonnet1` file in Benji's `Shakespeare` directory.

- Example: two *relative* pathnames to the `sonnet1` file in Benji's `Shakespeare` directory from `/home/mmatera` are:

    ```
    ../cis90/simben/poems/Shakespeare/sonnet1
    ../../boot/grub/../../home/cis90/simben/poems/Shakespeare/sonnet1
    ```

    Note that this is like giving someone walking instructions from their current location on the tree all the way to the specific `sonnet1` file in Benji's directory. Note: it doesn't have to be the shortest path just a complete path.

- Example: the *relative* pathname to the `sonnet1` file in Benji's `Shakespeare` directory from his `Shakespeare` directory is:

    ```
    sonnet1
    ```

- Use Tab completes to verify the pathname you are typing is correct. Press the Tab key once to see if enough characters have been typed to complete the current file name. Press the Tab key twice to show all the current possibilities. If there is no completion or possibilities you are most likely off in the weeds and not typing a correct pathname.

## Using absolute and relative pathnames

1) From your home directory, what `ls` command would show the permissions on the Linux kernel file `vmlinuz-*` On Opus, this file resides in the `/boot` directory. On your `ls` command, specify the Linux kernel using an *absolute* pathname.

2) From your home directory, what `ls` command would show the permissions on the `passwd` file where all user accounts are kept? This `passwd` file resides in the `/etc` directory. On your `ls` command, specify this `passwd` file using an *absolute* pathname.

3) From your home directory, what `ls` command would show the permissions on the `/etc` directory itself (and no other directories)? On your `ls` command, specify this particular `etc` directory using an *absolute* pathname and be sure to use the `-d` option.

4) From your home directory, what `cd` command would change to the top, "root", directory of the UNIX/Linux file tree? On your `cd` command, use a *relative* pathname to specify the top directory of the file tree.

5) From the top of the file tree, what `file` command would probe the `passwd` file where all user accounts are kept? This `passwd` file resides in the `/etc` directory. On your `file` command, specify this `passwd` file using a *relative* pathname that does not start with the "." character.

6) From the top of the file tree, what `ls` command would show the owners of all files in the `/dev/pts/` directory? On your `ls` command, use a *relative* pathname and one filename expansion (globbing) character.

7) From the top of the file tree, what `cd` command would change to the new `dogs` directory in your home directory? Use an *absolute* pathname to specify your `dogs` directory.

8) From your `dogs` directory, what `tree` command diagrams the `Italy` and `Germany` directories? Specify both directories with *relative* pathnames.

9) Again from your `dogs` directory, what `ls` command does a long, recursive listing showing inode numbers of the `Ukraine` directory? Specify the `Ukraine` directory using an *absolute* pathname.

10) Still from your `dogs` directory, what `head` command would list the first 2 lines of the Austen's `Persuasion` and Chekhov's `Wife` files? Use *relative* pathnames for both `Persuasion` and `Wife`.

11) Again from your `dogs` directory, what `head` command would list the first 2 lines of Burroughs' `Tarzan` and `Mars` files? Use an *absolute* pathname for the `Tarzan` file. Use a *relative* pathname for the `Mars` file that does not start with the "." character.

12) From your `dogs` directory, what `cd` command would change to the `Plato` directory (in Greece)? Use a *relative* pathname to specify the `Plato` directory that does not start with the "." character.

13) From the `Plato` directory, what `chmod` command would change the permissions on the `Ukraine` and `USA` directories to 744? Use a *relative* pathname with the wildcard \* meta-character to specify just the `USA` and `Ukraine` directories. You must also use the `-v` option (for verbose) which outputs the changes made.

14) From the `Plato` directory, what `ls` command would do a long listing on the `passwd` file in the `/etc` directory? Use an *absolute* pathname for the `passwd` file.

15) From the `Plato` directory, what `ls` command would do a long listing on the `passwd` file in the `/etc` directory? Use a *relative* pathname for the `passwd` file.

16) From the `Plato` directory, what `cd` command would change to the `France` directory? Use an *absolute* pathname to specify the `France` directory.

17) From the `France` directory, what `cp` command would copy Machiavelli's `War` to the `France` directory? Use *relative* pathnames to specify the Machiavelli's `War` and the `France` directory. Use the `-v` option to show what gets copied.

18) From the `France` directory, what `cp` command would copy Kafka's `Trial` to the `Cervantes` directory? Use *relative* pathnames to specify the `Trial` file and the `Cervantes` directory. Use the `-v` option to show what gets copied.

19) From the `France` directory, what `cp` command would copy Verne's `Moon` and Tolstoy's `Murad` to the `Cervantes` directory? Use a *relative* pathname to specify the `Moon` file that does not start with the "." character. Use a *relative* pathname for the `Cervantes` directory. Use an *absolute* pathname to specify the `Murad` file. Use the `-v` option to show what gets copied.

20) From the `France` directory, what `rm` command would remove the four files copied in steps 17-19 from the `France` and `Cervantes` directories? That is, remove the `War` file from `France` and the `Moon`, `Murad` and `Trial` files from the `Cervantes` directory. Use only *relative* pathnames and the `-v` option to show what gets removed. Use the `[]` and `*` meta-characters to specify all the files in `Cervantes` you want to delete.

21) From the `France` directory, what `cat` command would cat the `author` file in the `Verne` directory? Use a *relative* pathname for the `author` file.

22) From the `France` directory, what `cat` command would cat the `author` file in the Verne directory? Use an *absolute* pathname for the `author` file.

23) From the `France` directory, what `cat` command would cat the `author` files in the `USA``Alcott, Burroughs, Dickinson` and `Twain` directories? Use a *relative* pathname with the \* wildcard meta-character.

24) From the `France` directory, what `cd` command with an argument would change back to your home directory? Specify your home directory using a *relative* pathname that starts with the .. directory.

25) From your home directory, what non-recursive `grep` command would find all lines containing the string "dog" in all the works by the Ukrainian author Chekhov? Use a *relative* pathname with the wildcard \* meta-character to match each of his works.

26) From your home directory, what non-recursive `grep` command would find all lines containing the word dog in all the works of all the German authors? Use a *relative* pathname with the wildcard \* meta-character to match both authors and works.

27) From your home directory, what `cat` command would print all the files named `author` in all the directories under the `dogs` directory? Use an *absolute* pathname with the wildcard \* meta-character to match all country directories and author directories.

28) From your home directory, what `find` command would list all the directories (not regular files) in your `dogs` directory and down? Use a *relative* pathname to your `dogs` directory.

29) From your home directory, what `cp` command would copy /etc/passwd and Burroughs' `Oakdale` file to your home directory? Use *relative* pathnames for your home directory and the `Oakdale` file. Use an *absolute* pathname for the `passwd` file. Use the `-v` option (verbose) to show what gets copied.

30) From your home directory, what `rm` command would remove the `passwd` and `Oakdale` files from your home directory? Use *relative* pathnames and the `-v` option (verbose) to show what gets removed that do not start with the "." character.

## To turn in

Submit your final version of `labx2` as follows:

```bash
$ cp labx2 /home/rsimms/turnin/cis90/labx2.$LOGNAME
```
