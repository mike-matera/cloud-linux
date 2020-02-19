# Navigating the UNIX File System

The goal of this lab is to become proficient with system commands for viewing the directories and different file types that make up a UNIX file system.

## Warmup (not submitted or graded)

Log on to the opus3 server so that you have a command line shell at your service. Be sure you are in your home directory to start this lab. You do not need to record or submit your answers for this section.

- Display a listing of the files in your home directory. Are they in any special order?
- Use `ls -a` to display the contents of directory `Lab2.0`

Which filenames do not follow the UNIX file naming conventions?

- Use `ls -F` to determine what kind of files you have in your home directory.

Do all directories begin with an uppercase letter?

- Use the `file` command to analyze the following files: `Poems`, `proposal2`, `timecal`, and `empty`.
- Display the contents of the `mission` file on your screen.
- Display the contents of the `letter` file on your screen. Is it more appropriate to use `cat` or `less`?
- List the filenames stored under the root (`/`) directory. Are these files or subdirectories or both?
- Determine the absolute pathname of your home directory. Use this pathname as an argument to the `ls` command. What are two other ways of getting the same listing?
- List the contents of your `Poems` directory using a relative pathname.

Do the same thing using an absolute pathname, i.e. beginning with a slash (/)

- Display the contents of the `diner` file stored under the `Angelou` directory, which is under the `Poems` directory.
- Use a single `more` or `less` command to browse all of the files stored under the `Yeats` subdirectory. Why did you choose the command you used? How can you tell where one file ends and the next begins?
- Use the `head` and `tail` commands to look at the top and bottom ten lines of `bigfile`.
- Use the `ls` command to see what is stored in the `/bin` directory.

Do you recognize any of the filenames? What kind of files are these?

- Display the contents of the file `what_am_i`. Which command did you use?
- Use `ls -lia` to do a long listing of the files in the `Miscellaneous` directory.
- Use `ls -lid` to do a long listing of the `Miscellaneous` directory itself.
- Use `wc` on some of the sonnets in the `Shakespeare` directory. Use `man wc` to understand the results or try different options. Is the operation of the man page similar to the `more` or `less` command?

## Answer the following questions (graded)

Log on to the Opus server so that you have a command line shell at your service. Change to your home directory if you are not already there. Record the answers to the questions below and test them by executing them in your shell. Your answers will be graded as well as your history file:

1. What option is required on the `ls` command to do a "long listing"?
2. What option is required on the `ls` command to show inode numbers?
3. What option is required on the `ls` command to sort output by file size?
4. What option is required on the `ls` command to show hidden files?
5. What option is required on the `ls` command to list the directory itself rather than its contents?
6. Write down the absolute path of your home directory.
7. From your home directory, what is the relative pathname of the `hope` poem in the `Dickenson` subdirectory?
8. What command allows you to see the hidden files in your current directory?
9. What command shows the absolute pathname of your current working directory?
10. In your home directory, are any of the hidden files directories? If so, which ones?
11. What does the `cd` command do when it is invoked with no arguments?
12. Assuming you are in your home directory, what command will change your current working directory to the directory that holds Shakespeare's sonnets?
13. What is the inode number of the `dog` poem file in your `Neruda` directory?
14. Who is the owner of your home directory?
15. What's the name of the largest text file in your home directory?
16. What's the name AND size of the smallest file in your home directory?
17. How many non-hidden subdirectories does your `Poems` directory have?
18. What is the first line of the file `old` in the `Poems/Yeats` directory?
19. What is the last line of `sonnet3` in the `Shakespeare` directory?
20. What is the name of a regular file in your home directory that is not meant to be viewed with the `cat` or `more` commands?
21. What key should you type when you want to exit from the `less` command?
22. What `ls` command shows the permissions on your home directory while you are in your home directory? Be sure to test your answer. It should not show permissions on the files in your home directory.
23. What UNIX command will allow you to look at the contents of a binary data file?
24. How many words are there in the Neruda poem containing the most lines?
25. What is the inode number of the Yeats poem with the most recent timestamp?
26. How many lines are in Shakespeare's `sonnet1`?
27. What English word do you see between hex offset `00000f0` and `0000100` of the file `what_am_i`?
28. What file in the `Miscellaneous` directory is a symbolic link to another file?
29. What is the inode number of the file being linked to?

## Submit your work

Submit your answers in a document called `filesystem_lab`. In addition submit your BASH history file. The history file is stored in `~/.bash_history`. You can download the file onto your machine using FileZilla or Cyberduck. 

