
# Final Project

For the final project you will be writing a bash shell script that performs multiple interactive tasks. Your script can automate using some of your favorite commands that you have learned in this course. You will start with a template that you can modify and extend.

**Forum**

Use the forum to brainstorm script ideas, clarify requirements, and get help if you are stuck. When you have tested your script and think it is bug free then use the forum to ask others to test it some more. Post any valuable tips or lessons learned as well. Forum is at: [http://opus-ii.cis.cabrillo.edu/forum/](http://opus-ii.cis.cabrillo.edu/forum/)

**Commands**

. echo lpstat sort

at env ls spell

banner exit mail su

bash export man tail

bc file mesg tee

cal find mkdir touch

cancel finger more type

cat grep mv umask

cd head passwd uname

chgrp history ps unset

chmod id pwd vi

chown jobs rm wc

clear kill rmdir who

cp ln set write

date lp/lpr sleep xxd

## Commands by Categories

| **Type** | **Commands** |
| --- | --- |
| **Simple:** | banner, date, cal, finger, uname, type, ls, tree, cd, pwd, hostname |
| **Status:** | jobs, ps, who, id, env, lpstat, umask, mesg, history, tty |
| **File:** | file, cp, mv, ln, rm, rmdir, mkdir, touch, chmod, chgrp, xxd, head, tail, stat |
| **Filters:** | cat, sort, spell, grep, wc, tee |
| **Misc:** | bc, mail, vi, lp, cancel, at, kill, find, passwd |

**The Template**

```bash
#!/bin/bash

#
# menu: A simple menu template
#

while true
do
clear
echo -n "

CIS 90 Final Project

1) Task 1

2) Task 2

3) Task 3

4) Task 4

5) Task 5

6) Exit

Enter Your Choice: "

read response

case $response in

1) # Commands for Task 1

;;

2) # Commands for Task 2

;;

3) # Commands for Task 3

;;

4) # Commands for Task 4

;;

5) # Commands for Task 5

;;

6) exit 0

;;

\*) echo "Please enter a number between 1 and 6"

;;

esac

echo -n "Hit the Enter key to return to menu "

read response

done
```

## Procedure

Copy the template from _/home/cis90/depot/myscript_ to your own _bin/_ directory keeping it named **myscript**. Give the file execute permission for everyone. You will run your script by entering its name on the command line just as you do with any other Linux command.

Choose five tasks to implement. For each choice add a menu option and then develop the appropriate case statement. Expand the case statement with commands to query the user for input, then process that input.

Each task that you implement should:

- Be interactive:
  - Prompt the user for input.
  - Save the user's input in one or more variables.
  - Execute one or more commands using the variables as the options or arguments.
- Have at least one non-generic comment.
- Have the minimum number of commands according to the grading rubric below.

Make sure your script can run by itself and run from **allscripts** which is in the _/home/cis90/bin_ directory. You also need to set permissions so that everyone in the cis90 group can read and execute your script.

When finished, you will need to test your script and repair any defects you find. After your own testing it is helpful to have others test your work. Developers can't always imagine all the creative ways users will use their products. Use the forum to ask other students to run your script and give your feedback. This is also a good way to check your script can be run by others in the cis90 group.

**Tips**

- Run **allscripts** to see some work Homer, Duke and Benji have developed.
- Duke's work on a front-end to the **grep** command is a good example of the minimum expected for a single task. Duke and Homer still have more work to do when they get back from their walks as not all tasks are completed.
- Benji went a tad overboard on his tasks. He must have been thinking he would get chicken treats. You don't have to do as much as Benji did but you might get some ideas from viewing his work. His script also has many examples of how to do conditionals for other students wanting to go over the top.
- Use **vi** to look at Homer's, Duke's and Benji's scripts in their bin directories. **vi** adds color to make the commands easier to read.
- There are also a number of sample bash scripts in /_home/cis90/depot/scripts_ you can look at to see how to do some more complex things and get ideas.
- Save earlier versions of your work. You can easily do this by copying **myscript** to _myscript.v1_, _myscript.v2_, etc. to backup each version.

## Shell scripting topic ideas

An easier to use find command

View the File System

- Show files at the root (/) directory
- Show files in user's home directory
- Show files in the parent directory
- Show files in a specified directory

Tally Files

- Tally the number of directories from a given starting point
- Tally the number of symbolic links from a given starting point
- Tally the number of text files from a given starting point
- Tally the number of shell scripts from a given starting point
- Tally the number of data files from a given starting point
- Tally the number of symbolic links from a given starting point
- Draw a histogram showing the relative numbers of different file types

Search for files

- Search for a file by name
- Search for a file by inode number
- Search for a file by owner
- Search for a file by size
- Search for files that have been modified recently
- Search for files that contain a certain string of characters

View files

- Select a file for viewing
- View the entire file allowing paging through the file
- View a file in hexadecimal format
- View the top 20 lines of a file
- View the bottom 20 lines of a file

Process status

- Show just system processes
- Show processes belonging to a particular user
- Show any defunct processes
- Show all processes

**To turn in**

Copy your final version of **myscript** as follows:

**cp myscript /home/rsimms/turnin/cis90/myscript.$LOGNAME**

**Grading rubric (60 points maximum)**

| **Possible Points** | **Requirements** |
| --- | --- |
| 30 | Implementing all five tasks (6 points each):
- Requirements for each task:

- Minimum of 12 "original" bash command lines
- Has one or more non-generic comments to explain what it is doing
- Has user interaction
 |
| 24 | At least six bash constructs from this list:
- Redirecting stdin (4 points)
- Redirecting stdout (4 points)
- Redirecting stderr (4 points)
- Use of permissions (4 points)
- Use of filename expansion characters (4 points)
- Use of absolute pathname (4 points)
- Use of relative pathname (4 points)
- Use of a PID (4 points)
- Use of inodes (4 points)
- Use of links (4 points)
- Use of color (4 points)
- Use of scheduling (4 points)
- Use of a GID or group (4 points)
- Use of a UID or user (4 points)
- Use of a /dev/tty device (4 points)
- Use of a signal (4 points)
- Use of piping (4 points)
- Use of an environment variable (4 points)
- Use of /bin/mail (4 points)
- Use of a conditional (4 points)
- Use of $(_command_) (4 points)
The maximum for this section is 24 points. |
| 6 | Present your script to the class |
|
 |
 |
| **Points lost** |
 |
| -15 | Fails to run from **allscripts** |
| -15 | Other students in the class are unable to read and execute your script. |
| -15 | Error messages are displayed when running one or more tasks |
| -up to 90 | No credit for any task which contains unoriginal script code that:
- Doesn't give full credit to the original author.
- Doesn't indicate where the code was obtained from.
- Doesn't include licensing terms.
- Violates copyright or licensing terms.
 |
| -up to 90 | For any "malware" scripts that steal credentials, exfiltrate confidential information, remove or encrypt a user's files or creates a denial of service condition on Opus-II. |
| **Extra credit** |
 |
| 30 | Up to three additional tasks (10 points each) |
