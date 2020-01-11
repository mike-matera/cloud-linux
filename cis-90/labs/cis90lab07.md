# Lab 7: Input and Output

The goal of this lab is to gain proficiency in using I/O redirection to perform tasks on the system. You will combine commands you have learned in this course using shell redirection, pipes and tees to perform a variety of tasks on the system.

## Preparation

- Be sure to make the changes to your home directory asked for in Lab 5. This lab assumes the new names and directory structures.

- Skim Lesson 8 slides: [http://simms-teach.com/cis90calendar.php](http://simms-teach.com/cis90calendar.php)
- Check the forum for news on this lab: [http://opus-ii.cis.cabrillo.edu/forum/](http://opus-ii.cis.cabrillo.edu/forum/)

## Procedure

Log on to Opus so that you have a command line shell at your service. Be sure you are in your home directory to start this lab. We are going to experiment with how commands get their input and what they do with their output. Then we will perform a series of tasks by combining commands together and saving the output to a file.

## The find command

The syntax of the find command is:

**find** _starting-directory_ **-name** _filename_ **-user** _username_

When the **-name** option and its argument are omitted; all files are displayed.

1. Find all the files under your home directory by issuing the command:

**find $HOME**

1. Find all the files named _old_ that are somewhere in or below your parent directory using the command:

**find .. -name old**

Were there any error messages?

1. Filter out the error messages by redirecting _stderr_ to a file called _errors_ in your home directory:

**find .. -name old 2\> errors**

1. Another useful option to the find command is **-user** which takes an argument of a user's name or id #. With this command you can find all the files that you own on the entire system and save them in a text file. Since we may get some error messages for directories we don't have permission for, let's also redirect the errors to the "bit bucket". This command may take a minute or so.

**find / -user $LOGNAME \> myfiles 2\> /dev/null**

## The grep command

The syntax of the **grep** command is:

**grep "** _search-string_ **"** _filenames..._

1. Find out how many of the sonnets contain the string "love" by changing your directory to _Shakespeare_ and entering the command:

**grep "love" sonnet\***

Does **grep** find just the words "love" or the string of letters: l,o,v,e?

1. One of the nice things about **grep** is that it will read its input from _stdin_ if it is not specified on the command line. Change back to your home directory and try this command:

**who | grep $LOGNAME**

What command does this remind you of?

1. Run the above command again, but this time save the output to a file called _whoami_ in your home directory.

1. Can you combine the **file** command with **grep** to list all text files in your home directory?

**file \* | grep text**

## The wc command

This command will count characters, words and lines in a text file.

Often we are just interested in the number of lines in a file, so we use the -l option.

1. Let **wc** count the number of lines in Shakespeare's sonnets:

**wc -l poems/Sha\*/son\***

Notice they all have the same number of lines?

1. Use word count to count all the files that you own on the system:

**wc -l myfiles**

1. Count the number of files there are underneath your parent directory, _/home/cis90_ :

**find /home/cis90 | wc -l**

## The spell command

Can be used to check the spelling in text files.

1. Let's find out how many misspelled words are in the file _small\_town_.

Where is _small\_town_? Change to that directory and type:

**spell small\_town**

Notice that some words may be spelled correctly but aren't in UNIX's dictionary.

1. Change to the _Shakespeare_ directory and find how many misspellings there are in all the sonnets.

**spell sonnet\* | wc -l**

What if you wanted to see these misspelled words?

## The sort command

1. Change to your _misc_ directory and display the file _fruit._

**cat fruit**

1. Sort the contents of this file using the command:

**sort fruit**

Note: the contents of the _fruit_ are unchanged; only the output is sorted.

1. Sort the _fruit_ file in reverse order and save the results to _tiurf_

**sort -r fruit \> tiurf**

## The tee command

1. At times, you may want to see the results of a command on your screen as well as saving those results to a file. This may be accomplished using the **tee** command which takes one source of input (stdin) and writes that input to two outputs: stdout and to a file named as a command line argument. Change to the _Shakespeare_ directory and run the command:

**spell sonnet1 | tee words**

Notice how the misspelled words came to the screen and also went to the file _words_.

1. Now let's use the tee command to get a sorted list of the misspelled words in all of Shakespeare's sonnets and count how many there are all at the same time. Change to your home directory and use the **tee** command to collect the intermediary results:

**spell poems/Shakespeare/son\* | sort | tee words | wc -l**

Display the file _words_ to see all the misspelled words.

## Putting Commands Together

For your lab07, we are going to analyze your past 125 commands.

1. Create the file, _lab07_, by redirecting the output of the date command:

**date \> lab07**

1. Create a file that lists your past 125 commands:

**history 200 \> cmds**

1. How many times have you used the **cd** command? Send the results to the file _lab07_:

(Note: the following two lines represent two distinct commands.)

**echo -n "#Times I have used the cd command: " \>\> lab07**

**grep "cd" cmds | wc -l \>\> lab07**

Verify your results by displaying the file _lab07_ to the screen.

1. Repeat step three but count the number of times you have used the **clear** command.

1. Repeat step three but count the number of times you have used the **grep** command.

1. Add the sorted list of misspelled words from Shakespeare's sonnets to your _lab07_ file:

**cat words \>\> lab07**

1. Now tack on a list of all the files you own on opus in alphabetic order.

First update your list of files with:

**find / -user $LOGNAME \> myfiles 2\> /dev/null**

Sort the updated file, _myfiles_ in dictionary order and append it to your lab file:

**sort -d myfiles \>\> lab07**

1. Add the commands you used in this lab to your _lab07_ file:

**cat cmds \>\> lab07**

1. Review your _lab07_ file:

**less lab07**

Do you see the date, the three command counts, the misspelled words, the files you own, and all the commands you used to do this lab? If not you should repeat the steps above.

1. You are almost done with this lab. Congratulate yourself by mailing the banner message, GOOD WORK to your mailbox:

**banner Good Work | mail -s "Pat on the Back" $LOGNAME**

Notice how the -s option to the **mail** command allows you to specify a subject for your message.

##


## Submittal

You have now finished this lab. All you need left to do is copy it to me. The command to do that is given below:

**cp lab07 /home/rsimms/turnin/cis90/lab07.$LOGNAME**

You can submit as many times as you like up to the deadline. After you submit you will receive an email on Opus-II. Read this email to verify whether your submission succeeded or failed. If you run out of time be sure to submit what you have for partial credit.

Run **check7** to check your work and make sure you didn't forget anything. If you add new commands or make new files be sure and repeat the "Putting Commands Together" section above and check/submit again.

## Grading Rubric (30 points total)

30 points for successfully completing all steps.

Less 1 point for each step not completed correctly.

Be sure to submit your work before the deadline. **Remember, late work is not accepted.**

**Extra credit (optional)**

For two points extra credit complete:

**In NETLAB+:**

NISGTC Linux+ Series 1

Lab 7b: Using the BASH Shell

Send me a "signed" summary screenshot (see instructions below).

For two points extra credit complete:

**In NETLAB+:**

NISGTC Linux+ Series 1

Lab 10c: Managing Text Files

Send me a "signed" summary screenshot (see instructions below).

Summary screenshot:

1) Before ending the lab maximize the terminal window you used.

2) Use: **history** to show the commands you issued during the lab.

3) Use: **echo "** _firstname lastname_ **was here"** as your signature.

4) Take a screen shot of the above and email it to: risimms@cabrillo.edu

Extra credit is due when the lab is due. **Remember, late work is not accepted.**
