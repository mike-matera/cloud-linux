# Lab 8: Process Control

In this lab you will use the **ps** command to monitor processes as you create them using UNIX commands.

## Preparation

- Skim Lesson 10 slides: [http://simms-teach.com/cis90calendar.php](http://simms-teach.com/cis90calendar.php)
- Check the forum for news on this lab: [http://opus-ii.cis.cabrillo.edu/forum/](http://opus-ii.cis.cabrillo.edu/forum/)

## Procedure

Log on to Opus so that you have a command line shell at your service. Be sure you are in your home directory to start this lab.

1. Run the C shell program **csh**. Did your prompt change?

1. Now run the Bourne shell **sh**. Different prompt again?

1. Run the **ps** command to see that you have three shell processes running.

1. Run the **ps** command with the **-l** option ( **l** for **l** ong format). Look at the column headed by the symbol _SZ_. This is the size of the process in 1K blocks. Which of the three shells that you are running is the largest? Redirect that line of output to the file _bigshell_.

1. Now terminate the Bourne and C shells by typing the **exit** command twice.

1. Run the **ps** command with the **-ef** option. What is the parent (_PPID_) of your shell process? The Grandparent? The Great Grandparent? How far can you go?

1. What is the name of the program with the PID of 1? What is its parent?

1. Run the **app** command in the foreground.

1. Notice that you are stuck. Bring up another window on Opus and kill this process.

Hint: use the command **ps -u $LOGNAME** to find the PID number.

1. Run the **app** command in the background by adding an **&** on the command line.

(Hit the Enter key to get your prompt back)

1. Now try to log out by entering the **exit** command. What does the shell say?

1. Enter **exit** again, and then log back in. Use **ps** to check on the app process. Is it there? What happened?

1. This time enter the following command:

**find $HOME \> files.out 2\>/dev/null &**

**Submittal**

We will now use the **at** command to submit the work you have just done. Since the find process may not be finished running yet, we will set the command to be executed just before midnight. The **at** command gets its input from _stdin_, so you will have to type the following lines:

**at 11:59pm**

at\> **cat files.out bigshell \> lab08**

at\> **cp lab08 /home/rsimms/turnin/cis90/lab08.$LOGNAME**

at\>_\<Ctrl-D\>_

Note: You don't type the "at\>" portion. For the Ctrl-D hold down the Ctrl key and tap the D key which must be entered as the first character on the last line.

**It highly recommended that you don't do the submittal as shown above on the day the lab is due. If you make a mistake you will miss the deadline. Instead set an earlier time on the at command so you can verify it worked as expected or just do the lab earlier in the week.**

If you get a warning message from the **at** command about using the Bourne shell to execute your job, that is ok.

Tomorrow morning you should see the file, _lab08_ in your home directory and have an email acknowledging receipt of your lab.

You can submit as many times as you like up to the deadline. After you submit you will receive an email on Opus-II. Read this email to verify whether your submission succeeded or failed. If you run out of time be sure to submit what you have for partial credit. Run **check8** to check your work and make sure you didn't forget anything.

Be sure to verify that your submittal was completed before the deadline. **No late work is accepted.**

## Grading Rubric (30 points total)

10 points for creating _bigshell_ correctly

-2 if not using long format

-4 if indicates wrong shell

-5 if no shell selected or selection is not a shell

-10 if missing, empty or non-ps output

10 points for creating _files.out_ correctly

10 points for submitting correctly

Be sure to submit your work before the deadline. **Remember, late work is not accepted.**

**Extra credit (optional)**

For two points extra credit complete:

**In NETLAB+:**

NISGTC Linux+ Series 1

Lab 8: Monitoring Processes

Send me a "signed" summary screenshot (see instructions below).

For two points extra credit complete:

**In NETLAB+:**

NISGTC Linux+ Series 2

Lab 5: crontab and at

Send me a "signed" summary screenshot (see instructions below).

For one point extra credit complete:

**In NETLAB+:**

Red Hat Systems Administration - RH124

7.4. Practice: Background and Foreground Processes

Send me a "signed" summary screenshot (see instructions below).

Summary screenshot:

1) Before ending the lab maximize the terminal window you used.

2) Use: **history** to show the commands you issued during the lab.

3) Use: **echo "** _firstname lastname_ **was here"** as your signature.

4) Take a screen shot of the above and email it to: risimms@cabrillo.edu

Extra credit is due when the lab is due. **Remember, late work is not accepted.**
