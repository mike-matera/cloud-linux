# Lab 8: Process Control

In this lab you will use the `ps` command to monitor processes as you create them using UNIX commands.

## Procedure

Log on to opus3 so that you have a command line shell at your service. Be sure you are in your home directory to start this lab.

1. Run the C shell program `csh`. Did your prompt change?

1. Now run the Bourne shell `sh`. Different prompt again?

1. Run the `ps` command to see that you have three shell processes running.

1. Run the `ps` command with the `-l` option ( `l` for long format). Look at the column headed by the symbol `SZ`. This is the size of the process in `1K` blocks. Which of the three shells that you are running is the largest? Redirect that line of output to the file `bigshell`.

1. Now terminate the Bourne and C shells by typing the `exit` command twice.

1. Run the `ps` command with the `-ef` option. What is the parent (`PPID`) of your shell process? The Grandparent? The Great Grandparent? How far can you go?

1. What is the name of the program with the PID of 1? What is its parent?

1. Run the `app` command in the foreground.

1. Notice that you are stuck. Bring up another window on Opus and kill this process.

	Hint: use the command `ps -u $LOGNAME` to find the PID number.

1. Run the `app` command in the background by adding an `&` on the command line.

	(Hit the Enter key to get your prompt back)

1. Now log out by entering the `exit` command.

1. Log back in and use `ps` to check on the app process. Is it there? What happened?

1. This time enter the following command:

```
find $HOME > files.out 2>/dev/null &
```

## Submittal

We will now use the `at` command to submit the work you have just done. Since the find process may not be finished running yet, we will set the command to be executed just before midnight. The `at` command gets its input from `stdin`, so you will have to type the following lines:

```
at 11:59pm
at> cat files.out bigshell > lab08
at> cp lab08 /home/mmatera/turnin/lab08.$LOGNAME
at> <Ctrl-D>
```

**Note: You don't type the `at>` portion. For the `<Ctrl-D>` hold down the `Ctrl` key and tap the `D` key which must be entered as the first character on the last line.** If you get a warning message from the `at` command about using the Bourne shell to execute your job, that is ok. The next morning you should see the file, `lab08` in your home directory and have an email acknowledging receipt of your lab. You can submit as many times as you like. After you submit you will receive an email on opus3. Read this email to verify whether your submission succeeded or failed. 

I will enter your grade into Canvas. You don't have to submit there. 

