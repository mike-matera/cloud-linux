# Lab 4: The UNIX File System

The goal of this lab is to become proficient with system commands for viewing the directories and different file types that make up a UNIX file system.

## Preparation and getting help

1. Find and skim Lesson 4 slides: [http://simms-teach.com/cis90calendar.php](http://simms-teach.com/cis90calendar.php)
2. Check the forum for discussions on this lab: [http://opus-ii.cis.cabrillo.edu/forum/](http://opus-ii.cis.cabrillo.edu/forum/)
3. For additional help work the lab with a tutor. Click the "Tutors" link at the top of the my website: [https://simms-teach.com/](https://simms-teach.com/)

## Warmup (not submitted or graded)

Log on to the Opus server so that you have a command line shell at your service. Be sure you are in your home directory to start this lab. You do not need to record or submit your answers for this section.

- Display a listing of the files in your home directory. Are they in any special order?
- Use **ls -a** to display the contents of directory _Lab2.0_

Which filenames do not follow the UNIX file naming conventions?

- Use **ls -F** to determine what kind of files you have in your home directory.

Do all directories begin with an uppercase letter?

- Use the **file** command to analyze the following files: _Poems, proposal2, timecal_, and _empty_.
- Display the contents of the _mission_ file on your screen.
- Display the contents of the _letter_ file on your screen. Is it more appropriate to use **cat** or **more**?
- List the filenames stored under the root (/) directory. Are these files or subdirectories or both?
- Determine the absolute pathname of your home directory. Use this pathname as an argument to the **ls** command. What are two other ways of getting the same listing?
- List the contents of your _Poems_ directory using a relative pathname.

Do the same thing using an absolute pathname, i.e. beginning with a slash (/)

- Display the contents of the d_iner_ file stored under the _Angelou_ directory, which is under the _Poems_ directory.
- Use a single **more** or **less** command to browse all of the files stored under the _Yeats_ subdirectory. Why did you choose the command you used? How can you tell where one file ends and the next begins?
- Use the **head** and **tail** commands to look at the top and bottom ten lines of _bigfile_.
- Use the **ls** command to see what is stored in the _/bin_ directory.

Do you recognize any of the filenames? What kind of files are these?

- Display the contents of the file _what\_am\_i_. Which command did you use?
- Use **ls -lia** to do a long listing of the files in the _Miscellaneous_ directory.
- Use **ls -lid** to do a long listing of the _Miscellaneous_ directory itself.
- Use **wc** on some of the sonnets in the _Shakespeare_ directory. Use **man wc** to understand the results or try different options. Is the operation of the man page similar to the **more** or **less** command?

## Answer the following questions (graded)

Log on to the Opus server so that you have a command line shell at your service. Change to your home directory if you are not already there.

Use the **submit** command to record and submit your answers to the questions below.

1. What option is required on the **ls** command to do a "long listing"?
2. What option is required on the **ls** command to show inode numbers?
3. What option is required on the **ls** command to sort output by file size?
4. What option is required on the **ls** command to show hidden files?
5. What option is required on the **ls** command to list the directory itself rather than its contents?

1. Write down the absolute path of your home directory.
2. From your home directory, what is the relative pathname of the _hope_ poem in the _Dickenson_ subdirectory?
3. What command allows you to see the hidden files in your current directory?
4. What command shows the absolute pathname of your current working directory?
5. In your home directory, are any of the hidden files directories? If so, which ones?

1. What does the **cd** command do when it is invoked with no arguments?
2. Assuming you are in your home directory, what command will change your current working directory to the directory that holds Shakespeare's sonnets?
3. What is the inode number of the _dog_ poem file in your _Neruda_ directory?
4. Who is the owner of your home directory?
5. What's the name of the largest text file in your home directory?

1. What's the name AND size of the smallest file in your home directory?
2. How many non-hidden subdirectories does your _Poems_ directory have?
3. What is the first line of the file _old_ in the _Poems/Yeats_ directory?
4. What is the last line of _sonnet3_ in the _Shakespeare_ directory?
5. What is the name of a regular file in your home directory that is not meant to be viewed with the **cat** or **more** commands?

1. What key should you type when you want to exit from the **less** command?
2. What **ls** command shows the permissions on your home directory while you are in your home directory? Be sure to test your answer. It should not show permissions on the files in your home directory.
3. What UNIX command will allow you to look at the contents of a binary data file?
4. How many words are there in the Neruda poem containing the most lines?
5. What is the inode number of the Yeats poem with the most recent timestamp?

1. How many lines are in Shakespeare's _sonnet1_?
2. What English word do you see between hex offset 00000f0 and 0000100 of the file _what\_am\_i_?
3. What file in the _Miscellaneous_ directory is a symbolic link to another file?
4. What is the inode number of the file being linked to?
5. From your_bin_directory, what is the relative pathname of the directory containing the **submit** command?

## Extra credit questions

Correct answers will NOT use redirection and only use commands and constructs covered to date in the course. (e.g. don't use | (pipes), grep, etc.)

1. What single command would list only the hidden files (and nothing else) in your home directory?
2. From your home directory, what single command would produce a long listing PLUS show inode numbers for all the Neruda _dog_ files belonging to all the CIS 90 students?
3. On your Arya, what is the 3rd to last line of your _/etc/network/interfaces_ file?

## Submit your work

Use the **submit** command to record your answers and turn in your work. When asked for which lab, enter 4. Run **check4** to have a feedbot review your work and email you feedback. Use **verify** to see what you have submitted for grading.

You can change your mind and submit as many times as you like up to the deadline. There is no credit though for late work. If you run out of time be sure to submit what you have for partial credit.

## Grading Rubric (30 points total)

1 point for each correct answer to questions 1-30.

1 point extra credit for each correct answer to questions 31-33.

Be sure to submit your work before the deadline. **Remember, late work is not accepted.**
