# Lab X1: UNIX in Review - Extra Credit Lab

**Spring 2019**

**Objectives**

This lab will give you review exercises in UNIX commands, file systems, processes, and shell scripting. This will help you prepare for the final exam.

**Forum**

Browse to: [http://opus-ii.cis.cabrillo.edu/forum/](http://opus-ii.cis.cabrillo.edu/forum/)

Check the forum for any late breaking news about this lab. The forum is also the place to go if you get stuck, have a question or want to share something you have learned about this lab.

**Procedure**

Log into your home directory on Opus, and make a subdirectory called _review_. Perform the following tasks and place the results of any steps of your work into this directory.

1. The UNIX operating system is often divided into three parts:

- The kernel (_/boot/vmlinuz\*_)
- The shells (/bin/{bash,ksh,sh,csh,tcsh})
- The commands (_/bin/\*_)

Make one file, called _unix_, that contains a long listing of all these files. Make sure this _unix_ file ends up in your _review_ directory. There should be no duplicates. Count the number of files in your long listing and append this count to the end of your _unix_ file.

1. Copy the output of the man page for the banner command to a file called _banner_.

1. Find a way to list all the files in and under your home directory and save the output to a file called _myfiles_.

1. Find all regular files in the _/etc_ branch of the file tree that were modified between June 20, 2017 and July 20, 2017. Record their absolute pathnames in a file called, _doves_.

1. Using the _/etc/passwd_ file, mail yourself a list of just the UIDs for all the CIS 90 students. Then read your mail and save that message, with the mail headers, to a file called _mail90_ in your _review_ directory.

1. See if you can figure out a way to run the **banner** command on the output of the **date** command with the date formatted as the full weekday name (e.g. Sunday). Save the command you used and the output of the command to a file called _today_.

1. Save a list of all processes currently being run by root to a file called _processes_. **vi** this file and remove any lines that contain a process whose name does not end in the letter 'd'. For example you would keep the processes named [ksoftirqd/1], /usr/sbin/httpd and sshd:.

1. With one pipeline command make a sorted, single column list of the inode numbers, for all the poems in your _poems/_ directory and sub-directories. Save the command you used and the output of the command to a file called _iPoems_.

**Submittal**

You should now have 8 files in your _review_ directory. Write a shell script, named _labx1_, that will let me view these files one at a time. The shell script should let me view the files as many times as I want before exiting the program. I want to be able to run this program from anywhere on the system.

Once you have tested and debugged this program, copy it to the directory _/home/rsimms/turnin/cis90_ naming it _labx1.$LOGNAME_. Make sure it is executable for me and that I can read your files. (I am a member of the cis90 group).

**Grading rubric (30 points maximum)**

3 points each for doing each step above correctly and completely.

6 points for correct script submittal, permissions, and pathnames.
