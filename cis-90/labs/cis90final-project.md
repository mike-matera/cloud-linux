
# Final Project

For the final project you will be writing a bash shell script that performs multiple interactive tasks. Your script can automate using some of your favorite commands that you have learned in this course. You will start with a template that you can modify and extend.

## Commands by Categories

| Type | Commands |
| --- | --- |
| `Simple:` | banner, date, cal, finger, uname, type, ls, tree, cd, pwd, hostname |
| `Status:` | jobs, ps, who, id, env, lpstat, umask, mesg, history, tty |
| `File:` | file, cp, mv, ln, rm, rmdir, mkdir, touch, chmod, chgrp, xxd, head, tail, stat |
| `Filters:` | cat, sort, spell, grep, wc, tee |
| `Misc:` | bc, mail, vi, lp, cancel, at, kill, find, passwd |

## The Template

Start with this code for your final project (you can copy it from `/home/cis90/depot/myscript`):

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
	  1)  	# Commands for Task 1
		;;
	  2)  	# Commands for Task 2
		;;
	  3)  	# Commands for Task 3
		;;
	  4)  	# Commands for Task 4
		;;
	  5)  	# Commands for Task 5
		;;
	  6)	exit 0
		;;
	  *)    echo "Please enter a number between 1 and 6"
		;;
	esac
	echo -n "Hit the Enter key to return to menu "
	read response
done
```

## Procedure

Copy the template from `/home/cis90/depot/myscript` to your own `bin/` directory keeping it named `myscript`. Give the file execute permission for everyone. You will run your script by entering its name on the command line just as you do with any other Linux command.

Choose five tasks to implement. For each choice add a menu option and then develop the appropriate case statement. Expand the case statement with commands to query the user for input, then process that input.

Each task that you implement should:

- Be interactive:
  - Prompt the user for input.
  - Save the user's input in one or more variables.
  - Execute one or more commands using the variables as the options or arguments.
- Have at least one non-generic comment.
- Have the minimum number of commands according to the grading rubric below.

Make sure your script can run by itself and run from `allscripts` which is in the `/usr/local/bin` directory. You also need to set permissions so that everyone in the cis90 group can read and execute your script.

When finished, you will need to test your script and repair any defects you find. After your own testing it is helpful to have others test your work. Developers can't always imagine all the creative ways users will use their products. Use the forum to ask other students to run your script and give your feedback. This is also a good way to check your script can be run by others in the cis90 group.

## Tips 

- Run `allscripts` to see some work Luigi and Benji have developed.
- Luigi has a front-end to the `grep` command is a good example of the minimum expected for a single task as well as templates for doing more complicated things.
- Benji went a tad overboard on his tasks. He must have been thinking he would get chicken treats. You don't have to do as much as Benji did but you might get some ideas from viewing his work. His script also has many examples of how to do conditionals for other students wanting to go over the top.
- Use `vi` to look at Luigi's and Benji's scripts in their bin directories. `vi` adds color to make the commands easier to read.
- There are also a number of sample bash scripts in `/home/cis90/depot/scripts` you can look at to see how to do some more complex things and get ideas.
- Save earlier versions of your work. You can easily do this by copying `myscript` to `myscript.v1`, `myscript.v2`, etc. to backup each version.

## Shell scripting topic ideas

- Make the `find` command easier to use
- View the File System
  - Show files at the root (/) directory
  - Show files in user's home directory
  - Show files in the parent directory
  - Show files in a specified directory

- Tally Files
  - Tally the number of directories from a given starting point
  - Tally the number of symbolic links from a given starting point
  - Tally the number of text files from a given starting point
  - Tally the number of shell scripts from a given starting point
  - Tally the number of data files from a given starting point
  - Tally the number of symbolic links from a given starting point
  - Draw a histogram showing the relative numbers of different file types

- Search for files

  - Search for a file by name
  - Search for a file by inode number
  - Search for a file by owner
  - Search for a file by size
  - Search for files that have been modified recently
  - Search for files that contain a certain string of characters

- View files

  - Select a file for viewing
  - View the entire file allowing paging through the file
  - View a file in hexadecimal format
  - View the top 20 lines of a file
  - View the bottom 20 lines of a file

- Process status

  - Show just system processes
  - Show processes belonging to a particular user
  - Show any defunct processes
  - Show all processes
