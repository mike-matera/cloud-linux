# File Permissions Project

In this project you will learn how to assign permissions to files and directories to provide a measure of security and privacy to your files on a multi-user system.

## Before You Begin

- Be sure to make the changes to your home directory asked for in the [Navigating the Filesystem](filesystem_lab.md) and [Managing Files](managing_files.md) labs. This lab assumes the new names and directory structures.

## Procedure

Log on to `opus` so that you have a command line shell at your service. Be sure you are in your home directory to start this lab. Using the `chgrp`, and `chmod` commands, you will modify the permissions on files and subdirectories in your home directory.

1. From your home directory, do a long listing with the `ls -l` command.
	- Who owns these files? 
	- To which group do they belong?
	- How can you distinguish file entries from directory entries?


1. Do a long listing of the file, `/usr/local/bin/check5`. 
 	- Who owns it?
	- Can you move the file to your home directory? Why or why not?
	- Can you copy the file to your home directory? Why or why not?

1. Now that you have copied the file `check5` to your home directory, who owns it? What are the permissions?

1. Display the contents of the file `check5` on your screen.

	Now take away read permission using the command:

	`chmod -r check5`

	Try to display the contents of the file as you did above. Does it work?

1. Now give read permission back but take away write permission:

	`chmod 444 check5`

	Verify the success of the above command.

1. Take away execute (search) permission from the `misc` directory:

	`chmod -x misc`

	Do short and long listings of the `misc` directory using the `ls` and `ls -l` commands.

	Try to display the contents of the fruit file with the command:

	`cat misc/fruit`

	Try to change directories to `misc`.

1. Give yourself back execute permission but take away read permission:

	`chmod +x,-r misc`

	Change your current directory to the `misc` directory.

	Try displaying the contents of the `misc` directory.

	Display the contents of the `fruit` file.

1. Change back to your home directory and set the `misc` directory to full permissions:

	`chmod 777 misc`

1. Set the permissions of your `poems` directory and its subdirectories so that you have full permissions as owner, but group and others have no write permission. Group and others should still have read and execute permission.

1. Set all ordinary files under the `poems` directory to be read only for user, group, and others. We want everyone to read our poetry, but no one should modify it, including ourselves.

	See if you can do this using a minimum number of commands. (hint: use filename expansion characters).

1. Change the permissions of your `bin` directory so that you have full permission, group has read and execute, and all others have no permissions.

1. Set the executable files under bin to have the following permissions:

	`r-xr-x---`

	disallowing others outside the group from executing our commands.

1. Change the group id of the following directories: `class/labs`, and `class/tests` to be users:

	`chgrp users class/labs class/tests`

1. For the `class` directory set the permissions to `710`.

	For the `labs` subdirectory, set permissions to `530`.

	For the `tests` subdirectory, take away all permissions from group and others, leaving full permission for owner.

1. For the `edits` directory, give yourself full permission, but no permission for group or others.

	For the ordinary files under `edits`, take away read permission from group, leaving everything else as it is.

1. Add read permission for everyone to all the files in the `misc` directory.

1. Run the `umask` command and note the number displayed.

1. Create an empty file called `old` and an empty directory called `olddir`:

	`touch old; mkdir olddir`

1. Run the `umask` command giving it the argument: `000`

	`umask 000`

1. Create an empty file called `new` and an empty directory called `newdir`:

	`touch new; mkdir newdir`

1. Look at the permissions of these four files you've created.

	Notice how they have changed. Can you figure out what `umask` is for?

1. Try setting the umask to `777` and making a `newer` file.

	To finish, set your umask back to `002` with the command:

	`umask 002`

## Submittal

There's a program to help you check your work called `check6`. Run it and it tells you what steps you did correctly and which ones need fixing. 

Hit the `Enter` key to continue. If you see something that needs fixing, exit the program with `Ctrl-C`. After you fix the problem restart the checker. When you finish you'll see a screen like the following:

```bash
==============================================================
Submit this tar file on Canvas!
==============================================================

I have created a tar file of your home directory in: 

/tmp/files-simben90-3o340p.tar
```

A different file will be created for you every run. Submit the file on Canvas.
