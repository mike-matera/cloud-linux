# Lab 6: File Permissions

In this lab you will learn how to assign permissions to files and directories to provide a measure of security and privacy to your files on a multiuser system.

## Preparation

- Be sure to make the changes to your home directory asked for in Lab 5. This lab assumes the new names and directory structures.

- Find and skim Lesson 7 slides: [http://simms-teach.com/cis90calendar.php](http://simms-teach.com/cis90calendar.php)
- Check the forum for news on this lab: [http://opus-ii.cis.cabrillo.edu/forum/](http://opus-ii.cis.cabrillo.edu/forum/)

## Procedure

Log on to Opus-II so that you have a command line shell at your service. Be sure you are in your home directory to start this lab. Using the **chgrp** , and **chmod** commands, you will modify the permissions on files and subdirectories in your home directory.

1. From your home directory, do a long listing with the **ls -l** command.

Who owns these files? To which group do they belong?

How can you distinguish file entries from directory entries?

1. Do a long listing of the file, _/home/rsimms/uhistory_. Who owns it?

Can you move the file to your home directory? Why or why not?

Can you copy the file to your home directory? Why or why not?

1. Now that you have copied the file _uhistory_ to your home directory,

who owns it? What are the permissions?

1. Display the contents of the file _uhistory_ on your screen.

Now take away read permission using the command:

**chmod -r uhistory**

Try to display the contents of the file as you did above. Does it work?

1. Now give read permission back but take away write permission:

**chmod 444 uhistory**

Verify the success of the above command.

1. Take away execute (search) permission from the _misc_ directory:

**chmod -x misc**

Do short and long listings of the _misc_ directory using the **ls** and **ls -l** commands.

Try to display the contents of the fruit file with the command:

**cat misc/fruit**

Try to change directories to _misc_.

1. Give yourself back execute permission but take away read permission:

**chmod +x,-r misc**

Change your current directory to the _misc_ directory.

Try displaying the contents of the _misc_ directory.

Display the contents of the _fruit_ file.

1. Change back to your home directory and set the _misc_ directory to full permissions:

**chmod 777 misc**

![](cis90lab06_html_237499165a11f2b9.gif)

1. Set the permissions of your _poems_ directory and its subdirectories so that you have full permissions as owner, but group and others have no write permission. Group and others should still have read and execute permission.

1. Set all ordinary files under the _poems_ directory to be read only for user, group, and others. We want everyone to read our poetry, but no one should modify it, including ourselves.

See if you can do this using a minimum number of commands. (hint: use filename expansion characters).

1. Change the permissions of your _bin_ directory so that you have full permission, group has read and execute, and all others have no permissions.

1. Set the executable files under bin to have the following permissions:

**r-xr-x---**

disallowing others outside the group from executing our commands.

1. Change the group id of the following directories: _class/labs_, and _class/tests_ to be users:

**chgrp users class/labs class/tests**

1. For the _class_ directory set the permissions to 710.

For the _labs_ subdirectory, set permissions to 530.

For the _tests_ subdirectory, take away all permissions from group and others, leaving full permission for owner.

1. Make all ordinary files under _class/labs_ and _class/tests_ be:

read-write for owner

no permissions for group and

no permissions for others.

1. For the _edits_ directory, give yourself full permission, but no permission for group or others.

For the ordinary files under _edits_, take away read permission from group, leaving everything else as it is.

1. Add read permission for everyone to all the files in the _misc_ directory.

![](cis90lab06_html_237499165a11f2b9.gif)

1. Run the **umask** command and note the number displayed.

1. Create an empty file called _old_ and an empty directory called _olddir_:

**touch old; mkdir olddir**

1. Run the **umask** command giving it the argument: 000

**umask 000**

1. Create an empty file called _new_ and an empty directory called _newdir_:

**touch new; mkdir newdir**

1. Look at the permissions of these four files you've created.

Notice how they have changed. Can you figure out what **umask** is for?

1. Try setting the umask to 777 and making a _newer_ file.

To finish, set your umask back to 002 with the command:

**umask 002**

## Submittal

You have now finished the lab. To submit your work to be counted for this lab, you must run the **submit** command from your home directory.

Run **check6** to check your work and make sure you didn't forget anything. Run **verify** to doublecheck you submitted your lab for grading.

## Grading Rubric (30 points total)

- 30 points for successfully completing all steps.
- Less 1 point for each step not completed correctly.

Be sure to submit your work before the deadline. **Remember, late work is not accepted.**

**Extra credit (optional)**

For two points extra credit complete:

**In NETLAB+:**

NISGTC Linux+ Series 1

Lab 9: Working with Files

Send me a "signed" summary screenshot (see instructions below).

For one point extra credit complete:

**In NETLAB+:**

Red Hat Systems Administration - RH124

6.4. Practice: Managing File Security from the Command Line

Send me a "signed" summary screenshot (see instructions below).

Summary screenshot:

1) Before ending the lab maximize the terminal window you used.

2) Use: **history** to show the commands you issued during the lab.

3) Use: **echo "** _firstname lastname_ **was here"** as your signature.

4) Take a screen shot of the above and email it to: risimms@cabrillo.edu

Extra credit is due when the lab is due. **Remember, late work is not accepted.**
