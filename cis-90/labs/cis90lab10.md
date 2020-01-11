# Lab 10: The Shell Environment

In this lab you will customize your login environment to suit your needs and preferences. By modifying environment variables and editing your _.bash\_profile_ and _.bashrc_ files, you will customize your shell environment in a number of different ways.

**Preparation**

Find and skim Lesson 12 slides: [http://simms-teach.com/cis90calendar.php](http://simms-teach.com/cis90calendar.php)

Check the forum for news on this lab: [http://opus-ii.cis.cabrillo.edu/forum/](http://opus-ii.cis.cabrillo.edu/forum/)

**Procedure**

Log on to Opus so that you have a command line shell at your service. Start this lab from your home directory.

Environment Variables

1. Display the contents of your PWD environment variable. Change to your _bin_ subdirectory and display the same variable. How did it change?
2. Change back to your home directory.
3. Display the contents of your PATH environment variable. Note the colon (:) separating the different directory names. What is the last directory in which the system searches for commands?
4. Make a new environment variable called GREETING and assign it an appropriate salutation. Don't forget to use quotes if your message has whitespace in it.
5. Use the **env** command to see if it is in your environment. Is it there? What must you do to put it in the environment?
6. Export the variable GREETING and use **env** to verify it's there.
7. Invoke a new bash shell process by typing:

**bash**

Now use the **unset** command to unset the variable PS1. What Happened?

1. Reset the PS1 variable by entering the following command:

**PS1="Yes master: "**

What happens to your primary prompt?

1. Now exit out of the child shell by typing _ **Ctrl-D** _. What is the prompt now? What does this tell you about the effect changes made by children have on their parents?
2. Try to exit from your login shell by typing _ **Ctrl-D** _

This is a shell feature that protects you from accidentally logging out. You can turn it off using the **set** command:

**set +o ignoreeof**

Type the above command and then try to exit the shell with _ **Ctrl-D** _

_.bashrc_ and _.bash\_profile_ files

Aliasing is a mechanism provided by the bash shell that allows you to define your own commands, or to redefine UNIX commands. Alias definitions should be stored in your ._bashrc_ file.

1. Edit the _.bashrc_ file in your home directory by adding the following three lines to the bottom of the file:

**alias bye="clear; exit"**

**alias rm="rm -i"**

**alias bill="cd /home/cis90/${LOGNAME%90}/poems/Shakespeare"**

Note that there is no UNIX bye or bill commands.

Your _.bash\_profile_, like your _.bashrc_ file, is a shell script that is run once each time you log in. It establishes your working environment by defining environment variables, setting your terminal type and setting other shell characteristics, like ignoreeof.

1. Edit your _.bash\_profile_ and make the following changes:

- Clean up your path by replacing the directory **:$HOME/../bin:** with **:/home/cis90/bin:** in your PATH environment variable.
- Change the command that sets your umask to: **umask 006**
- Below the umask command line, turn messaging off with the command:

**mesg n**

- Add a shell environment variable named, BIRTHDAY and set it equal to the date of your birth (it doesn't have to be your real birthday) using the format mm/dd/yy.
- Export this variable, since you will want your children to know when your birthday is.
- At the bottom of the file add as the last line: **riddle**

1. Now that you have made these changes, run your _.bashrc_ file using the UNIX dot source command:

**source .bashrc**

1. Try out your new **rm** command by removing some file you don't need anymore.
2. Run your **bill** command. What happens?
3. Try out your **bye** command.

When you log back in again, you should be confronted with a riddle.

Try out the riddle and then submit your lab by following the instructions below.

**Submittal**

To turn in your lab, combine your _.bashrc_ file, your _.bash\_profile_ file, and the output of the **env** command into a new file called _lab10_. Then copy this file as follows:

**cp lab10 /home/rsimms/turnin/cis90/lab10.$LOGNAME**

If your submission succeeded you will get an acknowledgment email on Opus-II indicating your work was received. Read that email message to verify what you submitted is complete and what you want graded.

Run **check10** to check your work and make sure you didn't forget anything.

If you run out of time submit what you have completed by the deadline for partial credit. Remember that late work is not accepted.

**Grading Rubric (30 points total)**

_.bash\_profile_ (12 points)

2 points for each of the six requested modifications done correctly

_.bashrc_ (12 points)

4 points for each of the 3 requested alias additions done correctly

**env** output (6 points)

3 points for being actual output from the env command

3 points for BIRTHDAY variable included in the env output

**Extra credit (optional)**

For two points extra credit complete:

**In NETLAB+:**

NISGTC Linux+ Series 2

Lab 11a: BASH shell features

Send me a "signed" summary screenshot (see instructions below).

For one point extra credit complete:

**In NETLAB+:**

Red Hat Systems Administration - RH124

4.7. Lab: Creating, Viewing, and Editing Text Files

Send me a "signed" summary screenshot (see instructions below).

Summary screenshot:

1) Before ending the lab maximize the terminal window you used.

2) Use: **history** to show the commands you issued during the lab.

3) Use: **echo "** _firstname lastname_ **was here"** as your signature.

4) Take a screen shot of the above and email it to: risimms@cabrillo.edu

Extra credit is due when the lab is due. **Remember, late work is not accepted.**
