# Lab X2: Pathnames - Extra Credit Lab

**Objectives**

This lab will give you additional practice using **relative** an **absolute** pathnames as arguments on various Linux commands.

**Forum**

Browse to: [http://opus-ii.cis.cabrillo.edu/forum/](http://opus-ii.cis.cabrillo.edu/forum/)

Check the forum for any late breaking news about this lab. The forum is also the place to go if you get stuck, have a question or want to share something you have learned about this lab.

**Procedure**

There is a tarball named _dogs.tar_ in the _/home/cis90/depot_ directory. Copy this file to your home directory and extract the files using:

**cd**

**cp ../depot/dogs.tar .**

**tar -xvf dogs.tar**

You should now have a new _dogs_ directory. Use the **tree** command to verify you have unpacked the files successfully:

/home/cis90/simben $ tree dogs

dogs

|-- England

| |-- Austen

| | |-- Persuasion

| | |-- Sensibility

| | `-- author

| `-- Shakespeare

| |-- Caesar

| |-- Hamlet

| |-- Romeo

| `-- author

|-- France

| `-- Verne

| |-- Island

| |-- Moon

| `-- author

|-- Germany

| |-- Goethe

| | |-- Faust

| | |-- Lament

| | `-- author

| `-- Kafka

| |-- Trial

| `-- author

|-- Greece

| |-- Aesop

| | |-- Ass

| | |-- Fox

| | |-- Shadow

| | `-- author

| `-- Plato

| |-- Apology

| |-- Phaedo

| `-- author

|-- Italy

| `-- Machiavelli

| |-- War

| `-- author

|-- Russia

| `-- Tolstoy

| |-- Anna

| |-- Murad

| `-- author

|-- Spain

| `-- Cervantes

| |-- Estramaduran

| |-- Quixote

| `-- author

|-- USA

| |-- Alcott

| | |-- Boys

| | |-- Rose

| | |-- Women

| | `-- author

| |-- Burroughs

| | |-- Mars

| | |-- Oakdale

| | |-- Tarzan

| | `-- author

| |-- Dickinson

| | |-- Home

| | |-- Sea

| | `-- author

| `-- Twain

| |-- Italian

| |-- Race

| |-- Tale

| `-- author

|-- Ukraine

| `-- Chekhov

| |-- Art

| |-- Boys

| |-- Dependents

| |-- Wife

| `-- author

`-- readme

24 directories, 51 files

This is a collection of literature excerpts that mention dogs in one way or another. Notice that the _dogs_ directory contains directories named after countries. Each country directory had directories named after authors. Each author directory has files containing works or excerpts from that author. Each author directory also has a file named _author_, containing the name, birth year, death year, and country for that author.

Create a file named _labx2_. For each step in the lab you will construct a command and record it, one command per line in _labx2_. Preface each command with a tag to indicate the step. The tag should be the step number in parenthesis. Each command should fit on one line and not contain any semi-colons (;'s). Your _labx2_ file should have exactly 30 lines and look like the following:

(1) _your command goes here_

(2) _your command goes here_

(3) _your command goes here_

(4) _your command goes here_

(5) _your command goes here_

(6) _your command goes here_

(7) _your command goes here_

(8) _your command goes here_

(9) _your command goes here_

(10) _your command goes here_

(11) _your command goes here_

(12) _your command goes here_

(13) _your command goes here_

(14) _your command goes here_

(15) _your command goes here_

(16) _your command goes here_

(17) _your command goes here_

(18) _your command goes here_

(19) _your command goes here_

(20) _your command goes here_

(21) _your command goes here_

(22) _your command goes here_

(23) _your command goes here_

(24) _your command goes here_

(25) _your command goes here_

(26) _your command goes here_

(27) _your command goes here_

(28) _your command goes here_

(29) _your command goes here_

(30) _your command goes here_

You can check your work with the **checkx2** script.

You may find it helpful to have three Opus-II sessions running. In the first session display the output from the **tree** command on the _dogs_ directory for quick reference. In a second session, use **vi** to record your commands in the _labx2_ file, and in the third session test the commands you create.

**Review**

- A way is needed to uniquely specify files and directories in the UNIX/Linux file tree. Because there can be more than one file with the same name just specifying the filename on a command would be ambiguous. **Absolute** and **relative** pathnames solve this need.

- The top or "root" of the file tree is the / directory. By typing **ls /** you can view the standard top level directories of the UNIX/Linux file tree.

- An **absolute** pathname specifies the location of a file or directory relative to the top of the Unix file tree. An **absolute** pathname specifies the complete path starting from / (the top or "root" of the file tree) all the way to the file or directory being specified. **Absolute** pathnames always start with a / and contain no spaces.

- A **relative** pathname specifies the location of a file or directory **relative** to the current working directory. The current working directory changes every time you change directories using the **cd** command. A **relative** pathname specifies the complete path starting from the current working directory all the way to the file or directory being specified. **Relative** pathnames never start with a / and contain no spaces.

- The **pwd** command will show you where you are in the UNIX/Linux file tree by displaying the current working directory. The current working directory is the starting point for all **relative** pathnames.

- Tip: To verify if a pathname is correct, use it as an argument to the **ls** command. If you are specifying a file the **ls** command will print the name of the target file only if the pathname is correct. Same goes for directories however, the **-d** option must be used so the ls command will display the name of the target directory rather than its contents.

- Correct pathnames are required as arguments to commands that work with files such as **mv** , **cp** , **ls** , **cd** , **head** , **tail** , **rm** , etc.
- The . directory means "here". It is hard linked to the current directory you are in. You may use . below when asked for a **relative** path.

- The .. directory is the parent of the current directory. It is implemented as a hard link. You may use .. when asked for a **relative** pathname below. Use it to work your way up the tree towards the top or "root" of the tree.

- The ~ directory is shorthand for the user's home directory. Don't use it below when asked for an **absolute** path since it changes based on the user.

- Example: the **absolute** pathname to the _sonnet1_ file in Benji's _Shakespeare_ directory is:

/home/cis90/simben/poems/Shakespeare/sonnet1

Note that this is like giving someone walking instructions from the top of the tree all the way to the specific _sonnet1_ file in Benji's _Shakespeare_ directory.

- Example: two **relative** pathnames to the _sonnet1_ file in Benji's _Shakespeare_ directory from /home/rsimms are:

../cis90/simben/poems/Shakespeare/sonnet1

../../boot/grub/../../home/cis90/simben/poems/Shakespeare/sonnet1

Note that this is like giving someone walking instructions from their current location on the tree all the way to the specific _sonnet1_ file in Benji's directory. Note: it doesn't have to be the shortest path just a complete path.

- Example: the **relative** pathname to the _sonnet1_ file in Benji's _Shakespeare_ directory from his _Shakespeare_ directory is:

sonnet1

- Use Tab completes to verify the pathname you are typing is correct. Press the Tab key once to see if enough characters have been typed to complete the current file name. Press the Tab key twice to show all the current possibilities. If there is no completion or possibilities you are most likely off in the weeds and not typing a correct pathname.

**Using absolute and relative pathnames**

Important: for this lab do NOT use "~" or "./" to start your pathnames. Any answers containing them will not get credit!

1) From your home directory, what **ls** command would show the permissions on the Linux kernel file _vmlinuz-3.10.0-862.9.1.el7.x86\_64_? On Opus, this file resides in the _/boot_ directory. On your **ls** command, specify the Linux kernel using an **absolute** pathname.

2) From your home directory, what **ls** command would show the permissions on the _passwd_ file where all user accounts are kept? This _passwd_ file resides in the _/etc_ directory. On your **ls** command, specify this _passwd_ file using an **absolute** pathname.

3) From your home directory, what **ls** command would show the permissions on the _/etc_ directory itself (and no other directories)? On your **ls** command, specify this particular _etc_ directory using an **absolute** pathname and be sure to use the **-d** option.

4) From your home directory, what **cd** command would change to the top, "root", directory of the UNIX/Linux file tree? On your **cd** command, use a **relative** pathname to specify the top directory of the file tree.

5) From the top of the file tree, what **file** command would probe the _passwd_ file where all user accounts are kept? This _passwd_ file resides in the _/etc_ directory. On your **file** command, specify this _passwd_ file using a **relative** pathname that does not start with the "." character.

6) From the top of the file tree, what **ls** command would show the owners of all files in the _/dev/pts/_ directory? On your **ls** command, use a **relative** pathname and one filename expansion (globbing) character.

7) From the top of the file tree, what **cd** command would change to the new _dogs_ directory in your home directory? Use an **absolute** pathname to specify your _dogs_ directory.

8) From your _dogs_ directory, what **tree** command diagrams the _Italy_ and _Germany_ directories? Specify both directories with **relative** pathnames.

9) Again from your _dogs_ directory, what **ls** command does a long, recursive listing showing inode numbers of the _Ukraine_ directory? Specify the _Ukraine_ directory using an **absolute** pathname.

10) Still from your _dogs_ directory, what **head** command would list the first 2 lines of the Austen's _Persuasion_ and Chekhov's _Wife_ files? Use **relative** pathnames for both _Persuasion_ and _Wife_.

11) Again from your _dogs_ directory, what **head** command would list the first 2 lines of Burroughs' _Tarzan_ and _Mars_ files? Use an **absolute** pathname for the _Tarzan_ file. Use a **relative** pathname for the _Mars_ file that does not start with the "." character.

12) From your _dogs_ directory, what **cd** command would change to the _Plato_ directory (in Greece)? Use a **relative** pathname to specify the _Plato_ directory that does not start with the "." character.

13) From the _Plato_ directory, what **chmod** command would change the permissions on the _Ukraine_ and _USA_ directories to 744? Use a **relative** pathname with the wildcard \* meta-character to specify just the _USA_ and _Ukraine_ directories. You must also use the **-v** option (for verbose) which outputs the changes made.

14) From the _Plato_ directory, what **ls** command would do a long listing on the _passwd_ file in the _/etc_ directory? Use an **absolute** pathname for the _passwd_ file.

15) From the _Plato_ directory, what **ls** command would do a long listing on the _passwd_ file in the _/etc_ directory? Use a **relative** pathname for the _passwd_ file.

16) From the _Plato_ directory, what **cd** command would change to the _France_ directory? Use an **absolute** pathname to specify the _France_ directory.

17) From the _France_ directory, what **cp** command would copy Machiavelli's _War_ to the _France_ directory? Use **relative** pathnames to specify the Machiavelli's _War_ and the _France_ directory. Use the **-v** option to show what gets copied.

18) From the _France_ directory, what **cp** command would copy Kafka's _Trial_ to the _Cervantes_ directory? Use **relative** pathnames to specify the _Trial_ file and the _Cervantes_ directory. Use the **-v** option to show what gets copied.

19) From the _France_ directory, what **cp** command would copy Verne's _Moon_ and Tolstoy's _Murad_ to the _Cervantes_ directory? Use a **relative** pathname to specify the _Moon_ file that does not start with the "." character. Use a **relative** pathname for the _Cervantes_ directory. Use an **absolute** pathname to specify the _Murad_ file. Use the **-v** option to show what gets copied.

20) From the _France_ directory, what **rm** command would remove the four files copied in steps 17-19 from the _France_ and _Cervantes_ directories? That is, remove the _War_ file from _France_ and the _Moon_, _Murad_ and _Trial_ files from the _Cervantes_ directory. Use only **relative** pathnames and the **-v** option to show what gets removed. Use the [] and \* meta-characters to specify all the files in _Cervantes_ you want to delete.

21) From the _France_ directory, what **cat** command would cat the _author_ file in the _Verne_ directory? Use a **relative** pathname for the _author_ file.

22) From the _France_ directory, what **cat** command would cat the _author_ file in the Verne directory? Use an **absolute** pathname for the _author_ file.

23) From the _France_ directory, what **cat** command would cat the _author_ files in the _USA__Alcott, Burroughs, Dickinson_ and _Twain_ directories? Use a **relative** pathname with the \* wildcard meta-character.

24) From the _France_ directory, what **cd** command with an argument would change back to your home directory? Specify your home directory using a **relative** pathname that starts with the .. directory.

25) From your home directory, what non-recursive **grep** command would find all lines containing the string "dog" in all the works by the Ukrainian author Chekhov? Use a **relative** pathname with the wildcard \* meta-character to match each of his works.

26) From your home directory, what non-recursive **grep** command would find all lines containing the word dog in all the works of all the German authors? Use a **relative** pathname with the wildcard \* meta-character to match both authors and works.

27) From your home directory, what **cat** command would print all the files named _author_ in all the directories under the _dogs_ directory? Use an **absolute** pathname with the wildcard \* meta-character to match all country directories and author directories.

28) From your home directory, what **find** command would list all the directories (not regular files) in your _dogs_ directory and down? Use a **relative** pathname to your _dogs_ directory.

29) From your home directory, what **cp** command would copy /etc/passwd and Burroughs' _Oakdale_ file to your home directory? Use **relative** pathnames for your home directory and the _Oakdale_ file. Use an **absolute** pathname for the _passwd_ file. Use the **-v** option (verbose) to show what gets copied.

30) From your home directory, what **rm** command would remove the _passwd_ and _Oakdale_ files from your home directory? Use **relative** pathnames and the **-v** option (verbose) to show what gets removed that do not start with the "." character.

Important: for this lab do NOT use "~" or "./" to start your pathnames. Any answers containing them will not get credit!

**To turn in**

After verifying the output of your commands with the **checkx2** script, submit your final version of _labx2_ as follows:

**cp labx2 /home/rsimms/turnin/cis90/labx2.$LOGNAME**

Within a minute or two you should receive an acknowledgement email on Opus-II with the status of your submission. Be sure to read this email to make your work was submitted properly for grading.

**Grading rubric (30 points maximum)**

1 point for each correct command. A command will be considered correct if the output matches or is equivalent to the output from the **checkx2** script.
